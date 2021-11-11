#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import geopandas as gpd 
import folium 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
from statsmodels.formula.api import ols
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


#CSVs inladen
df_prv = pd.read_csv('data_prv.csv')
df_gem = pd.read_csv('data_gem.csv')

#Landsgrenzen inladen
provincies= gpd.read_file('bestuurlijkegrenzen.gpkg', layer= 'provincies')
gemeente = gpd.read_file('bestuurlijkegrenzen.gpkg', layer= 'gemeenten')


# In[3]:


st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.sidebar.subheader('Gemaakt Door:')
st.sidebar.write('• Robin Pelders')
st.sidebar.write('• Maarten Meeuwes')
st.sidebar.write('• Mark Yonan')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('')
st.sidebar.write('Hulpbronnen:')
st.sidebar.write('https://opendata.cbs.nl/statline/portal.html?_la=nl&_catalog=CBS&tableId=85068NED&_theme=299')
st.sidebar.write('https://opendata.cbs.nl/statline/portal.html?_la=nl&_catalog=CBS&tableId=83648NED&_theme=407')
st.sidebar.write('https://www.politie.nl/algemeen/open-data.html')


# ## Politie

# In[4]:


#Politiebureaus
st.subheader("Aantal politiebureau's per provincie en gemeente")

m = folium.Map(location=[52.0893191, 5.1101691], zoom_start= 7, tiles='cartodbpositron')

folium.Choropleth(
    geo_data= provincies,
    name= 'provincies',
    data= df_prv,
    columns=['provincienaam', 'politiebureaus'],
    key_on='feature.properties.provincienaam',
    fill_color= 'PuBuGn',
    fill_opacity= 0.5,
    line_opacity= 0.8,
    legend_name= 'Aantal politiebureaus(20km)'
).add_to(m)

folium.Choropleth(
    geo_data= gemeente,
    name= 'gemeentes',
    data= df_gem,
    columns=['gemeentenaam', 'politiebureaus'],
    key_on='feature.properties.gemeentenaam',
    fill_color= 'YlOrRd',
    fill_opacity= 0.5,
    line_opacity= 0.8,
    legend_name= 'Aantal politiebureaus(20km)'
).add_to(m)

folium.LayerControl().add_to(m)

folium_static(m)
''
''
''
''


# ## Inkomen provincie

# In[5]:


#Inkomen provincies
st.subheader("Gemiddeld vermogen per provincie")

m1 = folium.Map(location=[52.0893191, 5.1101691], zoom_start= 7, tiles='cartodbpositron', prefer_canvas=True)

folium.Choropleth(
    geo_data=provincies,
    name='geometry',
    data=df_prv,
    columns=['provincienaam', 'Gemiddeld vermogen (1000 euro)'],
    key_on='feature.properties.provincienaam',
    fill_color='Set1',
    fill_opacity=0.5,
    line_opacity=0.8, 
    bins=9,
    legend_name= 'Gemiddel vermogen (x1000 euro)').add_to(m1)

folium_static(m1)
''
''
''
''


# ## Inkomen gemeente

# In[6]:


#Inkomen gemeentes
st.subheader("Gemiddeld vermogen per gemeente")

m2 = folium.Map(location=[52.0893191, 5.1101691], zoom_start= 7, tiles='cartodbpositron', prefer_canvas=True)

folium.Choropleth(
    geo_data= gemeente,
    name='geometry',
    data= df_gem,
    columns=['gemeentenaam', 'Gemiddeld vermogen (1000 euro)'],
    key_on='feature.properties.gemeentenaam',
    fill_color='Set1',
    fill_opacity=0.5,
    line_opacity=0.8,
    bins= 9,
    legend_name='Gemiddel vermogen (x1000 euro)').add_to(m2)

folium_static(m2)
''
''
''
''


# ## Boxplots 

# In[7]:


#Boxplots creeren en opmaken
st.subheader('Boxplots percentage soorten misdrijven per gemeente')

data = pd.read_csv('boxplots.csv')

fig = px.box(data, x="SoortMisdrijf", 
             y="GeregistreerdeMisdrijvenRelatief_2", 
             color= 'SoortMisdrijf', 
             hover_data=['RegioS'])
