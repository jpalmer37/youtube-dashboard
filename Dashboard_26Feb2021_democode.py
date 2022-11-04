#!/usr/bin/env python
# coding: utf-8

# import plotly
# import dash
# 
# import pickle
# 
# import pandas as pd
# import folium
# 
# import seaborn as sns
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# from matplotlib.widgets import Slider
# 
# import pgeocode
# 
# import datetime as dt

# In[25]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import datetime as dt
import pgeocode
import folium
import isoweek
from numpy import random ## for demo purposes only


# In[26]:


raw_data= pd.read_csv('COVID_VOC_SAMP_forDashboard_19FEB2021.csv')


# In[27]:


#(raw_data['LOGIN_DATE'][0])

month_dict=dict([
    ('Jan','01'),
    ('Feb','02'),
    ('Mar','03'),
    ('Apr','04'),
    ('May','05'),
    ('Jun','06'),
    ('Jul','07'),
    ('Aug','08'),
    ('Sep','09'),
    ('Oct','10'),
    ('Nov','11'),
    ('Dec','12')])

def convert_string_to_dt(string):
    date_str = string[0:2]
    month_str = string[3:6]
    year_str = string[7:9]
    year_str = '20' + year_str
    time_str = '00:00:00.00'
    month = month_dict[month_str]
    string_2 = year_str + '-' + month + '-' + date_str + ' ' + time_str
    datetime_obj = dt.datetime.strptime(string_2, '%Y-%m-%d %H:%M:%S.%f')
    date = datetime_obj.date()
    return date


# In[28]:


raw_data['LOGIN_DATEOBJ']=raw_data['LOGIN_DATE'].apply(convert_string_to_dt, convert_dtype=True) # convert the date into object


# In[29]:


## following parts  FOR DEMO CODE ONLY.
## SHUFFLE ALL COLUMNS TO CREATE PSEUDO RECORDS -- COMMENT OUT THE NEXT FOR LOOP IN PRODUCTION VERSION

for j in range(0,10):
    for i in raw_data.columns:
        raw_data[i] = random.permutation(raw_data[i].values)


# In[31]:


phu_dict = dict(
    [('ALG','P6B 0A9'),
     ('BRN','N3R 1G7'),
     ('CHK','N7M 5L8'),
     ('TOR','M5B 1W2'),
     ('DUR','L1N 6A3'),
     ('ELG','N5P 1G9'),
     ('EOH','K6J 5T1'),
     ('GBO','N4K 0A5'),
     ('HAL','L6M 3L1'),
     ('HAM','L8P 4S6'),
     ('HDN','N3Y 4N5'),
     ('HKP','L1A 3V6'),
     ('HPE','K8P 4P1'),
     ('HUR','N5A 1L4'),
     ('KFL','K7M 1V5'),
     ('LAM','N7T 7Z6'),
     ('LGL','K6V 7A3'),
     ('MSL','N6A 3N7'),
     ('NIA','L2V 0A2'),
     ('NPS','P1B 2T2'),
     ('OTT','K2G 6J8'),
     ('OXF','N5P 1G9'),
     ('PDH','N5A 1L4'),
     ('PEE','L5W 1N4'),
     ('PQP','P4N 8B7'),
     ('PTC','K9J 2R8'),
     ('REN','K8A 6Y7'),
     ('SMD','L4M 6K9'),
     ('SUD','P3E 3A3'),
     ('THB','P7B 6E7'),
     ('TSK','P0J 1P0'),
     ('WAT','N2J 4V3'),
     ('WDG','N1G 0E1'),
     ('WEC','N9A 4J8'),
     ('YRK','L3Y 6Z1'),
     ('UNK','')
    ])

phu_dict_names = dict(
    [('ALG','ALGOMA'),
     ('BRN',''),
     ('CHK',''),
     ('TOR','Toronto'),
     ('DUR','Durham'),
     ('ELG','Elgin'),
     ('EOH','K6J 5T1'),
     ('GBO','N4K 0A5'),
     ('HAL','L6M 3L1'),
     ('HAM','Hamilton'),
     ('HDN','N3Y 4N5'),
     ('HKP','L1A 3V6'),
     ('HPE','K8P 4P1'),
     ('HUR','Huron'),
     ('KFL','K7M 1V5'),
     ('LAM','N7T 7Z6'),
     ('LGL','K6V 7A3'),
     ('MSL','N6A 3N7'),
     ('NIA','L2V 0A2'),
     ('NPS','P1B 2T2'),
     ('OTT','Ottawa'),
     ('OXF','Oxford'),
     ('PDH','N5A 1L4'),
     ('PEE','Mississauga'),
     ('PQP','Porcupine'),
     ('PTC','K9J 2R8'),
     ('REN','Renfrew'),
     ('SMD','L4M 6K9'),
     ('SUD','P3E 3A3'),
     ('THB','P7B 6E7'),
     ('TSK','P0J 1P0'),
     ('WAT','Waterloo'),
     ('WDG','Windsor'),
     ('WEC','N9A 4J8'),
     ('YRK','York'),
     ('UNK','')
    ])


