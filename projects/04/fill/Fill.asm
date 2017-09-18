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
@8192
D=A

@registros // Numero de registros que pertenecen a la pantalla
M=D
(BLOCKWHILE) // while(true)
	@i // 17
	M=0

	@KBD
	D=M
	@IFKBDEQ0
	D;JEQ
	(IFKBDNEQ0) // if (kbd != 0)

		(BLOCK1) // while (i<registros)
		@registros // 1
		D=M
		@i // 17
		D=M-D // D=i-(8192), this will be util on conditional
		@BLOCKWHILE
		D;JGE  // Condicion para salirse del while
		// start while

			@i
			D=M
			@SCREEN
			A=A+D
			D=A // screen+i
			@pointer // 18
			M=D // RAM[18] = screen+i
			//@32767 // linea 23
			//D=A
			//@32767
			//D=A+D
			D=-1
			@pointer
			A=M
			M=D


			@i // i++ start
			D=M
			M=D+1 // i++

		@BLOCK1
		0;JMP
	(IFKBDEQ0) // if (kbd == 0)
		(BLOCK2) // while (i<registros)
			@registros // 1
			D=M
			@i // 17
			D=M-D // D=i-(8192), this will be util on conditional
			@BLOCKWHILE
			D;JGE  // Condicion para salirse del while
			// start while

				
				@i
				D=M
				@SCREEN
				A=D+A // SCREEN[i]
				M=0 // SCREEN[i] = 0

				@i // i++ start
				D=M
				M=D+1 // i++

		@BLOCK2
		0;JMP

@BLOCKWHILE
0;JMP