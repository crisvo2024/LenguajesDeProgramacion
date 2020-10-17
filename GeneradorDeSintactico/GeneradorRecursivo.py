import os

primeros = dict()
reglas = dict()
siguientes = dict()
pilaSiguientes=list()
prediccion=dict()

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
		for token in prediccionA[i]:
			if '||' in token:
				old = token
				prediccionA[i].remove(token)
				prediccionA[i]+=old[1:-1].split("||")
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
	#analizador.write(f"	prediccion={prediccion}\n")
	analizador.write("	def __init__(self):\n")
	analizador.write("		self.Analex = AnalizadorLexico()\n")

	for noTerminal in reglas:
		analizador.write(f"	def {noTerminal}(self): \n")
		i=0
		for regla in reglas[noTerminal]:
			analizador.write(f"		if self.tokenList[-3] in {prediccion[noTerminal][i]}: \n")
			for token in regla:
				if token in primeros:
					analizador.write(f"			self.{token}()  \n")
				else:
					analizador.write(f"			self.emparejar('{token}')  \n")
			i+=1
	
	analizador.write("	def analizar(self):\n")
	analizador.write("		token=self.Analex.nextToken()\n")
	analizador.write("		self.tokenList=token[1:-1].split(',')\n")
	analizador.write("		try:\n")
	analizador.write("			self.prog()\n")
	analizador.write("		except RuntimeError:\n")
	analizador.write('			print("Error sintactico: se encontro final de archivo; se esperaba ‘end’")\n')
	analizador.write('		except:\n')	
	analizador.write("			print('<'+self.tokenList[-2]+':'+self.tokenList[-1]+'>Error sintactico:' + 'se encontro: '+self.tokenList[-3]+'; se esperaba: '+self.prediccion)\n")

	
	analizador.write("	def emparejar(self,tk_esperado):\n")
	analizador.write("		if self.tokenList[-3] in tk_esperado:\n")	
	analizador.write("			token=self.Analex.nextToken()\n")
	analizador.write("			self.tokenList=token[1:-1].split(',')\n")

	analizador.write("		else:\n")
	analizador.write("			self.prediccion=[tk_esperado]\n")
	analizador.write("			raise Exception('')\n")

	

	
	analizador.close()
	gramatica.close()

	
	