# In[32]:


country = pgeocode.Nominatim('CA')

phu_LatLong_dict={}
for i in phu_dict.keys():
    health_unit = i
    city = phu_dict[i]
    x={}
    if(city == ''):
        lat = ''
        long = ''
        place = 'Unknown'
    else:
        string = city
        try:
            lat = country.query_postal_code(string).latitude
            long = country.query_postal_code(string).longitude
            city = country.query_postal_code(string).county_name
        except:
            lat=''
            long = ''
        x['lat_long'] = (lat,long)
        x['city'] = city
    phu_LatLong_dict[i]=x    


# In[33]:


## clean up the list and remove NaNs
x = raw_data['PCR_RESULT_CLEANED'].unique()
pcr_cleaned_list=[]

for i in x:
    if(type(i) == str):
        pcr_cleaned_list.append(i)


        
x = raw_data['WGS_RESULT_CLEANED'].unique()
wgs_cleaned_list=[]

for i in x:
    if(type(i) == str):
        wgs_cleaned_list.append(i)


# In[34]:


## Age Count Table
age_groups = (range(0,20),range(20,40),range(40,60),range(60,80),range(80,100))
group_categories = {}
group_cat_list =['00-19','20-39','40-59','60-79','80+']

for i in range(0,5):
    group_categories[age_groups[i]] = group_cat_list[i]


# In[35]:


## Create several smaller dataframes for data retrieval

## Total_Count Table
total_count =[]
phu_list = raw_data['PHU'].unique()
dates = raw_data['LOGIN_DATEOBJ'].unique()
weeks = raw_data['WEEK'].unique()

def get_uniq_list(string):
    return_list=[]
    x = raw_data[string].unique()
    for i in x:
        if(type(i) == str):
            return_list.append(i)
    return return_list

field_string = 'PCR_RESULT_CLEANED'
list_pcr = get_uniq_list(field_string)
field_string = 'WGS_RESULT_CLEANED'
list_wgs = get_uniq_list(field_string)
gender=('M','F','O')


# In[36]:


for i in dates:
    x={}
    x['date'] = i
    count = len(raw_data[raw_data['LOGIN_DATEOBJ']== i])
    x['count'] = count
    total_count.append(x)
    
## Create count by date and PHU

def create_dict_structure(list1):
    dict_structure={}
    l = list1
    for i in l:
        dict_structure[i] = {}
        for j in phu_list:
            dict_structure[i][j]={}    
            dict_structure[i][j]['Total']=0
            dict_structure[i][j]['M'] = 0
            dict_structure[i][j]['F'] = 0
            dict_structure[i][j]['O'] = 0
            for pcr in list_pcr:
                pcr = str('pcr' + pcr)
                dict_structure[i][j][pcr] = 0
            for wgs in list_wgs:
                wgs = str('wgs' + wgs)
                dict_structure[i][j][wgs] = 0
            for age in group_cat_list:
                dict_structure[i][j][age] = 0
    return (dict_structure)

def fill_dict_structure(target_dict,flag): 
    # flag = 0 or 1. 0 = aggregation by date; 1 by week
    for i in raw_data.iterrows():
        phu = i[1]['PHU']
        date = i[1]['LOGIN_DATEOBJ']
        gender = i[1]['PATIENT_GENDER']
        pcr = i[1]['PCR_RESULT_CLEANED']
        wgs = i[1]['WGS_RESULT_CLEANED']
        age = i[1]['AGE']
        week = i[1]['WEEK']
        if(flag == 0):
            key1 = date
        elif(flag == 1):
            key1 = week
            
        
        for j in age_groups:
            if age in j:
                age_group = group_categories[j]
        if (gender == 'M'):
            target_dict[key1][phu]['M'] += 1
        elif (gender == 'F'):
            target_dict[key1][phu]['F'] += 1
        else:
            target_dict[key1][phu]['O'] += 1

        target_dict[key1][phu]['Total'] += 1
        if(type(pcr) == str):
            pcr_key = str('pcr' + pcr)
            target_dict[key1][phu][pcr_key] += 1

        if(type(wgs) == str):
            wgs_key = str('wgs' + wgs)
            target_dict[key1][phu][wgs_key] += 1
            
        target_dict[key1][phu][age_group] += 1
    return target_dict