fig.update_layout(title_text= 'Box Plot Percentage Misdrijven in Gemeenten',
                  yaxis_title= 'Percentage over totaal aantal misdrijven',
                 xaxis_title= 'Soort Misdrijf')

st.plotly_chart(fig)
''
''
''
''


# ## Barplots

# In[8]:


st.subheader('Barplots totaal geregistreerde misdrijven')

data_final = pd.read_csv('barplots.csv')
data = pd.read_csv('barplot_nl.csv')

#Per provincie aparte dataset creeren
data_gr = data_final[data_final['RegioS'].str.contains("Groningen")].reset_index()
data_fr = data_final[data_final['RegioS'].str.contains("Fryslân")].reset_index()
data_dr = data_final[data_final['RegioS'].str.contains("Dren")].reset_index()
data_ov = data_final[data_final['RegioS'].str.contains("Over")].reset_index()
data_fl = data_final[data_final['RegioS'].str.contains("Flevo")].reset_index()
data_nh = data_final[data_final['RegioS'].str.contains("Noord-Holland")].reset_index()
data_gl = data_final[data_final['RegioS'].str.contains("Gelderland")].reset_index()
data_ut = data_final[data_final['RegioS'].str.contains("Utrecht")].reset_index()
data_zh = data_final[data_final['RegioS'].str.contains("Zuid-Holland")].reset_index()
data_ze = data_final[data_final['RegioS'].str.contains("Zeeland")].reset_index()
data_li = data_final[data_final['RegioS'].str.contains("Limburg")].reset_index()
data_nb = data_final[data_final['RegioS'].str.contains("Brabant")].reset_index()

