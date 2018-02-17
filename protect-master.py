# coding=utf-8

from rede import Subestacao, Gerador

class IED(object):

	def __init__(self, 						
				nome,
				nmax,
				grupoAtivo,
				funcoes,
				BRKF=False,
				val_min=None,
				rtc=None):


		self.nome = nome						
							
		self.grupoAtivo = grupoAtivo 			# variavel que indica o grupo de ajuste ativo
		self.funcoes = funcoes 					# dicionario com as funcoes habilitadas no ied
		self.BRKF = BRKF 						# flag para habilitar/desabilitar falha de disjuntor

		self.nmax = nmax						# numero maximo de grupos de ajustes
		self.funcao_sensibilizada = None 		# flag que indica a funcao de protecao indicada no painel do ied

		self.corrente = float()					# inicializa a corrente do ied como zero

		# loop cria variavel que contera todos os grupos de ajustes cadastrados

		self.grupos = dict()

		for i in range(nmax):

			tag = str(i+1)
			self.grupos[tag] = None

		# valores minimos permitidos pelo rele

		if val_min is not None:

			self.iaj51_min = val_min['I51MIN']
			self.iaj51_max = val_min['I51MAX']

			self.iaj50_min = val_min['I50MIN']
			self.iaj50_max = val_min['I50MAX']

			self.dial_min = val_min['DIAL_MIN']
			self.dial_max = val_min['DIAL_MAX']

		self.rtc = rtc 	# relacao de transformacao de corrente
		

	def atuacao(self,corrente,tipo='F'):

		"""
			metodo para simular a atuacao do ied para 
			um determinado valor de corrente de entrada
		"""

		toperacao = None

		corrente = float(corrente) 

		grupo_ativo = self.grupos[self.grupoAtivo]

		# atuacao pela funcao de fase

		if tipo is 'F':

			if corrente <= grupo_ativo.ipk51p:

				self.funcao_sensibilizada = None
				toperacao = None

			if (corrente > grupo_ativo.ipk51p and corrente < grupo_ativo.ipk50p) and self.funcoes['51P'] is True:

				self.funcao_sensibilizada = '51P'

				toperacao = top(corrente,grupo_ativo.curvap,grupo_ativo.dialp,grupo_ativo.ipk51p)

				#top = (betap/((corrente/grupo_ativo.ipk51p)**alfap-1))*grupo_ativo.dialp

			if corrente >= grupo_ativo.ipk50p:

				if self.funcoes['50P'] is True:

					self.funcao_sensibilizada = '50P'
					toperacao = 0.1

				elif self.funcoes['51P']:

					self.funcao_sensibilizada = '51P'

					toperacao = top(corrente,grupo_ativo.curvap,grupo_ativo.dialp,grupo_ativo.ipk51p)

					#top = (betap/((corrente/grupo_ativo.ipk51p)**alfap-1))*grupo_ativo.dialp

		# atuacao pela funcao de neutro

		elif tipo is 'N':

			if corrente <= grupo_ativo.ipk51n:

				self.funcao_sensibilizada = None
				toperacao = None

			if (corrente > grupo_ativo.ipk51n and corrente < grupo_ativo.ipk50n) and self.funcoes['51N'] is True:

				self.funcao_sensibilizada = '51N'
				
				toperacao = top(corrente,grupo_ativo.curvan,grupo_ativo.dialn,grupo_ativo.ipk51n)

				# top = (betan/((corrente/grupo_ativo.ipk51n)**alfan-1))*grupo_ativo.dialn

			if corrente >= grupo_ativo.ipk50n:

				if self.funcoes['50N'] is True:

					self.funcao_sensibilizada = '50N'
					toperacao = 0.1

				elif self.funcoes['51N']:

					self.funcao_sensibilizada = '51N'
					
					toperacao = top(corrente,grupo_ativo.curvan,grupo_ativo.dialn,grupo_ativo.ipk51n)

					# top = (betan/((corrente/grupo_ativo.ipk51n)**alfan-1))*grupo_ativo.dialn

		# simula falha de disjuntor

		if self.BRKF:

			toperacao = 'BRKF'

		return self.funcao_sensibilizada, toperacao


	def reset(self): 

		"""
			metodo retorna os atributos do ied para as condicoes iniciais

		"""

		self.funcao_sensibilizada = None
		self.corrente = 0.0

	def geraCurva(self,tipo,cor='b'):

		"""
			metodo para gerar a curva baseado no 
			tipo da funcao fase (F) e neutro (N)
		"""

		import matplotlib.pyplot as plt
		import numpy as np
		
		grupo_ativo = self.grupos[self.grupoAtivo]

		alfap, betap = grupo_ativo.curvas(grupo_ativo.curvap)
		alfan, betan = grupo_ativo.curvas(grupo_ativo.curvan)

		numero_pontos = 1000

		if tipo is 'F':

			corrente = np.linspace(1.1*grupo_ativo.ipk51p,grupo_ativo.ipk50p,numero_pontos)

			top=list()

			for i in corrente:

				if i < grupo_ativo.ipk50p:
					
					top.append((betap/((i/grupo_ativo.ipk51p)**alfap-1))*grupo_ativo.dialp)
				
				elif i >= grupo_ativo.ipk50p:

					top.append(0.1)

			plt.axis((0.9*grupo_ativo.ipk51p,1.1*grupo_ativo.ipk50p,0,1.1*top[0])) # configura os eixos do grafico

			plt.grid(True)
			
			plt.plot(corrente,top,cor)

			self.curva_fase = plt

		elif tipo is 'N':

			corrente = np.linspace(1.1*grupo_ativo.ipk51n,grupo_ativo.ipk50n,numero_pontos) 

			top=list()

			for i in corrente:

				if i < grupo_ativo.ipk50n:
					
					top.append((betan/((i/grupo_ativo.ipk51n)**alfan-1))*grupo_ativo.dialn)
				
				elif i >= grupo_ativo.ipk50n:

					top.append(0.1)

			plt.axis((0.9*grupo_ativo.ipk51n,1.1*grupo_ativo.ipk50n,0,1.1*top[0])) # configura os eixos do grafico

			plt.grid(True)
			
			plt.plot(corrente,top,cor)

			self.curva_neutro = plt
		
	def exibeCurva(self,tipo):

		"""
			metodo para exibir as curvas do tipo fase ('F') e neutro ('N')
		"""

		if tipo is 'F':

			self.curva_fase.show()

		elif tipo is 'N':

			self.curva_neutro.show()

