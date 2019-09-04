# -*- coding: utf-8 -*- 

import os
import time
import sys

try:    
	import prody
	from prody import *
except ImportError:
	print ("ProDy module is required for processing pdb files!")
	quit()

if __name__ == '__main__':

	argnum = len(sys.argv)-1

	print ('\n------------------------------------------------------------------')
	print ('Pdb2xyzr.py version 1.1 by Sergio Decherchi --- Updated for python3')
	print ('--------------------------------------------------------------------')
	if (argnum==0):
		print ("This script converts a given pdb to a xyzr file according to an atom selection\nand to a given force field")
		print ('\nUsage: pdb2xyzr.py pdbCode "selection string" force_field\n\n')
		print ("--\tpdbCode is the code of the pdb entry in the database.\n\tIf the pdb file is not found in current directory it will be downloaded from pdb repository\n")
		print ('--\t"selection string" is a VMD style atom selections string.\n\tDefault value is "protein"\n')
		print ("--\tforce_field is the DelPhi format force field file name to be applied to set the radii.\n\tDefault value is amber.siz")
		print ("\n")
		quit()
		
	pdbName = sys.argv[1]
	selection = 'protein'
	FFfileName = 'amber.siz'
	
	if (argnum==2):
		selection = sys.argv[2]
	if (argnum==3):
		selection = sys.argv[2]
		FFfileName = sys.argv[3]
	
	#prody.setVerbosity('none')
	print ('<<INFO>> Getting pdb..')
	sys.stdout.flush()
	pdbSys = prody.parsePDB(('%s'%pdbName))
	print ('<<INFO>> Applying selection: "%s"'%selection)
	pdbSys = pdbSys.select(selection)
	
	if (pdbSys==None):
		print ("<<ERROR>> Wrong selection string")
		quit()
	prody.writePDB(('selection_%s.pdb'%pdbName),pdbSys.select(selection))
	pdbSys = prody.parsePDB(('selection_%s.pdb'%pdbName))
	
	if (os.path.exists(FFfileName)==False):
		print ('<<ERROR>> File %s does not exist'%FFfileName)
		quit()
		
	# load force field parameters
	fileFF = open(FFfileName,'r')
	
		
	defaultRadii = {}
	specificRadii = {}
	lineNum = 0
	while 1:
		line = fileFF.readline()
		lineNum = lineNum+1
			
		# stop reading
		if not line:
			break
			
		# skip empty lines
		if (len(line)<=1):
				continue
			
		# skip comment line
		if '!' in line:	
			continue
			
		if (line.startswith('atom__res_radius_')):
			print ('<<INFO>> Recognized DelPhi header for radii .siz file')
			continue
		
		listStr = line.split()
		if (len(listStr)==2):
			defaultRadii[listStr[0][0]]=float(listStr[1])
		elif (len(listStr)==3):
			specificRadii['%s_%s'%(listStr[0],listStr[1])]=float(listStr[2])
		else:
			print ('<<ERROR>> Unrecognized record in radii file at line %d, please check file and reload'%lineNum)
			quit()
			
	f = open(('%s.xyzr'%pdbName),'w')
	
	X = pdbSys.getCoords()
		
	print ('<<INFO>> Converting PDB using %s'%FFfileName)
	for i in range(len(pdbSys)):
		resName = pdbSys[i].getResname()
		atomName = pdbSys[i].getName()
		key = '%s_%s'%(atomName,resName)
		if not(key in specificRadii):
			if not(atomName[0] in defaultRadii):
				print ('<<INFO>> %s %s missing in radii set applying 1.0 Angstrom'%(atomName,resName))
				radius = 1.0
			else:
				radius = defaultRadii[atomName[0]]
		else:
			radius = specificRadii[key]
		
		f.write(('%f %f %f %f\n'%(X[i][0],X[i][1],X[i][2],radius)))
	f.close()
	
	print ('<<INFO>> File converted in %s.xyzr'%(pdbName))