#Dropdown buttons maken 
dropdown_buttons = [
{'method': 'update', 'label': 'Alle misdrijven','args': [{'visible': [True, True, True, True, True, True, True, True, True, True, True, True, True, True]}]},
{'method': 'update', 'label': 'Bedrog','args': [{'visible': [True, False, False, False, False, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': 'Brandstichting / ontploffing','args': [{'visible': [False, True, False, False, False, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': 'Diefstal/verduistering en inbraak','args': [{'visible': [False, False, True, False, False, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': 'Drugsmisdrijven','args': [{'visible': [False, False, False, True, False, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': 'Gewelds- en seksuele misdrijven','args': [{'visible': [False, False, False, False, True, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': 'Misdrijven WvSr','args': [{'visible': [False, False, False, False, False, True, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': 'Misdrijven overige wetten','args': [{'visible': [False, False, False, False, False, False, True, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': 'Openbaar gezag misdrijf','args': [{'visible': [False, False, False, False, False, False, False, True, False, False, False, False, False, False]}]},
{'method': 'update', 'label': 'Openbare orde misdrijf','args': [{'visible': [False, False, False, False, False, False, False, False, True, False, False, False, False, False]}]},
{'method': 'update', 'label': 'Valsheidsmisdrijven','args': [{'visible': [False, False, False, False, False, False, False, False, False, True, False, False, False, False]}]},
{'method': 'update', 'label': 'Verkeersmisdrijven','args': [{'visible': [False, False, False, False, False, False, False, False, False, False, True, False, False, False]}]},
{'method': 'update', 'label': 'Vermogensmisdrijven','args': [{'visible': [False, False, False, False, False, False, False, False, False, False, False, True, False, False]}]},
{'method': 'update', 'label': 'Vernieling en beschadiging','args': [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, True, False]}]},
{'method': 'update', 'label': 'Vuurwapenmisdrijven','args': [{'visible': [False, False, False, False, False, False, False, False, False, False, False, False, False, True]}]}]

#Colorscale opstellen
colors = ['red', 'orange', 'dimgray', 'lawngreen', 'turquoise', 'lightsalmon', 'darkgoldenrod', 'gray', 'yellow', 'olivedrab', 'maroon', 'magenta', 'dodgerblue', 'peru', 'darkorange']

#Nederland op basis van misdrijven.csv
#Dataset specifiek voor heel Nederland maken
data_nl = data[data['RegioS'] == "Nederland"]
indexNames = data_nl[data_nl['SoortMisdrijf'] == 'Misdrijven, totaal'].index
data_nl.drop(indexNames , inplace=True)
data_nl_final = data_nl.groupby(['SoortMisdrijf','RegioS', 'Perioden']).sum().reset_index()


# In[9]:


dropdown = st.selectbox('Selecteer een regio', ('Nederland', 'Groningen', 'Friesland', 'Drenthe', 'Overijssel', 'Flevoland', 
                                                'Noord-Holland', 'Gelderland', 'Utrecht', 'Zuid-Holland', 'Zeeland', 
                                                'Limburg', 'Noord-Brabant'))

if dropdown == 'Nederland':
    #Nederland
    fig = px.bar(data_nl_final, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence= colors)
    fig.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig.update_layout(legend_title_text='Soort Misdrijf')
    fig.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig.update_layout(xaxis_title="Jaartallen")
    fig.update_layout(title={'text': "Nederland", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig.update_xaxes(type='category')
    st.plotly_chart(fig)

if dropdown == 'Groningen':
    #Groningen
    fig1 = px.bar(data_gr, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig1.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig1.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig1.update_layout(legend_title_text='Soort Misdrijf')
    fig1.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig1.update_layout(xaxis_title="Jaartallen")
    fig1.update_layout(title={'text': "Groningen", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig1.update_xaxes(type='category')
    st.plotly_chart(fig1)

if dropdown == 'Friesland':
    #Friesland
    fig2 = px.bar(data_fr, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig2.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig2.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig2.update_layout(legend_title_text='Soort Misdrijf')
    fig2.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig2.update_layout(xaxis_title="Jaartallen")
    fig2.update_layout(title={'text': "Friesland", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig2.update_xaxes(type='category')
    st.plotly_chart(fig2)

if dropdown == 'Drenthe':
    #Drenthe
    fig3 = px.bar(data_dr, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig3.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig3.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig3.update_layout(legend_title_text='Soort Misdrijf')
    fig3.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig3.update_layout(xaxis_title="Jaartallen")
    fig3.update_layout(title={'text': "Drenthe", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig3.update_xaxes(type='category')
    st.plotly_chart(fig3)

if dropdown == 'Overijssel':
    #Overijssel
    fig4 = px.bar(data_ov, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig4.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig4.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig4.update_layout(legend_title_text='Soort Misdrijf')
    fig4.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig4.update_layout(xaxis_title="Jaartallen")
    fig4.update_layout(title={'text': "Overijssel", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig4.update_xaxes(type='category')
    st.plotly_chart(fig4)

if dropdown == 'Flevoland':
    #Flevoland
    fig5 = px.bar(data_fl, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig5.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig5.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig5.update_layout(legend_title_text='Soort Misdrijf')
    fig5.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig5.update_layout(xaxis_title="Jaartallen")
    fig5.update_layout(title={'text': "Flevoland", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig5.update_xaxes(type='category')
    st.plotly_chart(fig5)

if dropdown == 'Noord-Holland':
    #Noord-Holland
    fig6 = px.bar(data_nh, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig6.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig6.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig6.update_layout(legend_title_text='Soort Misdrijf')
    fig6.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig6.update_layout(xaxis_title="Jaartallen")
    fig6.update_layout(title={'text': "Noord-Holland", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig6.update_xaxes(type='category')
    st.plotly_chart(fig6)

if dropdown == 'Gelderland':
    #Gelderland
    fig7 = px.bar(data_gl, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig7.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig7.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig7.update_layout(legend_title_text='Soort Misdrijf')
    fig7.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig7.update_layout(xaxis_title="Jaartallen")
    fig7.update_layout(title={'text': "Gelderland", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig7.update_xaxes(type='category')
    st.plotly_chart(fig7)

if dropdown == 'Utrecht':
    #Utrecht
    fig8 = px.bar(data_ut, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig8.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig8.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig8.update_layout(legend_title_text='Soort Misdrijf')
    fig8.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig8.update_layout(xaxis_title="Jaartallen")
    fig8.update_layout(title={'text': "Utrecht", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig8.update_xaxes(type='category')
    st.plotly_chart(fig8)

if dropdown == 'Zuid-Holland':
    #Zuid-Holland
    fig9 = px.bar(data_zh, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig9.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig9.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig9.update_layout(legend_title_text='Soort Misdrijf')
    fig9.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig9.update_layout(xaxis_title="Jaartallen")
    fig9.update_layout(title={'text': "Zuid-Holland", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig9.update_xaxes(type='category')
    st.plotly_chart(fig9)

if dropdown == 'Zeeland':
    #Zeeland
    fig10 = px.bar(data_ze, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig10.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig10.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig10.update_layout(legend_title_text='Soort Misdrijf')
    fig10.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig10.update_layout(xaxis_title="Jaartallen")
    fig10.update_layout(title={'text': "Zeeland", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig10.update_xaxes(type='category')
    st.plotly_chart(fig10)

if dropdown == 'Limburg':
    #Limburg
    fig11 = px.bar(data_li, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig11.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig11.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig11.update_layout(legend_title_text='Soort Misdrijf')
    fig11.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig11.update_layout(xaxis_title="Jaartallen")
    fig11.update_layout(title={'text': "Limburg", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig11.update_xaxes(type='category')
    st.plotly_chart(fig11)

if dropdown == 'Noord-Brabant':
    #Brabant
    fig12 = px.bar(data_nb, x="Perioden", y="TotaalGeregistreerdeMisdrijven_1", color="SoortMisdrijf", color_discrete_sequence = colors)
    fig12.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
    fig12.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1, xanchor = 'left',
    y = 1.1, yanchor = 'top',)])
    fig12.update_layout(legend_title_text='Soort Misdrijf')
    fig12.update_layout(yaxis_title="Totaal aantal misdrijven")
    fig12.update_layout(xaxis_title="Jaartallen")
    fig12.update_layout(title={'text': "Noord-Brabant", 'xanchor': 'center', 'x': 0.5, 'y': 0.98, 'yanchor': 'top',})
    fig12.update_xaxes(type='category')
    st.plotly_chart(fig12)


# ## Voorspelmodel

# In[10]:


st.subheader('Voorspellen aantal geregistreerde misdrijven')

data_nl = pd.read_csv('voorspelmodel.csv')

mdl_tijd_vs_aantal = ols("GeregistreerdeMisdrijvenPer1000Inw_3 ~ Perioden ", data=data_nl).fit()
explanatory_data = pd.DataFrame({"Perioden": np.arange(2010, 2029, 1)})
pred_tijd_aantal = explanatory_data.assign(Misdrijven=mdl_tijd_vs_aantal.predict(explanatory_data))

fig13 = px.box(data_nl, x="Perioden", y="GeregistreerdeMisdrijvenPer1000Inw_3",
                 title='Voorspelmodel Jaren t.o.v. Misdrijven per 1000 inwoners', hover_data=['RegioS'])
fig13.update_layout(coloraxis_showscale=False, 
                  legend=dict(
                      yanchor="top",
                      y=0.99,
                      xanchor="right",
                      x=0.99),
                  title={'y':0.85,
                         'x':0.5,
                         'xanchor': 'center',
                         'yanchor': 'top'})
fig13.add_trace(go.Scatter(x=pred_tijd_aantal["Perioden"], y=pred_tijd_aantal["Misdrijven"], marker=dict(
            color='darkblue')))
fig13.update_layout(yaxis_title= 'Misdrijven per 1000 inwoners', xaxis_title= 'Jaren')
fig13.update_traces(name='Voorspellingslijn o.b.v. Linear Regression Modeling')
fig13.update_xaxes(type='category')
st.plotly_chart(fig13)


# In[16]:


img = Image.open("summary.png")
st.image(img, width=650)
''
''
''
''


# ## Matrix

# In[12]:


#Correlaties aanmaken
corrGem = df_gem.corr()
corrProv = df_prv.corr()


# In[13]:


st.subheader('Correlatie matrix gemeente')
#Correlatie matrix gemeente
sns.heatmap(corrGem, annot=True)
st.pyplot()


# In[14]:


st.subheader('Correlatie matrix provincie')
#Correlatie matrix provincies
sns.heatmap(corrProv, annot=True)
st.pyplot()

