class TC(object):

	def __init__(self):
		teste(2)
		pass

	def teste(self,parametro):
		print(parametro)



class IED(object):
	def __init__(self, 						
				name,
				nmax,
				activeGroup,
				functions,
				BRKF=False,
				min_val=None,
				rtc=None):


		self.name = name						
							
		self.activeGroup = activeGroup 			# variavel que indica o grupo de ajuste ativo
		self.functions = functions 					# dicionario com as funcoes habilitadas no ied
		self.BRKF = BRKF 						# flag para habilitar/desabilitar falha de disjuntor

		self.nmax = nmax						# numero maximo de grupos de ajustes
		self.function_sens = None 		# flag que indica a funcao de protecao indicada no painel do ied

		self.corrente = float()					# inicializa a corrente do ied como zero

		# loop cria variavel que contera todos os grupos de ajustes cadastrados

		self.groups = dict()

		for i in range(nmax):

			tag = str(i+1)
			self.groups[tag] = None

		# valores minimos permitidos pelo rele

		if min_val is not None:

			self.iaj51_min = min_val['I51MIN']
			self.iaj51_max = min_val['I51MAX']

			self.iaj50_min = min_val['I50MIN']
			self.iaj50_max = min_val['I50MAX']

			self.dial_min = min_val['DIAL_MIN']
			self.dial_max = min_val['DIAL_MAX']

		self.rtc = rtc 	# relacao de transformacao de corrente