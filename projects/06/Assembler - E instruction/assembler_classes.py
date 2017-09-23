import sys

# Unpacks each command into its underlying fields
class parser:
    # False cuando la linea este en blanco o sea un comentario
    isCommand = False;
    linestriped = '';
    commandType = '';
    ignoreLine = False;
    isMultilineComment = False;
    
    
    cCMDHaveDest = False;
    cCMDHaveComp = False;
    cCMDHaveJump = False;
    
    # TODO: Hacer un strip en cada metodo de la linea actual
    def __init__(self, line):
        # El cosntructor borra los comentarios de las lineas y les hace un strip
        striped = line.strip().replace(' ', '');
        cmnt1 = striped.find('//');
        cmnt2 = striped.find('/*');
        cmnt2End = striped.find('*/');

        # NOTA: Si un comentario multilinea se usa como uno singlelinea es decir, en una misma linea se abre y se cierra, el ensamblador ignorara todas las lineas que le sigan
        # WHY? Esto debido a que el no encuentra el en de finalizacion en las lineas siguientes y deja la variable de isMultilineComment true por el resto del programa en el asmhack.py
        if cmnt1 != -1:
            self.linestriped = striped[0:cmnt1];
        elif cmnt2 != -1:
            self.linestriped = striped[0: cmnt2];
            parser.isMultilineComment = True;
        elif cmnt2End != -1:
            self.linestriped = striped[cmnt2End+2:];
            '''
            En python un atributo puede ser de instancia o estatico
            y tener el mismo nombre, todo depende de como accedo a el.

            si accedo a travez del nombre de la instancia es un atributo de instancia

            si accedo a travez del nombre de la clase es un atriubuto estatico y por
            lo tanto el mismo para todas las instancias.
            https://stackoverflow.com/questions/27481116/how-to-declare-a-static-attribute-in-python
            '''
            parser.isMultilineComment = False;
        else:
            self.linestriped = striped;

        if self.linestriped == '':
        	self.ignoreLine = True;

    '''
    Returns
    A_COMMAND a-instruction
    C_COMMAND c-instruction
    L_COMMAND label-instruction
    '''
    def commandType(self):
        if self.linestriped[0] == '@':
            #print(line.strip(), ' is an A-instruction');
            commandType = 'A_COMMAND';
        elif self.linestriped[0] == '(':
            #print(line.strip(), ' Is a label instruction');
            commandType = 'L_COMMAND';
        elif self.linestriped[0] == 'E' or self.linestriped[0] == 'e':
            commandType = 'E_COMMAND';
        elif not (self.linestriped[0:2] == '/*' or self.linestriped[0:2] == '//' or self.linestriped[0] == '\n'):
            #TODO: Segun esto, sera c-comand en lineas en blanco, o que empiecen con comentarios, corregir esto
            #print(line.strip(), ' Is a C-intruction');
            commandType = 'C_COMMAND';
        else:
            commandType = 'UNDEFINED';

        return commandType;
    
    '''
    Returns the symbol or decimal xxx of the current command @xxx or (xxx),
    should be called only when commandType() is L or A
    '''
    def symbol(self, cmdType):
        cmnt1 = self.linestriped.find('//');
        cmnt2 = self.linestriped.find('/*');
        if cmdType == 'A_COMMAND':            

            if cmnt1 != -1:
                symbol = self.linestriped[1:cmnt1];
            elif cmnt2 != -1:
                symbol = self.linestriped[1:cmnt2];
            else:
                symbol = self.linestriped[1:];
            
            # TODO: Manejar simbolos
            '''
            if symbol.isDecimal():
                this is a value to asign to A register
            elif symbol.isidentifier():
                this is a variable.
            '''
            return symbol;

        elif cmdType == 'L_COMMAND':
            # TO-DO: Process this type of pseudo-instructions
            i = self.linestriped.find(')');
            rightIndex = 1;
            if i > 1:
                rightIndex = i;
            else:
                return 'ERROR';
            
            symbol = self.linestriped[1:rightIndex];
            
            if symbol.find(' ') > -1:
                return 'ERROR';
            
            '''
            if symbol.isDecimal():
                pass;
            elif symbol.test_isidentifier():
                pass;
            else:
                return 'ERROR';
            '''
            return symbol;
        else:
            return 'ERROR';
        
    def dest(self):
        rightIndexVal = 1;
        
        if self.linestriped.find('=') == -1:
            destval = 'NO';
        else:
            rightIndexVal = self.linestriped.find('=');        
            destval = self.linestriped[0:rightIndexVal];
        
        return destval;
    
    '''
    En una instruccion tipo C el valor el comp field es obligatorio,
    los otros dos en cambio, si son opcionales.
    '''
    def comp(self):
        # El comp field es obligatorio
        
        rightIndexVal = 1;
        
        leftIndexVal = 0;

        # Si no hay signo igual, los primeros caracteres son el comp field
        # si no tiene este signo entonces no se especifica el destino
        eqPos = self.linestriped.find('=');
        if (eqPos == -1):
            self.cCMDHaveDest = False;
            # Donde termina
            # termina en el ';' o en ' ' o en '\n'
            rightIndexVal = self.linestriped.find(';');
            leftIndexVal = 0;
        else:
            
            leftIndexVal = self.linestriped.find('=')+1;
            rightIndexVal = len(self.linestriped);       
        
        compval = self.linestriped[leftIndexVal:rightIndexVal];
        '''
        Validar que cCMDHaveComp sea true solo si compval es un valor correcto,
        compval in posibleCompValVector
        '''
        self.cCMDHaveComp = True;
        return compval;
    
    def jump(self):
        leftIndexLimit = 0;
        rightIndexLimit = 1;
        
        jumpval = '';
        
        if self.linestriped.find(';') == -1:
            #print(self.line.find(';'))
            jumpval = 'NO';
        else:
            leftIndexLimit = self.linestriped.find(';')+1;
            jumpval = self.linestriped[leftIndexLimit:];        
        
        return jumpval;

    def erase(self):
        return self.linestriped[1:];
                
    
    

