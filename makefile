CC=gcc
CFLAGS=-std=c99 -O3
SRC = src/NumberPrinter.c

.PHONY: default
default: NumberPrinter;

NumberPrinter:
	gcc $(SRC) -o $@ $(CFLAGS)