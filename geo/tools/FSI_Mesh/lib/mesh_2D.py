#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
--------------------------------------
SiNaMG 2D elememt Library

Global Variables:
`user_param`
`ele_id`

Basic Routines:
`start`
`end`
`input`
`input_check`
`create_grid`
`connectivity`
`reset_ele_id`
`ele_data`
`ele_prop`
`ele_BC`

--------------------------------------
'''
# Import system libraries
import numpy as np
import commentjson
import copy

# Import software libraries
import lib.common as com

# Global variables
user_param = { # Default values
    'Filename':'Nastran.bdf',
    'Mesh':{
        'Point': [
            np.array([0.0,0.0,0.0]),
            np.array([1.0,0.0,0.0]),
            np.array([1.0,1.0,0.0]),
            np.array([0.0,1.0,0.0])
        ],
        'Side': [
            {
                'N_ele':0,
                'Length':0.0,
                'Delta':0.0
            },{
                'N_ele':0,
                'Length':0.0,
                'Delta':0.0
            },{
                'N_ele':0,
                'Length':0.0,
                'Delta':0.0
            },{
                'N_ele':0,
                'Length':0.0,
                'Delta':0.0
            } 
        ]
        
    },
    'Boundary_Condition':{
        'Side_1':False,
        'Side_2':True,
        'Side_3':False,
        'Side_4':True
    }
}
ele_id = 1

#::::::::::::::::::::::::::::::::::::::::::::::::::
def start():
    print("------------------------------------")
    print("SiNaMG - Plate Mesh Generator")
    print("------------------------------------")

#::::::::::::::::::::::::::::::::::::::::::::::::::
def end():
    
    com.out_file.write( com.nfoot() )
    com.out_file.close()
    print('Output file writen to: "{0:s}"'.format(user_param['Filename']))
    print("------------------------------------")
    print("Finished")
    print("------------------------------------")

#::::::::::::::::::::::::::::::::::::::::::::::::::
def input():
    global user_param
    print('Reading input file ...')
    
    with open('Plate_input.jsonc') as jsonc_file:
        json_input = commentjson.load(jsonc_file)
        
    input_check(json_input)
    
    mesh = json_input['Mesh']
    for P in mesh['Point']:
        P = np.asarray(P)
    mesh['Point'] = np.asarray(mesh['Point'])
    
    mesh['Side'].extend(copy.deepcopy(mesh['Side'][:]))
    
    user_param.update(json_input)
    
    #Calculations:
    mesh = user_param['Mesh']
    
    i = [0,1,2,3,0]
    cont = 0
    for S in mesh['Side']:
        p1 = i[cont]
        p2 = i[cont+1]
        S['Length'] = np.linalg.norm( mesh['Point'][p2]-mesh['Point'][p1] )
        S['Delta'] = float(S['Length'])/float(S['N_ele'])
        cont+=1
    
    #Open file
    com.out_file = open(user_param['Filename'],"w")
    
    com.out_file.write( com.nheader() )

#::::::::::::::::::::::::::::::::::::::::::::::::::

def input_check(json_input):
    print('Checking input ...')
    
    #To-do

#::::::::::::::::::::::::::::::::::::::::::::::::::
def create_grid(fam):
    print('Writing grid points...')
    
    grid = {}
    grid['family'] = fam
    com.out_file.write( com.grid_header(grid) )
    
    mesh = user_param['Mesh']
    
    up_side2 = com.norm_vec(mesh['Point'][2]-mesh['Point'][1])
    up_side4 = com.norm_vec(mesh['Point'][3]-mesh['Point'][0])
    
    for j in range(0,mesh['Side'][1]['N_ele']+1):
        p1 = mesh['Point'][0]+float(j)*( up_side4*mesh['Side'][3]['Delta'] )
        p2 = mesh['Point'][1]+float(j)*( up_side2*mesh['Side'][1]['Delta'] )
        for i in range(0,mesh['Side'][0]['N_ele']+1):
            direction = com.norm_vec( p2-p1 )
            delta = np.linalg.norm( p2-p1 )/float(mesh['Side'][0]['N_ele'])
            
            grid['point'] = p1+float(i)*( direction*delta )
            com.out_file.write( com.grid_data(grid) )
            
#::::::::::::::::::::::::::::::::::::::::::::::::::
def connectivity(fam):
    print('Writing connectivity...')
    
    mesh = user_param['Mesh']
    
    l = com.nline( com.txt_field(com.ncomment())+'Plate element data for family    '+com.nas_int(fam) )
    com.out_file.write( l )
    node=1
    for j in range(0,mesh['Side'][1]['N_ele']):
        for i in range(0,mesh['Side'][0]['N_ele']):
            com.out_file.write( ele_data(node,fam,mesh['Side'][0]['N_ele']+1) )
            node+=1
        node+=1

#::::::::::::::::::::::::::::::::::::::::::::::::::
def reset_ele_id():
    global ele_id
    ele_id = 1
    
#::::::::::::::::::::::::::::::::::::::::::::::::::
def ele_data(node,f,nx):
    global ele_id
    
    label = com.txt_field('CQUAD4')
    blank = com.num_field('0')
    eid = com.num_field(com.nas_int(ele_id))
    fam = com.num_field(com.nas_int(f))
    n1 = com.num_field(com.nas_int(node))
    n2 = com.num_field(com.nas_int(node+1))
    n3 = com.num_field(com.nas_int(node+nx+1))
    n4 = com.num_field(com.nas_int(node+nx))

    s = com.nline( label +eid +fam +n1 +n2 +n3 +n4 )
    ele_id += 1
    return s

#::::::::::::::::::::::::::::::::::::::::::::::::::
def ele_BC(fam):
    
    d1 = user_param['Mesh']['Side'][0]['N_ele']
    d2 = user_param['Mesh']['Side'][1]['N_ele']
    
    bc = user_param['Boundary_Condition']
    if (bc['Side_1']):
        for c in range(1,d1+1):
            n1 = c
            n2 = n1+1
            com.out_file.write( BC_data(n1,n2,fam) )
    if (bc['Side_2']):
        for c in range(0,d2):
            n1 = (d1+1)*(c+1)
            n2 = (d1+1)*(c+2)
            com.out_file.write( BC_data(n1,n2,fam) )
    if (bc['Side_3']):
        for c in range(1,d1+1):
            n1 = (d1+1)*(d2) + c
            n2 = n1+1
            com.out_file.write( BC_data(n1,n2,fam) )
    if (bc['Side_4']):
        for c in range(0,d2):
            n1 = 1 + c*(d1+1)
            n2 = 1 + (c+1)*(d1+1)
            com.out_file.write( BC_data(n1,n2,fam) )

#::::::::::::::::::::::::::::::::::::::::::::::::::
def BC_data(n1,n2,f):
    global ele_id
    
    label = com.txt_field('CBAR')
    blank = com.num_field('0')
    eid = com.num_field(com.nas_int(ele_id))
    fam = com.num_field(com.nas_int(f))
    n1 = com.num_field(com.nas_int(n1))
    n2 = com.num_field(com.nas_int(n2))

    s = com.nline( label +eid +fam +n1 +n2 )
    ele_id += 1
    return s
    
#::::::::::::::::::::::::::::::::::::::::::::::::::

#::::::::::::::::::::::::::::::::::::::::::::::::::