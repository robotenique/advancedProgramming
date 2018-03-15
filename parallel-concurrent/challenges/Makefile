#
# @author: Juliano Garcia de Oliveira Nº USP: 9277086
#
CC=gcc
CFLAGS = -Wall -pedantic -O0 -std=gnu11
#LDFLAGS = -lrt -lm -pthread

.PHONY: clean


all: challenge_01

c_01: challenge_01.o
	$(CC) -o $@ $^ $(LDFLAGS)


%.o: %.c %.h
	$(CC) $(CFLAGS) -c $< -o $@ $(LDFLAGS)


%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@ $(LDFLAGS)


clean:
	rm -f *.o *~ *.out challenge_01
