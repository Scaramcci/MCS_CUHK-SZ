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


int main() {
    int opt = 1;
    int master_socket, addrlen, new_socket, client_socket[MAX_CLIENTS], valread;
    struct sockaddr_in address;
    char buffer[BUFFER_SIZE];
    struct pollfd poll_fds[MAX_CLIENTS + 1]; // +1 for the master socket
    int max_clients = MAX_CLIENTS;
    int poll_count;

    // Initialize all client_socket[] to 0 so not checked
    for (int i = 0; i < max_clients; i++) {
        client_socket[i] = 0;
    }


    /* TODO: socket()
    * Create a master socket using socket(); 
    * outputs an error message if it fails.
    */
/* BEGIN TODO IMPLEMENTATION */
    struct transfer {
        char filename[BUFFER_SIZE];
        size_t header_used;
        FILE *file;
    } transfers[MAX_CLIENTS] = {0};
    master_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (master_socket < 0) { perror("socket"); return EXIT_FAILURE; }
    memset(&address, 0, sizeof(address));
/* END TODO IMPLEMENTATION */
    

    /* TODO: setsockopt()
    * Use setsockopt() to enable the SO_REUSEADDR option. 
    * The server allows multiple connections on the same local address and port.
    */
/* BEGIN TODO IMPLEMENTATION */
    if (setsockopt(master_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("setsockopt"); close(master_socket); return EXIT_FAILURE;
    }
/* END TODO IMPLEMENTATION */


    // Type of socket created
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);


    /* TODO: bind()
    * The server should bind to the specified port and address without errors.
    */
/* BEGIN TODO IMPLEMENTATION */
    if (bind(master_socket, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind"); close(master_socket); return EXIT_FAILURE;
    }
/* END TODO IMPLEMENTATION */

    printf("Listener on port %d \n", PORT);
    /* TODO: listen()
    * The server listens on the specified port and can queue up to 3 pending 
    * connections for the master socket.
    */
/* BEGIN TODO IMPLEMENTATION */
    if (listen(master_socket, 3) < 0) {
        perror("listen"); close(master_socket); return EXIT_FAILURE;
    }
/* END TODO IMPLEMENTATION */

    // Accept the incoming connection
    addrlen = sizeof(address);
    puts("Waiting for connections ...");

    // Set up the initial listening socket and event for listening to incoming connections
    poll_fds[0].fd = master_socket;
    poll_fds[0].events = POLLIN;

    while (1) {
        /* TODO: 
        * Prepare the poll_fds array for existing connections.
        * Hint: poll_fds[0] is reserved for the listening socket.
        */
/* BEGIN TODO IMPLEMENTATION */
        for (int i = 0; i < max_clients; i++) {
            poll_fds[i + 1].fd = client_socket[i] ? client_socket[i] : -1;
            poll_fds[i + 1].events = POLLIN;
            poll_fds[i + 1].revents = 0;
        }
/* END TODO IMPLEMENTATION */

        // Wait for some event on one of the sockets with no timeout (NULL)
        poll_count = poll(poll_fds, max_clients + 1, -1);

        if (poll_count < 0) {
            perror("poll error");
            exit(EXIT_FAILURE);
        }

        // If something happened on the master socket, then it's an incoming connection
        if (poll_fds[0].revents & POLLIN) {
            /* TODO: accept()
            * Accept a new connection when there is incoming request on the master socket.
            */
/* BEGIN TODO IMPLEMENTATION */
            socklen_t peer_length = (socklen_t)addrlen;
            new_socket = accept(master_socket, (struct sockaddr *)&address, &peer_length);
            if (new_socket < 0) { perror("accept"); continue; }
/* END TODO IMPLEMENTATION */

            printf("New connection, socket fd is %d, ip is: %s, port: %d\n",
                   new_socket, inet_ntoa(address.sin_addr), ntohs(address.sin_port));

            /* TODO:
            * Add the new client socket to the client_socket array.
            */
/* BEGIN TODO IMPLEMENTATION */
            int slot;
            for (slot = 0; slot < max_clients; slot++) {
                if (client_socket[slot] == 0) { client_socket[slot] = new_socket; break; }
            }
            if (slot == max_clients) {
                fprintf(stderr, "Client capacity reached\n"); close(new_socket);
            }
/* END TODO IMPLEMENTATION */
            
        }

        // Loop through all client sockets
        for (int i = 0; i < max_clients; i++) {
            int sd = client_socket[i];

            // Skip if this slot is not connected
            if (sd == 0) continue;

            // Check if the socket has incoming data using poll
            if (poll_fds[i + 1].revents & POLLIN) {
                /* IMPLEMENTING SIMPLE FILE TRANSFER */

                // Variables you may need to declare:
                // char filename[BUFFER_SIZE];
                // FILE *file;

                /* TODO: Read the filename from the client
                * The client sends the filename first (padded to BUFFER_SIZE)
                */
/* BEGIN TODO IMPLEMENTATION */
                struct transfer *state = &transfers[i];
                int reading_header = state->header_used < BUFFER_SIZE;
                char *destination = reading_header ? state->filename + state->header_used : buffer;
                size_t capacity = reading_header ? BUFFER_SIZE - state->header_used : sizeof(buffer);
                valread = (int)recv(sd, destination, capacity, MSG_DONTWAIT);
                if (valread < 0) {
                    if (errno == EINTR || errno == EAGAIN || errno == EWOULDBLOCK) continue;
                    perror("recv");
                    if (state->file && fclose(state->file) != 0) perror("fclose");
                    close(sd); client_socket[i] = 0;
                    memset(state, 0, sizeof(*state));
                    continue;
                }
/* END TODO IMPLEMENTATION */

                /* TODO: Handle client disconnection
                * If read returns 0, the client has disconnected
                */
/* BEGIN TODO IMPLEMENTATION */
                if (valread == 0) {
                    if (reading_header) fprintf(stderr, "Client closed before complete filename\n");
                    else printf("File received: %s\n", state->filename);
                    if (state->file && fclose(state->file) != 0) perror("fclose");
                    close(sd); client_socket[i] = 0;
                    memset(state, 0, sizeof(*state));
                    continue;
                }
/* END TODO IMPLEMENTATION */

                /* TODO: Open the file for writing
                * Use fopen() with "wb" mode for binary write
                */
/* BEGIN TODO IMPLEMENTATION */
                if (reading_header) {
                    state->header_used += (size_t)valread;
                    if (state->header_used < BUFFER_SIZE) continue;
                    if (!memchr(state->filename, '\0', BUFFER_SIZE) || !state->filename[0] ||
                        strchr(state->filename, '/') || strcmp(state->filename, ".") == 0 ||
                        strcmp(state->filename, "..") == 0) {
                        fprintf(stderr, "Invalid filename header\n");
                        close(sd); client_socket[i] = 0;
                        memset(state, 0, sizeof(*state)); continue;
                    }
                    state->file = fopen(state->filename, "wb");
                    if (!state->file) {
                        perror("fopen"); close(sd); client_socket[i] = 0;
                        memset(state, 0, sizeof(*state)); continue;
                    }
                    printf("Receiving file: %s\n", state->filename);
                    /* Header and body are separate TCP byte ranges, not packets. */
                    continue;
                }
/* END TODO IMPLEMENTATION */

                // Uncomment the following after declaring 'file' and 'filename':
                // if (!file) {
                //     perror("Error opening file");
                //     continue;
                // }
                // printf("Receiving file: %s\n", filename);

                /* TODO: Receive file data from the client and write to file
                * Loop: read from socket, write to file, until no more data
                */
/* BEGIN TODO IMPLEMENTATION */
                if (fwrite(buffer, 1, (size_t)valread, state->file) != (size_t)valread) {
                    perror("fwrite");
                    if (fclose(state->file) != 0) perror("fclose");
                    close(sd); client_socket[i] = 0;
                    memset(state, 0, sizeof(*state));
                }
/* END TODO IMPLEMENTATION */

                // Confirm file save and clean up resources
                // Uncomment after implementing:
                // printf("File saved as: %s\n", filename);
                // fclose(file);
                // close(sd);
                // client_socket[i] = 0;
            }
        }
    }

    return 0;
}