'''*******************************************************
* Copyright 2017                                         *
* Names: Cristian, Rshakib                               *
* Research Proyect                                       *
* Organizer.py 											 *
* Description: This program organize one file with data  *
* and creates other files according to the field         *
*******************************************************'''

dataFile = 'shortversion.BHAccLog'

'''**********************
* Organize data function*
*************************************************
* The function takes one argument called        *
* "line".The line is converted into a string    *
* then it is splitted into a array in which each*
* word is an element.                           *
*********************************************'''

def organize_data(iterator, Files ,line):
	string_line = ''
	for l in line:
		string_line += l

	string_line = string_line.split()
	
	for i in range(0, 25):
		Files[i].write(str (iterator) + '  ' + string_line[i] + '\n')

'''***********
* Open File  *
**************************************************************
* The function creates many files if the files not exist     *
* or open them then assing and returned them in one variable * 
***********************************************************'''

def openFiles():
	properties = [    'BHiord'           ,\
					  'gasiord'          ,\
					  'time'             ,\
					  'Initial_Gas_Mass' ,\
					  'Initial_BH_Mass'  ,\
					  'Final_Gas_Mass'   ,\
					  'Final_BH_Mass'    ,\
					  'gasmass'          ,\
					  'dMacc'            ,\
					  'dMask'            ,\
					  'dx'               ,\
					  'dy'               ,\
					  'dz'               ,\
					  'dvx'              ,\
					  'dvy'              ,\
					  'dvz'              ,\
					  'u'                ,\
					  'bhsoft'           ,\
					  'tcooloff'         ,\
					  'afac'             ,\
					  'rho'              ,\
					  'temp'             ,\
					  'metals'           ,\
					  'h2frac'           ,\
					  'tcool']

	filedata = [ open(properties[i] + '.txt', 'wb') for i in range(len(properties)) ]
	return filedata

# Beggining of the program 
with open(dataFile) as file_object:
	
	# All the ouput files are open at once and manipulated with this variable
	Files = openFiles()
	i  = 0
	# the file is readed line by line instead of all the file at once
	for line in file_object:
		# we pass one line that will be break up add assing to a file 
		organize_data(i ,Files, line)
		i += 1

	# finally we close all the previous files open
	for File in Files:
		File.close()

print 'finish Organizing'