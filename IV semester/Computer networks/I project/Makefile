CC      = gcc
CFLAGS = -std=gnu17 -O2 \
         -Wall -Wextra -pedantic \
         -Wshadow -Wconversion -Wsign-conversion \
         -Wnull-dereference
LDFLAGS = -Wall

TARGETS = peer-time-sync

all: $(TARGETS)

peer-time-sync: peer-time-sync.o common.o err.o

common.o: common.c common.h err.h
err.o: err.c err.h
peer-time-sync.o: peer-time-sync.c common.h err.h

.PHONY: clean

clean:
	rm -f $(TARGETS) *.o *~
