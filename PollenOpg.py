import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime

def pollen_df_from_table(pollen_table):                   # takes the HTML pollen tables as input for a given week, and outputs the formatted dataframe 
    dfs = pd.read_html(str(pollen_table))                 # the HTML pollen table contains itself 2 tables: the one with pollen data with index 0, and the header with index 1
    df = dfs[0].iloc[1:, :].copy()                        # df now stores the pollen data, ignoring the first row containing free text
    df.columns = dfs[1].values.tolist()[0]                # adding the header to df
    df = df.transpose()                                   # transposing to get the species as columns and dates as row
    df.columns = df.iloc[1:2, :].values[0].tolist()          # defining the header as the species name, in Latin and dropping the other languages (to avoid multi-indexing)
    df = df.drop(['Français', 'Latin', 'Deutsch', 'Lëtzebuergesch'])
    df.index.name = 'Date'
    df.index = pd.to_datetime(df.index)                   # making sure the index is in date type
    df = df.astype(float)                                 # making sure the content is in float type
    return df

def weekly_pollen_numbers():
    year = datetime.now().year
    week = datetime.now().strftime("%V")
    
    url = 'http://www.pollen.lu/index.php?qsPage=data&year='+str(year)+'&week='+str(week)+'&qsLanguage=Fra'
    
    week_response = rq.get(url)
    
    soup = BeautifulSoup(week_response.text, 'html.parser')
    html_tables = soup.find_all('table')
    pollen_table = html_tables[5]
    
    df = pollen_df_from_table(pollen_table)
    
    return df

def daily_pollen_numbers():    
    year = datetime.now().year
    week = datetime.now().strftime("%V")
    month = datetime.now().month
    day = datetime.now().day
    
    url = 'http://www.pollen.lu/index.php?qsPage=data&year='+str(year)+'&week='+str(week)+'&qsLanguage=Fra'
    
    week_response = rq.get(url)
    
    soup = BeautifulSoup(week_response.text, 'html.parser')
    html_tables = soup.find_all('table')
    pollen_table = html_tables[5]
    
    df = pollen_df_from_table(pollen_table)
    
    df2 = df['%s/%s/%s' % (year, month, day)]
    
    #Can't assign column names for some reason. 
    #df2.columns = ["Pollen type", "Pollen Number"]    
    
    return df2    

def pollen_numbers_till_now():
    url_list = []
    
    response = rq.get("http://www.pollen.lu/index.php?qsPage=data&year=1992&week=0&qsLanguage=Fra")
    soup = BeautifulSoup(response.text, 'html.parser')
    html_tables = soup.find_all('table')
    pollen_table = html_tables[5]
    #print(pollen_table)
    
    date_start = pollen_table.text.find('Actualisation: ')+15                             
    actualization_date_str = pollen_table.text[date_start:date_start+10]                                                               
    actualization_date = datetime.strptime(actualization_date_str, '%d.%m.%Y')            
    #print(actualization_date)
    
    df = pollen_df_from_table(pollen_table)  
    
    for year in range(1992, actualization_date.year +1):
        url_year = 'http://www.pollen.lu/index.php?qsPage=data&year='+str(year)+'&week=0&qsLanguage=Fra'
        year_response = rq.get(url_year)
        soup2 = BeautifulSoup(year_response.text, 'html.parser')
        html_tables = soup2.find_all('table')
        
        link_table = html_tables[5]
        for option in link_table.find_all('option'):
            link = option['value']
            url_year_week = 'http://www.pollen.lu/'+link
            url_list.append(url_year_week)
           
    url_list.remove('http://www.pollen.lu/index.php?qsPage=data&year=2001&week=&qsLanguage=Fra')        
    url_list.remove('http://www.pollen.lu/index.php?qsPage=data&year=2001&week=&qsLanguage=Fra')        
    url_list.remove('http://www.pollen.lu/index.php?qsPage=data&year=2001&week=&qsLanguage=Fra')        
    url_list.remove('http://www.pollen.lu/index.php?qsPage=data&year=2001&week=&qsLanguage=Fra')        
    #print(url_list)     
        
        
    pollen_dfs = []
    ctn = 0
    
    for url_weekly in url_list:
        ctn += 1
        week_response = rq.get(url_weekly)
        print("response code : %s,  ctn : %s" % (week_response.status_code, ctn))
        soup3 = BeautifulSoup(week_response.text, 'html.parser')
        html_tables = soup3.find_all('table')
        pollen_table = html_tables[5]
        pollen_df = pollen_df_from_table(pollen_table)
        pollen_dfs.append(pollen_df)

        
    pollen_data = pd.concat(pollen_dfs, ignore_index=False)
    
    return pollen_data, actualization_date

