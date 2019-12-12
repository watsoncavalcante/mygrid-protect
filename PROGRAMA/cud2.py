#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import time
from terminaltables import AsciiTable
from mygrid.short_circuit.symmetrical_components import config_objects, calc_equivalent_impedance, calc_short_circuit
from mygrid.power_flow.backward_forward_sweep_3p import calc_power_flow
from mygrid.util import p2r, r2p
from mygrid.util import R, P
from mygrid.grid import Section, LoadNode, TransformerModel, Conductor, Auto_TransformerModel
from mygrid.grid import Substation, Sector, Switch, LineModel
from mygrid.grid import GridElements, ExternalGrid, Generation, Shunt_Capacitor
import sys
#sys.path.append('../')

# Canadian Urban Distribution (CUD) System

# Feeder 1 switches

ch1 = Switch(name='1', state=1)
ch2 = Switch(name='2', state=1)
ch3 = Switch(name='3', state=1)
ch4 = Switch(name='4', state=1)
ch5 = Switch(name='5', state=1)
ch6 = Switch(name='6', state=1)
ch7 = Switch(name='7', state=1)
ch8 = Switch(name='8', state=1)

# Feeder 2 switches

ch9 = Switch(name='9', state=1)
ch10 = Switch(name='10', state=1)
ch11 = Switch(name='11', state=1)
ch12 = Switch(name='12', state=1)
ch13 = Switch(name='13', state=1)
ch14 = Switch(name='14', state=1)
ch15 = Switch(name='15', state=1)
ch16 = Switch(name='16', state=1)

# Substation switch

ch17 = Switch(name='17', state=1)

# GD switches

ch18 = Switch(name='18', state=1)
ch19 = Switch(name='19', state=1)
ch20 = Switch(name='20', state=1)
ch21 = Switch(name='21', state=1)

# NO switch (new)

ch22 = Switch(name='22', state=0)


# Voltages

vll_hv = p2r(115e3, 0.0)
vll_mv = p2r(12.47e3, 0.0)
vll_lv = p2r(0.48e3, 0.0)


# Transformers

t1 = TransformerModel(name="T1",
                      primary_voltage=vll_mv,
                      secondary_voltage=vll_lv,
                      power=5e6,
                      #connection ='nyyn',
                      impedance=0 + 0.0046j)      # ohms (0.1 pu / 12.47 kV)

t2 = TransformerModel(name="T2",
                      primary_voltage=vll_mv,
                      secondary_voltage=vll_lv,
                      power=5e6,
                      #connection ='nyyn',
                      impedance=0 + 0.0046j)      # ohms (0.1 pu / 12.47 kV)

t3 = TransformerModel(name="T3",
                      primary_voltage=vll_mv,
                      secondary_voltage=vll_lv,
                      power=5e6,
                      #connection ='nyyn',
                      impedance=0 + 0.0046j)      # ohms (0.1 pu / 12.47 kV)

t4 = TransformerModel(name="T4",
                      primary_voltage=vll_mv,
                      secondary_voltage=vll_lv,
                      power=5e6,
                      #connection ='nyyn',
                      impedance=0 + 0.0046j)      # ohms (0.1 pu / 12.47 kV)

t5 = TransformerModel(name="T5",
                      primary_voltage=vll_hv,
                      secondary_voltage=vll_mv,
                      power=20e6,
                      #connection ='nyyn',
                      impedance=0 + 0.7775j)      # ohms (0.1 pu / 12.47 kV)


# External grid
Zr = np.eye(3, dtype=complex)*(4.3493+26.0898j) # ohms (S = 500 MVA, X/R = 6, V = 115 kV)

eg1 = ExternalGrid(name='EG1', vll=vll_hv, Z=Zr)


# Generations

Z = np.eye(3, dtype=complex)*(0+0.0154j) # ohms (0.2 pu, 480 V, 3 MVA)

# All dg's rated at 5 MVA

dg1 = Generation(name="DG1",
                   Pa=0.0e6 + 0.0e6j,
                   Pb=0.0e6 + 0.0e6j,
                   Pc=0.0e6 + 0.0e6j,
                   generation_type="PQ",
                   Z=Z)

dg2 = Generation(name="DG2",
                   Pa=0.0e6 + 0.0e6j,
                   Pb=0.0e6 + 0.0e6j,
                   Pc=0.0e6 + 0.0e6j,
                 generation_type="PQ",
                 Z=Z)

dg3 = Generation(name="DG3",
                   Pa=0.0e6 + 0.0e6j,
                   Pb=0.0e6 + 0.0e6j,
                   Pc=0.0e6 + 0.0e6j,
                 generation_type="PQ",
                 Z=Z)

