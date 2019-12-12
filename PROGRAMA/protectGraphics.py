
from PySide2.QtCore import *
from PySide2.QtGui import *

from protectCalc import *
from PySide2.QtWidgets import *
from PySide2 import QtGui, QtCore

class MainWindow(QWidget):
    def __init__(self,powerGrid):
        super().__init__()
        #self.main = self
        self.powerGrid=powerGrid
        self.graphicSwitches=[]
        self.checkButtons=[] 
        self.buttonPhase=[]        
        self.buttonNeutral=[]
        self.organize() 
        #self.setStyleSheet('background-color: #D8D8D8')


    def organize(self):
        self.layout = QVBoxLayout()
        self.layoutButtons = QHBoxLayout()
        #self.layoutButtons1 = QHBoxLayout()
        #self.layoutButtons2 = QHBoxLayout()

        self.plotTitle=QLabel("MyGrid.protect v0.1")
        self.layoutButtons.addWidget(self.plotTitle)
        
     
        self.nullLabel = QLabel()
        #self.nullLabel.setMaximumWidth(100)
        self.layoutButtons.addWidget(self.nullLabel)
        self.setLabel = QLabel("Auto-ajuste: MC")
        self.setLabel.setMaximumWidth(60)
        self.layoutButtons.addWidget(self.setLabel)
        self.timeEdit = QLineEdit("0.2")
        self.timeEdit.setMaximumWidth(30)
        self.layoutButtons.addWidget(self.timeEdit)
        self.selectButton = QPushButton("Seletivo")
        self.selectButton.setMaximumWidth(80)
        self.layoutButtons.addWidget(self.selectButton)
        self.coordButton = QPushButton("Coordenado")
        self.coordButton.setMaximumWidth(80)
        self.layoutButtons.addWidget(self.coordButton)


        self.plotLabel = QLabel("Plotar: ")
        self.plotLabel.setMaximumWidth(30)
        self.layoutButtons.addWidget(self.plotLabel)
        self.phaseButton = QPushButton("Coord. Fase")
        self.phaseButton.setMaximumWidth(80)
        self.layoutButtons.addWidget(self.phaseButton)
        self.neutralButton = QPushButton("Coord. Neutro")
        self.neutralButton.setMaximumWidth(80)
        self.layoutButtons.addWidget(self.neutralButton)


        #self.widgetButtons1 = QWidget()
        #self.widgetButtons1.setLayout(self.layoutButtons1)
        #self.layoutButtons.addWidget(self.widgetButtons1)
        #self.widgetButtons2 = QWidget()
        #self.widgetButtons2.setLayout(self.layoutButtons2)
        #self.layoutButtons.addWidget(self.widgetButtons2)

        #self.layoutButtons.addChildLayout(self.layoutButtons1)
        #self.layoutButtons.addChildLayout(self.layoutButtons2)

        #self.closeButton = QPushButton("Fechar")
        #self.closeButton.setMaximumWidth(150)
        #self.layoutButtons.addWidget(self.closeButton)

        self.widgetButtons = QWidget()
        self.widgetButtons.setLayout(self.layoutButtons)
        self.widgetButtons.setMaximumHeight(40)
        self.layout.addWidget(self.widgetButtons)


        self.layout.addWidget(IEDLevel(self.layout,self,self))#,self.layout


        self.resize(600,300)
        self.setLayout(self.layout)
        self.show()

        self.phaseButton.released.connect(self.plotCoordinationGraphPhase)
        self.neutralButton.released.connect(self.plotCoordinationGraphNeutral)
        self.coordButton.released.connect(self.autoSettingCoord)
        self.selectButton.released.connect(self.autoSettingSelect)
        #self.closeButton.released.connect(self.close)

    def autoSettingCoord(self):
        self.powerGrid.time=float(self.timeEdit.text())
        self.powerGrid.autoSettingCoord()
        for sw in self.graphicSwitches:
            if isinstance(sw.switch, FuseSwitch):
                sw.setLabelsValues()
        print("Coord")
        pass

    def autoSettingSelect(self):
        self.powerGrid.time=float(self.timeEdit.text())
        self.powerGrid.autoSettingSelect()
        for sw in self.graphicSwitches:
            if isinstance(sw.switch, FuseSwitch):
                sw.setLabelsValues()
        print("Select")
        pass

    def plotCoordinationGraphPhase(self):
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import matplotlib.lines as mlines
        patches=[]
        lines=[]
        color=['k','r','b','g','y']
        j=0
        plt.close()
        fig, ax = plt.subplots()
        for i in self.checkButtons:
            if i.isChecked():
                if isinstance(self.powerGrid.ieds[j], IED):
                    isc,t=self.powerGrid.ieds[j].calculateCurveP(None)#,len(self.checkButtons)-j)
                    ax.loglog(isc, t, color[j%len(color)], basex=10)
                    #plt.plot(isc,t,color[j%len(color)])
                else:
                    self.powerGrid.ieds[j].link.loadCurve()
                    isc,t=self.powerGrid.ieds[j].link.curve[0], self.powerGrid.ieds[j].link.curve[1]
                    ax.loglog(isc, t, color[j%len(color)], basex=10)
                    isc,t=self.powerGrid.ieds[j].link.curve[2], self.powerGrid.ieds[j].link.curve[3]
                    ax.loglog(isc, t, color[j%len(color)], basex=10)
                lines.append(mlines.Line2D([], [], color=color[j%len(color)], label=self.powerGrid.ieds[j].name))             
            j+=1
        ax.set(xlabel='Corrente - I (A)', ylabel='Tempo - t(s)')
        ax.grid(which='both')
        ax.grid()
        #fig.savefig("test.png")
        #plt.set(xlabel='time (s)', ylabel='voltage (mV)',title='About as simple as it gets, folks')
        plt.legend(handles=lines)
        plt.show()

    def plotCoordinationGraphNeutral(self):
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import matplotlib.lines as mlines
        patches=[]
        lines=[]
        color=['k','r','b','g','y']
        j=0
        plt.close()
        fig, ax = plt.subplots()
        for i in self.checkButtons:
            if i.isChecked():
                if isinstance(self.powerGrid.ieds[j], IED):
                    isc,t=self.powerGrid.ieds[j].calculateCurveN(None)#,len(self.checkButtons)-j)
                    ax.loglog(isc, t, color[j%len(color)]+'--', basex=10)
                    #plt.plot(isc,t,color[j%len(color)])
                else:
                    self.powerGrid.ieds[j].link.loadCurve()
                    isc,t=self.powerGrid.ieds[j].link.curve[0], self.powerGrid.ieds[j].link.curve[1]
                    ax.loglog(isc, t, color[j%len(color)]+'--', basex=10)
                    isc,t=self.powerGrid.ieds[j].link.curve[2], self.powerGrid.ieds[j].link.curve[3]
                    ax.loglog(isc, t, color[j%len(color)]+'--', basex=10)
                lines.append(mlines.Line2D([], [], color=color[j%len(color)], linestyle='--', label=self.powerGrid.ieds[j].name))    
            j+=1
        ax.set(xlabel='Corrente - I (A)', ylabel='Tempo - t(s)')
        ax.grid(which='both')
        plt.legend(handles=lines)
        plt.show()

