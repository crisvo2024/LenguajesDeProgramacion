import sys
class AnalizadorLexico:
    simbolosUnicos={
        '{':"llave_izq",
        '}':"llave_der",
        '(':"par_izq",
        ')':"par_der",
        ';':"puntoycoma",
        ',':"coma"
    }
    lexemasSimples={
        '>':"mayor",
        '<':"menor",
        '+':"mas",
        '-':"menos",
        '*':"mul",
        '/':"div",
        '%':"mod",
        ':':"dospuntos"
    }
    lexemasSimplesInvalidos=(
        '!',
        '='
    )
    lexemas_compuestos={
        ':=':"asignacion",
        '>=':"mayor_igual",
        '<=':"menor_igual",
        '+=':"sum_asig",
        '-=':"res_asig",
        '*=':"mul_asig",
        '/=':"div_asig",
        '%=':"mod_asig",
        '==':"igualdad",
        '!=':"diferente",
        '++':"incremento",
        '--':"decremento"
    }
    palabras_reservadas=(
        "bool",
        "num",
        "true",
        "false",
        "break",
        "next",
        "and",
        "or",
        "not",
        "print",
        "input",
        "if",
        "else",
        "while",
        "for",
        "do",
        "function",
        "return",
        "when",
        "unless",
        "until",
        "loop",
        "repeat",
        "var",
        "end"   
    )
    def __init__(self):
        # lines=""
        # while True:
        #     #var=sys.stdin.readline()
        #     var=input()
        #     if not var:
        #         break
        #     else:
        #         lines+=var+'\n'
        # self.stream=iter(lines)
        self.stream=iter("".join(sys.stdin.readlines()))
        self.valor=""
        self.line=1
        self.column=1
        self.finalizado=False 
        self.funcError=False 
        self.token=""  
        self.lenSym=0
        self.nextChar=next(self.stream) 
        self.testNoPrintable()

    def printToken(self):
        if self.token != self.valor:
            res=f"<{self.token},{self.valor},{self.line},{self.column}>"
        else:
            res=f"<{self.token},{self.line},{self.column}>"
        return res
        
    def printError(self):
        self.finalizado = True
        return str(f">>> Error léxico(línea:{self.line},posición:{self.column})")

    def numState(self):
        self.token="tk_num"
        while self.nextChar.isnumeric():
            self.valor+=self.nextChar
            self.nextChar=next(self.stream)
        if self.nextChar== '.':
            nextNext=next(self.stream)
            if nextNext.isnumeric():
                self.valor+=self.nextChar
                self.nextChar=nextNext
                while self.nextChar.isnumeric():
                    self.valor+=self.nextChar
                    self.nextChar=next(self.stream)

    def stringState(self):
        self.token="id"
        try:
            while self.nextChar.isalnum() or self.nextChar=='_':
                self.valor+=self.nextChar
                self.nextChar=next(self.stream)
            if self.valor in self.palabras_reservadas:
                self.token=self.valor
        except StopIteration:
            if self.valor in self.palabras_reservadas:
                self.token=self.valor
                self.finalizado=True


    def testNoPrintable(self):
        try:
            if self.nextChar == '#':
                while self.nextChar != '\n':
                    self.nextChar=next(self.stream)
            while not self.nextChar.isprintable() or self.nextChar.isspace() :
                if self.nextChar =='\n':
                    self.line+=1
                    self.column=1
                else:
                    if self.nextChar=='\t':
                        self.column+=4
                    else:
                        self.column+=1
                self.nextChar=next(self.stream)
                if self.nextChar == '#':
                    self.testNoPrintable()
        except StopIteration:
            self.finalizado=True
    
    def functionState(self):
        try:
            self.token="fid"
            self.valor+=self.nextChar
            self.nextChar=next(self.stream)
            if self.nextChar.isnumeric() or not (self.nextChar.isalpha() or self.nextChar=='_'):
                self.funcError=True
            while self.nextChar.isalnum() or self.nextChar=='_':
                self.valor+=self.nextChar
                self.nextChar=next(self.stream)
        except StopIteration:
            if len(self.valor)==1:
                self.funcError=True
        
    def symState(self):
        
        if self.nextChar in self.simbolosUnicos:
            self.token= "tk_"+self.simbolosUnicos.get(self.nextChar)
            self.valor= self.token
            self.nextChar=next(self.stream)
            self.lenSym=1
        else:
            try:
                if self.nextChar in self.lexemasSimples or self.nextChar in self.lexemasSimplesInvalidos:
                    self.valor=self.nextChar
                    self.nextChar=next(self.stream)
                    if self.valor+self.nextChar in self.lexemas_compuestos:
                        self.token= "tk_"+self.lexemas_compuestos.get(self.valor+self.nextChar)
                        self.valor= self.token
                        self.nextChar=next(self.stream)
                        self.lenSym=2
                    else:
                        if self.valor in self.lexemasSimples:
                            self.token= "tk_"+self.lexemasSimples.get(self.valor)
                            self.valor= self.token
                            self.lenSym=1
                        else:
                            self.funcError=True
            except StopIteration:
                if self.valor in self.lexemasSimples:
                    self.token= "tk_"+self.lexemasSimples.get(self.valor)
                    self.valor= self.token
                    self.lenSym=1
                else:
                    self.funcError=True


    def nextToken(self):
        res=""
        try:
            if self.nextChar in self.lexemasSimples or self.nextChar in self.simbolosUnicos or self.nextChar in self.lexemasSimplesInvalidos:
                self.symState()
                if self.funcError: return self.printError()
                res=self.printToken()
                self.column+=self.lenSym
            else:
                if self.nextChar == '@':
                    self.functionState()
                    if self.funcError: return self.printError()
                else:
                    if self.nextChar.isnumeric():
                        self.numState()
                    else:
                        if self.nextChar.isalpha() or self.nextChar=='_':
                            self.stringState()
                        else:
                            return self.printError()
                res=self.printToken()
                self.column+=len(self.valor)
            self.testNoPrintable()
        except StopIteration:
            res=self.printToken()
            self.finalizado=True
        self.valor=""
        return res