dg4 = Generation(name="DG4",
                   Pa=0.0e6 + 0.0e6j,
                   Pb=0.0e6 + 0.0e6j,
                   Pc=0.0e6 + 0.0e6j,
                 generation_type="PQ",
                 Z=Z)


# # All dg's rated at 3 MVA

# dg1 = Generation(name="DG1",
#                  Pa=9e5 + 4.36e5j,
#                  Pb=9e5 + 4.36e5j,
#                  Pc=9e5 + 4.36e5j,
#                  generation_type="PQ",
#                  Z=Z)

# dg2 = Generation(name="DG2",
#                  Pa=9e5 + 4.36e5j,
#                  Pb=9e5 + 4.36e5j,
#                  Pc=9e5 + 4.36e5j,
#                  generation_type="PQ",
#                  Z=Z)

# dg3 = Generation(name="DG3",
#                  Pa=9e5 + 4.36e5j,
#                  Pb=9e5 + 4.36e5j,
#                  Pc=9e5 + 4.36e5j,
#                  generation_type="PQ",
#                  Z=Z)

# dg4 = Generation(name="DG4",
#                  Pa=9e5 + 4.36e5j,
#                  Pb=9e5 + 4.36e5j,
#                  Pc=9e5 + 4.36e5j,
#                  generation_type="PQ",
#                  Z=Z)


# Load buses

# External grid bus (bus 0)

b0 = LoadNode(name='B0',
              voltage=vll_hv,
              external_grid=eg1)

# Substation bus (bus 1)

b1 = LoadNode(name='B1',
              power=0 + 0j,
              voltage=vll_mv)

# Generations buses

b_dg1 = LoadNode(name='B_DG1',
                 power=0 + 0j,
                 voltage=vll_lv,
                 generation=dg1)

b_dg2 = LoadNode(name='B_DG2',
                 power=0 + 0j,
                 voltage=vll_lv,
                 generation=dg2)

b_dg3 = LoadNode(name='B_DG3',
                 power=0 + 0j,
                 voltage=vll_lv,
                 generation=dg3)

b_dg4 = LoadNode(name='B_DG4',
                 power=0 + 0j,
                 voltage=vll_lv,
                 generation=dg4)

# Feeder 1 - load buses:

b2 = LoadNode(name='B2',
              power=1.8e6 + 8.72e5j,
              voltage=vll_mv)

b3 = LoadNode(name='B3',
              power=1.8e6 + 8.72e5j,
              voltage=vll_mv)

b4 = LoadNode(name='B4',
              power=1.8e6 + 8.72e5j,
              voltage=vll_mv)

b5 = LoadNode(name='B5',
              power=1.8e6 + 8.72e5j,
              voltage=vll_mv)

# Feeder 2 - load buses:

b6 = LoadNode(name='B6',
              power=1.8e6 + 8.72e5j,
              voltage=vll_mv)

b7 = LoadNode(name='B7',
              power=1.8e6 + 8.72e5j,
              voltage=vll_mv)

b8 = LoadNode(name='B8',
              power=1.8e6 + 8.72e5j,
              voltage=vll_mv)

b9 = LoadNode(name='B9',
              power=1.8e6 + 8.72e5j,
              voltage=vll_mv)

# Fault points

f1 = LoadNode(name='F1',
              power=0 + 0j,
              voltage=vll_mv)

f2 = LoadNode(name='F2',
              power=0 + 0j,
              voltage=vll_mv)

f3 = LoadNode(name='F3',
              power=0 + 0j,
              voltage=vll_mv)

f4 = LoadNode(name='F4',
              power=0 + 0j,
              voltage=vll_mv)

f5 = LoadNode(name='F5',
              power=0 + 0j,
              voltage=vll_mv)

f6 = LoadNode(name='F6',
              power=0 + 0j,
              voltage=vll_mv)

f7 = LoadNode(name='F7',
              power=0 + 0j,
              voltage=vll_mv)

f8 = LoadNode(name='F8',
              power=0 + 0j,
              voltage=vll_mv)


# Line models

spacing500 = [0.0 + 29.0j,
              2.5 + 29.0j,
              7.0 + 29.0j,
              4.0 + 25.0j]

phase_conductor = Conductor(id=47)

neutral_cond = Conductor(id=31)

line_model = LineModel(loc=spacing500,
                        conductor=phase_conductor,
                        neutral_conductor=neutral_cond)#,
                        #Transpose=True)


# Sections

# Feeder 1 Sections

b0b1 = Section(name='B0B1',
                n1=b0,
                n2=b1,
                switch=ch17,
                line_model=line_model,
                transformer=t5,
                length=0.5)

b1f1 = Section(name='B1F1',
               n1=b1,
               n2=f1,
               switch=ch1,
               line_model=line_model,
               length=0.5)

