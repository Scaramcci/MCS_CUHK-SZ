// file_client.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    struct sockaddr_in serv_addr;
    int sock = 0;
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

    /* IMPLEMENTING SIMPLE FILE TRANSFER */

    // Variables you may need to declare:
    // FILE *file;
    // char *base_filename;

    /* TODO: Open file for reading in binary mode
    * Use fopen() with "rb" mode
    */
/* BEGIN TODO IMPLEMENTATION */
    FILE *file = fopen(argv[1], "rb");
    if (!file) { perror("fopen"); close(sock); return EXIT_FAILURE; }
/* END TODO IMPLEMENTATION */

    /* TODO: Extract filename from path (argv[1])
    * Use strrchr() to find the last '/' in the path
    * Example: "../file1.zip" -> "file1.zip"
    * If no '/' found, use the entire path as filename
    * Store result in base_filename
    */
/* BEGIN TODO IMPLEMENTATION */
    const char *base_filename = strrchr(argv[1], '/');
    base_filename = base_filename ? base_filename + 1 : argv[1];
    size_t filename_length = strlen(base_filename);
    if (!filename_length || filename_length >= BUFFER_SIZE ||
        strcmp(base_filename, ".") == 0 || strcmp(base_filename, "..") == 0) {
        fprintf(stderr, "Invalid filename\n"); fclose(file); close(sock); return EXIT_FAILURE;
    }
/* END TODO IMPLEMENTATION */

    /* TODO: Send filename to server
    * Send the filename (padded to BUFFER_SIZE) so server knows what to name the file
    */
/* BEGIN TODO IMPLEMENTATION */
    memcpy(buffer, base_filename, filename_length);
    size_t sent = 0;
    while (sent < sizeof(buffer)) {
        ssize_t count = send(sock, buffer + sent, sizeof(buffer) - sent, MSG_NOSIGNAL);
        if (count < 0 && errno == EINTR) continue;
        if (count <= 0) {
            if (count < 0) perror("send filename");
            else fprintf(stderr, "send returned zero\n");
            fclose(file); close(sock); return EXIT_FAILURE;
        }
        sent += (size_t)count;
    }
/* END TODO IMPLEMENTATION */

    // You can add a small delay to avoid data mix-up

    /* TODO: Send file content
    * Read file in chunks of BUFFER_SIZE and send each chunk
    */
/* BEGIN TODO IMPLEMENTATION */
    size_t count;
    int failed = 0;
    while ((count = fread(buffer, 1, sizeof(buffer), file)) > 0) {
        size_t offset = 0;
        while (offset < count) {
            ssize_t written = send(sock, buffer + offset, count - offset, MSG_NOSIGNAL);
            if (written < 0 && errno == EINTR) continue;
            if (written <= 0) {
                if (written < 0) perror("send file");
                else fprintf(stderr, "send returned zero\n");
                failed = 1; break;
            }
            offset += (size_t)written;
        }
        if (failed) break;
    }
    if (ferror(file)) { perror("fread"); failed = 1; }
/* END TODO IMPLEMENTATION */

    // printf("File '%s' uploaded successfully.\n", base_filename);

    /* TODO: Close file and socket */
/* BEGIN TODO IMPLEMENTATION */
    if (fclose(file) != 0) { perror("fclose"); failed = 1; }
    /* Half-close marks EOF; no int-sized cumulative length or whole-file buffer. */
    if (!failed && shutdown(sock, SHUT_WR) < 0) { perror("shutdown"); failed = 1; }
    if (!failed) {
        ssize_t count_read;
        do { count_read = read(sock, buffer, sizeof(buffer)); }
        while (count_read > 0 || (count_read < 0 && errno == EINTR));
        if (count_read < 0) { perror("read"); failed = 1; }
    }
    if (close(sock) < 0) { perror("close"); failed = 1; }
    if (failed) return EXIT_FAILURE;
    printf("File '%s' sent; connection closed by server.\n", base_filename);
/* END TODO IMPLEMENTATION */

    return 0;
}