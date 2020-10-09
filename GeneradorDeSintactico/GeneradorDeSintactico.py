if __name__ == "__main__":
	gramatica = open("Gramatica.txt")
	analizador = open("AnalizadorSintactico.py","wt")
	analizador.write("from AnalizadorLexico import AnalizadorLexico \n")
	primeros = dict()
	siguientes = dict()
	for line in gramatica:
		tokens = line.split()
		#print(tokens)
		if(not tokens[0] in primeros):
			primeros[tokens[0]]= list()
			siguientes[tokens[0]]= list()
			primeros[tokens[0]].append(tokens[3])
		# else:
		# 	primeros[tokens[0]].append(tokens[3])
	Terminal=False
	while not Terminal:
		Terminal = True
		for token in primeros:
			for opcion in primeros[token]:
				if opcion in primeros:
					Terminal = False
					primeros[token].remove(opcion)
					for primero in primeros[opcion]:
						if not primero in primeros[token]:
							primeros[token].append(primero)
	print(primeros)
	gramatica.close()
	analizador.close()