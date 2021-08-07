CC_FLAGS = -Wall

all: ttt.o board.o
	cc $(CC_FLAGS) -o ttt ttt.o board.o

ttt.o: ttt.c
	cc $(CC_FLAGS) -c -o ttt.o ttt.c

board.o: board.c
	cc $(CC_FLAGS) -c -o board.o board.c

run: ttt
	./ttt

clean:
	rm *.o
	rm ttt

