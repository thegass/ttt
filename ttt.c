#include <stdio.h>
#include <stdlib.h>
#include "board.h"

int main()
{
    Board mainBoard;

    initBoard(&mainBoard,3);
    
    printf("Hello World %d\n", mainBoard.size);
    
    return 0;
}