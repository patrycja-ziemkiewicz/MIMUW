#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <poll.h>
#include <signal.h>
#include <stdbool.h>
#include <stdio.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <endian.h>

#include "err.h"
#include "common.h"

// Komunikaty.
#define HELLO 1
#define HELLO_REPLY 2
#define CONNECT 3
#define ACK_CONNECT 4
#define SYNC_START 11
#define DELAY_REQUEST 12
#define DELAY_RESPONSE 13
#define LEADER 21
#define GET_TIME 31
#define TIME 32

// Dlugosci komunikatow.
#define LEN_HELLO 1
#define LEN_HELLO_REPLY_BASE 3
#define LEN_CONNECT 1
#define LEN_ACK_CONNECT 1
#define LEN_SYNC_START 10
#define LEN_DELAY_REQUEST 1
#define LEN_DELAY_RESPONSE 10
#define LEN_LEADER 2
#define LEN_GET_TIME 1
#define LEN_TIME 10

#define MAX_MESSAGE_SIZE 65507
#define MAX_PEERS 65535
#define SYNC_START_TIMEOUT 7000
#define SYNCHRONIZATION_TIMEOUT 25000

typedef struct {
    struct sockaddr_in address;
    bool ack_received;
    bool connect_send;
    bool sync_send;
} peer_record;

static struct timespec program_start;

static inline uint64_t htonll(uint64_t x) { return htobe64(x); }
static inline uint64_t ntohll(uint64_t x) { return be64toh(x); }

void init_clock() {
    clock_gettime(CLOCK_MONOTONIC, &program_start);
}

// Obecny czas w MS.
uint64_t now_ms() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);

    int64_t sec_diff = (int64_t)ts.tv_sec - (int64_t)program_start.tv_sec;
    int64_t ns_diff = (int64_t)ts.tv_nsec - (int64_t)program_start.tv_nsec;

    return (uint64_t)(sec_diff * 1000 + ns_diff / 1000000);
}

bool sockaddr_in_equal(struct sockaddr_in *a,struct sockaddr_in *b) {
    return a->sin_family == b->sin_family
    && a->sin_addr.s_addr == b->sin_addr.s_addr
    && a->sin_port == b->sin_port;
}

bool is_known_peer(peer_record *peers, uint16_t n_peers, struct sockaddr_in client) {
    for (uint16_t i = 0; i < n_peers; ++i) {
        if (sockaddr_in_equal(&client, &peers[i].address)) {
            return true;
        }
    }
    return false;
}

bool can_receive_request(peer_record *peers, uint16_t n_peers, struct sockaddr_in client) {
    for (uint16_t i = 0; i < n_peers; ++i) {
        if (sockaddr_in_equal(&client, &peers[i].address) && peers[i].sync_send) {
            return true;
        }
    }
    return false;
}

void add_peer(struct sockaddr_in client_address, peer_record *peers, uint16_t* n_peers){
    if (!is_known_peer(peers, *n_peers, client_address)) {
        peers[*n_peers].address = client_address;
        peers[*n_peers].sync_send = false;
        (*n_peers)++;
    }
}

void unsynchronize(uint8_t *synchronized, int64_t *clock_offset, bool *is_synchronized) {
    *is_synchronized = false;
    *synchronized = 255;
    *clock_offset = 0;
}

ssize_t pack_hello_reply(uint8_t *buf, peer_record peers[], uint16_t n_peers) {
    size_t size = LEN_HELLO_REPLY_BASE;
    size += (1 + 4 + 2) * n_peers;

    if (size >= MAX_MESSAGE_SIZE)
        return -1;

    ssize_t off = 0;
    buf[off++] = HELLO_REPLY;

    uint16_t cnt_be = htons(n_peers);
    memcpy(buf + off, &cnt_be, 2);
    off += 2;

    for (uint16_t i = 0; i < n_peers; i++) {
        peer_record *pr = &peers[i];

        buf[off++] = 4;

        memcpy(buf + off, &pr->address.sin_addr.s_addr, 4);
        off += 4;

        memcpy(buf + off, &pr->address.sin_port, 2);
        off += 2;
    }

    return off;
}