class IEDLine(QFrame):
    def __init__(self,switch,window,main):
        super().__init__()
        self.main = main
        self.main.graphicSwitches.append(self)
        self.setLayout(QVBoxLayout())
        #self.setStyleSheet('background-color: #ffffff')

        #self.setFrameStyle(QFrame.HLine | QFrame.Plain)
        #self.setFixedWidth(20)
        #self.setLineWidth(6)

        self.switch = switch
        self.window = window

        self.lineWidget = QWidget()
        self.lineLayout = QHBoxLayout(self.lineWidget)

        # tentativa de contornar o level

        #self.lineWidget.setFrameStyle(QFrame.Panel | QFrame.Plain)
        #self.lineWidget.setLineWidth(2)

        #
        self.graphWidget = QWidget()
        self.lineLayout.addWidget(self.graphWidget)


        self.plotCheck = QCheckBox(self.switch.name)
        #self.plotCheck.setFixedWidth(100)
        #self.lineLayout.addWidget(self.plotCheck)
        self.configButton = QPushButton("config.")
        #self.configButton.setFixedWidth(50)
        self.linkInLabel = QLineEdit("15")
        self.linkCurveTypeLabel = QLineEdit("K")


        '''
        self.plotCheck = QCheckBox(self.ied.name)
        self.plotCheck.setFixedWidth(100)
        self.lineLayout.addWidget(self.plotCheck)
        self.configButton = QPushButton("config.")
        self.configButton.setFixedWidth(50)
        self.lineLayout.addWidget(self.configButton)
        '''
        if isinstance(self.switch, IED):
            sType="ied"
        else:
            sType="fuseSwitch"

        self.setSwitchType(self.graphWidget,sType)
        self.lineLayout.addWidget(QFrame())
        self.lineLayout.itemAt(1).widget().setFixedWidth(6)
        self.lineLayout.itemAt(1).widget().setFrameStyle(QFrame.VLine | QFrame.Plain)
        self.lineLayout.itemAt(1).widget().setLineWidth(6)
        self.lineLayout.addWidget(IEDLevel(self.graphWidget.layout().itemAt(2).widget().layout(),window,self.main))#self.lineLayout,
        #self.graphWidget.layout()

        self.layout().addWidget(self.lineWidget)
        self.configButton.released.connect(self.configIED)
        self.linkInLabel.editingFinished.connect(self.configFuseSwitch)
        self.linkCurveTypeLabel.editingFinished.connect(self.configFuseSwitch)

        self.graphWidget.setMaximumSize(50+80+10+50,90)

        window.checkButtons.append(self.plotCheck)
        window.powerGrid.ieds.append(self.switch)

    def configIED(self):
        IEDWindow(self.switch,self.window)

    def setSwitchType(self,w,type):
        w.setLayout(QGridLayout())
        f = []
        for j in range(3):
            f.append(QFrame())

        w.resize(300,300)
        k=-1
        if type == 'ied':
            for i in range(1):
                for j in range(3):
                    k=k+1                    
                    if (j==0 and i==0):
                        f[k].setFrameStyle(QFrame.HLine | QFrame.Plain)
                        f[k].setFixedWidth(20)
                        f[k].setLineWidth(6)
                        #f[k].setAutoFillBackground(True)
                        #f[k].setFrameStyle(QFrame.VLine | QFrame.Plain)
                        #f[k].setLineWidth(6)
                    elif (i==0 and j==1):
                        f[k].setFixedSize(80,80)
                        f[k].setFrameStyle(QFrame.Box | QFrame.Plain)
                        f[k].setLineWidth(6)
                        f[k].setLayout(QVBoxLayout())
                        f[k].layout().addWidget(self.plotCheck)
                        f[k].layout().addWidget(self.configButton)
                    else:
                        f[k].setFrameStyle(QFrame.HLine | QFrame.Plain)
                        f[k].setFixedWidth(70)
                        f[k].setLineWidth(6)
                        f[k].setLayout(QVBoxLayout())
                        f[k].layout().addWidget(QWidget())
                        f[k].layout().itemAt(0).widget().setFixedHeight(60)
                    w.layout().addWidget(f[k],i,j)
        else:
            for i in range(1):
                for j in range(3):
                    k=k+1                    
                    if (j==0 and i==0):
                        f[k].setFixedWidth(20)
                        f[k].setFrameStyle(QFrame.HLine | QFrame.Plain)
                        f[k].setLineWidth(6)
                        #f[k].setBackgroundRole(QPalette.Base)
                        #f[k].setAutoFillBackground(True)
                        #f[k].setFrameStyle(QFrame.VLine | QFrame.Plain)
                        #f[k].setLineWidth(6)
                    elif (i==0 and j==1):
                        f[k].setFixedSize(80,80)
                        f[k].setFrameStyle(QFrame.Box | QFrame.Plain)
                        f[k].setLineWidth(6)

                        f[k].setLayout(QGridLayout())
                        f[k].layout().addWidget(self.plotCheck,0,0)
                        f[k].layout().itemAt(0).widget().setMinimumWidth(50)
                        f[k].layout().addWidget(self.linkInLabel,1,0)
                        f[k].layout().addWidget(self.linkCurveTypeLabel,1,1)
                    else:
                        f[k].setFrameStyle(QFrame.HLine | QFrame.Plain)
                        f[k].setFixedWidth(70)
                        f[k].setLineWidth(6)
                        f[k].setLayout(QVBoxLayout())
                        f[k].layout().addWidget(QWidget())
                        f[k].layout().itemAt(0).widget().setFixedHeight(60)
                    w.layout().addWidget(f[k],i,j)

        p = w.palette()
        p.setColor(w.backgroundRole(), Qt.white)
        w.setPalette(p)

    def configFuseSwitch(self):
        self.switch.link.In = float(str(self.linkInLabel.text()))
        self.switch.link.standardIn()
        self.switch.link.setCurveType(str(self.linkCurveTypeLabel.text()))
        #print(str(self.switch.link.In)+" "+self.switch.link.curveType)
        self.linkInLabel.clear()#insert(str(self.switch.link.In))
        self.linkCurveTypeLabel.clear()#insert(self.switch.link.curveType)
        if self.switch.link.In > 1:
            self.switch.link.In = int(self.switch.link.In)
        self.linkInLabel.insert(str(self.switch.link.In))
        self.linkCurveTypeLabel.insert(self.switch.link.curveType)

    def setLabelsValues(self):
        self.linkInLabel.setText(str(int(self.switch.link.In)))
        self.linkCurveTypeLabel.setText(self.switch.link.curveType)   



