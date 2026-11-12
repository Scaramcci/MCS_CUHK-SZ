import socket
import threading
import hashlib
import json
import time
import math

class Node:
    def __init__(self, node_id, host, port, m=5):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.m = m  # number of bits in the identifier space
        self.max_id = 2 ** m  # size of the identifier ring (e.g. 32 for m=5)
        self.predecessor = None  # (node_id, host, port) tuple or None
        self.successor = (node_id, host, port)  # initially points to self
        # Finger table: indices 1..m; finger[i] stores the successor of (node_id + 2^(i-1)) mod 2^m
        self.finger = [None] * (m + 1)
        for i in range(1, m + 1):
            self.finger[i] = (node_id, host, port)
        self.next = 1  # index of the next finger to fix
        self.data = {}  # local key-value storage
        self.running = True  # server control flag
        self.stopped = False  # whether the node has been stopped

        # Initialize the server socket before starting the thread
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Start the TCP server thread
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True
        self.server_thread.start()

    # ========================================================================
    # Helper Methods (provided)
    # ========================================================================

    def in_interval(self, id, start, end, inclusive_right=True):
        """
        Check if 'id' falls within an interval on the Chord ring.

        By default checks the half-open interval (start, end].
        Set inclusive_right=False to check the open interval (start, end).

        Must handle ring wraparound (e.g. when start > end).

        Args:
            id: The identifier to check
            start: Start of the interval (exclusive)
            end: End of the interval
            inclusive_right: If True, check (start, end]; if False, check (start, end)

        Returns:
            True if id is in the interval, False otherwise
        """
        # TODO: Implement interval check, considering ring wraparound
        offset = (id - start) % self.max_id
        span = (end - start) % self.max_id
        if span == 0:
            return inclusive_right or offset != 0
        return 0 < offset <= span if inclusive_right else 0 < offset < span

    # ========================================================================
    # Core Chord Protocol (Section 1)
    # ========================================================================

    def find_successor(self, id):
        """
        Find the successor node responsible for a given identifier.

        This is the core lookup operation of Chord. It should:
        1. Check if 'id' falls in (self.node_id, self.successor], if so return self.successor
        2. Otherwise, find the closest preceding node and ask it to continue the search

        Hint: Use self.in_interval(), self.closest_preceding_node(), and self.remote_call().

        Args:
            id: The identifier to find successor for

        Returns:
            (node_id, host, port) of the successor
        """
        # TODO: Implement this method
        id %= self.max_id
        own = (self.node_id, self.host, self.port)
        if id == self.node_id:
            return own
        self._repair_successor()
        if self.in_interval(id, self.node_id, self.successor[0]):
            return self.successor
        preceding = self.closest_preceding_node(id)
        target = self.successor if preceding == own else preceding
        try:
            result = self.remote_call(target, "find_successor", {"id": id})
            if result is not None:
                return tuple(result)
        except Exception:
            self._forget(target)
        self._repair_successor()
        if self.successor == own:
            return own
        if target != self.successor:
            result = self.remote_call(self.successor, "find_successor", {"id": id})
            if result is not None:
                return tuple(result)
        raise RuntimeError("No route to identifier")

    def closest_preceding_node(self, id):
        """
        Find the closest preceding node for a given identifier by scanning the finger table.

        Search the finger table from index m down to 1. Return the first finger
        whose node_id falls in the open interval (self.node_id, id).

        Args:
            id: The identifier to find closest preceding node for

        Returns:
            (node_id, host, port) of the closest preceding node, or self's address if none found
        """
        # TODO: Implement this method
        for i in range(self.m, 0, -1):
            candidate = self.finger[i]
            if candidate and self.in_interval(candidate[0], self.node_id, id, False):
                if self._alive(candidate):
                    return tuple(candidate)
                self._forget(candidate)
        return (self.node_id, self.host, self.port)

    def create(self):
        """
        Create a new Chord ring with this node as the only member.

        Should set predecessor to None and successor to self.
        """
        # TODO: Implement this method
        own = (self.node_id, self.host, self.port)
        self.predecessor = None
        self.successor = own
        self.finger = [None] + [own] * self.m
        self.next = 1
        self.successor_list = []

    def join(self, existing_node_addr):
        """
        Join an existing Chord ring via a known node.

        Should set predecessor to None, and ask the existing node to find
        this node's successor using find_successor.

        Args:
            existing_node_addr: (node_id, host, port) of a node already in the ring
        """
        # TODO: Implement this method
        self.predecessor = None
        result = self.remote_call(existing_node_addr, "find_successor", {"id": self.node_id})
        if result is None:
            raise RuntimeError("Unable to join ring")
        self.successor = tuple(result)
        self.finger = [None] + [self.successor] * self.m
        self.next = 1
        self.successor_list = [self.successor]

    def stabilize(self):
        """
        Periodically verify this node's immediate successor and inform the successor about this node.

        Steps:
        1. Ask successor for its predecessor (x)
        2. If x is between self and successor, update successor to x
        3. Notify the (possibly new) successor about self

        Hint: Use remote_call with "get_predecessor" and "notify" commands.
        """
        # TODO: Implement this method
        self.check_predecessor()
        self._repair_successor()
        try:
            candidate = self.remote_call(self.successor, "get_predecessor", {})
            if (candidate and self.in_interval(candidate[0], self.node_id,
                                               self.successor[0], False)
                    and self._alive(candidate)):
                self.successor = tuple(candidate)
            self.remote_call(self.successor, "notify", {
                "node_id": self.node_id, "host": self.host, "port": self.port})
            # Cache the next successor through the existing lookup RPC.
            following = self.remote_call(self.successor, "find_successor", {
                "id": (self.successor[0] + 1) % self.max_id})
            candidates = getattr(self, "successor_list", []) + [self.successor]
            if following:
                candidates.append(tuple(following))
            self.successor_list = self._ordered_candidates(candidates)
            self.finger[1] = self.successor
        except Exception:
            self._repair_successor()

    def notify(self, node_addr):
        """
        Handle notification from a node that thinks it is this node's predecessor.

        Update self.predecessor if:
        - Current predecessor is None, OR
        - node_addr falls in (self.predecessor, self) on the ring

        Args:
            node_addr: (node_id, host, port) of the potential predecessor
        """
        # TODO: Implement this method
        node_addr = tuple(node_addr)
        if node_addr == (self.node_id, self.host, self.port):
            return
        if (self.predecessor is None or
                self.in_interval(node_addr[0], self.predecessor[0], self.node_id, False)):
            self.transfer_keys(node_addr)
            self.predecessor = node_addr

    def fix_fingers(self):
        """
        Refresh one finger table entry per call.

        Use self.next to track which finger to fix (cycling from 1 to m).
        finger[i] should be the successor of (self.node_id + 2^(i-1)) mod 2^m.
        """
        # TODO: Implement this method
        index = self.next
        self.finger[index] = self.find_successor(
            (self.node_id + 2 ** (index - 1)) % self.max_id)
        self.next = index % self.m + 1

    def check_predecessor(self):
        """
        Check if the predecessor has failed by pinging it.

        If the predecessor does not respond, set self.predecessor to None.

        Hint: Use remote_call with "ping" command and handle exceptions.
        """
        # TODO: Implement this method (Optional / Bonus)
        predecessor = self.predecessor
        if predecessor and not self._alive(predecessor):
            self._forget(predecessor)

    # ========================================================================
    # Key Storage (Section 2)
    # ========================================================================

    def hash_key(self, key):
        """
        Hash a string key to an identifier in the Chord ring space [0, 2^m - 1].

        Use a standard hash function (e.g. SHA-1 from hashlib) and take modulo 2^m.

        Args:
            key: The string key to hash

        Returns:
            An integer identifier in [0, 2^m - 1]
        """
        # TODO: Implement this method
        return int.from_bytes(hashlib.sha1(key.encode("utf-8")).digest(), "big") % self.max_id

    def put(self, key, value):
        """
        Store a key-value pair in the DHT.

        Steps:
        1. Hash the key to get an identifier
        2. Find the successor node responsible for that identifier
        3. Store the key-value pair on that node using remote_call with "store" command

        Args:
            key: The key to store
            value: The value to store

        Returns:
            True if the operation succeeded, False otherwise
        """
        # TODO: Implement this method
        try:
            owner = self.find_successor(self.hash_key(key))
            return self.remote_call(owner, "store", {"key": key, "value": value}) is True
        except Exception:
            return False

    def get(self, key):
        """
        Retrieve a value from the DHT by key.

        Steps:
        1. Hash the key to get an identifier
        2. Find the successor node responsible for that identifier
        3. Retrieve the value from that node using remote_call with "retrieve" command

        Args:
            key: The key to retrieve

        Returns:
            The associated value, or None if the key is not found
        """
        # TODO: Implement this method
        owner = self.find_successor(self.hash_key(key))
        return self.remote_call(owner, "retrieve", {"key": key})

    def transfer_keys(self, new_node_addr):
        """
        Transfer keys that should now belong to a new node.

        When a new node joins, this node (the successor) should transfer any keys
        whose hashed identifier falls in the range that the new node is now responsible for.

        Use remote_call with "store" command to send each key-value pair to the new node,
        then remove the transferred keys from self.data.

        Args:
            new_node_addr: (node_id, host, port) of the new node
        """
        # TODO: Implement this method
        new_node_addr = tuple(new_node_addr)
        if new_node_addr == (self.node_id, self.host, self.port):
            return
        if self.predecessor and tuple(self.predecessor) == new_node_addr:
            return
        start = self.predecessor[0] if self.predecessor else self.node_id
        for key, value in list(self.data.items()):
            if self.in_interval(self.hash_key(key), start, new_node_addr[0]):
                stored = self.remote_call(new_node_addr, "store", {"key": key, "value": value})
                if stored is not True:
                    raise RuntimeError("Key transfer was not acknowledged")
                if key in self.data and self.data[key] == value:
                    del self.data[key]

    def _alive(self, address):
        try:
            return self.remote_call(address, "ping", {}, timeout=0.5) == "pong"
        except Exception:
            return False

    def _ordered_candidates(self, candidates):
        own = (self.node_id, self.host, self.port)
        addresses = {tuple(a) for a in candidates if a and tuple(a) != own}
        return sorted(addresses, key=lambda a: (a[0] - self.node_id) % self.max_id)

    def _forget(self, address):
        address = tuple(address)
        own = (self.node_id, self.host, self.port)
        self.successor_list = [a for a in getattr(self, "successor_list", [])
                               if tuple(a) != address]
        for i in range(1, self.m + 1):
            if self.finger[i] and tuple(self.finger[i]) == address:
                self.finger[i] = own
        if self.predecessor and tuple(self.predecessor) == address:
            self.predecessor = None

    def _repair_successor(self):
        own = (self.node_id, self.host, self.port)
        if self.successor != own and self._alive(self.successor):
            return
        candidates = self._ordered_candidates(
            [self.successor, self.predecessor] + self.finger[1:]
            + getattr(self, "successor_list", []))
        self.successor = own
        for candidate in candidates:
            if self._alive(candidate):
                self.successor = candidate
                break
            self._forget(candidate)
        self.finger[1] = self.successor

    # ========================================================================
    # Network Communication (provided - do not modify)
    # ========================================================================

    def remote_call(self, node_addr, command, params, timeout=5.0):
        """
        Make a remote call to another node. Handles both local and remote calls transparently.

        Args:
            node_addr: (node_id, host, port) of the target node
            command: The command to execute (e.g. "find_successor", "notify", "store", "retrieve", ...)
            params: Dictionary of parameters for the command
            timeout: Socket timeout in seconds

        Returns:
            The result of the remote call, or None if it failed

        Raises:
            Exception: If the target node cannot be contacted
        """
        target_id, target_host, target_port = node_addr

        # Local call: if the target is this node, handle directly
        if target_id == self.node_id and target_host == self.host and target_port == self.port:
            if command == "find_successor":
                return self.find_successor(params.get("id"))
            elif command == "closest_preceding_node":
                return self.closest_preceding_node(params.get("id"))
            elif command == "get_predecessor":
                return self.predecessor
            elif command == "notify":
                n_id = params.get("node_id")
                n_host = params.get("host")
                n_port = params.get("port")
                self.notify((n_id, n_host, n_port))
                return (self.node_id, self.host, self.port)
            elif command == "ping":
                return "pong"
            elif command == "store":
                self.data[params.get("key")] = params.get("value")
                return True
            elif command == "retrieve":
                return self.data.get(params.get("key"))
            elif command == "get_data":
                return self.data
            elif command == "transfer_keys":
                n_id = params.get("node_id")
                n_host = params.get("host")
                n_port = params.get("port")
                self.transfer_keys((n_id, n_host, n_port))
                return True
            else:
                return "Unknown command"

        # Remote call: send request over TCP
        if target_id == -1 or target_host == "" or target_port == 0:
            raise Exception(f"Cannot contact node {target_id} - node address is invalid")

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((target_host, target_port))
                message = json.dumps({"command": command, "params": params})
                s.sendall(message.encode())
                data = s.recv(4096)
                if data:
                    response = json.loads(data.decode())
                    return response.get("result")
            return None
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            raise Exception(f"Failed to connect to node {target_id} at {target_host}:{target_port} - {str(e)}")

    # TCP server: listens for incoming requests and handles them in separate threads.
    def run_server(self):
        # Implementation provided - handles TCP server operation
        try:
            # Socket is already initialized in __init__, just bind and listen
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            
            while self.running:
                try:
                    self.server.settimeout(1)  # Add timeout to check running flag
                    client, addr = self.server.accept()
                    client_thread = threading.Thread(target=self.handle_client, args=(client,))
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:  # Only print error if we're supposed to be running
                        print(f"Server error: {e}")
        except Exception as e:
            print(f"Failed to start server: {e}")

    def handle_client(self, client_socket):
        # Implementation provided - handles incoming client connections
        try:
            data = client_socket.recv(4096)
            if not data:
                client_socket.close()
                return
            request = json.loads(data.decode())
            command = request.get("command")
            params = request.get("params")
            result = None

            if command == "find_successor":
                id = params.get("id")
                result = self.find_successor(id)
            elif command == "closest_preceding_node":
                id = params.get("id")
                result = self.closest_preceding_node(id)
            elif command == "get_predecessor":
                result = self.predecessor
            elif command == "notify":
                node_id = params.get("node_id")
                host = params.get("host")
                port = params.get("port")
                node_addr = (node_id, host, port)
                self.notify(node_addr)
                result = (self.node_id, self.host, self.port)
            elif command == "ping":
                result = "pong"
            elif command == "store":
                # Handle store operation
                key = params.get("key")
                value = params.get("value")
                self.data[key] = value
                result = True
            elif command == "retrieve":
                # Handle retrieve operation
                key = params.get("key")
                result = self.data.get(key)
            elif command == "get_data":
                # Return all data stored in this node
                result = self.data
            elif command == "transfer_keys":
                # Handle transfer_keys operation
                node_id = params.get("node_id")
                host = params.get("host")
                port = params.get("port")
                node_addr = (node_id, host, port)
                self.transfer_keys(node_addr)
                result = True
            else:
                result = "Unknown command"

            response = json.dumps({"result": result})
            client_socket.sendall(response.encode())
        except Exception as e:
            error_response = json.dumps({"result": None, "error": str(e)})
            client_socket.sendall(error_response.encode())
        finally:
            client_socket.close()

    def stop(self):
        """Stop the node's server thread and mark as stopped."""
        self.running = False
        self.stopped = True
        if self.server:
            self.server.close()