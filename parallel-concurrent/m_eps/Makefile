#
# @author: Juliano Garcia de Oliveira Nº USP: 9277086
#
CC=gcc
CFLAGS = -Wall -pedantic -O0 -std=gnu11
#LDFLAGS = -lrt -lm -pthread

.PHONY: clean


all: m_ep01

m_ep01: m_ep01.o
	$(CC) -o $@ $^ $(LDFLAGS)


%.o: %.c %.h
	$(CC) $(CFLAGS) -c $< -o $@ $(LDFLAGS)


%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@ $(LDFLAGS)


clean:
	rm -f *.o *~ *.out m_ep01
