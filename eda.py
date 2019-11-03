# -*- coding: utf-8 -*-
"""EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/maxrgnt/pythdc2-project2/blob/master/EDA2.ipynb
"""

# Commented out IPython magic to ensure Python compatibility.
# Panel Data
import pandas as pd
# System folders
import os
from pathlib import Path
# Visualization
import plotly.graph_objs as go
import seaborn as sns
# %matplotlib inline

url = 'https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/unemployment.csv'
bls = pd.read_csv(url)
print(bls.shape)
bls.sample(1)

url = 'https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/pctChangeGDP.csv'
bea = pd.read_csv(url)
print(bea.shape)
bea.sample(1)

# read in the data
url='https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/borderCrossing.csv'
bts = pd.read_csv(url)
print(bts.shape)
bts.sample(1)

def checkPctChange(df):
  print(df[(df['Abrv']=='TX') & (df['Year']==2014)])
  print(df[(df['Abrv']=='TX') & (df['Year']==2015)])
  print(df[(df['Abrv']=='TX') & (df['Year']==2016)])

def calcPctChange(df, col, pctChange_id):
  for y in list(df['Year'].unique()):
    states = list(df['Abrv'].unique())
    for s in states:
      if y != df['Year'].min():
        t0 = df.loc[(df['Year'] == y-1) & (df['Abrv'] == s), col].tolist()[0]
        t1 = df.loc[(df['Year'] == y) & (df['Abrv'] == s), col].tolist()[0]
        df.loc[(df['Year']==y) & (df['Abrv']==s), pctChange_id+'_pctChange'] = ((t1/t0)-1)*100
      else:
        df.loc[(df['Year']==y) & (df['Abrv']==s), pctChange_id+'_pctChange'] = 'N/A'
  # set drop index for first year where pctChange not calculated
  dropIndex = df.loc[df[pctChange_id+'_pctChange']=='N/A'].index
  df.drop(dropIndex, inplace=True)

bts2 = bts.groupby(['Year','Abrv'])[['Value']].sum().reset_index()
bts2.sample(1)

calcPctChange(bts2, 'Value', 'border')
checkPctChange(bts2)

bea.rename(columns={'Value':'gdp_pctChange'},inplace = True)
checkPctChange(bea)

calcPctChange(bls, 'UnemploymentRate', 'unemp')
checkPctChange(bls)

df = df[df['Abrv']=='TX']
df = bls[['Year','Abrv','unemp_pctChange']].merge(bea[['Year','Abrv','gdp_pctChange']], how = 'left', left_on=['Year','Abrv'], right_on=['Year','Abrv'],sort=True)
df = df.merge(bts2[['Year','Abrv','border_pctChange']], how = 'left', left_on=['Year','Abrv'], right_on=['Year','Abrv'],sort=True)
df['Year'] = df['Year'].astype(float)
df['border_pctChange'] = df['border_pctChange'].astype(float)
df['gdp_pctChange'] = df['gdp_pctChange'].astype(float)
df['unemp_pctChange'] = df['unemp_pctChange'].astype(float)
df_melt = df.melt(['Year','Abrv'], var_name='cols', value_name='vals')
df_melt.sample(3)

sns.set(rc={'figure.figsize':(18,6)})
sns.lineplot(x = 'Year', y = 'vals', hue = 'cols', ci=None, data = df_melt);
sns.pairplot(df, vars=['border_pctChange','gdp_pctChange','unemp_pctChange'], kind='reg');

# mapbox_access_token = open("assets/mytoken.mapbox_token").read()

# fig = go.Figure(go.Scattermapbox(
#     lat=df['Latitude'],
#     lon=df['Longitude'],
#     mode='markers',
#     marker=go.scattermapbox.Marker(
#         size=20,
#         colorscale='Purples',
#         color=df['Value']
#     ),
#     text=df['Value']

# ))
# fig.update_layout(
#     autosize=True,
#     hovermode='closest',
#     mapbox=go.layout.Mapbox(
#         accesstoken=mapbox_access_token,
#         bearing=0,
#         center=go.layout.mapbox.Center(
#             lat=39.8283,
#             lon=-98.5795
#         ),
#         pitch=0,
#         zoom=3
#     ),
# )
# fig

# fig = go.Figure(data=go.Choropleth(
#     locations=df2['StateAbrv'], # Spatial coordinates
#     z = df2['Value'].astype(float), # Data to be color-coded
#     locationmode = 'USA-states', # set of locations match entries in `locations`
#     colorscale = 'Purples',
#     colorbar_title = "Pedestrians",
# ))

# fig.update_layout(
#     title_text = 'Migration',
#     geo_scope='usa', # limite map scope to USA
# )

# fig.show()

