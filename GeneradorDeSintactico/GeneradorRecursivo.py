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
	return list(dict.fromkeys(primerosAlpha))

def siguientesF(alpha):
	if alpha=="prog":
		return list(["$"])
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
					primerosBeta=primerosF(regla[regla.index(alpha)+i])
					i+=1
				if regla.index(alpha)+i == len(regla) and "lambda" in primerosBeta:
					siguientesAlpha+=siguientesF(noTerminal)
	return list(dict.fromkeys(siguientesAlpha))
						
			
		

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
		primeros[noTerminal]=primerosF(noTerminal)
		#print(noTerminal)
		#print(primeros[noTerminal])
	print(siguientesF("stmt"))