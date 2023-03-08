
// ==================== push constant 10 ==================== 
@10
D=A
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== pop local 0 ==================== 
// calculating address offset
@LCL
D=M
@0
D=D+A

// decrementing stack pointer
@SP
M=M-1

// popping value to address A=D
@SP
A=M
D=M
A=D
M=D

// ==================== push constant 21 ==================== 
@21
D=A
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== push constant 22 ==================== 
@22
D=A
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== pop argument 2 ==================== 
// calculating address offset
@ARG
D=M
@2
D=D+A

// decrementing stack pointer
@SP
M=M-1

// popping value to address A=D
@SP
A=M
D=M
A=D
M=D

// ==================== pop argument 1 ==================== 
// calculating address offset
@ARG
D=M
@1
D=D+A

// decrementing stack pointer
@SP
M=M-1

// popping value to address A=D
@SP
A=M
D=M
A=D
M=D

// ==================== push constant 36 ==================== 
@36
D=A
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== pop this 6 ==================== 
// calculating address offset
@THIS
D=M
@6
D=D+A

// decrementing stack pointer
@SP
M=M-1

// popping value to address A=D
@SP
A=M
D=M
A=D
M=D

// ==================== push constant 42 ==================== 
@42
D=A
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== push constant 45 ==================== 
@45
D=A
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== pop that 5 ==================== 
// calculating address offset
@THAT
D=M
@5
D=D+A

// decrementing stack pointer
@SP
M=M-1

// popping value to address A=D
@SP
A=M
D=M
A=D
M=D

// ==================== pop that 2 ==================== 
// calculating address offset
@THAT
D=M
@2
D=D+A

// decrementing stack pointer
@SP
M=M-1

// popping value to address A=D
@SP
A=M
D=M
A=D
M=D

// ==================== push constant 510 ==================== 
@510
D=A
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== pop temp 6 ==================== 
// decrementing stack pointer
@SP
M=M-1

// popping value to address @11
@SP
A=M
D=M
@11
M=D

// ==================== push local 0 ==================== 
// calculating address offset
@LCL
D=M
@0
D=D+A

// pushing value to stack from A=D
A=D
D=M
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== push that 5 ==================== 
// calculating address offset
@THAT
D=M
@5
D=D+A

// pushing value to stack from A=D
A=D
D=M
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== push argument 1 ==================== 
// calculating address offset
@ARG
D=M
@1
D=D+A

// pushing value to stack from A=D
A=D
D=M
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== push this 6 ==================== 
// calculating address offset
@THIS
D=M
@6
D=D+A

// pushing value to stack from A=D
A=D
D=M
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== push this 6 ==================== 
// calculating address offset
@THIS
D=M
@6
D=D+A

// pushing value to stack from A=D
A=D
D=M
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1

// ==================== push temp 6 ==================== 
// pushing value to stack from @11
@11
D=M
@SP
A=M
M=D
// incrementing stack pointer
@SP
M=M+1