ssize_t unpack_hello_reply(uint8_t *buf, size_t buf_len, peer_record potential_peers[], uint16_t* n_potential_peers) {

    if (buf_len < LEN_HELLO_REPLY_BASE) return -1;

    uint16_t count;
    memcpy(&count, buf + 1, 2);
    count = ntohs(count);

    if (count >= MAX_PEERS) return -1;

    size_t off = LEN_HELLO_REPLY_BASE;
    for (uint16_t i = 0; i < count; ++i) {

        if (off + 1 > buf_len) return -1;

        peer_record *pr = &potential_peers[i];
        uint8_t addr_len = buf[off++];

        if (addr_len != 4) return -1;  // Spodziewam się IPv4.
        pr->address.sin_family = AF_INET;

        if (off + addr_len + 2 > buf_len) return -1;

        memcpy(&pr->address.sin_addr.s_addr, buf + off, addr_len);
        off += addr_len;

        memcpy(&pr->address.sin_port, buf + off, 2);
        if (pr->address.sin_port == 0) // Niepoprawny port.
            return -1;
        off += 2;

        pr->connect_send  = false;
        pr->ack_received  = false;
    }

    *n_potential_peers = count;

    return 0;
}

// Funkcja zapisujaca w buforze message, synchronized i obecny czas zegara.
void pack_current_time(uint8_t *buf, uint8_t synchronized, int64_t clock_offset, uint8_t message) {
    buf[0] = message;
    buf[1] = synchronized;

    uint64_t now = now_ms();

    int64_t corrected = (int64_t)now - clock_offset;

    uint64_t time = htonll((uint64_t)corrected);
    memcpy(buf + 2, &time, 8);
}