class GrupoAjuste(object):

	def __init__(self, ipk51p,ipk50p,curvap,dialp,ipk51n,ipk50n,curvan,dialn):
		
		# ajustes de fase

		self.ipk51p = ipk51p
		self.ipk50p = ipk50p
		self.curvap = curvap
		self.dialp = dialp

		# ajustes de neutro

		self.ipk51n = ipk51n
		self.ipk50n = ipk50n
		self.curvan = curvan
		self.dialn = dialn

	def curvas(self,curva):

		if curva == 'NI':

			beta = 0.14
			alfa = 0.02

		elif curva == 'MI':

			beta = 13.5
			alfa = 1.0

		elif curva == 'EI':

			beta = 80
			alfa = 2.0

		return alfa, beta

class sprot(object):

	"""Simulador de protecao"""

	def __init__(self):
		
		pass

	def coordenograma(self,lista_ied,tipo='F',lista_nos=None,exibir_coordenograma=True,save_dir=None):

		"""
			Metodo gera o coordenograma de uma lista de ied e retorna o objeto grafico do tipo pyplot

			lista_ied (list) = [ied1,ied2,ied3,...]
			tipo (str) = 'F' ou 'N'
			lista_nos (tuple) = (subestacao,alimentador,lista_nos)
			save_dir = diretorio para salvar o grafico

		"""

		import matplotlib.pyplot as plt
		import numpy as np

		cor = ['b', 'r', 'g', 'k', 'y','m','c']

		j=0	

		for ied in lista_ied:

			grupo_ativo = ied.grupos[ied.grupoAtivo]
	
			if tipo is 'F':

				ipk51 = grupo_ativo.ipk51p
				ipk50 = grupo_ativo.ipk50p
				dial = grupo_ativo.dialp
				alfa, beta = grupo_ativo.curvas(grupo_ativo.curvap)
				funcao_temporizada = '51P'

			elif tipo is 'N':

				ipk51 = grupo_ativo.ipk51n
				ipk50 = grupo_ativo.ipk50n
				dial = grupo_ativo.dialn
				alfa, beta = grupo_ativo.curvas(grupo_ativo.curvan)
				funcao_temporizada = '51N'

			corrente = list(np.linspace(1.1*ipk51,8e3,8e3))

			top=list()
			
			for i in corrente:

				if i < ipk50:

					ponto_ipk50 = i 	# grava ultimo ponto antes do ipk50
					top.append((beta/((i/ipk51)**alfa-1))*dial)
				
				elif i >= ipk50:

					top.append(0.1)

			if ied.funcoes[funcao_temporizada] is False:

				corrente_aux = list()

				for i in range(len(corrente)):

					corrente_aux.append(ipk50)

				corrente = corrente_aux

			plt.loglog(corrente,top,cor[j],linewidth=2.0,label=ied.nome)
			plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)	


			j+=1 # atualiza cor

		if lista_nos is not None:

			cor2 = ['--k','--b', '--r', '--g', '--y','--m','--c']
			n=0

			subestacao = lista_nos[0]
			alimentador = lista_nos[1]
			lista_nos = lista_nos[2]

			for no in lista_nos:

				if tipo is 'F':
					
					cc = cc3f(subestacao,alimentador,no) 

				elif tipo is 'N':

					cc = cc1f(subestacao,alimentador,no) 					

				curto_circuito  = [cc for t in top]

				plt.autoscale(enable=True,axis='both')

				plt.loglog(curto_circuito,top,cor2[n],linewidth=2.0,label='Icc ' + no.nome)
				plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

				n+=1 # atualiza cor
		
		plt.autoscale(enable=True,axis='both',tight=True)
		
		plt.xlabel('Corrente (A)',fontsize=14)
		plt.ylabel('Tempo de Operacao (s)',fontsize=14)
		plt.grid(True,which='both',ls='-')
		
		if save_dir != None: plt.savefig(save_dir, bbox_inches='tight')

		if exibir_coordenograma: plt.show()	

		plt.figure()	

		return plt


