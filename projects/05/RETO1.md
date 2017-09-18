// A instruction
0 11 1 111111 111 111 // @32767

// C instruction
1 11 0 110000 010 000 // D=A

// A instruction
0 00 0 000000 000 001 // @1

// C instruction
1 11 0 000010 010 000 // D=D+A

// A instruction
0 00 0 000000 000 000 // @0

// C instruction
1 11 0 001100 001 000 // M=D

var foo = 32767;
foo = foo + 1; // 32768
RAM[0] = foo;

var foo = 32767 + 1; // outs: -32768

// El resultado esperado es 32768 sin enbargo el resultado obtenido es -32768 (1000 0000 0000 0000)
// El hack simulator supone que el resultado esta en complemento a 2, razon por la cual se obtiene dicho resultado 