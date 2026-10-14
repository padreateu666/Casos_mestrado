#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
--------------------------------------
SiNaMG 1D elememt Library

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
`ele_data`
`ele_prop`
`mat_prop`
`mat_data`
`reset_ele_id`
`ele_BC`
`BC_data`
`Force_data`
`ele_Force`

--------------------------------------
'''
# Import system libraries
import numpy as np
import commentjson

# Import software libraries
import lib.common as com

# Global variables
user_param = { # Default values
    'Filename':'Nastran.bdf',
    'Mesh':{
        'N_ele':1,
        'Start_Point':np.array([0.0,0.0,0.0]),
        'End_Point':np.array([1.0,0.0,0.0]),
        'BC_nodes':np.array([1,2]),
        'Direction':np.array([0.0,0.0,0.0]),
        'Length':0.0,
        'Delta':0.0
    },
    'Geometry':{
        'Area':1.0,
        'I1':1.0,
        'I2':1.0,
        'I12':0.0,
        'J':1.0,
    },
    'Static_Force':{
        'Weight':{
            'Density': 0.0,
            'Gravity':np.array([0.0,0.0,0.0])
            },
        'Extra': np.array([0.0,0.0,0.0])
    }
}
ele_id = 1

#::::::::::::::::::::::::::::::::::::::::::::::::::
def start():
    print("------------------------------------")
    print("SiNaMG - Beam Mesh Generator")
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
    
    with open('Beam_input.jsonc') as jsonc_file:
        json_input = commentjson.load(jsonc_file)
        
    input_check(json_input)
    
    mesh = json_input['Mesh']
    mesh['Start_Point'] = np.asarray(mesh['Start_Point'])
    mesh['End_Point'] = np.asarray(mesh['End_Point'])
    
    user_param.update(json_input)
    
    #Calculations:
    mesh = user_param['Mesh']
    mesh['Length'] = np.linalg.norm( mesh['End_Point']-mesh['Start_Point'] )
    mesh['Direction'] = com.norm_vec(mesh['End_Point']-mesh['Start_Point'])
    mesh['Delta'] = float(mesh['Length'])/float(mesh['N_ele'])
    
    #Open file
    com.out_file = open(user_param['Filename'],"w")
    
    com.out_file.write( com.nheader() )

#::::::::::::::::::::::::::::::::::::::::::::::::::
def input_check(json_input):
    print('Checking input ...')
    
    mesh = json_input['Mesh']
    if ( np.min(mesh['BC_nodes'])<1 or np.max(mesh['BC_nodes'])>mesh['N_ele']+1 ):
        print( 'ERROR: Boundary condition nodes outside limits {0}:{1}'.format(1,mesh['N_ele']+1) )
        quit()
    
    if 'Static_Force' in json_input:
        force = json_input['Static_Force']
        if 'Weight' in force:
            try:
                force['Weight']['Gravity'] = np.asarray(force['Weight']['Gravity'])
            except:
                print('ERROR: "Gravity" entry not defined in "Weight"')
                quit()
            try:
                aux = force['Weight']['Density']
            except:
                print('ERROR: "Density" entry not defined in "Weight"')
                quit()
                
        else:
            force['Weight'] = user_param['Static_Force']['Weight']
            
        if 'Extra' in force:
            force['Extra'] = np.asarray(force['Extra'])
        else:
            force['Extra'] = user_param['Static_Force']['Extra']

#::::::::::::::::::::::::::::::::::::::::::::::::::
def create_grid(fam):
    print('Writing grid points...')
    
    grid = {}
    grid['family'] = fam
    com.out_file.write( com.grid_header(grid) )
    
    mesh = user_param['Mesh']
    
    grid['point'] = mesh['Start_Point']
    com.out_file.write( com.grid_data(grid) )
    
    for i in range(0,mesh['N_ele']):
        grid['point'] = grid['point'] + mesh['Delta']*mesh['Direction']
        com.out_file.write( com.grid_data(grid) )

#::::::::::::::::::::::::::::::::::::::::::::::::::
def connectivity(fam):
    print('Writing connectivity...')
    
    l = com.nline( com.txt_field(com.ncomment())+'Beam element data for family    '+com.nas_int(fam) )
    com.out_file.write( l )
    for node in range(1,user_param['Mesh']['N_ele']+1):
        com.out_file.write( ele_data(node,fam) )

#::::::::::::::::::::::::::::::::::::::::::::::::::
def ele_data(node,f):
    global ele_id
    
    label = com.txt_field('CBEAM')
    blank = com.num_field('0')
    eid = com.num_field(com.nas_int(ele_id))
    fam = com.num_field(com.nas_int(f))
    n1 = com.num_field(com.nas_int(node))
    n2 = com.num_field(com.nas_int(node+1))

    s = com.nline( label +eid +fam +n1 +n2 )
    ele_id += 1
    return s

#::::::::::::::::::::::::::::::::::::::::::::::::::
def ele_prop(m,f):
    l = ele_geo(m,f)
    com.out_file.write( l )

#::::::::::::::::::::::::::::::::::::::::::::::::::
def ele_geo(m,f):
    com.out_file.write( com.nline(com.ncomment()+'  Beam Property') )
    Mesh_geo = user_param['Geometry']
    
    label = com.txt_field('PBEAM')
    fam = com.num_field(com.nas_int(f))
    mat = com.num_field(com.nas_int(m))
    A = com.num_field(com.nas_float(Mesh_geo['Area']))
    Ix = com.num_field(com.nas_float(Mesh_geo['I1']))
    Iz = com.num_field(com.nas_float(Mesh_geo['I2']))
    Ixz = com.num_field(com.nas_float(Mesh_geo['I12']))
    J = com.num_field(com.nas_float(Mesh_geo['J']))

    s = com.nline( label +fam +mat +A +Ix +Iz +Ixz +J )

    return s

#::::::::::::::::::::::::::::::::::::::::::::::::::
def mat_prop(m):
    l = mat_data(m)
    com.out_file.write( l )

#::::::::::::::::::::::::::::::::::::::::::::::::::
def mat_data(m):
    com.out_file.write( com.nline( com.ncomment()+'  Material Properties') )
    label = com.txt_field('MAT{0:d}'.format(m))
    mat = com.num_field(com.nas_int(m))
    
    #To-do:
    s = com.nline( label +mat ) #+ E, G, ni, rho

    return s

#::::::::::::::::::::::::::::::::::::::::::::::::::
def reset_ele_id():
    global ele_id
    ele_id = 1
    
#::::::::::::::::::::::::::::::::::::::::::::::::::
def ele_BC():
    com.out_file.write( com.nline( com.txt_field(com.ncomment())+'Single point Constraint') )
    
    for n_id in user_param['Mesh']['BC_nodes']:
        com.out_file.write( BC_data(n_id) )
        
#::::::::::::::::::::::::::::::::::::::::::::::::::
def BC_data(n_id):
    label = com.txt_field('SPC1')
    blank = com.num_field('0')
    node = com.num_field(com.nas_int(n_id))
    
    s = com.nline( label +blank +blank +node )
    
    return s
    
#::::::::::::::::::::::::::::::::::::::::::::::::::
def Force_data(n_id,F):
    label = com.txt_field('FORCE')
    blank = com.num_field('0')
    node = com.num_field(com.nas_int(n_id))
    Fx = com.num_field(com.nas_float(F[0]))
    Fy = com.num_field(com.nas_float(F[1]))
    Fz = com.num_field(com.nas_float(F[2]))
    
    s = com.nline( label +blank +node +blank +blank +Fx +Fy +Fz )
    
    return s
    
#::::::::::::::::::::::::::::::::::::::::::::::::::
def ele_Force():
    print('Writing forces ...')
    
    com.out_file.write( com.nline( com.txt_field(com.ncomment())+'Static Force') )
    Mesh = user_param['Mesh']
    Mesh_geo = user_param['Geometry']
    St_F = user_param['Static_Force']
    St_Fw = St_F['Weight']
    
    Fw = St_Fw['Density'] *St_Fw['Gravity'] *Mesh_geo['Area']
    Fe = St_F['Extra']
    Ftot = (Fw + Fe)*Mesh['Delta']
    
    for ele in range(1,Mesh['N_ele']+1):
        n1 = ele
        com.out_file.write( Force_data(n1,Ftot/2.0) )
        n2 = ele+1
        com.out_file.write( Force_data(n2,Ftot/2.0) )
    
#::::::::::::::::::::::::::::::::::::::::::::::::::
