Lab Scenario
COVID-19 is a virus that belongs to a family of viruses known as coronaviruses. COVID-19 virus can infect both human beings and animals. The two primary symptoms of COVID-19 include dry cough and fever. The secondary components can be nasal congestion, fatigue and ache. On 11th March 2020, World Health Organisation (WHO) declares COVID-19 as a pandemic disease. 
In this lab, you will learn how to analyse the spread of COVID-19 virus across different states /Union Territories in India using different Python visualisation libraries. 
Lab Environment
In order to carry out this lab, you will require the various Python visualisation libraries such as Matplotlib, PrettyTable, Requests,BeautifulSoup, GeoPandas, Seaborn and Pandas installed in your Anaconda environment. To install GeoPandas you need to first install Fiona library and Descartes libraries. 
Lab Tasks
The following steps should be followed to perform data analysis:

# Import libraries.
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import geopandas as gpd
from prettytable import PrettyTable
print('Pandas version:', pd.__version__)
print('Seaborn version:', sns.__version__)
print('Matplotlib version:', matplotlib.__version__)
print('Requests version:', requests.__version__)

print('GeoPandas:', gpd.__version__)

# Importing HTTPs data.
web_content = requests.get('https://www.mohfw.gov.in/').content
soup = BeautifulSoup(web_content, "html.parser")
extract_contents = lambda row: [x.text.replace('\n', '') for x in row]
stats = [] 
all_rows = soup.find_all('tr')
for row in all_rows:
    stat = extract_contents(row.find_all('td')) 
    if len(stat) == 5: 
        stats.append(stat)
new_cols = ["Sr.No", "States/UT","Confirmed Cases","Recovered Cases","Deceased Cases"]
state_data = pd.DataFrame(data = stats, columns = new_cols)
state_data.head(31)  
# Converting string datatype into int datatype. 
state_data['Confirmed Cases'] = state_data['Confirmed Cases'].map(int)
state_data['Recovered Cases'] = state_data['Recovered Cases'].map(int)
state_data['Deceased Cases']  = state_data['Deceased Cases'].map(int)
# Displaying data using PrettyTable. 
table = PrettyTable()
table.field_names = (new_cols)
for i in stats:
    table.add_row(i)
table.add_row(["","Total", 
               sum(state_data['Confirmed Cases']), 
               sum(state_data['Recovered Cases']), 
               sum(state_data['Deceased Cases'])])
print(table)
# Analysing State/UT wise COVID-19 cases.
sns.set_style("ticks")
plt.figure(figsize = (15,10))
plt.barh(state_data["States/UT"], state_data["Confirmed Cases"].map(int),
         align = 'center', color = 'darkblue', edgecolor = 'Black')
plt.xlabel('Total Number of Confirmed Cases', fontsize = 18)
plt.ylabel('States/UT', fontsize = 18)
plt.gca().invert_yaxis() 
plt.xticks(fontsize = 12) 
plt.yticks(fontsize = 12)
plt.title('COVID-19 Data Analysis', fontsize = 20)

for index, value in enumerate(state_data["Confirmed Cases"]):
    plt.text(value, index, str(value), fontsize = 12, verticalalignment = 'center')
plt.show()
# Displaying nationwide cases.
group_size = [sum(state_data['Confirmed Cases']), 
              sum(state_data['Recovered Cases']), 
              sum(state_data['Deceased Cases'])]

group_labels = ['Confirmed Cases\n' + str(sum(state_data['Confirmed Cases'])), 
                'Recovered Cases\n' + str(sum(state_data['Recovered Cases'])), 
                'Deceased Cases\n'  + str(sum(state_data['Deceased Cases']))]
custom_colors = ['orange','green','red']

plt.figure(figsize = (8, 8))
plt.pie(group_size, labels = group_labels, colors = custom_colors)
central_circle = plt.Circle((0,0), 0.5, color = 'white')
fig = plt.gcf()
fig.gca().add_artist(central_circle)
plt.rc('font', size = 18) 
plt.title('Nationwide total Confirmed, Recovered and Deceased Cases', fontsize = 20)
plt.show()


# Representing different State/UT geometry loaction GeoDataFrame.
map_data = gpd.read_file('Indian_States.shp')
map_data.rename(columns = {'st_nm':'States/UT'}, inplace = True)
merged_data.head(32)
# Modify State/UT names in the GeoDataFrame.
map_data['States/UT'] = map_data['States/UT'].str.replace('&', 'and')
map_data['States/UT'].replace('Arunanchal Pradesh', 'Arunachal Pradesh', inplace = True)
map_data['States/UT'].replace('Telangana', 'Telengana', inplace = True)
map_data['States/UT'].replace('NCT of Delhi', 'Delhi', inplace = True)
# Display State wise data using India Map.
fig, ax = plt.subplots(1, figsize=(20, 12))
ax.axis('off')
ax.set_title('Covid-19 Statewise Data — Confirmed Cases', 
             fontdict =  {'fontsize': '25', 'fontweight' : '3'})
merged_data.plot(column = 'Confirmed Cases', cmap='YlOrRd', 
                 linewidth=0.8, ax=ax, edgecolor='0.8', 
                 legend = True)
plt.show()

