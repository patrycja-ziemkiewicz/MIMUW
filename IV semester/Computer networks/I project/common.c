#include <sys/types.h>
#include <sys/socket.h>
#include <errno.h>
#include <inttypes.h>
#include <limits.h>
#include <netdb.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <stdbool.h>

#include "err.h"
#include "common.h"

uint16_t read_port(char const *string) {
    char *endptr;
    errno = 0;
    unsigned long port = strtoul(string, &endptr, 10);
    if (errno != 0 || *endptr != 0 || port > UINT16_MAX) {
        fatal("%s is not a valid port number", string);
    }
    return (uint16_t) port;
}

struct sockaddr_in get_server_address(char const *host, uint16_t port) {
    struct addrinfo hints;
    memset(&hints, 0, sizeof(struct addrinfo));
    hints.ai_family = AF_INET; // IPv4
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_protocol = IPPROTO_UDP;

    struct addrinfo *address_result;
    int errcode = getaddrinfo(host, NULL, &hints, &address_result);
    if (errcode != 0) {
        fatal("getaddrinfo: %s", gai_strerror(errcode));
    }

    struct sockaddr_in send_address;
    send_address.sin_family = AF_INET;   // IPv4
    send_address.sin_addr.s_addr =       // IP address
            ((struct sockaddr_in *) (address_result->ai_addr))->sin_addr.s_addr;
    send_address.sin_port = htons(port); // port from the command line

    freeaddrinfo(address_result);

    return send_address;
}

void read_params(int argc, char *argv[], cfg *params) {
    bool b_set = false, a_set = false, p_set = false, r_set = false;

    params->bind_addr = NULL;
    params->peer_addr = 0;
    params->peer_addr = NULL;
    params->port = 0;
    params->send_hello = false;

    // Reading params.
    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "-b") == 0 && (i + 1 < argc) && !b_set) {
            params->bind_addr = argv[++i];
            b_set = true;
        }
        else if (strcmp(argv[i], "-a") == 0 && (i + 1 < argc) && !a_set) {
            params->peer_addr = argv[++i];
            a_set = true;
        }
        else if (strcmp(argv[i], "-p") == 0 && (i + 1 < argc) && !p_set) {
            params->port = read_port(argv[++i]);
            p_set = true;
        }
        else if (strcmp(argv[i], "-r") == 0 && (i + 1 < argc) && !r_set) {
            params->peer_port = read_port(argv[++i]);
            r_set = true;
            if (params->peer_port == 0)
                fatal("peer port cannot be 0");
        }
        else {
            fatal("invalid parameter: %s ", argv[i]);
        }
    }

    if (a_set != r_set) {
        fatal("Options -a and -r must be used together or not at all.");
    }

    if (a_set && r_set) {
        params->send_hello = true;
    }

}

ssize_t send_msg(int socket_fd, const uint8_t *buffer, size_t len, struct sockaddr_in *dst) {
    socklen_t dst_length = (socklen_t) sizeof(*dst);
    ssize_t sent_length = sendto(socket_fd, buffer, len, MSG_DONTWAIT,
        (struct sockaddr *) dst, dst_length);
    if (sent_length < 0) {
        if (errno == EAGAIN || errno == EWOULDBLOCK) {
            //error("couldn't send message");
            return -2;
        }
        else {
            syserr("sendto");
        }
    }
    else if ((size_t) sent_length != len) {
        fatal("incomplete sending");
    }

    return sent_length;
}

ssize_t recv_msg(int socket_fd, uint8_t *buffer, size_t max, struct sockaddr_in *src, socklen_t* src_length) {
    int flags = 0;

    ssize_t received_length = recvfrom(socket_fd, buffer, max, flags,
                            (struct sockaddr *) src, src_length);
    if (received_length < 0) {
        if (errno == EAGAIN || errno == EWOULDBLOCK)
            return -2; 
        syserr("recvfrom");
    }
    return received_length;
}