# Translates each field into its corresponding binary value and assembles the resulting values
class code:
    '''
    Dest mnemonic table:
    '''
    destMnemonic = {
        'NO':  '000', # Null
        'M':   '001',
        'D':   '010',
        'MD':  '011',
        'A':   '100',
        'AM':  '101',
        'AD':  '110',
        'AMD': '111'
        };

    eraseMnemonic = {
        'ADC': '111',
        'A': '100',
        'D': '010',
        'C': '001',
        'AC': '101',
        'DC': '011',
        'AD': '110',
        'NO': '000'
    };
        
    jumpMnemonic = {
        'NO':  '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
        };
        
    compMnemonic = {
        # When a=0
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        '!D': '0001101',
        '!A': '0110001',
        '-D': '0001111',
        '-A': '0110011',
        
        'D+1': '0011111',
        '1+D': '0011111',
        
        'A+1': '0110111',
        '1+A': '0110111',
        
        'D-1': '0001110',
        '-1+D': '0001110',
        
        'A-1': '0110010',
        '-1+A': '0110010',
        
        'D+A': '0000010',
        'A+D': '0000010', # A+D = D+A
        
        'D-A': '0010011',
        '-A+D': '0010011',
        
        'A-D': '0000111',
        '-D+A': '0000111',
        
        'D&A': '0000000',
        'A&D': '0000000',
        
        'D|A': '0010101',
        'A|D': '0010101',
        
        # when a=1
        'M': '1110000',
        '!M': '1110001',
        '-M': '1110011',
        
        'M+1': '1110111',
        '1+M': '1110111',
        
        'M-1': '1110010',
        '-1+M': '1110010',
        
        'D+M': '1000010',
        'M+D': '1000010',
        
        'D-M': '1010011',
        '-M+D': '1010011',
        
        'M-D': '1000111',
        '-D+M': '1000111',
        
        'D&M': '1000000',
        'M&D': '1000000',
        
        'D|M': '1010101',
        'M|D': '1010101'
        }
    
    def __init__(self):
        pass;
    
    def ainstr(self, val):
        valstrip = val.replace(' ', '').strip();
        code = '0'+bin(int(valstrip))[2:].zfill(15);
        
        return code;
            
    
    def dest(self, mnemonic):
        mnemonicstrip = mnemonic.replace(' ', '').strip();
        code = '000';
        
        if mnemonicstrip in self.destMnemonic:
            code = self.destMnemonic[mnemonicstrip];
        else:
            code = '000';
        
        return code;
    
    def comp(self, mnemonic):
        mnemonicstrip = mnemonic.replace(' ', '').strip();
        code = '000';
        
        if mnemonicstrip in self.compMnemonic:
            code = self.compMnemonic[mnemonicstrip];
        else:
            print('Syntax error in Asembly code');
            sys.exit(-1);
        
        return code;
    
    def jump(self, mnemonic):
        mnemonicstrip = mnemonic.replace(' ', '').strip();
        code = '000';
        
        if mnemonicstrip in self.jumpMnemonic:
            code = self.jumpMnemonic[mnemonicstrip];
        else:
            code = '000';
        
        return code;

    def erase(self, mnemonic):
        mnemonicstrip = mnemonic.replace(' ', '').strip();
        code = '000';

        if mnemonicstrip in self.eraseMnemonic:
            code = self.eraseMnemonic[mnemonicstrip];
        else:
            code = '000';

        return code;

# Manages the symbol table
class symbolTable:
    symbolTable = '';
    def __init__(self):
        self.symbolTable = {
            'R0': 0,
            'R1': 1,
            'R2': 2,
            'R3': 3,
            'R4': 4,
            'R5': 5,
            'R6': 6,
            'R7': 7,
            'R8': 8,
            'R9': 9,
            'R10': 10,
            'R11': 11,
            'R12': 12,
            'R13': 13,
            'R14': 14,
            'R15': 15,
            'SP': 0,
            'LCL': 1,
            'ARG': 2,
            'THIS': 3,
            'THAT': 4,
            'SCREEN': 16384,
            'KBD': 24576
            };
            
    def addEntry(self, symbol, addr):
        self.symbolTable[symbol] = addr;
    
    def contains(self, symbol):
        val = False;
        
        if symbol in self.symbolTable:
            val = True;
        
        return val;
    
    def getAddress(self, symbol):
        return self.symbolTable.get(symbol);