def cc3f(subestacao,alimentador,no_falta):

	"""
		metodo para calcular o curto circuito trifasico total 

		biblioteca implementada para atualizar o modulo 
		de curto circuito utilizado pelo modulo de protecao
	"""

	from curto_circuito.componentes_simetricas_gd import curto3f_geracao, curto3f_gd
	from rede import Gerador
	# print "debug cc3f: ", subestacao.nome, alimentador.nome, no_falta.nome
	cc = curto3f_geracao(subestacao,alimentador,no_falta)	
	
	for alimentador in subestacao.alimentadores.values():

		for no in alimentador.nos_de_carga.values():

			if isinstance(no,Gerador):

				cc = cc + curto3f_gd(subestacao,no_falta,no)

	return cc


def cc1f(subestacao,alimentador,no_falta):

	"""
		metodo para calcular o curto circuito monofasico total 

		biblioteca implementada para atualizar o modulo 
		de curto circuito utilizado pelo modulo de protecao
	"""

	from curto_circuito.componentes_simetricas_gd import curto1f_geracao, curto1f_gd
	from rede import Gerador

	cc = curto1f_geracao(subestacao,alimentador,no_falta)

	for alimentador in subestacao.alimentadores.values():

		for no in alimentador.nos_de_carga.values():

			if isinstance(no,Gerador):

				cc = cc + curto1f_gd(subestacao,no_falta,no)

	return cc

def top(corrente,curva,dial,ipk51):

	corrente = float(corrente)
	ipk51 = float(ipk51)
	dial = float(dial)

	if curva == 'NI':

		beta = 0.14
		alfa = 0.02

	elif curva == 'MI':

		beta = 13.5
		alfa = 1.0

	elif curva == 'EI':

		beta = 80
		alfa = 2.0 

	return (beta/((corrente/ipk51)**alfa-1))*dial
		

	
