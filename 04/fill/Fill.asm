// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


// QUESTION: How big is the screen again? Like how do I know when I'm done?

(LOOP)
    // check for keyboard input
    @KBD
    D=M;
    @FILL
    D; JGT  // jump to FILL if D > 0 (which should indicate a key being pressed)

    // restart the loop to wait for keyboard input
    @LOOP
    0;JMP

(FILL)
    // set up for fill loop
    @8191
    D=A
    @i
    M=D  // store 8191 in @i for looping purposes

(FILLLOOP)
    // let's DO, CHECK, DEC for this loop
    // pixel arithmetic to get to desired pixel
    @i
    D=M
    @SCREEN
    A=D+A    // add @SCREEN to @i to fill pixels last-to-first
    M=-1     // turn it black

    // check if we're done with loop
    @i
    D=M
    @FILLEDLOOP
    D; JEQ   // this is the only way out of this loop  

    // decrement value of @i
    @i
    M=M-1
    @FILLLOOP
    0; JMP



(FILLEDLOOP)
    // hang out here until key is lifted, when key is lifted, go back to main loop
    @KBD
    D=M
    @UNFILL
    D; JEQ
    @FILLEDLOOP
    0; JMP



(UNFILL)  // maybe combine fill and unfil and just use a variable?
    // set up for fill loop
    @8191
    D=A
    @i
    M=D  // store 8191 in @i for looping purposes


(UNFILLLOOP)
    // let's DO, CHECK, DEC for this loop
    // pixel arithmetic to get to desired pixel
    @i
    D=M
    @SCREEN
    A=D+A    // add @SCREEN to @i to fill pixels last-to-first
    M=0     // turn it white

    // check if we're done with loop
    @i
    D=M
    @LOOP
    D; JEQ   // this is the only way out of this loop  

    // decrement value of @i
    @i
    M=M-1
    @UNFILLLOOP
    0; JMP

