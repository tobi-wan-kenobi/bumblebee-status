CC=gcc
CFLAGS=

%.o: %.c
	$(CC) -c -o $@ $< $(CFLAGS)

../bin/get-kbd-layout: layout.o
	$(CC) -o $@ layout.o -lX11

.PHONY: clean

clean:
	rm -f *.o
