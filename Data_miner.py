import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import numpy as np
import json
import os
import sys
import time 
import pandas as pd
import re
#import regex


def get_county_names():
    url = "https://en.wikipedia.org/wiki/California_locations_by_crime_rate"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.findAll('table')[1];
    l_county_names = []
    # Collecting Ddata
    for row in table.tbody.find_all('tr'):    
        columns = row.find_all('td') 
        if(columns != []):
            County = columns[0].text.strip()
            l_county_names.append(County)
    return(l_county_names)
    

def get_crime_violent(county):
    url = "https://en.wikipedia.org/wiki/California_locations_by_crime_rate"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.findAll('table')[1];

    #df = pd.DataFrame(columns=['Country','ViolentCrimeRate', 'PropertyCrimeRate'])

    # Collecting Ddata
    l_violent=[]
    l_county_names=[]
    for row in table.tbody.find_all('tr'):    
    # Find data for each column
        columns = row.find_all('td')
    
        if(columns != []):
            County = columns[0].text.strip()
            l_county_names.append(County)
            ViolentCrimeRate = columns[4].text.strip()
            l_violent.append(ViolentCrimeRate)
            dict_violent=dict(zip(l_county_names,l_violent))
            violent_rate = dict_violent.get(county)
            #print(dict_violent)
            #print(ViolentCrimeRate)
    
    return violent_rate


def get_crime_property(county):
    url = "https://en.wikipedia.org/wiki/California_locations_by_crime_rate"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.findAll('table')[1];

    #df = pd.DataFrame(columns=['Country','ViolentCrimeRate', 'PropertyCrimeRate'])

    # Collecting Ddata
    l_property=[]
    for row in table.tbody.find_all('tr'):    
    # Find data for each column
        columns = row.find_all('td')
    
        if(columns != []):
            County = columns[0].text.strip()
            l_county_names.append(County)
            PropertyCrimeRate = columns[6].text.strip()
            l_property.append(PropertyCrimeRate)
            dict_property=dict(zip(l_county_names,l_property))
            propertyRate= dict_property.get(county)
            #print(dict_property)
    return propertyRate


def get_median_age(county):
    url = "https://fred.stlouisfed.org/release/tables?rid=430&eid=326943"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    l=[]
    l2 =[]
    table = soup.find_all('table')

    #df = pd.DataFrame(columns=['County','MedianAge'])
    dict_median = {}    
    for body in table:
        body=body.find_all('tbody')
        #print(body)
        for rows in body:
            row = rows.find_all('tr')
            #print(row)
            for el in row:
                columns = el.find_all('td')
                County = columns[1].text.strip()
                l.append(County[:-11])
            #print(l)
                Median_age = columns[2].text.strip()
                l2.append(Median_age)
                dict_median = dict(zip(l,l2))
                medianAge = dict_median.get(county)
    return(medianAge)

def get_poverty_rate(county):
    
    getattributes="SAEPOVRTALL_LB90,NAME"; ## poverty rate
    state = "06" ## for CA
    time = "2018"
    apikey = "eab552260d654eb2532ac3ce99a25f61f36e7234"
    url = "https://api.census.gov/data/timeseries/poverty/saipe?get="+getattributes+"&for=county:*&in=state:"+state+"&time="+time+"&key=" + apikey;
    #print(url)
    response = requests.get(url)
    d = {}
    l = []
    l2 = []
    json = response.json()
    for i in range(len(json)):
        if i==0:
            continue
        County = json[i][1][:-7]
        #l.append(County)
        poverty = json[i][0]
        #l2.append(poverty)
        d[County]=float(poverty)
        #d=dict(zip(l,l2))
        povertyRate = d.get(county)
    
    return povertyRate


def get_dataset(l_county_names):
    dataset = {"County":[],"Violent_cryme_rate":[],"Property_crime_rate":[],"Median_age_by_county":[],"Poverty_rate":[]}
    print(len(l_county_names))
    for i in range(len(l_county_names)):
        county = l_county_names[i]
        ViolentCrimeRate = get_crime_violent(county) 

        PropertyCrimeRate=get_crime_property(county)
        
        Median_age = get_median_age(county) 
         
        Poverty_rate = get_poverty_rate(county)
     
        

        curr_county = dataset["County"]
        curr_ViolentCrimeRate= dataset["Violent_cryme_rate"]
        curr_PropertyCrimeRate = dataset["Property_crime_rate"]
        curr_Median_age = dataset["Median_age_by_county"]
        curr_Poverty_rate = dataset["Poverty_rate"]
        
        
        curr_county.append((county))
        curr_ViolentCrimeRate.append(float(ViolentCrimeRate))
        curr_PropertyCrimeRate.append(float(PropertyCrimeRate))
        curr_Median_age.append(float(Median_age))
        curr_Poverty_rate.append(float(Poverty_rate))  

        dataset["County"] = curr_county 
        dataset["Violent_cryme_rate"] = curr_ViolentCrimeRate
        dataset["Property_crime_rate"] = curr_PropertyCrimeRate
        dataset["Median_age_by_county"] =curr_Median_age
        dataset["Poverty_rate"] = curr_Poverty_rate
        print("Fetched data for {}".format(county))
        
    df = pd.DataFrame.from_dict(dataset)
    df
   
    df.to_csv(r'.\my_final_dataset.csv', index=False)
    return df

