// socket_client.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    struct sockaddr_in serv_addr;
    int sock = 0;
    char *hello = "Hello from client";
    char buffer[BUFFER_SIZE] = {0};

    /* TODO: socket()
    * Create a socket using socket(AF_INET, SOCK_STREAM, 0)
    * Store the result in 'sock' variable
    * Print an error message and exit if it fails
    */
/* BEGIN TODO IMPLEMENTATION */
#include <errno.h>
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) { perror("socket"); return EXIT_FAILURE; }
    memset(&serv_addr, 0, sizeof(serv_addr));
/* END TODO IMPLEMENTATION */

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    /* TODO: inet_pton()
    * Convert the IP address "127.0.0.1" from text to binary form
    * Use inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)
    * Print an error message and exit if conversion fails (returns <= 0)
    */
/* BEGIN TODO IMPLEMENTATION */
    int converted = inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);
    if (converted <= 0) {
        if (converted < 0) perror("inet_pton");
        else fprintf(stderr, "Invalid server address\n");
        close(sock); return EXIT_FAILURE;
    }
/* END TODO IMPLEMENTATION */
    

    /* TODO: connect()
    * Connect to the server.
    */
/* BEGIN TODO IMPLEMENTATION */
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("connect"); close(sock); return EXIT_FAILURE;
    }
/* END TODO IMPLEMENTATION */


    // Send data to the server
    send(sock, hello, strlen(hello), 0);
    printf("Hello message sent\n");


    /* TODO: read()
    * Read data from the server into buffer with size BUFFER_SIZE.
    */
/* BEGIN TODO IMPLEMENTATION */
    size_t received = 0;
    size_t expected = strlen(hello);
    while (received < expected) {
        ssize_t count = read(sock, buffer + received, expected - received);
        if (count < 0 && errno == EINTR) continue;
        if (count <= 0) {
            if (count < 0) perror("read");
            else fprintf(stderr, "Server closed before the complete echo\n");
            close(sock); return EXIT_FAILURE;
        }
        received += (size_t)count;
    }
    buffer[received] = '\0';
    if (memcmp(buffer, hello, expected) != 0) {
        fprintf(stderr, "Echo does not match\n"); close(sock); return EXIT_FAILURE;
    }
/* END TODO IMPLEMENTATION */
    printf("Message from server: %s\n", buffer);

    // Introduce a delay to keep the connection open
    sleep(2); // Waits for 2 seconds. You can adjust this value as needed.

    /* TODO: close()
    * Close the socket.
    */
/* BEGIN TODO IMPLEMENTATION */
    if (close(sock) < 0) { perror("close"); return EXIT_FAILURE; }
/* END TODO IMPLEMENTATION */

    return 0;
}