class IEDLevel(QWidget):

    def __init__(self,layout,window,main):
        super().__init__()
        self.resize(10,10)
        self.main=main
        #self.setStyleSheet('background-color: #ffffff')

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.newButton = QPushButton("Novo")
        self.newButton.setFixedWidth(50)
        layout.addWidget(self.newButton)

        self.newButton.released.connect(self.createSwitch)
        self.window = window

    def createIED(self):
        newIEDWindow = IEDWindow(1,self.window)
        if newIEDWindow.flag:
            self.layout.addWidget(IEDLine(newIEDWindow.ied,self.window,self.main))

    def createSwitch(self):
        newWindow = newSwitchWindow(self)

class IEDWindow(QDialog):
    def __init__(self,ied,window):
        super().__init__()
        self.ied = ied
        self.window = window
        if isinstance(ied,int):
            self.organizeCreate()
        else:
            self.organizeEdit()

    def organizeCreate(self):
        self.flag = False
        
        self.layout = QVBoxLayout()
       
        self.formWidget = QWidget()
        self.formLayout = QFormLayout(self.formWidget)
        self.layout.addWidget(self.formWidget)
        self.tabWidget=QTabWidget()
        self.tabWidget.setFixedHeight(140)
        self.layout.addWidget(self.tabWidget)
        self.formWidgetPhase = QWidget()
        self.formLayoutPhase = QFormLayout(self.formWidgetPhase)
        self.formWidgetNeutral = QWidget()
        self.formLayoutNeutral = QFormLayout(self.formWidgetNeutral)
        self.tabWidget.addTab(self.formWidgetPhase,"Fase")
        self.tabWidget.addTab(self.formWidgetNeutral,"Neutro")
        self.buttonsWidget = QWidget()
        self.buttonsLayout = QHBoxLayout(self.buttonsWidget)

        w = len(self.window.powerGrid.ieds)
        z = 1000

        Ipn = z-(((z/10)*w/9)+((z/5)*w/11))
        self.nameLineEdit = QLineEdit('S'+str(6+w))
        self.ipk50LineEdit = QLineEdit(str(Ipn*4))
        self.ipk51LineEdit = QLineEdit(str(Ipn*1.5))
        self.dialLineEdit = QLineEdit(str(1))
        self.curveLineEdit = QLineEdit("NI")
        self.ipk50NLineEdit = QLineEdit(str(Ipn*0.7))
        self.ipk51NLineEdit = QLineEdit(str(Ipn*0.11))
        self.dialNLineEdit = QLineEdit(str(0.1))
        self.curveNLineEdit = QLineEdit("NI")

        self.formLayout.addRow(self.tr("&Nome:"), self.nameLineEdit)  
        self.formLayoutPhase.addRow(self.tr("&Ipk50:"), self.ipk50LineEdit)
        self.formLayoutPhase.addRow(self.tr("&Ipk51:"), self.ipk51LineEdit)
        self.formLayoutPhase.addRow(self.tr("&Dial:"), self.dialLineEdit)
        self.formLayoutPhase.addRow(self.tr("&Curva:"), self.curveLineEdit)
        #self.formLayoutNeutral.addRow(self.tr("&Nome:"), self.nameLineEdit) 
        self.formLayoutNeutral.addRow(self.tr("&Ipk50N:"), self.ipk50NLineEdit)
        self.formLayoutNeutral.addRow(self.tr("&Ipk51N:"), self.ipk51NLineEdit)
        self.formLayoutNeutral.addRow(self.tr("&Dial(N):"), self.dialNLineEdit)
        self.formLayoutNeutral.addRow(self.tr("&Curva(N):"), self.curveNLineEdit)

        self.confirmButton = QPushButton("Confirmar")
        self.buttonsLayout.addWidget(self.confirmButton)
        self.cancelButton = QPushButton("Cancelar")
        self.buttonsLayout.addWidget(self.cancelButton)
        self.layout.addWidget(self.buttonsWidget)

        self.setLayout(self.layout)

        self.cancelButton.released.connect(self.cancel)
        self.confirmButton.released.connect(self.confirm)

        self.exec()

    def organizeEdit(self):
        self.flag = True

        self.layout = QVBoxLayout()
       
        self.formWidget = QWidget()
        self.formLayout = QFormLayout(self.formWidget)
        self.layout.addWidget(self.formWidget)
        self.tabWidget=QTabWidget()
        self.layout.addWidget(self.tabWidget)
        self.formWidgetPhase = QWidget()
        self.formLayoutPhase = QFormLayout(self.formWidgetPhase)
        self.formWidgetNeutral = QWidget()
        self.formLayoutNeutral = QFormLayout(self.formWidgetNeutral)
        self.tabWidget.addTab(self.formWidgetPhase,"Fase")
        self.tabWidget.addTab(self.formWidgetNeutral,"Neutro")
        self.buttonsWidget = QWidget()
        self.buttonsLayout = QHBoxLayout(self.buttonsWidget)

        '''
        self.layout = QVBoxLayout()
        self.formWidget = QWidget()
        self.formLayout = QFormLayout(self.formWidget)
        self.layout.addWidget(self.formWidget)
        self.buttonsWidget = QWidget()
        self.buttonsLayout = QHBoxLayout(self.buttonsWidget)
        '''

        self.nameLabel = QLabel(self.ied.name)
        self.ipk50LineEdit = QLineEdit(str(self.ied.activeGroup.ipk50))
        self.ipk51LineEdit = QLineEdit(str(self.ied.activeGroup.ipk51))
        self.dialLineEdit = QLineEdit(str(self.ied.activeGroup.dialP))
        self.curveLineEdit = QLineEdit(str(self.ied.activeGroup.curveP))
        self.ipk50NLineEdit = QLineEdit(str(self.ied.activeGroup.ipk50N))
        self.ipk51NLineEdit = QLineEdit(str(self.ied.activeGroup.ipk51N))
        self.dialNLineEdit = QLineEdit(str(self.ied.activeGroup.dialN))
        self.curveNLineEdit = QLineEdit(str(self.ied.activeGroup.curveN))

        self.formLayout.addRow(self.tr("&Nome:"), self.nameLabel)  
        self.formLayoutPhase.addRow(self.tr("&Ipk50:"), self.ipk50LineEdit)
        self.formLayoutPhase.addRow(self.tr("&Ipk51:"), self.ipk51LineEdit)
        self.formLayoutPhase.addRow(self.tr("&Dial:"), self.dialLineEdit)
        self.formLayoutPhase.addRow(self.tr("&Curva:"), self.curveLineEdit)
        #self.formLayoutNeutral.addRow(self.tr("&Nome:"), self.nameLineEdit) 
        self.formLayoutNeutral.addRow(self.tr("&Ipk50N:"), self.ipk50NLineEdit)
        self.formLayoutNeutral.addRow(self.tr("&Ipk51N:"), self.ipk51NLineEdit)
        self.formLayoutNeutral.addRow(self.tr("&Dial(N):"), self.dialNLineEdit)
        self.formLayoutNeutral.addRow(self.tr("&Curva(N):"), self.curveNLineEdit)

        '''
        self.formLayout.addRow(self.tr("&Nome:"), self.nameLabel)  
        self.formLayout.addRow(self.tr("&Ipk50:"), self.ipk50LineEdit)
        self.formLayout.addRow(self.tr("&Ipk51:"), self.ipk51LineEdit)
        self.formLayout.addRow(self.tr("&Dial:"), self.dialLineEdit)
        self.formLayout.addRow(self.tr("&Curva:"), self.curveLineEdit)
        self.formLayout.addRow(self.tr("&Ipk50N:"), self.ipk50NLineEdit)
        self.formLayout.addRow(self.tr("&Ipk51N:"), self.ipk51NLineEdit)
        self.formLayout.addRow(self.tr("&Dial(N):"), self.dialNLineEdit)
        self.formLayout.addRow(self.tr("&Curva(N):"), self.curveNLineEdit)
        '''

        self.editButton = QPushButton("Editar")
        self.buttonsLayout.addWidget(self.editButton)
        self.cancelButton = QPushButton("Cancelar")
        self.buttonsLayout.addWidget(self.cancelButton)
        self.layout.addWidget(self.buttonsWidget)

        self.setLayout(self.layout)

        self.cancelButton.released.connect(self.cancel)
        self.editButton.released.connect(self.edit)

        self.exec()

    def confirm(self):
        Ipk50 = int(float(self.ipk50LineEdit.text()))
        Ipk50N = int(float(self.ipk50NLineEdit.text()))
        tcs = [CT("TCA",1.3*Ipk50,5),CT("TCB",1.3*Ipk50,5),CT("TCC",1.3*Ipk50,5),CT("TCN",1.3*Ipk50N,5)]
        adjust = AdjustGroup(int(float(self.ipk50LineEdit.text())),int(float(self.ipk51LineEdit.text())),
                            str(self.curveLineEdit.text()),float(self.dialLineEdit.text()),
                            int(float(self.ipk50NLineEdit.text())),int(float(self.ipk51NLineEdit.text())),
                            str(self.curveNLineEdit.text()),float(self.dialNLineEdit.text()))
        self.ied=IED(str(self.nameLineEdit.text()),1,dict(),tcs,adjust)
        self.flag = True
        self.close()

    def edit(self):
        adjust = AdjustGroup(int(float(self.ipk50LineEdit.text())),int(float(self.ipk51LineEdit.text())),
                            str(self.curveLineEdit.text()),float(self.dialLineEdit.text()),
                            int(float(self.ipk50NLineEdit.text())),int(float(self.ipk51NLineEdit.text())),
                            str(self.curveNLineEdit.text()),float(self.dialNLineEdit.text()))
        self.ied.activeGroup = adjust
        self.flag = True
        self.close()

    def cancel(self):
        self.close()