f1b2 = Section(name='F1B2',
               n1=f1,
               n2=b2,
               switch=ch2,
               line_model=line_model,
               length=0.5)

b2f2 = Section(name='B2F2',
               n1=b2,
               n2=f2,
               switch=ch3,
               line_model=line_model,
               length=0.5)

f2b3 = Section(name='F2B3',
               n1=f2,
               n2=b3,
               switch=ch4,
               line_model=line_model,
               length=0.5)

b3f3 = Section(name='B3F3',
               n1=b3,
               n2=f3,
               switch=ch5,
               line_model=line_model,
               length=0.5)

f3b4 = Section(name='F3B4',
               n1=f3,
               n2=b4,
               switch=ch6,
               line_model=line_model,
               length=0.5)

b4f4 = Section(name='B4F4',
               n1=b4,
               n2=f4,
               switch=ch7,
               line_model=line_model,
               length=0.5)

f4b5 = Section(name='F4B5',
               n1=f4,
               n2=b5,
               switch=ch8,
               line_model=line_model,
               length=0.5)

f4b5 = Section(name='F4B5',
               n1=f4,
               n2=b5,
               switch=ch8,
               line_model=line_model,
               length=0.5)

# Feeder 2 Sections

b1f5 = Section(name='B1F5',
               n1=b1,
               n2=f5,
               switch=ch9,
               line_model=line_model,
               length=0.5)

f5b6 = Section(name='F5B6',
               n1=f5,
               n2=b6,
               switch=ch10,
               line_model=line_model,
               length=0.5)

b6f6 = Section(name='B6F6',
               n1=b6,
               n2=f6,
               switch=ch11,
               line_model=line_model,
               length=0.5)

f6b7 = Section(name='F6B7',
               n1=f6,
               n2=b7,
               switch=ch12,
               line_model=line_model,
               length=0.5)

b7f7 = Section(name='B7F7',
               n1=b7,
               n2=f7,
               switch=ch13,
               line_model=line_model,
               length=0.5)

f7b8 = Section(name='F7B8',
               n1=f7,
               n2=b8,
               switch=ch14,
               line_model=line_model,
               length=0.5)

b8f8 = Section(name='B8F8',
               n1=b8,
               n2=f8,
               switch=ch15,
               line_model=line_model,
               length=0.5)

f8b9 = Section(name='F8B9',
               n1=f8,
               n2=b9,
               switch=ch16,
               line_model=line_model,
               length=0.5)

# NO section

b9b5 = Section(name='B9B5',
               n1=b9,
               n2=b5,
               switch=ch22,
               line_model=line_model,
               length=0.5)

# Generation sections

b4dg1 = Section(name='B4DG1',
               n1=b4,
               n2=b_dg1,
               switch=ch18,
               line_model=line_model,
               transformer=t1,
               length=0.5)

b5dg2 = Section(name='B5DG2',
                n1=b5,
                n2=b_dg2,
                switch=ch19,
                line_model=line_model,
                transformer=t2,
                length=0.5)

b6dg3 = Section(name='B6DG3',
                n1=b6,
                n2=b_dg3,
                switch=ch20,
                line_model=line_model,
                transformer=t3,
                length=0.5)

b9dg4 = Section(name='B9DG4',
                n1=b9,
                n2=b_dg4,
                switch=ch21,
                line_model=line_model,
                transformer=t4,
                length=0.5)


load_nodes = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,
              b_dg1,b_dg2,b_dg3,b_dg4,
              f1,f2,f3,f4,f5,f6,f7,f8]

sections = [b0b1,b1f1,f1b2,b2f2,f2b3,b3f3,f3b4,b4dg1,b4f4,f4b5,b5dg2,
            b1f5,f5b6,b6dg3,b6f6,f6b7,b7f7,f7b8,b8f8,f8b9,b9dg4,
            b9b5]

switches = [ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8,ch9,ch10,ch11,
            ch12,ch13,ch14,ch15,ch16,ch17,ch18,ch19,ch20,ch21,ch22]

grid_elements = GridElements(name='my_grid_elements')

grid_elements.add_switch(switches)
grid_elements.add_load_node(load_nodes)
grid_elements.add_section(sections)

grid_elements.create_grid()

              

from mygrid.short_circuit.phase_components import biphasic
from mygrid.short_circuit.phase_components import biphasic_to_ground
from mygrid.short_circuit.phase_components import three_phase, mono_phase
from mygrid.short_circuit.phase_components import min_mono_phase
from mygrid.short_circuit.phase_components import three_phase_to_ground

distgrid=grid_elements.dist_grids['F0']

#ah=three_phase(distgrid,'F1', Df = True)

