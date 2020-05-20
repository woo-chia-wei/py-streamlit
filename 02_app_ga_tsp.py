import streamlit as st
import random
import time
import numpy as np
from ga_tsp import *

max_iterations = 200
city_count = 25
population_size = 100
elite_size = 20
mutation_rate = 0.05

st.markdown('## Genetic Algorithm (Travelling Postman Problem)')

##################
# Progress Update
##################
latest_iteration = st.empty()
bar = st.progress(0)

###########################
# Initialize cities
# Initialize GA algorithm
###########################
cityList = [City(x=int(random.gauss(0, 1) * 100), y=int(random.gauss(0, 1) * 100)) for i in range(city_count)]
GA_gen = geneticAlgorithm(population=cityList, 
							popSize=population_size, 
							eliteSize=elite_size, 
							mutationRate=mutation_rate)

#######################
# Create Line plot
#######################
fig, ax = plt.subplots()
line, = ax.plot(np.asarray(list(map(lambda c: c.x, cityList))), 
	            np.asarray(list(map(lambda c: c.y, cityList))),
	            'bo--', alpha=0.5)
ax.set_xticks([])
ax.set_yticks([])
best_distance_text = st.empty()
main_plot = st.pyplot(plt)
global_best_distance = None
global_best_route = None

def init():
	line.set_ydata(list(map(lambda c: c.y, cityList)))

def animate():
	global global_best_distance
	global global_best_route
	##########################
	# Create next population
	##########################
	population = next(GA_gen)
	topRankRoute = rankRoutes(population)[0]
	bestRouteDistance = topRankRoute[1]
	bestRouteIndex = topRankRoute[0]
	bestRoute = population[bestRouteIndex]
	
	####################
	# Update plot
	####################
	currentDistance = 1/bestRouteDistance
	if global_best_distance is None:
		global_best_distance = currentDistance
		global_best_route = bestRoute

	elif global_best_distance > currentDistance:
		global_best_distance = currentDistance
		global_best_route = bestRoute

	best_distance_text.text(f'Global Best Distance: {global_best_distance:.2f} KM')
	ax.set_title(f'Current Iteration Best Distance: {currentDistance:.2f} KM')
	line.set_xdata(list(map(lambda c: c.x, bestRoute)))
	line.set_ydata(list(map(lambda c: c.y, bestRoute)))
	main_plot.pyplot(plt)

#############################
# Iteratively plot GA result
#############################
init()
for i in range(max_iterations):
	latest_iteration.text(f'Iteration {i+1}')
	pct = int(float(100 * (i+1)) / max_iterations)
	bar.progress(pct)
	animate()
	time.sleep(0.1)

###################
# Update last plot
###################
fig, ax = plt.subplots()
ax.plot(np.asarray(list(map(lambda c: c.x, global_best_route))), 
        np.asarray(list(map(lambda c: c.y, global_best_route))),
        'go--', alpha=0.5)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title(f'Global Best Distance: {global_best_distance:.2f} KM')
main_plot.pyplot()