def convert_dict_to_dFList(filled_dict,list_key1,flag): ## flag 0 = days, flag 1 = weeks

    list_for_dF = []

    if (flag == 0):
        key_name='date'
    elif(flag == 1):
        key_name='week'

    for key in list_key1:
        for phu in phu_list:
            x = {}
            x[key_name] = key;
            x['phu'] = phu
            x['total'] = filled_dict[key][phu]['Total']
            for gen in gender:
                x[gen] = filled_dict[key][phu][gen]
            for wgs in list_wgs:
                wgs_key = str('wgs' + wgs)
                x[wgs_key] = filled_dict[key][phu][wgs_key]
            for pcr in list_pcr:
                pcr_key = str('pcr' + pcr)
                x[pcr_key] = filled_dict[key][phu][pcr_key]
            for age in group_cat_list:
                x[age] = filled_dict[key][phu][age]
            list_for_dF.append(x)
    return list_for_dF


# In[37]:


date_phu  = create_dict_structure(dates)
week_phu  = create_dict_structure(weeks)


# In[38]:


date_phu = fill_dict_structure(date_phu,0) # flag 0 indicates the use of date
week_phu = fill_dict_structure(week_phu,1) # flag 1 indicates aggregation by week


# In[39]:


aggregate_data_by_date = convert_dict_to_dFList(date_phu,dates,0)
aggregate_data_by_week = convert_dict_to_dFList(week_phu,weeks,1)


# In[40]:


len(raw_data[raw_data['PCR_RESULT_CLEANED'].isna() == False])


# In[41]:


all_data_reformatted = pd.DataFrame(aggregate_data_by_date)
week_data_reformatted = pd.DataFrame(aggregate_data_by_week)


# In[42]:


def convert_weeks_to_date(string):
    year,week = string.split('-')
    date_conv=isoweek.Week(int(year),int(week)).thursday()
    return date_conv

week_data_reformatted['week_date']=week_data_reformatted['week'].apply(convert_weeks_to_date, convert_dtype=True)


# In[43]:


phu_list=list(phu_list)
phu_list.append('All')


# In[44]:


list_wgs = ('wgsB.1.1.7','wgsB.1.351','wgsP.1','wgsVOC NOT DETECTED','wgsUNABLE TO COMPLETE'); # WGS Cleaned List
list_pcr = ('pcrUNABLE TO COMPLETE','pcrNOT DETECTED','pcrN501Y DECTECTED') # PCR Cleaned List    


# In[45]:


l=['wgsB.1.1.7','wgsVOC NOT DETECTED','wgsUNABLE TO COMPLETE','wgsB.1.351','wgsP.1','total','phu','week_date']
week_data_wgs_limited = week_data_reformatted[l]


# In[46]:


dfList=[]
def calculate_proportion(var,total):
    if(total == 0):
        prop = 0
    else:
        prop = var / total
    return prop

for x in week_data_wgs_limited.iterrows():
    y={}
    total = x[1]['total']
    y['week'] = x[1]['week_date']
    y['phu'] = x[1]['phu']
    for i in list_wgs:
        string = 'prop_'+i
        var = int(x[1][i])
        y[string]=calculate_proportion(var,total)
    dfList.append(y)

df = pd.DataFrame(dfList)


# In[48]:


summary_list=[]
y={}
for i in week_data_wgs_limited.iterrows():
    week = i[1]['week_date']
    y[week]={}
    for j in list_wgs:
        y[week][j] = 0

for i in week_data_wgs_limited.iterrows():
    week = i[1]['week_date']
    for j in list_wgs:
        y[week][j] += i[1][j]
    


# In[49]:


lx=[]
for i in y.keys():
    dx={}
    dx['week']=i
    dx['total']=0
    for j in list_wgs:
        dx[j]=y[i][j]
        dx['total']+= dx[j]
    lx.append(dx)


# In[50]:


week_summed_data=pd.DataFrame(lx)


# In[52]:


ls = []
for row in week_summed_data.iterrows():
    dx = {}
    total = row[1]['total']
    dx['total']=total
    dx['week'] = row[1]['week']
    for i in list_wgs:
        string = 'prop_'+i
        var = row[1][i]
        if(total == 0):
            dx[string] = 0
        else:
            dx[string] = 100*var/total
    ls.append(dx)
            
