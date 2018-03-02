import time

class CT(object):
	'''
		Classe que modela o TC, ***
	'''
	def __init__(self,
				name,
				Ipn = 500,
				Isn = 5,
				accuracyClass = None,
				Isat = None):
		self.name = name 						# Identificacao do TC
		self.Ipn = Ipn							# Corrente nominal do primario do TC
		self.Isn = Isn							# Corrente nominal do secundario do TC
		self.rtc = float(Ipn/Isn)				# Relacao de transformacao do TC
		self.current = 0 	 					# Leitura atual de corrente do primario TC
		self.accuracyClass = accuracyClass		# Classe de exatidao do TC (valores tipicos para TC 
												# de protecao: 2.5/5.0/10.0)

		if Isat is None:						# Corrente do primario que leva o TC ao estado de saturacao
			self.Isat = 20*Ipn 					# Caso nao seja passada na criacao do objeto, assume 20*Ipn
		else:
			self.Isat = Isat

		self.isSaturated = False				# Flag que indica se o TC entrou em estado de saturacao

	def offSetCurrent(self,Ip):
		'''
			Funcao que retorna a corrente do secundario TC quando o primario
			e percorrido por uma corrente Ip.
		'''

		if self.Isat<Ip or self.isSaturated:		# Testa se o TC ficou ou esta saturado
			self.setSaturation()
			return float(self.Isat)/self.rtc
		else:
			return float(Ip)/self.rtc

	def setPrimaryCurrent(self,Ip):
		self.current=Ip
	
	def setSaturation(self,saturation=True):
		'''
			Funcao que seta o estado do TC para saturado (saturation=True) ou
			funcional (Saturation=False). Por padrao, se nenhum parametro eh 
			passado, o TC sera saturado.
		'''

		if saturation:
			print (self.name+" saturou. Prever manutencao.")
			self.isSaturated = True				# Em caso de saturacao, eh exibido um alerta de manutencao
		else:									# do TC. Eh necessario setar o parametro isSaturated = False
			self.isSaturated = False			# para que o TC tenha sua funcionalidade reestabelecida
					 	

class IED(object):
	'''
		Classe que modela o IED, ***
	'''
	def __init__(self, 						
				name,
				nmax,
				functions=None,
				ct=None,
				activeGroup=None,
				limits=None):

		# parametros do IED, passados na criacao do objeto

		self.name = name
		self.functions = functions 				# dicionario com as funcoes habilitadas no ied **>implementar logica
		self.nmax = nmax						# numero maximo de grupos de ajustes
		
		# Laco que associa os TCs de fase e neutro ao IED
		if ct is None:
			self.ct=[CT("TC A do "+self.name)]
			self.ct.append(CT("TC B do "+self.name))
			self.ct.append(CT("TC C do "+self.name))
			self.ct.append(CT("TC N do "+self.name))
		else:
			self.ct = ct		

		self.activeGroup = activeGroup			# objeto da classe AdjustGroup contendo o grupo de
												# ajustes ativo do IED
		self.BRKF = False 						# flag para habilitar/desabilitar falha de disjuntor
		self.function_sens = None 				# flag que indica a funcao de protecao indicada no 
												# painel do ied
		self.current = float()					# inicializa a corrente do ied como zero

		self.trip = False

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

	def sendTrip(self):
		currents = []
		for t in self.ct:
			## currents.append(t.offSetCurrent(t.current))
			currents.append(t.current)
	
		if self.activeGroup.tripF50(max(currents)):
			self.function_sens = '50'
			self.trip = True
		elif self.activeGroup.tripF50N(currents[3]):
			self.function_sens = '50N'
			self.trip = True
		elif self.activeGroup.tripF51(max(currents)):
			#time.sleep(self.activeGroup.delayF51(max(currents)))
			self.function_sens = '51'
			self.trip = True
		elif self.activeGroup.tripF51N(currents[3]):
			#time.sleep(self.activeGroup.delayF51N(currents[3]))
			self.function_sens = '51N'
			self.trip = True

	def reset(self):
		self.trip = False
		self.current = 0


