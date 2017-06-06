import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon

m = Basemap(llcrnrlon=-125, llcrnrlat=18, urcrnrlon=-64, urcrnrlat=49, projection='lcc',lat_1=33, lat_2=45, lon_0=-95)

shp_info = m.readshapefile('st99_d00', 'states', drawbounds=True)

popdensity = {
'New Jersey':  438.00,
'Rhode Island':   387.35,
'Massachusetts':   312.68,
'Connecticut':    271.40,
'Maryland':   209.23,
'New York':    155.18,
'Delaware':    154.87,
'Florida':     114.43,
'Ohio':  107.05,
'Pennsylvania':  105.80,
'Illinois':    86.27,
'California':  83.85,
'Hawaii':  72.83,
'Virginia':    69.03,
'Michigan':    67.55,
'Indiana':    65.46,
'North Carolina':  63.80,
'Georgia':     54.59,
'Tennessee':   53.29,
'New Hampshire':   53.20,
'South Carolina':  51.45,
'Louisiana':   39.61,
'Kentucky':   39.28,
'Wisconsin':  38.13,
'Washington':  34.20,
'Alabama':     33.84,
'Missouri':    31.36,
'Texas':   30.75,
'West Virginia':   29.00,
'Vermont':     25.41,
'Minnesota':  23.86,
'Mississippi':   23.42,
'Iowa':  20.22,
'Arkansas':    19.82,
'Oklahoma':    19.40,
'Arizona':     17.43,
'Colorado':    16.01,
'Maine':  15.95,
'Oregon':  13.76,
'Kansas':  12.69,
'Utah':  10.50,
'Nebraska':    8.60,
'Nevada':  7.03,
'Idaho':   6.04,
'New Mexico':  5.79,
'South Dakota':  3.84,
'North Dakota':  3.59,
'Montana':     2.39,
'Wyoming':      1.96,
'Alaska':     0.42}

colors={}
statenames=[]
cmap = plt.cm.hot
vmin = 0; vmax = 450
for shapedict in m.states_info:
	statename = shapedict['NAME']
	if statename not in ['District of Columbia', 'Puerto Rico']:
		pop = popdensity[statename]
		colors[statename] = cmap(1.-np.sqrt((pop-vmin)/(vmax-vmin)))[:3]
#	statenames.append(statename)

ax=plt.gca()
for i, shapedict in enumerate(m.states_info):
	if shapedict['NAME'] not in ['District of Columbia', 'Puerto Rico']:
		seg = m.states[int(shapedict['SHAPENUM']) - 1]
		color = rgb2hex(colors[shapedict['NAME']])
		if shapedict['NAME'] == 'Hawaii' and float(shapedict['AREA']) > 0.005:
			seg = list(map(lambda (x,y): (x + 5100000, y - 1400000), seg))
		elif shapedict['NAME'] == 'Alaska':
			seg = list(map(lambda (x,y): (0.35*x + 1100000, 0.35*y - 1300000), seg))
		poly = Polygon(seg, facecolor=color, edgecolor='black', linewidth =0.5)
		ax.add_patch(poly)
plt.title('Filling State Polygons by Population Density')
plt.savefig('fig.png')
plt.show()