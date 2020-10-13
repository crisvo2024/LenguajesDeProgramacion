import os

primeros = dict()
reglas = dict()
siguientes = dict()

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
			listaSinLambda=primerosAn
			listaSinLambda.remove("lambda")
			primerosAlpha+=listaSinLambda
			if i == len(regla)-1:
				primerosAlpha.append("lambda")
			else:
				primerosAn=primerosF(regla[i+1])
	return primerosAlpha
			
		

if __name__ == "__main__":
	dirname = os.path.dirname(__file__)
	gramatica = open(dirname+"/Gramatica.txt")
	analizador = open("AnalizadorSintactico.py","wt")
	analizador.write("from AnalizadorLexico import AnalizadorLexico \n")
	for line in gramatica:
		tokens = line.split()
		if(not tokens[0] in primeros):
			primeros[tokens[0]] = list()
			siguientes[tokens[0]] = list()
			reglas[tokens[0]] = list()
			reglas[tokens[0]].append(tokens[2:])
		else:
			reglas[tokens[0]].append(tokens[2:])
	for noTerminal in reglas:
		primeros[noTerminal]=list(dict.fromkeys(primerosF(noTerminal))) 
		print(noTerminal)
		print(primeros[noTerminal])