class TC(object):
	'''
		Classe que modela o TC, ***
	'''
	def __init__(self,
				name,
				Ipn,
				Isn,
				classExat = None,
				Isat = None):
		self.name = name
		self.Ipn = Ipn							# Corrente nominal do primario do TC
		self.Isn = Isn							# Corrente nominal do secundario do TC
		self.rtc = float(Ipn/Isn)						# Relacao de transformacao do TC
		self.classExat = classExat				# Classe de exatidao do TC (valores tipicos para TC 
												# de protecao: 2.5/5.0/10.0)

		if Isat is None:						# Corrente do primario que leva o TC ao estado de saturacao
			self.Isat = 20*Ipn
		else:
			self.Isat = Isat

	def offSetCurrent(self,Ip):
		'''
			Funcao que retorna a corrente do secundario TC quando o primario
			e percorrido por uma corrente Ip.
		'''

		if self.Isat>Ip:
			print "Nao saturou"
			return float(Ip)/self.rtc
		else:
			print "Saturou"
			return float(self.Isat)/self.rtc


class IED(object):
	'''
		Classe que modela o IED, ***
	'''
	def __init__(self, 						
				name,
				nmax,
				functions,
				tc,
				limits=None):

		# parametros do IED, passados na criacao do objeto

		self.name = name
		self.functions = functions 				# dicionario com as funcoes habilitadas no ied
		self.nmax = nmax						# numero maximo de grupos de ajustes
		self.TC = tc 							# TC associado ao IED						
							
		self.activeGroup = 0	 				# variavel que indica o grupo de ajuste ativo (por 
		                                        # padrao, 0: sem funcoes habilitadas)
		self.BRKF = False 						# flag para habilitar/desabilitar falha de disjuntor
		self.function_sens = None 				# flag que indica a funcao de protecao indicada no 
												# painel do ied
		self.corrente = float()					# inicializa a corrente do ied como zero

		if limits is not None:					# limites permitidos pelo rele

			self.iaj51_min = limits['I51MIN']
			self.iaj51_max = limits['I51MAX']

			self.iaj50_min = limits['I50MIN']
			self.iaj50_max = limits['I50MAX']

			self.dial_min = limits['DIAL_MIN']
			self.dial_max = limits['DIAL_MAX']

		# loop cria variavel que contera todos os grupos de ajustes cadastrados

		self.groups = dict()

		for i in range(nmax):

			tag = str(i+1)
			self.groups[tag] = None

class AdjustGroup(object):
	'''
		Classe que modela um grupo de ajuste: cada objeto criado armazena
		as correntes de pickup das funcoes 50/51 e 50/51N, os tipos de
		curva e os valores de dial.
	'''
	def __init__(self,ipk51,ipk50,curvaP,dialP,ipk51N,ipk50N,curveN,dialN):
		
		# ajustes de fase

		self.ipk51 = ipk51						# ajuste da corrente de pickup da funcao 51
		self.ipk50 = ipk50						# ajuste da corrente de pickup da funcao 50
		self.curveP = curveP					# tipo ('NI','MI' ou 'EI') de curva de atuacao da funcao 50 
		self.dialP = dialP						# dial da curva de atuacao da funcao 50 de fase

		# ajustes de neutro

		self.ipk51N = ipk51N					# ajuste da corrente de pickup da funcao 51N
		self.ipk50N = ipk50N					# ajuste da corrente de pickup da funcao 50N
		self.curveN = curveN					# tipo ('NI','MI' ou 'EI') de curva de atuacao da funcao 50N
		self.dialN = dialN						# dial da curva de atuacao da funcao 50N

	def returnParameters(self,curve):
		'''
			Funcao que retorna os parametros alfa e beta de acordo com o tipo
			de curva passada como parametro:
				'NI'/'SI': Normalmente Inversa
				'MI'/'VI': Muito Inversa
				'EI': Extremamente Inversa
		'''

		if curve == 'NI' | curve == 'SI':

			beta = 0.14
			alpha = 0.02

		elif curve == 'MI' | curve == 'VI':

			beta = 13.5
			alpha = 1.0

		elif curve == 'EI':

			beta = 80
			alpha = 2.0

		return alpha,beta


tc1 = TC("TC1",500,5)
ied = IED("IED1",3,dict(),tc1)

print "Nome do IED: " + ied.name
print "Nome do TC: " + tc1.name
print "Corrente nominais do TC: " + str(tc1.Ipn)
print "Corrente de saturacao do TC: " + str(tc1.Isat)

tc2 = TC("TC2",500,1,2.5,5000)
print "Nome do TC: " + tc2.name
print "Corrente nominais do TC: " + str(tc2.Ipn)
print "Corrente de saturacao do TC: " + str(tc2.Isat)

ipList = range(0,5010)
isList = []

for i in ipList:
	isList.append(tc2.offSetCurrent(ipList[i]))
	print "Ip=" + str(ipList[i]) + "A, Is=" + str(isList[i]) +"A"