def main():
    l = list(sys.argv)

    if len(l)==2 and l[1]=='--scrape':
        l_county_names = get_county_names()
        print("Number of CA counties",len(l_county_names))
        df = get_dataset(l_county_names)
        # op = "./my_final_dataset.csv"
        # df.to_csv(op)
        print(df.head())

    elif len(l)==2 and l[1]=='--analysis':
        # getting the dataset 
        df = pd.read_csv('my_final_dataset.csv', index_col=0)
        print('Here is how our dataset looks like:\n')
        #loading dataset 
        print(df.head()) 
        
        print('\n This data set contains {} rows and {} columns'.format(df.shape[0],df.shape[1]))
        time.sleep(3)

        print('\n================================================================================\n')
        print('Informationn on the null values and datatypes present in the dataframe:\n')
        print(df.info())
        
        print('\n As the table above suggests there are no null values in the dataframe.\n')
        time.sleep(3)
        # print(df.info())
        print('\n================================================================================\n')
        print('\nStatistical summmary of the dataset:\n', df.describe())   
        time.sleep(3)
        print('\n================================================================================\n')  
        print('\n checking Correlation between the variables and poverty_rate:\n') 
        # correlation test  
        corr_matrix=df.corr()
        print(corr_matrix["Poverty_rate"].sort_values(ascending=False))
        time.sleep(3)

        print('\n We will keep the these features because they have a high comparable correlation with poverty_rate\n')
        print('\n Below given are some points we can make after having look at correlation matrix:\n')  
        time.sleep(1)
        print('\n 1. Violent rate and Property crime rate show positive relationn which means that county with high value for these will also have high value for poverrty rate.\n')  
        time.sleep(1)
        print('\n 2. Median age and poverty rate show negative relation which means that increased median age will result in low powerty rate for a county.\n')
        time.sleep(3)
        print('\n================================================================================\n')  
        print('\n We can then create scatter plots to get visual representation of the relation\n')  
        print('\n Plotting has started\n')
        # plotting graphs for each feature vs Poverty_rate 
        x = df.drop(columns = ['County', 'Poverty_rate'])
        y = df['Poverty_rate']

        i = 0
        plt.figure(figsize=(22,18))
        for a in x.columns:    
            
            plt.subplot(1,3,1+i)
            plt.scatter(df[a], df['Poverty_rate'])
           
            plt.xlabel(a)   
            plt.ylabel('Poverty_rate') 
            
            i += 1 

            print('                                    | |                                          '*i)
        
        plt.suptitle('Poverty_rate VS Violent_cryme_rate, Property_crime_rate, Median_age_by_county')
        plt.savefig('features_VS_Poverty_rate.png')
        plt.show() 
        print('You can check all the graphs saved in .png format in the current directory\n')


        
        
        print('\n================================================================================\n')  
        print('\n Creating a regression model\n')
        print('\n================================================================================\n')
        x = df.drop(columns = ['County', 'Poverty_rate'])
        y = df['Poverty_rate']
        
        X1 = sm.add_constant(x)
        model = sm.OLS(y, X1)
        model = model.fit()
        # model.tvalues
        print("\n Summary of our model............\n")

        print(model.summary())

        print('\n================================================================================\n')  
        b=model.params[0] 
        W_v = model.params[1]  
        W_p = model.params[2]   
        W_a = model.params[3]  
        w_list = [W_v,W_p,W_a]
        print('Linear regression Plotting for each feature vs Poverty_rate\n')   
        j = 0
        plt.figure(figsize=(22,18))
        for a in x.columns:    
            
            plt.subplot(1,3,1+j)
            plt.scatter(df[a], df['Poverty_rate'])
            plt.plot(df[a], b + w_list[j]*df[a])
            plt.xlabel(a)   
            plt.ylabel('Poverty_rate') 
            
            j += 1 


        plt.suptitle('Regression Plotting for each feature vs Poverty_rate')
        plt.savefig('LR_features_VS_Poverty_rate.png')
        plt.show() 
        print('You can check all the graphs saved in .png format in the current directory\n')    

        print('--> There maybe some impact of the areas which is making it hard for our model the predict the poverty rate of the counties based on values of features in our dataset.\n-->Also the size of the dataset is not enough to train the model well.\n')




    elif len(l)==3 and l[1]=='--static': # Print all the rows of the dataset (by loading from the stored CSV file) along with some statistics
        path = l[2]
        df = pd.read_csv(path,index_col=0)
        print("\nSample data (first 5 rows):\n")
        print(df.head())
        print("\nColumn wise statistics:\n")
        print(df.describe())
    elif len(l)==1: # Print all the rows of the dataset (by scraping and the API) along with some statistics
        l_county_names = get_county_names()
        print("Number of CA counties",len(l_county_names))
        df = get_dataset(l_county_names)
        op = "./my_final_dataset.csv"
        df.to_csv(op)
        print("\nSample data ( 5 rows):\n")
        print(df.head())
        print("\nColumn wise statistics:\n")
        print(df.describe())
        print("\nFull dataset \n")
        print(df)

    else: # Print a statement for the wrong/unrecognized arguments input
        print("The arguments do not match the requirements. Please refer README.md for understanding the requirements")

if __name__ == "__main__":
    # running our main function.
    main()