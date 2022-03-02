// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

//So I need to do some type of loop
//If I'm doing 3 * 5:
//
//x = 0
//n = 5
//i = 3
//
//LOOP {
//  x = x + n;
//  i = i - 1;
//  if i > 0; jump to LOOP
//  if i == 0; jump to END
//}
//
//END {
//@0;
//0; JMP
//}

// for i=0; i < R0; i++
// @answer += R1

// REAL CODE

// this is where we'll accumulate our answer
// initialize it to zero

// initialize our answer register to zero

    @R2
    M=0

    @R0
    D=M // store the value of @R0 in D

    @i
    M=D  // store the value of @R0 in @i

(LOOP)
    // check if end of loop
    @END
    D; JEQ

    // do the addition
    @R1
    D=M
    @R2
    M=D+M   // accumulating the answer here in R2

    // decrement i
    @i
    D=M
    MD=D-1

    // if M (@i) value is greater than zero then jump back to loop
    @LOOP
    D; JGT  // issue here, this isn't jumping... what is it looking at to determine if jump should happen?

(END)
    @END
    0; JMP