class Breaker(object):
	'''
		Classe que modela o disjuntor, ***
	'''
	def __init__(self,
				name,
				opStatus='NC',
				relay=None):
		
		self.name = name 						# Nome do disjuntor
		self.relay = relay						# Associacao do rele ao disjuntor
		if opState is 'NO':						# Define o estado inicial do disjuntor pelo seu estado 
			self.status = 'open' 				# normal de operacao: open quando 'NO'(normalmente aberto) 
		else:									# 					  closed nos demais casos.
			self.status = 'closed'				# Por padrao, opState recebe 'NC'
	
	def isOpen(self):
		if self.status == 'open':
			return True
		else:
			return False

	def setOpen(self):
		self.state = 'open'

	def setClosed(self):
		self.state = 'closed' 			


class AdjustGroup(object):
	'''
		Classe que modela um grupo de ajuste: cada objeto criado armazena
		as correntes de pickup das funcoes 50/51 e 50/51N, os tipos de
		curva e os valores de dial.
	'''
	def __init__(self,ipk50,ipk51,curveP,dialP,ipk50N,ipk51N,curveN,dialN):
		
		# ajustes de fase

		self.ipk50 = ipk50						# ajuste da corrente de pickup da funcao 50

		self.ipk51 = ipk51						# ajuste da corrente de pickup da funcao 51
		self.curveP = curveP					# tipo ('NI','MI' ou 'EI') de curva de atuacao da funcao 50 
		self.dialP = dialP						# dial da curva de atuacao da funcao 50 de fase

		# ajustes de neutro

		self.ipk50N = ipk50N					# ajuste da corrente de pickup da funcao 50N
		
		self.ipk51N = ipk51N					# ajuste da corrente de pickup da funcao 51N
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

		if curve == 'NI' or curve == 'SI':

			beta = 0.14
			alpha = 0.02

		elif curve == 'MI' or curve == 'VI':

			beta = 13.5
			alpha = 1.0

		elif curve == 'EI':

			beta = 80
			alpha = 2.0

		return alpha,beta

	def tripF50(self,Iphase):
		if self.ipk50 > Iphase:
			return False
		else:
			return True

	def tripF51(self,Iphase):
		if self.ipk51 < Iphase:
			#time.sleep(self.delayF51(Iphase))						#desabilitado para teste
			return True
		else:
			return False	

	def delayF51(self,Iphase):
			a,b = self.returnParameters(self.curveP)
			return self.dialP*b/(((Iphase/self.ipk51)**a)-1)	

	def tripF50N(self,Ineutral):
		if self.ipk50N > Ineutral:
			return False
		else:
			return True

	def tripF51N(self,Ineutral):
		if self.ipk51N < Ineutral:
			#time.sleep(self.delayF51N(Ineutral))					#desabilitado para teste
			return True
		else:
			return False

	def delayF51N(self,Ineutral):
		a,b = self.returnParameters(self.curveP)
		return self.dialP*b/(((Ineutral/self.ipk51N)**a)-1)

