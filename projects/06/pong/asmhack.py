import sys
import os;
from assembler_classes import *;

debug = False;

def main():
	"""
	Algorithm description:
	1. cargar archivo .asm
	"""
	translator = code();
	symbolt = symbolTable();
	
	try:
		fileName = sys.argv[1];
	except:
		print('Especifique un fichero .asm');
		fileName = 'Max.asm';
		#sys.exit(-1);
	
	outfileName = fileName.split('.')[0]+'.hack';
	asmWithoutSymbolsName = fileName.split('.')[0]+'-temp.asm';
	print(sys.argv[0]);
	print(fileName);
	try:
		outfile = open(outfileName, 'w');
		asmWithoutSymbols = open(asmWithoutSymbolsName, 'w'); # En este archivo se guardara el codigo con los symbols resueltos
	except:
		print('Error creating .hack file');

	# Agregando las labels romAddresses a la tabla de simbolos 
	romAddr = 0;
	try:
		with open(fileName, 'r') as fp2:
			print('Creating user defined GOTO labels...');
			for line in fp2:

				if line.strip(' \n') == '\n':
					continue;

				p2 = parser(line);
				if debug:
					print(repr(p2.linestriped));
				if p2.ignoreLine:
					continue;

				commandType = p2.commandType();
				if commandType == 'L_COMMAND':
					# Si el simbolo no esta en la tabla de simbolos
					
					if not symbolt.contains(p2.symbol(commandType)):
						if debug:
							print(p2.symbol(commandType));
						#pass;
						symbolt.addEntry(p2.symbol(commandType), romAddr);
				else:
					romAddr = romAddr + 1;
					
	except:
		print('Ha ocurrido un error con los labels');

	if debug:
		print(symbolt.symbolTable);

	# To-DO hacer el symbol resolver
	ramAddr = 16; # The allocated RAM addreses are running starting at address 16
	try:
		with open(fileName, 'r') as fp:
			print('Handling symbols and creating TEMP cleaned assembly file...');
			for line in fp:
				#print(repr(line))

				# Hace que las lineas en blanco se ignoren
				# Hace un strip de los caracteres ' ' y '\n' unicamente 
				if line.strip(' \t') == '\n':
					continue; # Continuar con la siguiente linea
				
				modline = '';
				
				p1 = parser(line);
				#print(repr(p1.linestriped))
				if p1.ignoreLine:
					continue;
				commandType = p1.commandType();
				
				if commandType == 'A_COMMAND':

					#print(repr(p1.symbol(commandType)) + 'foo');
					#print(str(symbolt.getAddress('R0')));
					
					if p1.symbol(commandType).isdigit():
						modline = p1.linestriped;
					else:
						if symbolt.contains(p1.symbol(commandType)): # puede ser una variable o un label
							# en python no se hace casting automatico al sumar un strin y un int
							modline = '@'+str(symbolt.getAddress(p1.symbol(commandType)));
						else: # Se refiere a una variable
							symbolt.addEntry(p1.symbol(commandType), ramAddr);
							ramAddr = ramAddr + 1;
							modline = '@'+str(symbolt.getAddress(p1.symbol(commandType)))

				elif commandType == 'L_COMMAND':
					continue;
				elif commandType == 'C_COMMAND':
					modline = p1.linestriped;
				
				#print(repr(modline));
				asmWithoutSymbols.write(modline+'\n');
	except:
		print('Error manejando los simbolos');
	asmWithoutSymbols.close();

	# string methods
	# https://docs.python.org/3/library/stdtypes.html#string-methods
	# str.find return -1 when no value was encountered while str.index raises a value error
	try:
		with open(asmWithoutSymbolsName, 'r') as fp:
			print('Generating machine binary code...');
			#print(fp)
			for line in fp:
				# Se quita el salto de linea del print para que se lea el que viene en el archivo .asm
				#print(repr(line), end='');
				'''
				Una linea puede ser:
				a. c-instruction
				b. a-instruction
				'''
				p = parser(line);
				commandType = p.commandType();
				if commandType == 'A_COMMAND':    
					#print(repr(line));                
					#print(p.symbol(commandType), ' @xxx', translator.ainstr(p.symbol(commandType)));
					outfile.write(translator.ainstr(p.symbol(commandType))+'\n')
				elif commandType == 'C_COMMAND':
					'''
					print(repr(line));
					print(p.comp(), ' ALU Computation', translator.comp(p.comp()));
					print(p.dest(), ' Dest ALU Output ', translator.dest(p.dest()));
					print(p.jump(), ' Jump ALU condition', translator.jump(p.jump()));
					'''
					outfile.write('111' + translator.comp(p.comp()) + translator.dest(p.dest()) + translator.jump(p.jump()) + '\n');
				else:
					#print(p.symbol(commandType), ' (xxx)');
					pass;
				
				#outfile.write('out: ' + line);
	except:
		print('Ha ocurrido un error creando el archivo .hack');
		sys.exit(-1);
	
	try:
		outfile.close();
	except:
		print('Ha ocurrido un error cerrando el .hack file')
	
	try:
		if not debug:
			print('Removing TEMP cleaned assembly file...');
			os.remove(asmWithoutSymbolsName);
	except:
		print('Error while was Removing TEMP cleaned assembly file.');
	

if __name__ == '__main__':
	main();
