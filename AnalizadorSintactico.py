from AnalizadorLexico import AnalizadorLexico
class AnalizadorSintactico:
	tokens={'tk_llave_izq': '{', 'tk_llave_der': '}', 'tk_par_izq': '(', 'tk_par_der': ')', 'tk_puntoycoma': ';', 'tk_coma': ',', 'tk_mayor': '>', 'tk_menor': '<', 'tk_mas': '+', 'tk_menos': '-', 'tk_mul': '*', 'tk_div': '/', 'tk_mod': '%', 'tk_dospuntos': ':', 'tk_asignacion': ':=', 'tk_mayor_igual': '>=', 'tk_menor_igual': '<=', 'tk_sum_asig': '+=', 'tk_res_asig': '-=', 'tk_mul_asig': '*=', 'tk_div_asig': '/=', 'tk_mod_asig': '%=', 'tk_igualdad': '==', 'tk_diferente': '!=', 'tk_incremento': '++', 'tk_decremento': '--', 'fid': 'identificador de funcion', 'id': 'identificador', 'tk_num': 'numero'}
	def __init__(self):
		self.Analex = AnalizadorLexico()
	def prog(self): 
		if self.tokenList[0] in ['function', 'var', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			self.fn_decl_list()  
			self.main_prog()  
			return
		else: 
			self.prediccion = ['function', 'var', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']
			raise Exception('')
	def fn_decl_list(self): 
		if self.tokenList[0] in ['function']: 
			self.f()  
			self.fn_decl_list()  
			return
		if self.tokenList[0] in ['var', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			pass  
			return
		else: 
			self.prediccion = ['function', 'var', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']
			raise Exception('')
	def f(self): 
		if self.tokenList[0] in ['function']: 
			self.emparejar('function')  
			self.emparejar('fid')  
			self.emparejar('tk_dospuntos')  
			self.emparejar('(bool||num)')  
			self.emparejar('tk_par_izq')  
			self.var_dec()  
			self.emparejar('tk_par_der')  
			self.stmt_var_list()  
			self.stmt_block()  
			return
		else: 
			self.prediccion = ['function']
			raise Exception('')
	def main_prog(self): 
		if self.tokenList[0] in ['var', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			self.stmt_var_list()  
			self.stmt_mp()  
			self.emparejar('end')  
			return
		else: 
			self.prediccion = ['var', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']
			raise Exception('')
	def stmt_var_list(self): 
		if self.tokenList[0] in ['var']: 
			self.emparejar('var')  
			self.var_dec()  
			self.emparejar('tk_puntoycoma')  
			return
		if self.tokenList[0] in ['tk_llave_izq', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			pass  
			return
		else: 
			self.prediccion = ['var', 'tk_llave_izq', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']
			raise Exception('')
	def var_dec(self): 
		if self.tokenList[0] in ['id']: 
			self.emparejar('id')  
			self.emparejar('tk_dospuntos')  
			self.emparejar('(bool||num)')  
			self.add_var()  
			return
		else: 
			self.prediccion = ['id']
			raise Exception('')
	def add_var(self): 
		if self.tokenList[0] in ['tk_coma']: 
			self.emparejar('tk_coma')  
			self.emparejar('id')  
			self.emparejar('tk_dospuntos')  
			self.emparejar('(bool||num)')  
			self.add_var()  
			return
		if self.tokenList[0] in ['tk_par_der', 'tk_puntoycoma']: 
			pass  
			return
		else: 
			self.prediccion = ['tk_coma', 'tk_par_der', 'tk_puntoycoma']
			raise Exception('')
	def stmt_block(self): 
		if self.tokenList[0] in ['tk_llave_izq']: 
			self.emparejar('tk_llave_izq')  
			self.stmt()  
			self.stmt_p()  
			self.emparejar('tk_llave_der')  
			return
		if self.tokenList[0] in ['print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			self.stmt()  
			return
		else: 
			self.prediccion = ['tk_llave_izq', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']
			raise Exception('')
	def stmt_mp(self): 
		if self.tokenList[0] in ['print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			self.stmt()  
			self.stmt_mp()  
			return
		if self.tokenList[0] in ['end']: 
			pass  
			return
		else: 
			self.prediccion = ['print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento', 'end']
			raise Exception('')
	def stmt_p(self): 
		if self.tokenList[0] in ['print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			self.stmt()  
			self.stmt_p()  
			return
		if self.tokenList[0] in ['tk_llave_der']: 
			pass  
			return
		else: 
			self.prediccion = ['print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento', 'tk_llave_der']
			raise Exception('')
	def stmt(self): 
		if self.tokenList[0] in ['print']: 
			self.emparejar('print')  
			self.lexpr()  
			self.emparejar('tk_puntoycoma')  
			return
		if self.tokenList[0] in ['input']: 
			self.emparejar('input')  
			self.emparejar('id')  
			self.emparejar('tk_puntoycoma')  
			return
		if self.tokenList[0] in ['when']: 
			self.emparejar('when')  
			self.par_lexpr()  
			self.do_block()  
			return
		if self.tokenList[0] in ['if']: 
			self.emparejar('if')  
			self.par_lexpr()  
			self.do_block()  
			self.emparejar('else')  
			self.stmt_block()  
			return
		if self.tokenList[0] in ['unless', 'while', 'until']: 
			self.emparejar('(unless||while||until)')  
			self.par_lexpr()  
			self.do_block()  
			return
		if self.tokenList[0] in ['do']: 
			self.do_block()  
			self.emparejar('(while||until)')  
			self.par_lexpr()  
			return
		if self.tokenList[0] in ['return']: 
			self.emparejar('return')  
			self.lexpr()  
			self.emparejar('tk_puntoycoma')  
			return
		if self.tokenList[0] in ['loop']: 
			self.emparejar('loop')  
			self.stmt_block()  
			return
		if self.tokenList[0] in ['repeat']: 
			self.emparejar('repeat')  
			self.emparejar('tk_num')  
			self.emparejar('tk_dospuntos')  
			self.stmt_block()  
			return
		if self.tokenList[0] in ['for']: 
			self.emparejar('for')  
			self.emparejar('tk_par_izq')  
			self.lexpr()  
			self.emparejar('tk_puntoycoma')  
			self.lexpr()  
			self.emparejar('tk_puntoycoma')  
			self.forexpr()  
			self.emparejar('tk_par_der')  
			self.do_block()  
			return
		if self.tokenList[0] in ['next']: 
			self.emparejar('next')  
			self.emparejar('tk_puntoycoma')  
			return
		if self.tokenList[0] in ['break']: 
			self.emparejar('break')  
			self.emparejar('tk_puntoycoma')  
			return
		if self.tokenList[0] in ['id']: 
			self.emparejar('id')  
			self.operation()  
			return
		if self.tokenList[0] in ['tk_decremento', 'tk_incremento']: 
			self.emparejar('(tk_decremento||tk_incremento)')  
			self.emparejar('id')  
			self.emparejar('tk_puntoycoma')  
			return
		else: 
			self.prediccion = ['print', 'input', 'when', 'if', 'unless', 'while', 'until', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'tk_decremento', 'tk_incremento']
			raise Exception('')
	def do_block(self): 
		if self.tokenList[0] in ['do']: 
			self.emparejar('do')  
			self.stmt_block()  
			return
		else: 
			self.prediccion = ['do']
			raise Exception('')
	def par_lexpr(self): 
		if self.tokenList[0] in ['tk_par_izq']: 
			self.emparejar('tk_par_izq')  
			self.forexpr()  
			self.emparejar('tk_par_der')  
			return
		else: 
			self.prediccion = ['tk_par_izq']
			raise Exception('')
	def operation(self): 
		if self.tokenList[0] in ['tk_asignacion', 'tk_sum_asig', 'tk_res_asig', 'tk_mul_asig', 'tk_div_asig', 'tk_mod_asig']: 
			self.emparejar('(tk_asignacion||tk_sum_asig||tk_res_asig||tk_mul_asig||tk_div_asig||tk_mod_asig)')  
			self.lexpr()  
			self.emparejar('tk_puntoycoma')  
			return
		if self.tokenList[0] in ['tk_incremento', 'tk_decremento']: 
			self.emparejar('(tk_incremento||tk_decremento)')  
			self.emparejar('tk_puntoycoma')  
			return
		else: 
			self.prediccion = ['tk_asignacion', 'tk_sum_asig', 'tk_res_asig', 'tk_mul_asig', 'tk_div_asig', 'tk_mod_asig', 'tk_incremento', 'tk_decremento']
			raise Exception('')
	def lexpr(self): 
		if self.tokenList[0] in ['not', 'id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.expr()  
			self.nexpr()  
			return
		else: 
			self.prediccion = ['not', 'id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']
			raise Exception('')
	def expr(self): 
		if self.tokenList[0] in ['not']: 
			self.emparejar('not')  
			self.par_lexpr()  
			return
		if self.tokenList[0] in ['id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.rexpr()  
			return
		else: 
			self.prediccion = ['not', 'id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']
			raise Exception('')
	def nexpr(self): 
		if self.tokenList[0] in ['and', 'or']: 
			self.emparejar('(and||or)')  
			self.lexpr()  
			return
		if self.tokenList[0] in ['tk_puntoycoma']: 
			pass  
			return
		else: 
			self.prediccion = ['and', 'or', 'tk_puntoycoma']
			raise Exception('')
	def rexpr(self): 
		if self.tokenList[0] in ['id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.simple_expr()  
			self.comp_expr()  
			return
		else: 
			self.prediccion = ['id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']
			raise Exception('')
	def comp_expr(self): 
		if self.tokenList[0] in ['tk_mayor_igual', 'tk_menor_igual', 'tk_mayor', 'tk_menor', 'tk_igualdad', 'tk_diferente']: 
			self.emparejar('(tk_mayor_igual||tk_menor_igual||tk_mayor||tk_menor||tk_igualdad||tk_diferente)')  
			self.simple_expr()  
			return
		if self.tokenList[0] in ['tk_puntoycoma', 'tk_coma', 'tk_par_der', 'and', 'or']: 
			pass  
			return
		else: 
			self.prediccion = ['tk_mayor_igual', 'tk_menor_igual', 'tk_mayor', 'tk_menor', 'tk_igualdad', 'tk_diferente', 'tk_puntoycoma', 'tk_coma', 'tk_par_der', 'and', 'or']
			raise Exception('')
	def simple_expr(self): 
		if self.tokenList[0] in ['id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.term()  
			self.sum_expr()  
			return
		else: 
			self.prediccion = ['id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']
			raise Exception('')
	def sum_expr(self): 
		if self.tokenList[0] in ['tk_mas', 'tk_menos']: 
			self.emparejar('(tk_mas||tk_menos)')  
			self.simple_expr()  
			return
		if self.tokenList[0] in ['tk_puntoycoma', 'tk_coma', 'tk_par_der', 'and', 'or', 'tk_mayor_igual', 'tk_menor_igual', 'tk_mayor', 'tk_menor', 'tk_igualdad', 'tk_diferente']: 
			pass  
			return
		else: 
			self.prediccion = ['tk_mas', 'tk_menos', 'tk_puntoycoma', 'tk_coma', 'tk_par_der', 'and', 'or', 'tk_mayor_igual', 'tk_menor_igual', 'tk_mayor', 'tk_menor', 'tk_igualdad', 'tk_diferente']
			raise Exception('')
	def term(self): 
		if self.tokenList[0] in ['id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.factor()  
			self.mul_expr()  
			return
		else: 
			self.prediccion = ['id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']
			raise Exception('')
	def mul_expr(self): 
		if self.tokenList[0] in ['tk_mul', 'tk_div', 'tk_mod']: 
			self.emparejar('(tk_mul||tk_div||tk_mod)')  
			self.term()  
			return
		if self.tokenList[0] in ['tk_puntoycoma', 'tk_coma', 'tk_par_der', 'and', 'or', 'tk_mayor_igual', 'tk_menor_igual', 'tk_mayor', 'tk_menor', 'tk_igualdad', 'tk_diferente', 'tk_mas', 'tk_menos']: 
			pass  
			return
		else: 
			self.prediccion = ['tk_mul', 'tk_div', 'tk_mod', 'tk_puntoycoma', 'tk_coma', 'tk_par_der', 'and', 'or', 'tk_mayor_igual', 'tk_menor_igual', 'tk_mayor', 'tk_menor', 'tk_igualdad', 'tk_diferente', 'tk_mas', 'tk_menos']
			raise Exception('')
	def factor(self): 
		if self.tokenList[0] in ['tk_num', 'true', 'false']: 
			self.emparejar('(tk_num||true||false)')  
			return
		if self.tokenList[0] in ['id']: 
			self.emparejar('id')  
			self.incre()  
			return
		if self.tokenList[0] in ['tk_incremento', 'tk_decremento']: 
			self.emparejar('(tk_incremento||tk_decremento)')  
			self.emparejar('id')  
			return
		if self.tokenList[0] in ['tk_par_izq']: 
			self.par_lexpr()  
			return
		if self.tokenList[0] in ['fid']: 
			self.emparejar('fid')  
			self.emparejar('tk_par_izq')  
			self.fexpr()  
			self.coma_fexper()  
			self.emparejar('tk_par_der')  
			return
		else: 
			self.prediccion = ['tk_num', 'true', 'false', 'id', 'tk_incremento', 'tk_decremento', 'tk_par_izq', 'fid']
			raise Exception('')
	def incre(self): 
		if self.tokenList[0] in ['tk_incremento', 'tk_decremento']: 
			self.emparejar('(tk_incremento||tk_decremento)')  
			return
		if self.tokenList[0] in ['tk_puntoycoma', 'tk_coma', 'tk_par_der', 'and', 'or', 'tk_mayor_igual', 'tk_menor_igual', 'tk_mayor', 'tk_menor', 'tk_igualdad', 'tk_diferente', 'tk_mas', 'tk_menos', 'tk_mul', 'tk_div', 'tk_mod']: 
			pass  
			return
		else: 
			self.prediccion = ['tk_incremento', 'tk_decremento', 'tk_puntoycoma', 'tk_coma', 'tk_par_der', 'and', 'or', 'tk_mayor_igual', 'tk_menor_igual', 'tk_mayor', 'tk_menor', 'tk_igualdad', 'tk_diferente', 'tk_mas', 'tk_menos', 'tk_mul', 'tk_div', 'tk_mod']
			raise Exception('')
	def coma_fexper(self): 
		if self.tokenList[0] in ['tk_coma']: 
			self.emparejar('tk_coma')  
			self.fexpr()  
			self.coma_fexper()  
			return
		if self.tokenList[0] in ['tk_par_der']: 
			pass  
			return
		else: 
			self.prediccion = ['tk_coma', 'tk_par_der']
			raise Exception('')
	def fexpr(self): 
		if self.tokenList[0] in ['not', 'id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.expr()  
			self.fnexpr()  
			return
		else: 
			self.prediccion = ['not', 'id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']
			raise Exception('')
	def fnexpr(self): 
		if self.tokenList[0] in ['and', 'or']: 
			self.emparejar('(and||or)')  
			self.fexpr()  
			return
		if self.tokenList[0] in ['tk_coma', 'tk_par_der']: 
			pass  
			return
		else: 
			self.prediccion = ['and', 'or', 'tk_coma', 'tk_par_der']
			raise Exception('')
	def forexpr(self): 
		if self.tokenList[0] in ['not', 'id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.expr()  
			self.fornexpr()  
			return
		else: 
			self.prediccion = ['not', 'id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']
			raise Exception('')
	def fornexpr(self): 
		if self.tokenList[0] in ['and', 'or']: 
			self.emparejar('(and||or)')  
			self.forexpr()  
			return
		if self.tokenList[0] in ['tk_par_der']: 
			pass  
			return
		else: 
			self.prediccion = ['and', 'or', 'tk_par_der']
			raise Exception('')
	def analizar(self):
		token=self.Analex.nextToken()
		self.tokenList=token[1:-1].split(',')
		try:
			self.prog()
		except RuntimeError:
			print('<'+str(self.Analex.line)+':'+str(self.Analex.column)+'> Error sintactico: se encontro final de archivo; se esperaba '+chr(39)+'end'+chr(39)+'.')
			return
		except:
			for simbolo in self.prediccion:
				if simbolo in self.tokens:
					self.prediccion[self.prediccion.index(simbolo)]=self.tokens[simbolo]
			if '(bool||num)' in self.prediccion :
				self.prediccion.remove("(bool||num)")
				self.prediccion.append('bool')
				self.prediccion.append('num')
			self.prediccion.sort()
			if 'identificador' in self.prediccion and 'identificador de funcion' in self.prediccion:  
				index = self.prediccion.index('identificador')
				self.prediccion[index]='identificador de funcion'
				self.prediccion[index+1]='identificador'
			if self.tokenList[-3] in self.tokens:
				print('<'+self.tokenList[-2]+':'+self.tokenList[-1]+'> Error sintactico: ' + 'se encontro: '+chr(39)+self.tokens[self.tokenList[-3]]+chr(39)+'; se esperaba: '+str(self.prediccion)[1:-1]+'.')
			else:
				print('<'+self.tokenList[-2]+':'+self.tokenList[-1]+'> Error sintactico: ' + 'se encontro: '+chr(39)+self.tokenList[-3]+chr(39)+'; se esperaba: '+str(self.prediccion)[1:-1]+'.')
			return
		print('El analisis sintactico ha finalizado correctamente.')
	def emparejar(self,tk_esperado):
		if self.tokenList[0] in tk_esperado:
			if self.tokenList[0] !='end':
				token=self.Analex.nextToken()
				self.tokenList=token[1:-1].split(',')
		else:
			self.prediccion=[tk_esperado]
			raise Exception('')
