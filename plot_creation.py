from operator import itemgetter

def conversion_unit(x):
    return {
        'Time'            : 38759428183.8,
        'Initial_Gas_Mass': 1.84793e16,
        'Initial_BH_Mass' : 1.84793e16,
        'Final_Gas_Mass'  : 1.84793e16,
        'Final_BH_Mass'   : 1.84793e16,
        'Gasmass'         : 1.84793e16,
        'dMacc'           : 1.84793e16,
        'DMask'           : 1.84793e16,
        'dx'              : 50000.0,
        'dy'              : 50000.0,
        'dz'              : 50000.0,
        'dvx'             : 50000.0,
        'dvy'             : 50000.0,
        'dvz'             : 50000.0,
        'rho'             : 148.6344
    }.get(x, 1)


def format_axis(rows, field):
	axis = []
	
	length = max(rows, key=lambda x:x[field])
	length = str(length[field])
	length = length[::-1].find('.')
	length = '.' + str(length + 2)

	for row in rows:
	    row[field] = format(row[field], '.19')

	rows = sorted(rows,key=lambda x: x[field])

	multiplier = conversion_unit(field)

	for row in rows:
		axis.append(float(row[field]) * multiplier)

	return axis
'''
Mass:                       multiply by 1.84793e16      (new unit Solar Mass)
Distance/Length/Position:   multiply by 50000.0         (new unit kiloparsec)
Time:                       multiply by 38759428183.8   (new unit years)
Velocity:                   multiply by 1260            (new unit km/s)
Density:                    multiply by 148.6344         
Distance:                   multiply by 50000.0

the rest:
Temperature:  leave it how it is
afac:         leave it
any iord:     leave it
metals:       leave it
h2frac:       leave it
u:            I am not actually sure.  leave it for now, we probably won't use it.
mass:         1.84793e16 # (new unit Solar Mass)
'''


