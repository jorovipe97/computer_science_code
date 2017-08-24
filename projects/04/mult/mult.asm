// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@R0 // 0
D=M
@sum // 16
M=0 // RAM[16] = 0
@i // 17
M=0

(BLOCK1)
@R1 // 1
D=M
@i // 17
D=M-D // D=sum-(R1-1), this will be util on conditional
@BLOCK2
D;JGE  // Condicion para salirse del while
// start while


@R0
D=M
@sum
M=M+D


@i // i++ start
D=M
M=D+1 // i++
@BLOCK1
0;JMP
(BLOCK2)
@sum
D=M
@R2
M=D
(END)
@END
0;JMP