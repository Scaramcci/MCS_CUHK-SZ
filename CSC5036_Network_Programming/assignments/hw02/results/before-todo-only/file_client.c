// file_client.c

#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
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

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    struct sockaddr_in serv_addr;
    int sock = 0;
    char buffer[BUFFER_SIZE] = {0};

    /* Implemented: socket()
    * Create a socket using socket(AF_INET, SOCK_STREAM, 0)
    * Store the result in 'sock' variable
    * Print an error message and exit if it fails
    */
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) { perror("socket"); return EXIT_FAILURE; }
    memset(&serv_addr, 0, sizeof(serv_addr));

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    /* Implemented: inet_pton()
    * Convert the IP address "127.0.0.1" from text to binary form
    * Use inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)
    * Print an error message and exit if conversion fails (returns <= 0)
    */
    int converted = inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);
    if (converted <= 0) {
        if (converted < 0) perror("inet_pton");
        else fprintf(stderr, "Invalid server address\n");
        close(sock);
        return EXIT_FAILURE;
    }
    

    /* Implemented: connect()
    * Connect to the server.
    */
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("connect"); close(sock); return EXIT_FAILURE;
    }

    /* IMPLEMENTING SIMPLE FILE TRANSFER */

    // Variables you may need to declare:
    // FILE *file;
    // char *base_filename;

    /* Implemented: Open file for reading in binary mode
    * Use fopen() with "rb" mode
    */
    FILE *file = fopen(argv[1], "rb");
    if (!file) { perror("fopen"); close(sock); return EXIT_FAILURE; }

    /* Implemented: Extract filename from path (argv[1])
    * Use strrchr() to find the last '/' in the path
    * Example: "../file1.zip" -> "file1.zip"
    * If no '/' found, use the entire path as filename
    * Store result in base_filename
    */
    const char *base_filename = strrchr(argv[1], '/');
    base_filename = base_filename ? base_filename + 1 : argv[1];
    size_t filename_length = strlen(base_filename);
    if (filename_length == 0 || filename_length >= BUFFER_SIZE ||
        strcmp(base_filename, ".") == 0 || strcmp(base_filename, "..") == 0) {
        fprintf(stderr, "Invalid filename\n");
        fclose(file); close(sock); return EXIT_FAILURE;
    }

    /* Implemented: Send filename to server
    * Send the filename (padded to BUFFER_SIZE) so server knows what to name the file
    */
    memcpy(buffer, base_filename, filename_length);
    if (send_all(sock, buffer, sizeof(buffer)) < 0) {
        fclose(file); close(sock); return EXIT_FAILURE;
    }

    // You can add a small delay to avoid data mix-up

    /* Implemented: Send file content
    * Read file in chunks of BUFFER_SIZE and send each chunk
    */
    size_t count;
    int failed = 0;
    while ((count = fread(buffer, 1, sizeof(buffer), file)) > 0) {
        if (send_all(sock, buffer, count) < 0) { failed = 1; break; }
    }
    if (ferror(file)) { perror("fread"); failed = 1; }

    // printf("File '%s' uploaded successfully.\n", base_filename);

    /* Implemented: Close file and socket */
    if (fclose(file) != 0) { perror("fclose"); failed = 1; }
    /* EOF on the write half marks the end, regardless of file size. */
    if (!failed && shutdown(sock, SHUT_WR) < 0) { perror("shutdown"); failed = 1; }
    /* The server closes after flushing the file. Wait so tests can read it. */
    if (!failed) {
        ssize_t count_read;
        do { count_read = read(sock, buffer, sizeof(buffer)); }
        while (count_read > 0 || (count_read < 0 && errno == EINTR));
        if (count_read < 0) { perror("read"); failed = 1; }
    }
    if (close(sock) < 0) { perror("close"); failed = 1; }
    if (failed) return EXIT_FAILURE;
    printf("File '%s' sent; connection closed by server.\n", base_filename);

    return 0;
}