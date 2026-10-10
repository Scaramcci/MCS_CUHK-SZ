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



struct transfer {
    char filename[BUFFER_SIZE];
    size_t header_used;
    FILE *file;
};

static void close_transfer(int *fd, struct transfer *state) {
    if (state->file && fclose(state->file) != 0) perror("fclose");
    if (close(*fd) < 0) perror("close");
    *fd = 0;
    memset(state, 0, sizeof(*state));
}

/* Read at most one available chunk, so a slow sender cannot block others. */
static void receive_file(int *fd, struct transfer *state) {
    char data[BUFFER_SIZE];
    int reading_header = state->header_used < BUFFER_SIZE;
    char *destination = reading_header ? state->filename + state->header_used : data;
    size_t capacity = reading_header ? BUFFER_SIZE - state->header_used : sizeof(data);
    ssize_t count = recv(*fd, destination, capacity, MSG_DONTWAIT);
    if (count < 0) {
        if (errno == EINTR || errno == EAGAIN || errno == EWOULDBLOCK) return;
        perror("recv");
        close_transfer(fd, state);
        return;
    }
    if (count == 0) {
        if (reading_header) fprintf(stderr, "Client closed before complete filename\n");
        else printf("File received: %s\n", state->filename);
        close_transfer(fd, state);
        return;
    }
    if (reading_header) {
        state->header_used += (size_t)count;
        if (state->header_used < BUFFER_SIZE) return;
        /* Only accept a base name, never a directory path supplied by a peer. */
        if (!memchr(state->filename, '\0', BUFFER_SIZE) ||
            state->filename[0] == '\0' || strchr(state->filename, '/') ||
            strcmp(state->filename, ".") == 0 || strcmp(state->filename, "..") == 0) {
            fprintf(stderr, "Invalid filename header\n");
            close_transfer(fd, state);
            return;
        }
        state->file = fopen(state->filename, "wb");
        if (!state->file) { perror("fopen"); close_transfer(fd, state); return; }
        printf("Receiving file: %s\n", state->filename);
    } else if (fwrite(data, 1, (size_t)count, state->file) != (size_t)count) {
        perror("fwrite");
        close_transfer(fd, state);
    }
}

int main() {
    int opt = 1;
    int master_socket, new_socket, client_socket[MAX_CLIENTS];
    socklen_t addrlen;
    struct sockaddr_in address;
    struct pollfd poll_fds[MAX_CLIENTS + 1]; // +1 for the master socket
    int max_clients = MAX_CLIENTS;
    int poll_count;
    struct transfer transfers[MAX_CLIENTS] = {0};

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

        // Loop through all client sockets
        for (int i = 0; i < max_clients; i++) {
            int sd = client_socket[i];

            // Skip if this slot is not connected
            if (sd == 0) continue;

            // Check if the socket has incoming data using poll
            if (poll_fds[i + 1].revents & (POLLIN | POLLHUP | POLLERR | POLLNVAL)) {
                receive_file(&client_socket[i], &transfers[i]);
            }
        }
    }

    return 0;
}