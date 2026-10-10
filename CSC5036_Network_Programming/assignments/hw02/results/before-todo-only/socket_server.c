#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <poll.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 8080
#define MAX_CLIENTS 30
#define BUFFER_SIZE 1024



/* TCP can send fewer bytes than requested. Retry until the whole chunk is sent. */
static int send_all(int fd, const char *data, size_t length) {
    while (length > 0) {
        ssize_t sent = send(fd, data, length, MSG_NOSIGNAL);
        if (sent < 0 && errno == EINTR) continue;
        if (sent <= 0) {
            if (sent < 0) perror("send");
            else fprintf(stderr, "send returned zero\n");
            return -1;
        }
        data += sent;
        length -= (size_t)sent;
    }
    return 0;
}

int main() {
    int opt = 1;
    int master_socket, new_socket, client_socket[MAX_CLIENTS];
    socklen_t addrlen;
    ssize_t valread;
    struct sockaddr_in address;
    char buffer[BUFFER_SIZE];
    struct pollfd poll_fds[MAX_CLIENTS + 1]; // +1 for the master socket
    int max_clients = MAX_CLIENTS;
    int poll_count;

    // Initialize all client_socket[] to 0 so not checked
    for (int i = 0; i < max_clients; i++) {
        client_socket[i] = 0;
    }


    /* Implemented: socket()
    * Create a master socket using socket(); 
    * outputs an error message if it fails.
    */
    master_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (master_socket < 0) { perror("socket"); return EXIT_FAILURE; }
    memset(&address, 0, sizeof(address));
    

    /* Implemented: setsockopt()
    * Use setsockopt() to enable the SO_REUSEADDR option. 
    * The server allows multiple connections on the same local address and port.
    */
    if (setsockopt(master_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("setsockopt"); close(master_socket); return EXIT_FAILURE;
    }


    // Type of socket created
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);


    /* Implemented: bind()
    * The server should bind to the specified port and address without errors.
    */
    if (bind(master_socket, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind"); close(master_socket); return EXIT_FAILURE;
    }

    printf("Listener on port %d \n", PORT);
    /* Implemented: listen()
    * The server listens on the specified port and can queue up to 3 pending 
    * connections for the master socket.
    */
    if (listen(master_socket, 3) < 0) {
        perror("listen"); close(master_socket); return EXIT_FAILURE;
    }

    // Accept the incoming connection
    addrlen = sizeof(address);
    puts("Waiting for connections ...");

    // Set up the initial listening socket and event for listening to incoming connections
    poll_fds[0].fd = master_socket;
    poll_fds[0].events = POLLIN;

    while (1) {
        /* Implemented: 
        * Prepare the poll_fds array for existing connections.
        * Hint: poll_fds[0] is reserved for the listening socket.
        */
        for (int i = 0; i < max_clients; i++) {
            poll_fds[i + 1].fd = client_socket[i] ? client_socket[i] : -1;
            poll_fds[i + 1].events = POLLIN;
            poll_fds[i + 1].revents = 0;
        }

        // Wait for some event on one of the sockets with no timeout (NULL)
        poll_count = poll(poll_fds, max_clients + 1, -1);

        if (poll_count < 0) {
            if (errno == EINTR) continue;
            perror("poll error");
            exit(EXIT_FAILURE);
        }

        if (poll_fds[0].revents & (POLLERR | POLLHUP | POLLNVAL)) {
            fprintf(stderr, "Listening socket failed\n");
            close(master_socket); return EXIT_FAILURE;
        }

        // If something happened on the master socket, then it's an incoming connection
        if (poll_fds[0].revents & POLLIN) {
            /* Implemented: accept()
            * Accept a new connection when there is incoming request on the master socket.
            */
            addrlen = sizeof(address);
            new_socket = accept(master_socket, (struct sockaddr *)&address, &addrlen);
            if (new_socket < 0) { perror("accept"); continue; }

            printf("New connection, socket fd is %d, ip is: %s, port: %d\n",
                   new_socket, inet_ntoa(address.sin_addr), ntohs(address.sin_port));

            /* Implemented:
            * Add the new client socket to the client_socket array.
            */
            int slot;
            for (slot = 0; slot < max_clients; slot++) {
                if (client_socket[slot] == 0) { client_socket[slot] = new_socket; break; }
            }
            if (slot == max_clients) {
                fprintf(stderr, "Client capacity reached\n");
                close(new_socket);
            }
            
        }

        // Else it's some IO operation on some other socket
        for (int i = 0; i < max_clients; i++) {
            int sd = client_socket[i];

            // Skip if this slot is not connected
            if (sd == 0) continue;

            if (poll_fds[i + 1].revents & (POLLIN | POLLHUP | POLLERR | POLLNVAL)) {
                // Check if it was a closing and also read the incoming message
                if ((valread = read(sd, buffer, BUFFER_SIZE - 1)) == 0) {
                    // Somebody disconnected, get details and print
                    getpeername(sd, (struct sockaddr*)&address, &addrlen);
                    printf("Host disconnected, ip %s, port %d\n",
                           inet_ntoa(address.sin_addr), ntohs(address.sin_port));

                    // Close the socket and mark as 0 in list for reuse
                    close(sd);
                    client_socket[i] = 0;
                } else if (valread < 0) {
                    if (errno == EINTR)
                        continue;

                    perror("read");
                    close(sd);
                    client_socket[i] = 0;
                } else {
                    // Echo back the message that came in
                    buffer[valread] = '\0';
                    if (send_all(sd, buffer, (size_t)valread) < 0) {
                        close(sd);
                        client_socket[i] = 0;
                    }
                }
            }
        }
    }

    return 0;
}