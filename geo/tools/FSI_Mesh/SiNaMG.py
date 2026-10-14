#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
--------------------------------------
Simple Nastran Mesh Generator (SiNaMG)

Generates simplified mesh files for Beam
and Plate elements

Python module Dependencies:
`sys`
`copy`
`commentjson`
`numpy`

--------------------------------------
'''
# Import system libraries
import sys

# Import software libraries
import lib.common as com
import lib.mesh_1D as m1D
import lib.mesh_2D as m2D

label_1d = ['--beam','-b','-1d']
label_2d = ['--plate','-p','-2d']

try:
    arg = sys.argv[1]
except:
    print('ERROR: Missing Mesh type parameter')
    print('       Please type an option to choose the operation:')
    print('       1D options:   {0}'.format(label_1d))
    print('       2D options:   {0}'.format(label_2d))
    quit()

if (arg in label_1d):
    m1D.start()
    m1D.input()
    m1D.create_grid(0)
    m1D.connectivity(0)
    m1D.mat_prop(1)
    m1D.ele_prop(1,0)
    m1D.ele_BC()
    m1D.ele_Force()
    m1D.end()
    
elif (arg in label_2d):
    m2D.start()
    m2D.input()
    m2D.create_grid(0)
    m2D.connectivity(0)
    m2D.ele_BC(1)
    m2D.end()

else:
    print('ERROR: Wrong Mesh type parameter "{0}"'.format(arg))
    print('       Please type an option to choose the operation:')
    print('       1D options:   {0}'.format(label_1d))
    print('       2D options:   {0}'.format(label_2d))
    quit()