aggregate_weekly_data=pd.DataFrame(ls)


# In[54]:


input_id='All'
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('SARS CoV-2 Variants of Concern (VOC)', style={'font-weight': 'bold','text-align':'center'}),
    html.H3(children=[
        html.Label(['Public Health Unit'], style={'font-weight': 'bold'})]),
    html.Div(
        [dcc.Dropdown
            (
                id="PHU Code",
                options=[
                    {
                        'label': i,
                        'value': i
                    } for i in phu_list],
                value='All')],
        style={'width': '25%','display': 'inline-block'}),
    html.Div(
        dcc.Graph(id='Unique Samples Tested for a VOC'),
    ),
    html.Div(
        dcc.Graph(id='Unique Samples Tested for a VOC by Gender')
    ),
    html.Div(
        dcc.Graph(id='Unique Samples Tested for a VOC by Age Group'),
    ),
    html.Div(
        dcc.Graph(id='Unique Samples Screened for the N501Y Mutation by Results'),
    ),
    html.Div(
        dcc.Graph(id='Unique Samples by Whole Genome Sequence Results'),
    ),
    html.Div(
        dcc.Graph(id = 'Unique Samples by WGS - Weekly Results'),
    )
])

## For the next three app callbacks we need all the data -- checked.

@app.callback(
    dash.dependencies.Output('Unique Samples Tested for a VOC','figure'),
    [dash.dependencies.Input('PHU Code', 'value')])

def update_graph_total(input_id):
    if input_id == 'All':
        reordered_data = all_data_reformatted.copy()
    else:
        reordered_data = all_data_reformatted[all_data_reformatted['phu']== input_id]
    
    trace_total_count= go.Bar(x=reordered_data.date,y=reordered_data['total'],
                              name="No. of Unique Samples")

    return{
        'data' : [trace_total_count],
        'layout': go.Layout(title='Unique Samples Tested for a VOC - [PHU: {}]'.format(input_id),
                            barmode = 'stack',hovermode='closest')
    }


@app.callback(
    dash.dependencies.Output('Unique Samples Tested for a VOC by Gender','figure'),
    [dash.dependencies.Input('PHU Code','value')])

def update_graph_gender(input_id):
    if input_id == 'All':
        reordered_data = all_data_reformatted.copy()
    else:
        reordered_data = all_data_reformatted[all_data_reformatted['phu']==input_id]

    trace_count_men = go.Bar(x = reordered_data.date,y=reordered_data['M'],name="Male")
    trace_count_women = go.Bar(x = reordered_data.date,y=reordered_data['F'],name="Female")
    trace_count_other = go.Bar(x = reordered_data.date,y=reordered_data['O'],name = "Other / Unknown")

    return {
        'data': [trace_count_women,trace_count_men,trace_count_other],
        'layout': go.Layout(title = 'Unique Samples Tested for a VOC by Gender - [PHU: {}]'.format(input_id),
                            barmode='stack',hovermode='closest',
                           legend={'traceorder':'normal'})
        }

@app.callback(
     dash.dependencies.Output('Unique Samples Tested for a VOC by Age Group', 'figure'),
     [dash.dependencies.Input('PHU Code','value')])

def update_graph_age(input_id):
    if input_id == 'All':
        reordered_data = all_data_reformatted.copy()
    else:
        reordered_data = all_data_reformatted[all_data_reformatted['phu']== input_id]
    trace_group1 = go.Bar(x = reordered_data.date,y = reordered_data['00-19'],name = 'Ages: 19 and under')
    trace_group2 = go.Bar(x = reordered_data.date,y = reordered_data['20-39'],name = 'Ages: 20 - 39')
    trace_group3 = go.Bar(x = reordered_data.date,y = reordered_data['40-59'],name = 'Ages: 40 - 59')
    trace_group4 = go.Bar(x = reordered_data.date,y = reordered_data['60-79'],name = 'Ages: 60 - 79')
    trace_group5 = go.Bar(x = reordered_data.date,y = reordered_data['80+'],name = 'Ages: 80 and over')
    
    return {
        'data': [trace_group1,trace_group2,trace_group3,trace_group4,trace_group5],
        'layout': go.Layout(title='Unique Samples Tested for a VOC by Age Group - [PHU: {}]'.format(input_id),
                            barmode='stack',hovermode='closest',
                            legend={'traceorder':'normal'})
    }

