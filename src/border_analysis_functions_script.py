import csv
import datetime
import os
from itertools import product


def unique_list(key_parameter,filename):
    '''Return list of unique values for the given key'''
    
    #with open('Border_Crossing_Entry_Data.csv','r') as read_csv:
    with open(filename,'r') as read_csv:
        csv_reader=csv.DictReader(read_csv)
        values_list=[]
        for row in csv_reader:
            current_value=row[key_parameter]
            if current_value not in values_list:
                values_list.append(current_value)
    return values_list


def date_convert(dateString):
    '''convert date string of a specific format to datetime object'''
    
    return datetime.datetime.strptime(dateString,'%m/%d/%Y %I:%M:%S %p')


def date_str(dtime):
    '''convert datetime object to date string'''
    
    dtime=datetime.datetime.strptime(dtime,'%Y-%m-%d')
    dtStr=dtime.date().strftime('%m/%d/%Y')
    return dtStr+' 12:00:00 AM'


def monthly_totals(month,measure,border,filename):
    '''Return the monthly total value per border for the given measure'''
    
    with open(filename,'r') as read_csv:
    #with open('update_Border_Crossing_Entry_Data.csv','r') as read_csv:
        csv_reader=csv.DictReader(read_csv)
        sum=0
        for row in csv_reader:
            if (month in row['Date']) and (measure in row['Measure']) and (border in row['Border']):
                sum+=int(row['Value'])
                
    return sum


def sort_column(key1,key2,key3,key4,filename):
    '''Sort table using the specified columns keys in decreasing order'''
    
    reader = csv.DictReader(open(filename+'.csv','r'))
    result = sorted(reader, reverse=True, key=lambda d: (d[key1],int(d[key2]),d[key3],d[key4]))
   
    newfile=filename+'_.csv'
    writer = csv.DictWriter(open(newfile,'w'), reader.fieldnames)
    writer.writeheader()
    return writer.writerows(result)