int main(int argc, char *argv[]) {

    // Uruchomienie zegara.
    init_clock();
    cfg params;
    read_params(argc, argv, &params);

    int socket_fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (socket_fd < 0) {
        syserr("cannot create a socket");
    }

    struct sockaddr_in server_address;
    server_address.sin_family = AF_INET;

    if (params.bind_addr != NULL) {
        if (inet_pton(AF_INET, params.bind_addr, &server_address.sin_addr) != 1) {
            fatal("Invalid IPv4 address given by -b: %s", params.bind_addr);
        }
    }
    else {
        server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    }
    server_address.sin_port = htons(params.port);

    if (bind(socket_fd, (struct sockaddr *) &server_address, (socklen_t) sizeof(server_address)) < 0) {
        syserr("bind");
    }

    // Ustawiam limit czasu funkcji recvfrom na 2s.
    struct timeval tv = { .tv_sec = 2, .tv_usec = 0 };
    if (setsockopt(socket_fd, SOL_SOCKET, SO_RCVTIMEO, (void *)&tv, sizeof(tv))) {
        syserr("setsockopt");
    }

    static uint8_t buffer[MAX_MESSAGE_SIZE];
    static peer_record peers[MAX_PEERS], potential_peers[MAX_PEERS];

    //sync_synchronized - zmienna trzymajaca wartosc pola synchronized otrzymanego w komunikacie SYNC_START.
    uint8_t synchronized = 255, sync_synchronized = 255;
    uint16_t n_peers = 0, n_potential_peers = 0;
    struct sockaddr_in hello_reply_addr = {0}, synchronized_addr = {0}, sync_start_addr = {0};
    // last_sync_recv - zmienna okreslajaca ostatni czas wyslania komunikatu SYNC_START.
    // last_sync_recv - zmienna okreslajaca ostatni czas otrzymania komunikatu SYNC_START od wezla z ktorym jestsmy zsynchronizowani.
    // sync_start - zmienna okreslajaca czas otrzymanego komunikatu SYNC_START po ktorym rozpoczal sie proces synchronizacji.
    uint64_t last_sync_sent = 0, last_sync_recv = 0, sync_start = 0, T1 = 0, T2 = 0, T3 = 0, T4 = 0;
    int64_t clock_offset = 0;
    bool sync_in_progress = false, is_synchronized = false;

    // Sending HELLO message.
    if (params.send_hello) {
        buffer[0] = HELLO;
        hello_reply_addr = get_server_address(params.peer_addr, params.peer_port);
        if (send_msg(socket_fd, buffer, LEN_HELLO, &hello_reply_addr) != LEN_HELLO) {
            // Nie udalo sie wyslac komunikatu HELLO.
            params.send_hello = false;
        }
    }

    // Glowna petla programu.
    while(1) {
        struct sockaddr_in client_address;
        socklen_t address_length = (socklen_t) sizeof(client_address);

        ssize_t received_length = recv_msg(socket_fd, buffer, MAX_MESSAGE_SIZE, &client_address, &address_length);
        if (received_length > 0) {
            uint8_t message = buffer[0];
            switch (message) {
                case HELLO: {
                    // Obsługa HELLO
                    if (received_length != LEN_HELLO) {
                        error_msg(buffer, received_length);
                        break;
                    }
                    if (n_peers >= MAX_PEERS) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    ssize_t size_of_reply = pack_hello_reply(buffer, peers, n_peers);

                    // Jezeli jeszcze nie znamy tego wezla dodajemy go do listy znanych wezlow.
                    add_peer(client_address, peers, &n_peers);

                    // Komunikat HELLO_REPLY przekracza wielkosc maksymalnej wiadomosci jaka mozemy wyslac.
                    if (size_of_reply < 0) {
                        // Ignorowanie wyslania HELLO_REPLY.
                        error("can't send hello reply");
                        break;
                    }

                    send_msg(socket_fd, buffer, (size_t) size_of_reply, &client_address);

                    break;
                }
                case HELLO_REPLY: {
                    // Obsługa HELLO_REPLY
                    // Sprawdzenie czy czekamy na hello_reply.
                    if (!params.send_hello) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    if (!(sockaddr_in_equal(&hello_reply_addr, &client_address))) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    if (n_peers >= MAX_PEERS) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    // Odebralismy komunikat HELLO_REPLY.
                    params.send_hello = false;

                    // Sprawdzam czy komunikat HELLO_REPLY jest poprawny.
                    if(unpack_hello_reply(buffer, (size_t) received_length, potential_peers, &n_potential_peers) < 0) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    if (is_known_peer(potential_peers, n_potential_peers, server_address)) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    if (is_known_peer(potential_peers, n_potential_peers, hello_reply_addr)) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    // Jezeli jeszcze nie znamy tego wezla dodajemy go do listy znanych wezlow.
                    add_peer(client_address, peers, &n_peers);

                    buffer[0] = CONNECT;

                    for (ssize_t i = 0; i < n_potential_peers; ++i) {
                        struct sockaddr_in dest = potential_peers[i].address;

                        if (send_msg(socket_fd, buffer, LEN_CONNECT, &dest) == LEN_CONNECT) {
                            potential_peers[i].connect_send = true;
                        }
                    }
                    break;
                }
                case CONNECT: {
                    // Obsługa CONNECT
                    if (received_length != LEN_CONNECT) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    if (n_peers >= MAX_PEERS) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    add_peer(client_address, peers, &n_peers);

                    buffer[0] = ACK_CONNECT;

                    send_msg(socket_fd, buffer, LEN_ACK_CONNECT, &client_address);

                    break;
                }
                case ACK_CONNECT: {
                    // Obsługa ACK_CONNECT
                    if (received_length != LEN_ACK_CONNECT) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    if (n_peers >= MAX_PEERS) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    bool correct_message = false;
                    for (uint16_t i = 0; i < n_potential_peers; ++i) {
                        // Sprawdzamy czy wyslalismy wezlowi CONNECT i nie otrzymalismy jeszcze ACK_CONNECT.
                        if (!potential_peers[i].ack_received && potential_peers[i].connect_send) {
                            if (sockaddr_in_equal(&client_address, &potential_peers[i].address)) {
                                add_peer(client_address, peers, &n_peers);
                                potential_peers[i].ack_received = true;
                                correct_message = true;
                                break;
                            }
                        }
                    }

                    if (!correct_message) {
                        error_msg(buffer, received_length);
                    }
                    break;
                }
                case SYNC_START: {
                    // Obsługa SYNC_START
                    if (received_length != LEN_SYNC_START) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    if (!is_known_peer(peers, n_peers, client_address)) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    uint8_t rec_sync = buffer[1];
                    uint64_t now = now_ms();

                    if (sync_in_progress || rec_sync >= 254) {
                        // Sprawdzam czy nie otrzymalismy komunikaty od wezla z ktorym jestesmy zsychronizowani.
                        if (is_synchronized && sockaddr_in_equal(&client_address, &synchronized_addr)) {
                            if (rec_sync < synchronized) {
                                last_sync_recv = now;
                            }
                            else {
                                unsynchronize(&synchronized, &clock_offset, &is_synchronized);
                            }
                        }
                        // ignorowana wiadomosc
                        break;
                    }

                    T2 = now;

                    if (is_synchronized && sockaddr_in_equal(&client_address, &synchronized_addr)) {
                        if (rec_sync < synchronized) {
                            last_sync_recv = now;
                        }
                        else {
                            unsynchronize(&synchronized, &clock_offset, &is_synchronized);
                            break;
                        }
                    }
                    else if (rec_sync >= synchronized - 1) {
                        // igonrowana wiadomosc
                        break;
                    }

                    sync_in_progress = true;
                    sync_start_addr = client_address;
                    sync_synchronized = rec_sync;
                    sync_start = now;

                    uint64_t t1;
                    memcpy(&t1, &buffer[2], 8);
                    T1 = ntohll(t1);

                    buffer[0] = DELAY_REQUEST;

                    send_msg(socket_fd, buffer, LEN_DELAY_REQUEST, &client_address);

                    T3 = now_ms();
                    break;
                }
                case DELAY_REQUEST: {
                    // Obsługa DELAY_REQUEST
                    if (received_length != LEN_DELAY_REQUEST) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    if (!can_receive_request(peers, n_peers, client_address)) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    pack_current_time(buffer, synchronized, clock_offset, DELAY_RESPONSE);
                    send_msg(socket_fd, buffer, LEN_DELAY_RESPONSE, &client_address);
                    break;
                }
                case DELAY_RESPONSE: {
                    // Obsługa DELAY_RESPONSE
                    if (received_length != LEN_DELAY_RESPONSE) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    uint64_t now = now_ms();
                    if (!sync_in_progress || now >= sync_start + SYNC_START_TIMEOUT) {
                        sync_in_progress = false;
                        error_msg(buffer, received_length);
                        break;
                    }

                    if (!sockaddr_in_equal(&client_address, &sync_start_addr)) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    uint8_t rec_synchronized = buffer[1];
                    if (rec_synchronized != sync_synchronized) {
                        error_msg(buffer, received_length);
                        sync_in_progress = false;
                        break;
                    }

                    uint64_t t;
                    memcpy(&t, &buffer[2], 8);
                    T4 = ntohll(t);

                    if (T1 > T4) {
                        error_msg(buffer, received_length);
                        sync_in_progress = false;
                        break;
                    }
                    // Węzęł został zsynchronizowany.
                    clock_offset = ((int64_t) T2 - (int64_t) T1 + (int64_t) T3 - (int64_t) T4) / 2;
                    synchronized = sync_synchronized + 1;
                    synchronized_addr = sync_start_addr;
                    last_sync_recv = sync_start;
                    is_synchronized = true;
                    sync_in_progress = false;
                    break;
                }
                case LEADER: {
                    // Obsługa LEADER
                    if (received_length != LEN_LEADER) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    uint8_t rec_sync = buffer[1];

                    if (rec_sync == 0) {
                        sync_in_progress = false;
                        unsynchronize(&synchronized, &clock_offset, &is_synchronized);
                        synchronized = 0;
                    }
                    else if (rec_sync == 255 && synchronized == 0) {
                        synchronized = 255;
                    }
                    else {
                        error_msg(buffer, received_length);;
                    }
                    break;
                }
                case GET_TIME: {
                    // Obsługa GET_TIME
                    if (received_length != LEN_GET_TIME) {
                        error_msg(buffer, received_length);
                        break;
                    }

                    pack_current_time(buffer, synchronized, clock_offset, TIME);
                    send_msg(socket_fd, buffer, LEN_TIME, &client_address);
                    break;
                }
                default: {
                    error_msg(buffer, received_length);
                    break;
                }
            }
        }
        else if (received_length == 0){
            error_msg(buffer, received_length);
        }
        // Checking synchronization.
        uint64_t now = now_ms();
        if (is_synchronized && now >= last_sync_recv + SYNCHRONIZATION_TIMEOUT) {
            unsynchronize(&synchronized, &clock_offset, &is_synchronized);
        }

        if (sync_in_progress && now >= sync_start + SYNC_START_TIMEOUT) {
            sync_in_progress = false;
        }

        // Sending SYNC_START.
        if (synchronized < 254 && now >= last_sync_sent + SYNC_START_TIMEOUT){
            last_sync_sent = now;

            pack_current_time(buffer, synchronized, clock_offset, SYNC_START);

            for (size_t i = 0; i < n_peers; ++i) {
                struct sockaddr_in dest = peers[i].address;
                if (send_msg(socket_fd, buffer, LEN_SYNC_START, &dest) == LEN_SYNC_START) {
                    peers[i].sync_send = true;
                }
                else {
                    peers[i].sync_send = false;
                }
            }
        }
    }

    close(socket_fd);

    return 0;
}
