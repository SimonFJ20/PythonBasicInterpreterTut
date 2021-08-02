

BIN=program

CC=gcc

CFLAGS=-g -Wall
LFLAGS=

SRC=src
HDR=src
OBJ=obj
LIB=lib

SRCS=$(wildcard $(SRC)/*.c)
HDRS=$(wildcard $(HDR)/*.h)
OBJS=$(patsubst $(SRC)/%.c, $(OBJ)/%.o, $(SRCS))

$(BIN): $(OBJS) $(OBJ)
	$(CC) $(CFLAGS) $(LFLAGS) $(OBJS) -o $@ -L$(LIB)

$(OBJ)/%.o: $(SRC)/%.c $(OBJ) $(HDRS)
	$(CC) $(CFLAGS) -c $< -o $@ -I$(HDR)

$(OBJ):
	mkdir -p $@

.PHONY: clean

clean:
	$(RM) -r $(OBJ)
	$(RM) $(BIN)


