
#
# Makefile
# For ostest/texrec
# By Simon From Jakobsen
#

BIN=program

CC=gcc
CFLAGS=-g -Wall
LFLAGS= 

SRC=src
OBJ=obj
HDR=include
LIB=lib

SRCS=$(wildcard $(SRC)/*.c)
OBJS=$(patsubst $(SRC)/%.c, $(OBJ)/%.o, $(SRCS))
HDRS=$(wildcard $(HDR)/*.h)

$(BIN): $(OBJS) $(OBJ)
	$(CC) $(CFLAGS) $(OBJS) -o $@ $(LFLAGS) -L$(LIB)

$(OBJ)/%.o: $(SRC)/%.c $(OBJ) $(HDRS)
	$(CC) $(CFLAGS) -c $< -o $@ -I$(HDR)

$(OBJ):
	mkdir -p $@

.PHONY: clean run
clean:
	$(RM) -r $(OBJ)
	$(RM) $(BIN)

run:
	./program

