import streamlit as st
import pandas as pd
from bokeh.plotting import figure

st.title("Exploratory Dashboard (Titanic)")

################
# Load Data
################

def get_embark_location(row):
	columns = ['embarked_from_cherbourg', 
				'embarked_from_queenstown', 
				'embarked_from_southampton']
	for column in columns:
		if row[column]:
		    return column.split('_')[-1]
	return "unknown"

df = pd.read_csv('titanic.csv')
df['gender'] = df['male'].map({0: 'Male', 1: 'Female'})
df['embarked_from'] = df.apply(get_embark_location, axis=1)

df = df.drop(columns=['male', 
                      'age_was_missing',
                      'embarked_from_cherbourg', 
                      'embarked_from_queenstown', 
                      'embarked_from_southampton'])

embarked_from_values = list(df['embarked_from'].unique())
dropdown_embarked_froms = st.sidebar.multiselect("Embarked From",
													embarked_from_values)

#########################
# Filter [embarked_from]
#########################
if not dropdown_embarked_froms:
	df_view = df
else:
	df_view = df[df['embarked_from'].isin(dropdown_embarked_froms)]

######################
# Display total count
######################
st.markdown(f'## **Number of Records:** {len(df_view)}')

#####################
# Display DataFrame
#####################
df_view

#######################
# Display Scatter Plot
########################
st.markdown('## Scatter Plot by Vega Lite')
st.vega_lite_chart(df_view, 
		spec={
			# 'width': ',
			# 'height': 400,
			'mark': {'type': 'circle', 'tooltip': True},
			'encoding': {
				'x': {'field': 'age', 'type': 'quantitative'},
				'y': {'field': 'fare', 'type': 'quantitative'},
				'color': {'field': 'survived', 'type': 'nominal'},
				"opacity": {"value": 0.5},
				# "fill": {"value": "transparent"}
			}
		},
		use_container_width=True
)

st.markdown('## Scatter Plot by Bokeh')
p = figure(plot_width=400, plot_height=200, 
	       x_axis_label="Age",
           y_axis_label="Fare")

p.circle(df_view.query("survived==0")['age'], 
		 df_view.query("survived==0")['fare'], 
	     color='blue', 
	     alpha=0.5, legend_label='Survived 0')

p.circle(df_view.query("survived==1")['age'], 
		 df_view.query("survived==1")['fare'], 
	     color='orange', 
	     alpha=0.5, legend_label='Survived 1')

st.bokeh_chart(p, use_container_width=True)