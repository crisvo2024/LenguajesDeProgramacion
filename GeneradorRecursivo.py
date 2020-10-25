import os

primeros = dict()
reglas = dict()
siguientes = dict()
pilaSiguientes=list()
prediccion=dict()
dictTokens={
	"tk_llave_izq":'{',
	"tk_llave_der":'}',
	"tk_par_izq":'(',
	"tk_par_der":')',
	"tk_puntoycoma":';',
	"tk_coma":',',
	"tk_mayor":'>',
	"tk_menor":'<',
	"tk_mas":'+',
	"tk_menos": '-',
	"tk_mul": '*',
	"tk_div": '/',
	"tk_mod": '%',
	"tk_dospuntos": ':',
	"tk_asignacion":':=',
	"tk_mayor_igual":'>=',
	"tk_menor_igual": '<=',
	"tk_sum_asig": '+=',
	"tk_res_asig": '-=',
	"tk_mul_asig": '*=',
	"tk_div_asig": '/=',
	"tk_mod_asig": '%=',
	"tk_igualdad": '==',
	"tk_diferente": '!=',
	"tk_incremento": '++',
	"tk_decremento": '--',
	"fid": 'identificador de funcion',
	"id": 'identificador',
	"tk_num":'numero',
	
}

def primerosF(alpha):
	if not alpha in reglas:
		return [alpha]
	primerosAlpha=list()
	for regla in reglas[alpha]:
		primerosAn=primerosF(regla[0])
		for i in range(len(regla)):
			if not "lambda" in primerosAn:
				primerosAlpha+=primerosAn
				break
			listaSinLambda=primerosAn.copy()
			listaSinLambda.remove("lambda")
			primerosAlpha+=listaSinLambda
			if i == len(regla)-1:
				primerosAlpha.append("lambda")
			else:
				primerosAn=primerosF(regla[i+1])
	return list(dict.fromkeys(primerosAlpha))

def siguientesF(alpha):
	if alpha=="prog":
		return list(["$"])
	pilaSiguientes.append(alpha)
	siguientesAlpha=list()
	for noTerminal in reglas:	
		for regla in reglas[noTerminal]:
			if alpha==noTerminal:continue
			if alpha in regla:
				i=1
				primerosBeta=list(["lambda"])
				while "lambda" in primerosBeta and regla.index(alpha)+i<len(regla):
					primerosBeta.remove("lambda")
					siguientesAlpha+=primerosBeta
					if regla[regla.index(alpha)+i] in primeros:
						primerosBeta=primeros[regla[regla.index(alpha)+i]].copy()
					else:
						primerosBeta=list([regla[regla.index(alpha)+i]])
					i+=1
				if "lambda" in primerosBeta and regla.index(alpha)+i != len(regla):
					primerosBeta.remove("lambda")
				if regla.index(alpha)+i == len(regla) and "lambda" in primerosBeta:
					if not noTerminal in pilaSiguientes:
						siguientesAlpha+=siguientesF(noTerminal)
					primerosBeta.remove("lambda")
				siguientesAlpha+=primerosBeta
	pilaSiguientes.pop()
	return list(dict.fromkeys(siguientesAlpha))

def prediccionF(A):
	prediccionA=list() 
	i=0
	for regla in reglas[A]:
		prediccionA.append(list())
		lista = regla.copy()
		while len(lista)>0:
			primerS = lista[0]
			if not primerS in reglas: 
				if "lambda" != primerS:
					prediccionA[i].append(primerS)
				else: 
					prediccionA[i]+=siguientes[A]
				break
			elif "lambda" in primeros[primerS]:
				listasinLambda = primeros[primerS].copy()
				listasinLambda.remove("lambda")
				prediccionA[i]+=listasinLambda
				lista.remove(primerS)
			else:
				prediccionA[i]+=primeros[primerS]
				break
		else:
			prediccionA[i]+=siguientes[A]
		prediccionCopy=prediccionA[i].copy()
		for token in prediccionA[i]:
			if '||' in token:
				old = token
				prediccionCopy.remove(token)
				prediccionCopy+=old[1:-1].split("||")
		prediccionA[i]=prediccionCopy
		i+=1	
	return prediccionA		
			
		

