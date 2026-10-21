#include "utils.h"
#include "server.h"
#include "network.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <sys/types.h>
#include <unistd.h>


/* Auxiliary startup synchronization, implemented in server.c. */
void waitForServer(void);

int main(int argc, char **argv) {
    // Read in port number, TTL, directory, and neighbors from arguments
    int portNumber, neighborPortNumber; // host port number
    int ttl; // host ttl
    char directory[128]; // host directory

    neighbors_t neighbors;
    pthread_mutex_t lock;

    if (argc < 4) {
        ERROR("ERROR: Insufficient arguments provided. Usage: ./p2p_server [PORT_NUM] [TTL] [DIR] [NEIGHBOR_HOST, ...]\n");
    }

    if (argc >= 4) {
        // Parse arguments
        portNumber = atoi(argv[1]);
        ttl = atoi(argv[2]);
        strcpy(directory, argv[3]);

        // Initialize neighbors
        initializeNeighbors(&neighbors);
        int i;
        for (i = 4; i < argc - 1; i += 2) {  // Increment by 2 to process both IP and port at the same time
            unsigned long hostIpAddress = getHostAddr(argv[i]);
            printf("[NEIGHBOR] HostIPaddr: %lu\n", hostIpAddress);
            neighborPortNumber = atoi(argv[i+1]);
            if (hostIpAddress < 0) {
                ERROR("ERROR: Could not find host\n");
            }
            // TODO: Save to neighbor data structure
            if (hostIpAddress == 0 || neighborPortNumber < 1 || neighborPortNumber > 65535) {
                ERROR("ERROR: Invalid neighbor address or port\n");
            }
            addNeighbor(&neighbors, hostIpAddress, neighborPortNumber);
            
            // print neighbor information
            printNeighborData(&neighbors);
            printf("[NEIGHBOR] Sent connection request to neighbor with address %s:%d \n", argv[i], portNumber);
        }
    }

    IDlist_t idList;
    serverArg_t serverArg;

    // Initialize ID list
    initializeList(&idList);

    /*
     * TODO: Send CONNECT packet to all neighbors
     */

    // Your code starts here
    packet_t connectPacket;
    generatePacket(&connectPacket, "", CONNECT, 0);
    connectPacket.port = portNumber;
    /* Send after the receiving thread has bound its listening socket. */
    // Your code ends here

    // Add values to server arguments
    serverArg.idList = &idList;
    serverArg.port = portNumber;
    serverArg.directory = directory;
    serverArg.lock = &lock;
    serverArg.neighbors = &neighbors;

    // TODO: Initialize the mutex, then create a thread to handle server operations
    // The server thread receives and handles CONNECT, QUERY, and RESPONSE packets.
    // Hint: The server() function is defined in server.c
    
    // Your code starts here
    pthread_t serverThread;
    if (pthread_mutex_init(&lock, NULL) != 0) {
        ERROR("ERROR: Could not initialize mutex\n");
    }
    if (pthread_create(&serverThread, NULL, server, &serverArg) != 0) {
        ERROR("ERROR: Could not create server thread\n");
    }
    waitForServer();
    pthread_mutex_lock(&lock);
    floodRequest(&neighbors, portNumber, &connectPacket, sizeof(connectPacket));
    pthread_mutex_unlock(&lock);
    // Your code ends here
    
    // The main thread while loop: reads filenames from the user, searches
    // locally and sends queries to neighbors if the file is not found.
    while (1) {
        // Read input from user
        char input[MAX_STRLEN];

        // Input filename for search
        printf("[FILE] Enter the File Name for Search: \n");
        fgets(input, MAX_STRLEN, stdin);
        int len = strlen(input);
        if (input[0] != '\0' && input[len - 1] == '\n') {
            input[len - 1] = '\0';
        }
      
        // First search local server directory
        if (findInDirectory(directory, input)) {
            printf("[FILE] Found file '%s' in local directory \n", input);
            continue;
        }
        
        /*
         * TODO: flooding
         * Hint: Ensure thread safety by using a mutex
         */
        
        // Your code starts here
        if (input[0] == '\0') {
            continue;
        }
        packet_t query;
        pthread_mutex_lock(&lock);
        generatePacket(&query, input, QUERY, ttl);
        while (findInList(&idList, query.ID)) {
            query.ID = generateIdentifier();
        }
        query.port = portNumber;
        addToDataList(&idList, query.ID);
        floodRequest(&neighbors, portNumber, &query, sizeof(query));
        pthread_mutex_unlock(&lock);

        // Your code ends here
    }

    return 0;
}
