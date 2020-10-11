if __name__ == "__main__":
	gramatica = open("Gramatica.txt")
	analizador = open("AnalizadorSintactico.py","wt")
	analizador.write("from AnalizadorLexico import AnalizadorLexico \n")
	primeros = dict()
	reglas = dict()
	siguientes = dict()
	for line in gramatica:
		tokens = line.split()
		if(not tokens[0] in primeros):
			primeros[tokens[0]] = list()
			siguientes[tokens[0]] = list()
			primeros[tokens[0]].append(tokens[2])
			reglas[tokens[0]] = list()
			reglas[tokens[0]].append(tokens[2:])
		else:
			if not tokens[2] in primeros[tokens[0]]:
				primeros[tokens[0]].append(tokens[2])
			reglas[tokens[0]].append(tokens[2:])
	Terminal=False
	for noTerminal in reglas:
		for regla in reglas[noTerminal]:
			for i in range(len(regla)):
				if not regla[i] in reglas:
					if not regla[i] in primeros[noTerminal]:
						primeros[noTerminal].append(regla[i])
					break
				if not "lambda" in primeros[regla[i]]:
					primeros[noTerminal].remove(regla[i])
					primeros[noTerminal]+=primeros[regla[i]]
					break
				else:
					primerosSinLambda=primeros[regla[i]]
					primerosSinLambda.remove("lambda")
					primeros[noTerminal].remove(regla[i])
					primeros[noTerminal]+=primerosSinLambda
				if i == len(regla):
					primeros[noTerminal].append("lambda")
	while not Terminal:
		Terminal = True
		#token cada elemento de la lista primeros
		for token in primeros:
			#opcion cada opcion de primero que tiene el token
			for opcion in primeros[token]:
				#si opcion es no terminal
				if opcion in primeros:
					Terminal = False
					primeros[token].remove(opcion)
					# primero es cada primero de la opcion de token
					for primero in primeros[opcion]:
						if not primero in primeros[token]:
							primeros[token].append(primero)
	#print(reglas)
	#print(primeros)
	gramatica.close()
	analizador.close()