if __name__ == "__main__":
	dirname = os.path.dirname(__file__)
	gramatica = open(dirname+"/Gramatica.txt")	
	for line in gramatica:
		tokens = line.split()
		if(not tokens[0] in primeros):
			primeros[tokens[0]] = list()
			siguientes[tokens[0]] = list()
			prediccion[tokens[0]] = list()
			reglas[tokens[0]] = list()
			reglas[tokens[0]].append(tokens[2:])
		else:
			reglas[tokens[0]].append(tokens[2:])
	for noTerminal in reglas:
		primeros[noTerminal]=primerosF(noTerminal)
	for noTerminal in reglas:
		siguientes[noTerminal]=siguientesF(noTerminal)
	for noTerminal in reglas:
		prediccion[noTerminal]=prediccionF(noTerminal)
	
	analizador = open(dirname+"/AnalizadorSintactico.py","wt")
	analizador.write("from AnalizadorLexico import AnalizadorLexico\n")
	analizador.write("class AnalizadorSintactico:\n")
	analizador.write(f"	tokens={dictTokens}\n")
	analizador.write("	def __init__(self):\n")
	analizador.write("		self.Analex = AnalizadorLexico()\n")

	for noTerminal in reglas:
		analizador.write(f"	def {noTerminal}(self): \n")
		i=0
		for regla in reglas[noTerminal]:
			analizador.write(f"		if self.tokenList[0] in {prediccion[noTerminal][i]}: \n")
			for token in regla:
				if token in primeros:
					analizador.write(f"			self.{token}()  \n")
				elif token != 'lambda':
					analizador.write(f"			self.emparejar('{token}')  \n")
				else:
					analizador.write(f"			pass  \n")
			i+=1
			analizador.write(f"			return\n")
		analizador.write(f"		else: \n")
		printPrediction=list()
		for  lista in prediccion[noTerminal]:
			printPrediction.extend(lista)
		analizador.write(f"			self.prediccion = {printPrediction}\n")
		analizador.write("			raise Exception('')\n")
	
	analizador.write("	def analizar(self):\n")
	analizador.write("		token=self.Analex.nextToken()\n")
	analizador.write("		self.tokenList=token[1:-1].split(',')\n")
	analizador.write("		try:\n")
	analizador.write("			self.prog()\n")
	analizador.write("		except RuntimeError:\n")
	analizador.write("			print('<'+str(self.Analex.line)+':'+str(self.Analex.column)+'> Error sintactico: se encontro final de archivo; se esperaba '+chr(39)+'end'+chr(39)+'.')\n")
	analizador.write('			return\n')
	analizador.write('		except:\n')	
	analizador.write("			for simbolo in self.prediccion:\n")
	analizador.write("				if simbolo in self.tokens:\n")
	analizador.write("					self.prediccion[self.prediccion.index(simbolo)]=self.tokens[simbolo]\n")
	analizador.write("			if '(bool||num)' in self.prediccion :\n")
	analizador.write('				self.prediccion.remove("(bool||num)")\n')
	analizador.write("				self.prediccion.append('bool')\n")
	analizador.write("				self.prediccion.append('num')\n")
	analizador.write("			self.prediccion.sort()\n")
	analizador.write("			if 'identificador' in self.prediccion and 'identificador de funcion' in self.prediccion:  \n")
	analizador.write("				index = self.prediccion.index('identificador')\n")
	analizador.write("				self.prediccion[index]='identificador de funcion'\n")
	analizador.write("				self.prediccion[index+1]='identificador'\n")
	analizador.write("			if self.tokenList[-3] in self.tokens:\n")
	analizador.write("				print('<'+self.tokenList[-2]+':'+self.tokenList[-1]+'> Error sintactico: ' + 'se encontro: '+chr(39)+self.tokens[self.tokenList[-3]]+chr(39)+'; se esperaba: '+str(self.prediccion)[1:-1]+'.')\n")
	analizador.write("			else:\n")
	analizador.write("				print('<'+self.tokenList[-2]+':'+self.tokenList[-1]+'> Error sintactico: ' + 'se encontro: '+chr(39)+self.tokenList[-3]+chr(39)+'; se esperaba: '+str(self.prediccion)[1:-1]+'.')\n")
	analizador.write('			return\n')
	analizador.write("		print('El analisis sintactico ha finalizado correctamente.')\n")
	
	analizador.write("	def emparejar(self,tk_esperado):\n")
	analizador.write("		if self.tokenList[0] in tk_esperado:\n")
	analizador.write("			if self.tokenList[0] !='end':\n")	
	analizador.write("				token=self.Analex.nextToken()\n")
	analizador.write("				self.tokenList=token[1:-1].split(',')\n")

	analizador.write("		else:\n")
	analizador.write("			self.prediccion=[tk_esperado]\n")
	analizador.write("			raise Exception('')\n")

	

	
	analizador.close()
	gramatica.close()

	
	