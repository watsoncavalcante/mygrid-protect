from protectCalc import *
from protectGraphics import *
#from MyGrid.cud1 import *
import sys

app = QApplication(sys.argv)
'''
nIED = 3
Ipn=10000
IEDs=[]
for i in range(nIED):
    Ipn+=i*5000
    tcs = [CT("TCA",10*Ipn,5),CT("TCB",10*Ipn,5),CT("TCC",10*Ipn,5),CT("TCN",Ipn,5)]
    adjust = AdjustGroup(4*Ipn,1.5*Ipn,'NI',0.1,0.7*Ipn,0.11*Ipn,'NI',1)
    IEDs.append(IED("IED"+str(i),1,dict(),tcs,adjust))
'''
#IEDs=[]
FuseSwitches=[]
Switches=[]
grid_data = grid_elements
Grid = PowerGrid(grid_data,Switches)
window = MainWindow(Grid)
app.exec_()