class newSwitchWindow(QDialog):
    def __init__(self,switchLevel):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.switchLevel = switchLevel

        self.formWidget = QWidget()
        self.formLayout = QFormLayout(self.formWidget)
        self.layout().addWidget(self.formWidget)
        self.nameLineEdit = QLineEdit('S'+str(6+len(self.switchLevel.window.powerGrid.ieds)))
        self.formLayout.addRow(self.tr("&Nome:"), self.nameLineEdit) 

        self.iedButton = QPushButton("Criar IED")
        self.switchButton = QPushButton("Criar Chave-Fusível")
        self.layout().addWidget(self.switchButton)
        self.layout().addWidget(self.iedButton)
        self.iedButton.released.connect(self.Switch_is_ied)
        self.switchButton.released.connect(self.Switch_is_fuseSwitch)

        self.exec()

    def Switch_is_ied(self):
        self.close()
        self.switchLevel.createIED()

    def Switch_is_fuseSwitch(self):
        '''
        Ipk50 = int(float(self.ipk50LineEdit.text()))
        Ipk50N = int(float(self.ipk50NLineEdit.text()))
        tcs = [CT("TCA",1.3*Ipk50,5),CT("TCB",1.3*Ipk50,5),CT("TCC",1.3*Ipk50,5),CT("TCN",1.3*Ipk50N,5)]
        adjust = AdjustGroup(int(float(self.ipk50LineEdit.text())),int(float(self.ipk51LineEdit.text())),
                            str(self.curveLineEdit.text()),float(self.dialLineEdit.text()),
                            int(float(self.ipk50NLineEdit.text())),int(float(self.ipk51NLineEdit.text())),
                            str(self.curveNLineEdit.text()),float(self.dialNLineEdit.text()))
        self.ied=IED(str(self.nameLineEdit.text()),1,dict(),tcs,adjust)
        self.flag = True
        '''
        #name = ("S"+str(len(self.switchLevel.window.powerGrid.ieds)))
        name = str(self.nameLineEdit.text())
        #print(name)
        link = FuseLink("K",15)
        fuseSwitch = FuseSwitch(name,link)


        self.switchLevel.layout.addWidget(IEDLine(fuseSwitch,self.switchLevel.window,self.switchLevel.main))
        self.close()