class PowerGrid(object):
	'''
		Classe que modela uma rede eletrica.
	'''
	def __init__(self,ieds):
		# Inserir rede com os valores de curto circuito atraves
		# do parametro shortCircuitSimulatedGrid

		self.ieds = ieds
		pass

	def setProtection(self):
		pass

	def plotCurves(self,iscmax=1000,ieds=None):

		import matplotlib.pyplot as plt
		import numpy as np

		cor = ['b', 'r', 'g', 'k', 'y','m','c']

		if ieds == None:
			ieds = self.ieds

		
		isclist = []
		for i in ieds:
			isclist.append(i.activeGroup.ipk50N)
	
		iscmin = int(min(isclist))
		iscmax = int(iscmax)

		isc = range(iscmin,iscmax)
		opTime5051 = []
		opTime5051N = []
		isc = []
		iscN = []
		j=0

		for ied in ieds:

			isc.append(range(int(ied.activeGroup.ipk50*1.05),int(ied.activeGroup.ipk51*1.05)))
			opTime5051.append([])
			for i in isc[j]:
				if ied.activeGroup.ipk50 < i:
					opTime5051[j].append(j*0.3)
				elif ied.activeGroup.ipk51 < i:
					opTime5051[j].append(ieds[0].activeGroup.delayF51(i))

			iscN.append(range(int(ied.activeGroup.ipk50N*1.05),int(ied.activeGroup.ipk51N*1.05)))
			opTime5051N.append([])
			for i in iscN[j]:
				if ied.activeGroup.ipk50N < i:
					opTime5051N[j].append(j*0.3)
				elif ied.activeGroup.ipk51N < i:
					opTime5051N[j].append(ieds[0].activeGroup.delayF51(i))

			#plt.plot(isc[j],opTime5051[j])
			j+=1
		
		i=[0,1,2,3,4,5]
		j=[0,1,2,3,4,5]
		for k in range(0,3):
			j[]
			plt.plot(i,j)

		#plt.plot(isc[0],opTime5051[0])
		plt.show()




	
# Rotinas de teste
'''
tcs = [CT("TCA",500,5),CT("TCB",500,5),CT("TCC",500,5),CT("TCN",50,5)]
ied = IED("IED1",3,dict(),tcs)

print "Nome do IED: " + ied.name
print "Nome do TC: " + ied.ct[1].name
print "Corrente nominais do TC: " + str(tcs[1].Ipn)
print "Corrente de saturacao do TC: " + str(tcs[1].Isat)

tc2 = CT("TC2",500,1,2.5,5000)
tcs[2] = tc2 
print "Nome do TC: " + ied.ct[2].name
print "Corrente nominais do TC: " + str(tcs[2].Ipn)
print "Corrente de saturacao do TC: " + str(tcs[2].Isat)

j=4990
ipList = range(j,5010)
isList = []

for i in ipList:
	isList.append(tc2.offSetCurrent(ipList[i-j]))
	print "Ip=" + str(ipList[i-j]) + "A, Is=" + str(isList[i-j]) +"A"

for i in ipList:
	isList[i-j]=tc2.offSetCurrent(ipList[i-j])
	print "Ip=" + str(ipList[i-j]) + "A, Is=" + str(isList[i-j]) +"A"
'''

Ipn=10000
tcs = [CT("TCA",10*Ipn,5),CT("TCB",10*Ipn,5),CT("TCC",10*Ipn,5),CT("TCN",Ipn,5)]
adjust = AdjustGroup(9*Ipn,1.4*Ipn,'NI',0.1,0.9*Ipn,0.14*Ipn,'NI',1)
ied1 = IED("IED1",1,dict(),tcs,adjust)

Ipn=15000
tcs = [CT("TCA",10*Ipn,5),CT("TCB",10*Ipn,5),CT("TCC",10*Ipn,5),CT("TCN",Ipn,5)]
adjust = AdjustGroup(9*Ipn,1.4*Ipn,'NI',0.1,0.9*Ipn,0.14*Ipn,'NI',1)
ied = IED("IED1",1,dict(),tcs,adjust)

Rede = PowerGrid([ied1,ied])
Rede.plotCurves(30000)

'''
print ("teste 50/51 e 50/51N")
for t in tcs:
	t.setPrimaryCurrent(1)
for i in range(0,200):
	tcs[0].setPrimaryCurrent(i*10)
	tcs[3].setPrimaryCurrent(i*1.11)
	ied.sendTrip()
	print ("Ip:"+str(tcs[0].current)+"A ;In:"+str(tcs[3].current)+"A ; F.Sens:"+str(ied.function_sens))
	ied.reset()
'''