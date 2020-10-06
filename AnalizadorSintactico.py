from AnalizadorLexico import AnalizadorLexico
class AnalizadorSintactico:
	def __init__(self):
		self.Analex = AnalizadorLexico()
    
	def ListarTokens(self):
		while not self.Analex.finalizado:
			print(self.Analex.nextToken())


    