#! Python 2.7
# statesmapdf uses pandas dataframes in conjunction with matplotlib
# and basemap to generate infographics.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import matplotlib
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from matplotlib.colors import Normalize

#Remove unwanted territories
def remove_territories(df, terr_list):
	for territory in terr_list:
		df = df[df.states != territory]

#Generate a dataframe from a csv file
def df_from_csv(csv, colNames):
	df = pd.read_csv(csv, header=None)
	df.columns = colNames
	return df

#Create dataframe with all required spatial map data
def generate_US_map_df():
	m = Basemap(llcrnrlon=-125, llcrnrlat=18, urcrnrlon=-64, urcrnrlat=49, projection='lcc',lat_1=33, lat_2=45, lon_0=-95)
	#setting drawbounds=False prevents the map from rendering somehow
	m.readshapefile('st99_d00', 'states', drawbounds=True)
	
	df = pd.DataFrame({
		'states': [states['NAME'] for states in m.states_info],
		'num': [states['SHAPENUM'] for states in m.states_info],
		'coords': [m.states[int(states['SHAPENUM']) - 1] for states in m.states_info],
		'area': [states['AREA'] for states in m.states_info]
	})
	#Remove unwanted territories
	df = df[df.states != 'Puerto Rico']
	df = df[df.states != 'District of Columbia']
	#Shrink and translate Hawaii and Alaska
	for i, state in enumerate(df.states):
		#Leave out islands with small land area
		if state == 'Hawaii' and float(df.get_value(i, 'area')) > 0.005:
			df.set_value(i, 'coords', list(map(lambda (x,y): (x + 5100000, y - 1400000), df.at[i, 'coords'])))
		elif state == 'Alaska':
			df.set_value(i, 'coords', list(map(lambda (x,y): (0.35*x + 1100000, 0.35*y - 1300000), df.at[i, 'coords'])))
	#Create and append a column of polygons to the dataframe
	polygons = []
	for row in df['coords']:
		polygons.append(Polygon(np.array(row), True))
	df_polygons = pd.DataFrame({
		#Add a 'num' column to make sure the rows get merged properly
		'num': df['num'],
		'shapes': polygons
		})
	df = df.merge(df_polygons, on='num', how='right')
	return df


ax = plt.gca()
df_map = generate_US_map_df()

df_pop = df_from_csv('State Population Data.csv', ['states', 'Population'])
df_pop = df_pop.merge(df_map, on='states', how='right')

cmap = plt.get_cmap('Greens')

#zorder changes how things are layered
pc = PatchCollection(df_pop.shapes, zorder=2)
norm = Normalize()
pc.set_edgecolor('k')
pc.set_facecolor(cmap(norm(df_pop['Population'].fillna(0).values)))
ax.add_collection(pc)

mapper = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
mapper.set_array(df_pop['Population'])
plt.colorbar(mapper, shrink=0.65)

plt.show()