def weather_data():
    weather_data = pd.read_csv('https://data.public.lu/en/datasets/r/a67bd8c0-b036-4761-b161-bdab272302e5', encoding='latin', index_col=0, parse_dates=True, dayfirst=True)
    weather_data.columns = ['High Temperature','Low Temperature', 'Precipitation']
    weather_data.index.name = 'Date'
    
    weather_data.index = pd.to_datetime(weather_data.index, dayfirst=True, format="mixed")
    
    return weather_data

def pollen_numbers_till_now_custom():
    c_year = datetime.now().year
    c_week = datetime.now().strftime("%V")
    url_list = []
    
    for year in range(1992, c_year):
        for week in range(0, 52):
            if year < c_year:
                url_year_week = 'http://www.pollen.lu/index.php?qsPage=data&year='+str(year)+'&week='+str(week)+'&qsLanguage=Fra'
                url_list.append(url_year_week)
            else:
                if week < c_week:
                    url_year_week = 'http://www.pollen.lu/index.php?qsPage=data&year='+str(year)+'&week='+str(week)+'&qsLanguage=Fra'
                    url_list.append(url_year_week)
                else:
                    break
                    
    url_list.remove('http://www.pollen.lu/index.php?qsPage=data&year=2001&week=22&qsLanguage=Fra')        
    url_list.remove('http://www.pollen.lu/index.php?qsPage=data&year=2001&week=23&qsLanguage=Fra')        
    url_list.remove('http://www.pollen.lu/index.php?qsPage=data&year=2001&week=24&qsLanguage=Fra')        
    url_list.remove('http://www.pollen.lu/index.php?qsPage=data&year=2001&week=25&qsLanguage=Fra')        
    print(url_list)    
    
    pollen_dfs = []
    
    for url_weekly in url_list:
        week_response = rq.get(url_weekly)
        soup3 = BeautifulSoup(week_response.text, 'html.parser')
        html_tables = soup3.find_all('table')
        pollen_table = html_tables[5]
        pollen_df = pollen_df_from_table(pollen_table)
        pollen_dfs.append(pollen_df)
        
    pollen_data = pd.concat(pollen_dfs, ignore_index=False)
    
    return pollen_data
 
def post_read_manipulation(df):
    df = df.fillna(0)   
    df['Mean Temp'] = (df['High Temperature'] + df['Low Temperature'])/2  

    df['Year'] = df.index
    df['Year'] = df['Year'].dt.year
    df['Day of year'] = df.index
    df['Day of year'] = df['Day of year'].dt.dayofyear
    
    df.ne(0).idxmax()
        
    return df

def find_first_day_with_pollen():
    df = "find start dato og vis først dag med pollen for hvert år"
    return df

def find_trends():
    df = "find trends"
    return df


def main():
    print(weekly_pollen_numbers())
    print(pollen_numbers_till_now())
    #print(pollen_numbers_till_now_custom()) #Initial thoughts. 
    print(daily_pollen_numbers())
    
    pollen_df, act_date = pollen_numbers_till_now()
    weather_df = weather_data()
    
    data = pd.merge(weather_df, pollen_df, left_on='Date', right_on='Date', how='outer', )
    data = data[(data.index >= '1992-01-01') & (data.index < act_date)]
    
    #print(data)
    df = post_read_manipulation(data)

    df.to_csv('data.csv', index=True)
    
if __name__ == "__main__":
    main()
    
    



