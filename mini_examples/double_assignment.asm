
// store 2 in RAM[0]
@2
D=A
@0
M=D

// store 5 in RAM[3]
@5
D=A
@3
M=D

// point at RAM[0] and execute AM=M+1
@0
AM=M+1

// RAM[0] becomes 3 (M+1) and A now points at RAM[3]