@app.callback(
    dash.dependencies.Output('Unique Samples Screened for the N501Y Mutation by Results','figure'),
    [dash.dependencies.Input('PHU Code','value')]
)

def update_graph_PCR(input_id):
    if input_id == 'All':
        reordered_data = all_data_reformatted.copy()
    else:
        reordered_data = all_data_reformatted[all_data_reformatted['phu']== input_id]
    
    #trace_pcrNAN = go.Bar(x = reordered_data.date,y = reordered_data[list_pcr[0]],name = 'Data Not Available')
    trace_pcrUC = go.Bar(x = reordered_data.date, y = reordered_data[list_pcr[0]],name = 'Unable to Complete')
    trace_pcrND = go.Bar(x = reordered_data.date, y = reordered_data[list_pcr[1]],name = 'N501Y Not Detected')
    trace_pcrPos = go.Bar(x = reordered_data.date, y = reordered_data[list_pcr[2]],name = 'N501Y Detected')

    return {
        'data': [trace_pcrUC,trace_pcrND,trace_pcrPos],
        'layout': go.Layout(title='Unique Samples Screened for the N501Y Mutation by Results - [PHU: {}]'.format(input_id),
                            barmode='stack',hovermode='closest')
    }
     
@app.callback(
    dash.dependencies.Output('Unique Samples by Whole Genome Sequence Results','figure'),
    [dash.dependencies.Input('PHU Code','value')]
)
     
def update_graph_WGS(input_id):
    if input_id == 'All':
        reordered_data = all_data_reformatted.copy()
    else:
        reordered_data = all_data_reformatted[all_data_reformatted['phu']== input_id]
    
    #trace_wgsNAN = go.Bar(x = reordered_data.date, y = reordered_data['wgsnan'], name = 'Data Not Available')
    trace_wgsUC = go.Bar(x = reordered_data.date, y = reordered_data['wgsUNABLE TO COMPLETE'], name = 'Unable to Complete')
    trace_noVOC = go.Bar(x = reordered_data.date, y= reordered_data['wgsVOC NOT DETECTED'], name = 'VOC Not Detected')
    trace_wgsB117 = go.Bar(x= reordered_data.date, y = reordered_data['wgsB.1.1.7'], name = 'B.1.1.7' )
    trace_wgsB1351 = go.Bar(x = reordered_data.date, y= reordered_data['wgsB.1.351'], name = 'B.1.351')
    trace_wgsP1 = go.Bar(x = reordered_data.date, y = reordered_data['wgsP.1'], name = 'P.1')
     
    return {
        'data': [trace_wgsUC,trace_noVOC,trace_wgsP1,trace_wgsB1351,trace_wgsB117],
        'layout': go.Layout(title='Unique Samples by Whole Genome Sequence Results - [PHU: {}]'.format(input_id),
                            barmode='stack',hovermode='closest')
    }

     
@app.callback(
    dash.dependencies.Output('Unique Samples by WGS - Weekly Results','figure'),
    [dash.dependencies.Input('PHU Code','value')]
)
     
def update_graph_WGS(input_id):
    reordered_data = aggregate_weekly_data.copy()
    
    #trace_wgsNAN = go.Bar(x = reordered_data.date, y = reordered_data['wgsnan'], name = 'Data Not Available')
    trace_wgsUC_w = go.Bar(x = reordered_data['week'], y = reordered_data['prop_wgsUNABLE TO COMPLETE'], name = 'percent Unable to Complete')
    trace_noVOC_w = go.Bar(x = reordered_data['week'], y= reordered_data['prop_wgsVOC NOT DETECTED'], name = 'percent VOC Not Detected')
    trace_wgsB117_w = go.Bar(x= reordered_data['week'], y = reordered_data['prop_wgsB.1.1.7'], name = 'percent B.1.1.7' )
    trace_wgsB1351_w = go.Bar(x = reordered_data['week'], y= reordered_data['prop_wgsB.1.351'], name = 'percent B.1.351')
    trace_wgsP1_w = go.Bar(x = reordered_data['week'], y = reordered_data['prop_wgsP.1'], name = 'percent P.1')
    
    return {
        'data': [trace_wgsUC_w,trace_noVOC_w,trace_wgsP1_w,trace_wgsB1351_w,trace_wgsB117_w],
        'layout': go.Layout(title='Unique Samples by WGS - Weekly Results',
                            barmode='group',hovermode='closest')
    }


# In[56]:


if __name__ == '__main__':
    app.run_server()


# In[ ]:




