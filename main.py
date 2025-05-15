




import requests
import pandas as pd 
import io
import plotly.express as px

from utils import get_all, get_by_cantons, get_by_agegroup, get_by_sex

# r.status_code
# r.headers['content-type']
# r.encoding

# full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/COVID19_wastewater_sequencing/csv'
# full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/INFLUENZA_sentinella/csv'


full_query_string = 'https://api.idd.bag.admin.ch/api/v1/data/version'
r = requests.get(full_query_string, allow_redirects=True)
data_version = r.json()


full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/files'
r = requests.get(full_query_string, allow_redirects=True)
data_file_list = r.json()

data_di = {}
for li_index in range(len(data_file_list)):
    print(li_index)
    data_set_name = data_file_list[li_index]
    full_query_string = 'https://api.idd.bag.admin.ch/api/v1/export/latest/' + data_set_name + '/csv'
    r = requests.get(full_query_string, allow_redirects=True)
    raw_text = r.text
    df = pd.read_csv(io.StringIO(raw_text, newline='\n')  , sep=",")
    data_di[data_set_name] = df


[data_di[a].shape for a in data_di.keys()]



# df = data_di['INFLUENZA_sentinella']




# ----------------------------

df = data_di['INFLUENZA_oblig']

df.shape
df.head()
df.columns



df['value'].value_counts()
df['georegion'].value_counts()
df['georegion_type'].value_counts()
df['agegroup'].value_counts()
df['agegroup_type'].value_counts()
df['sex'].value_counts()
df['type'].value_counts()
df['dataComplete'].value_counts()
df['valueCategory'].value_counts()


df['agegroup'] = pd.Categorical(df['agegroup']).rename_categories({
    'all'      : 'All',   
    '0 - 4'    : '00-04' , 
    '5 - 14'   : '05-14' ,       
    '15 - 29'  : '15-29',      
    '30 - 64'  : '30-64',      
    '65+'      : '65+',     
    'unknown'  : 'Unknown',       
    })









# make a continuous time variable 
df['date'] = df["temporal"].apply(pd.Timestamp.fromisoformat)


df_all = get_all(df)
df_can = get_by_cantons(df)
df_age = get_by_agegroup(df)
df_sex = get_by_sex(df)
df_all.shape
df_can.shape
df_age.shape
df_sex.shape



plotcol_seq02 = ['#ffbb00', '#0077ff', '#33ff00', '#00ffff', '#ff00ff', '#ffff66', '#ff0000']

fig_all = px.line(
    data_frame = df_all, 
    color = 'georegion', 
    x = 'date', y = 'incValue', markers=True, template="plotly_dark", color_discrete_sequence = plotcol_seq02,)

fig_can = px.line(
    data_frame = df_can, 
    color = 'georegion', 
    x = 'date', y = 'incValue', markers=True, template="plotly_dark", color_discrete_sequence = plotcol_seq02,)

fig_age = px.line(
    data_frame = df_age, 
    color = 'agegroup', 
    x = 'date', y = 'incValue', markers=True, template="plotly_dark", color_discrete_sequence = plotcol_seq02,)

fig_sex = px.line(
    data_frame = df_sex, 
    color = 'sex', 
    x = 'date', y = 'incValue', markers=True, template="plotly_dark", color_discrete_sequence = plotcol_seq02,)



fig_all.show()
fig_can.show()
fig_age.show()
fig_sex.show()


start_date = "2019-09-26"
end_date = "2019-10-18"

_ = fig_sex.update_xaxes(type="date", range=[start_date, end_date])
fig_sex.show()





# df_sel["temporal"].apply(pd.Timestamp.fromisoformat)
# import datetime
# pd.to_datetime(df_sel["temporal"], format='%Y-W%U')
# datetime.date.fromisoformat('2025-W16')
# pd.Timestamp.fromisoformat('2025-W16')





# df_all['grouping_type'] = 'all'
# df_can['grouping_type'] = 'can'
# df_age['grouping_type'] = 'age'
# df_sex['grouping_type'] = 'sex'
# df_all = df_all.rename(columns={"georegion": "plot_group"})
# df_can = df_can.rename(columns={"georegion": "plot_group"})
# df_age = df_age.rename(columns={"agegroup": "plot_group"})
# df_sex = df_sex.rename(columns={"sex": "plot_group"})
# df_for_plot = pd.concat([df_all, df_can, df_age, df_sex])





# df_sel["date"]
# df_sel["value"]
# df_sel["pop"]
# df_sel["incValue"]
# df_sel["prct"]