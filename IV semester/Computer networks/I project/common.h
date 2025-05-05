#ifndef MIM_COMMON_H
#define MIM_COMMON_H

#include <stddef.h>
#include <stdint.h>
#include <sys/types.h>

typedef struct {
    const char *bind_addr;
    const char *peer_addr;
    uint16_t port;
    uint16_t peer_port;
    bool send_hello;
} cfg;

uint16_t read_port(char const *string);
struct sockaddr_in get_server_address(char const *host, uint16_t port);
void read_params(int argc, char *argv[], cfg *params);
ssize_t send_msg(int socket_fd, const uint8_t *buffer, size_t len, struct sockaddr_in *dst);
ssize_t recv_msg(int socket_fd, uint8_t *buffer, size_t max, struct sockaddr_in *src, socklen_t* src_length); 
#endif
