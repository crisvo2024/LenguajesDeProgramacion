from AnalizadorLexico import AnalizadorLexico
class AnalizadorSintactico:
	def __init__(self):
		self.Analex = AnalizadorLexico()
	def prog(self): 
		if self.tokenList[-3] in ['function', 'var', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			self.fn_decl_list()  
			self.main_prog()  
	def fn_decl_list(self): 
		if self.tokenList[-3] in ['function']: 
			self.f()  
			self.fn_decl_list()  
		if self.tokenList[-3] in ['var', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			self.emparejar('lambda')  
	def f(self): 
		if self.tokenList[-3] in ['function']: 
			self.emparejar('function')  
			self.emparejar('fid')  
			self.emparejar('tk_dospuntos')  
			self.emparejar('(bool||num)')  
			self.emparejar('tk_par_izq')  
			self.var_dec()  
			self.emparejar('tk_par_der')  
			self.stmt_var_list()  
			self.stmt_block()  
	def main_prog(self): 
		if self.tokenList[-3] in ['var', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			self.stmt_var_list()  
			self.stmt_p()  
			self.emparejar('end')  
	def stmt_var_list(self): 
		if self.tokenList[-3] in ['var']: 
			self.emparejar('var')  
			self.var_dec()  
			self.emparejar('tk_puntoycoma')  
		if self.tokenList[-3] in ['tk_llave_izq', 'print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'end', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			self.emparejar('lambda')  
	def var_dec(self): 
		if self.tokenList[-3] in ['id']: 
			self.emparejar('id')  
			self.emparejar('tk_dospuntos')  
			self.emparejar('(bool||num)')  
			self.add_var()  
	def add_var(self): 
		if self.tokenList[-3] in ['tk_coma']: 
			self.emparejar('tk_coma')  
			self.emparejar('id')  
			self.emparejar('tk_dospuntos')  
			self.emparejar('(bool||num)')  
			self.add_var()  
		if self.tokenList[-3] in ['tk_par_der', 'tk_puntoycoma']: 
			self.emparejar('lambda')  
	def stmt_block(self): 
		if self.tokenList[-3] in ['tk_llave_izq']: 
			self.emparejar('tk_llave_izq')  
			self.stmt()  
			self.stmt_p()  
			self.emparejar('tk_llave_der')  
		if self.tokenList[-3] in ['print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			self.stmt()  
	def stmt_p(self): 
		if self.tokenList[-3] in ['print', 'input', 'when', 'if', 'do', 'return', 'loop', 'repeat', 'for', 'next', 'break', 'id', 'unless', 'while', 'until', 'tk_decremento', 'tk_incremento']: 
			self.stmt()  
			self.stmt_p()  
		if self.tokenList[-3] in ['end', 'tk_llave_der']: 
			self.emparejar('lambda')  
	def stmt(self): 
		if self.tokenList[-3] in ['print']: 
			self.emparejar('print')  
			self.lexpr()  
			self.emparejar('tk_puntoycoma')  
		if self.tokenList[-3] in ['input']: 
			self.emparejar('input')  
			self.emparejar('id')  
			self.emparejar('tk_puntoycoma')  
		if self.tokenList[-3] in ['when']: 
			self.emparejar('when')  
			self.par_lexpr()  
			self.do_block()  
		if self.tokenList[-3] in ['if']: 
			self.emparejar('if')  
			self.par_lexpr()  
			self.do_block()  
			self.emparejar('else')  
			self.stmt_block()  
		if self.tokenList[-3] in ['unless', 'while', 'until']: 
			self.emparejar('(unless||while||until)')  
			self.par_lexpr()  
			self.do_block()  
		if self.tokenList[-3] in ['do']: 
			self.do_block()  
			self.emparejar('(while||until)')  
			self.par_lexpr()  
		if self.tokenList[-3] in ['return']: 
			self.emparejar('return')  
			self.lexpr()  
			self.emparejar('tk_puntoycoma')  
		if self.tokenList[-3] in ['loop']: 
			self.emparejar('loop')  
			self.stmt_block()  
		if self.tokenList[-3] in ['repeat']: 
			self.emparejar('repeat')  
			self.emparejar('num')  
			self.emparejar('tk_dospuntos')  
			self.stmt_block()  
		if self.tokenList[-3] in ['for']: 
			self.emparejar('for')  
			self.emparejar('tk_par_izq')  
			self.lexpr()  
			self.emparejar('tk_puntoycoma')  
			self.lexpr()  
			self.emparejar('tk_puntoycoma')  
			self.lexpr()  
			self.emparejar('tk_par_der')  
			self.do_block()  
		if self.tokenList[-3] in ['next']: 
			self.emparejar('next')  
			self.emparejar('tk_puntoycoma')  
		if self.tokenList[-3] in ['break']: 
			self.emparejar('break')  
			self.emparejar('tk_puntoycoma')  
		if self.tokenList[-3] in ['id']: 
			self.emparejar('id')  
			self.operation()  
		if self.tokenList[-3] in ['tk_decremento', 'tk_incremento']: 
			self.emparejar('(tk_decremento||tk_incremento)')  
			self.emparejar('id')  
			self.emparejar('tk_puntoycoma')  
	def do_block(self): 
		if self.tokenList[-3] in ['do']: 
			self.emparejar('do')  
			self.stmt_block()  
	def par_lexpr(self): 
		if self.tokenList[-3] in ['tk_par_izq']: 
			self.emparejar('tk_par_izq')  
			self.lexpr()  
			self.emparejar('tk_par_der')  
	def operation(self): 
		if self.tokenList[-3] in ['tk_asignacion', 'tk_sum_asig', 'tk_res_asig', 'tk_mul_asig', 'tk_div_asig', 'tk_mod_asig']: 
			self.emparejar('(tk_asignacion||tk_sum_asig||tk_res_asig||tk_mul_asig||tk_div_asig||tk_mod_asig)')  
			self.lexpr()  
			self.emparejar('tk_puntoycoma')  
		if self.tokenList[-3] in ['tk_incremento', 'tk_decremento']: 
			self.emparejar('(tk_incremento||tk_decremento)')  
			self.emparejar('tk_puntoycoma')  
	def lexpr(self): 
		if self.tokenList[-3] in ['not', 'id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.expr()  
			self.nexpr()  
	def expr(self): 
		if self.tokenList[-3] in ['not']: 
			self.emparejar('not')  
			self.emparejar('tk_par_izq')  
			self.rexpr()  
			self.emparejar('tk_par_der')  
		if self.tokenList[-3] in ['id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.rexpr()  
	def nexpr(self): 
		if self.tokenList[-3] in ['and', 'or']: 
			self.emparejar('(and||or)')  
			self.lexpr()  
		if self.tokenList[-3] in ['tk_puntoycoma', 'tk_par_der', 'tk_coma', 'coma_lexpr']: 
			self.emparejar('lambda')  
	def rexpr(self): 
		if self.tokenList[-3] in ['id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.simple_expr()  
			self.comp_expr()  
	def comp_expr(self): 
		if self.tokenList[-3] in ['tk_mayor_igual', 'tk_menor_igual', 'tk_mayor', 'tk_menor', 'tk_igualdad', 'tk_diferente']: 
			self.emparejar('(tk_mayor_igual||tk_menor_igual||tk_mayor||tk_menor||tk_igualdad||tk_diferente)')  
			self.simple_expr()  
		if self.tokenList[-3] in ['tk_par_der', 'tk_puntoycoma', 'tk_coma', 'coma_lexpr', 'and', 'or']: 
			self.emparejar('lambda')  
	def simple_expr(self): 
		if self.tokenList[-3] in ['id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.term()  
			self.sum_expr()  
	def sum_expr(self): 
		if self.tokenList[-3] in ['tk_mas', 'tk_menos']: 
			self.emparejar('(tk_mas||tk_menos)')  
			self.simple_expr()  
		if self.tokenList[-3] in ['tk_par_der', 'tk_puntoycoma', 'tk_coma', 'coma_lexpr', '(tk_mayor_igual||tk_menor_igual||tk_mayor||tk_menor||tk_igualdad||tk_diferente)', 'and', 'or']: 
			self.emparejar('lambda')  
	def term(self): 
		if self.tokenList[-3] in ['id', 'tk_par_izq', 'fid', 'tk_num', 'true', 'false', 'tk_incremento', 'tk_decremento']: 
			self.factor()  
			self.mul_expr()  
	def mul_expr(self): 
		if self.tokenList[-3] in ['tk_mul', 'tk_div', 'tk_mod']: 
			self.emparejar('(tk_mul||tk_div||tk_mod)')  
			self.term()  
		if self.tokenList[-3] in ['tk_par_der', 'tk_puntoycoma', 'tk_coma', 'coma_lexpr', '(tk_mayor_igual||tk_menor_igual||tk_mayor||tk_menor||tk_igualdad||tk_diferente)', 'and', 'or', 'tk_mas', 'tk_menos']: 
			self.emparejar('lambda')  
	def factor(self): 
		if self.tokenList[-3] in ['tk_num', 'true', 'false']: 
			self.emparejar('(tk_num||true||false)')  
		if self.tokenList[-3] in ['id']: 
			self.emparejar('id')  
			self.incre()  
		if self.tokenList[-3] in ['tk_incremento', 'tk_decremento']: 
			self.emparejar('(tk_incremento||tk_decremento)')  
			self.emparejar('id')  
		if self.tokenList[-3] in ['tk_par_izq']: 
			self.par_lexpr()  
		if self.tokenList[-3] in ['fid']: 
			self.emparejar('fid')  
			self.emparejar('par_izq')  
			self.lexpr()  
			self.coma_lexper()  
			self.emparejar('tk_par_der')  
	def incre(self): 
		if self.tokenList[-3] in ['tk_incremento', 'tk_decremento']: 
			self.emparejar('(tk_incremento||tk_decremento)')  
		if self.tokenList[-3] in ['tk_par_der', 'tk_puntoycoma', 'tk_coma', 'coma_lexpr', '(tk_mayor_igual||tk_menor_igual||tk_mayor||tk_menor||tk_igualdad||tk_diferente)', '(tk_mul||tk_div||tk_mod)', 'and', 'or', 'tk_mas', 'tk_menos']: 
			self.emparejar('lambda')  
	def coma_lexper(self): 
		if self.tokenList[-3] in ['tk_coma']: 
			self.emparejar('tk_coma')  
			self.lexpr()  
			self.emparejar('coma_lexpr')  
		if self.tokenList[-3] in ['tk_par_der']: 
			self.emparejar('lambda')  
	def analizar(self):
		token=self.Analex.nextToken()
		self.tokenList=token[1:-1].split(',')
		try:
			self.prog()
		except RuntimeError:
			print("Error sintactico: se encontro final de archivo; se esperaba ‘end’")
		except:
			print('<'+self.tokenList[-2]+':'+self.tokenList[-1]+'>Error sintactico:' + 'se encontro: '+self.tokenList[-3]+'; se esperaba: '+self.prediccion)
	def emparejar(self,tk_esperado):
		if self.tokenList[-3] in tk_esperado:
			token=self.Analex.nextToken()
			self.tokenList=token[1:-1].split(',')
		else:
			raise Exception('')
