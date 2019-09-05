import csv
import datetime
import os
from itertools import product
from border_analysis_functions_script import *

directory='/home/asmsclique/insight/input/'

measures=unique_list('Measure', directory+'Border_Crossing_Entry_Data.csv')
borders=unique_list('Border', directory+'Border_Crossing_Entry_Data.csv')
months=unique_list('Date', directory+'Border_Crossing_Entry_Data.csv')
months.reverse()


#remove columns not needed #format the Value column #format the Date columns
with open(directory+'Border_Crossing_Entry_Data.csv','r') as readcsv:
    csv_reader=csv.DictReader(readcsv)
    
    with open(directory+'update_Border_Crossing_Entry_Data.csv','w') as newfile_:
        fieldnames=['Border','Date','Measure','Value']
        csv_writer=csv.DictWriter(newfile_,fieldnames=fieldnames)
        csv_writer.writeheader()
        
        for line in csv_reader:
            del line['Port Name']
            del line['State']
            del line['Port Code']
            date_row=date_convert(line['Date']).date()
            value_row = line['Value'].replace(',','')
            csv_writer.writerow({'Border':line['Border'],'Date': date_row,'Measure':line['Measure'],'Value':value_row})            

#new months list with new format
months_=[]
for i in months:
    months_.append(str(date_convert(i).date()))
            
#try:
#    with open(directory+'result_2.csv','r') as readcsv:
#        csv_reader=csv.DictReader(readcsv)
#except:
with open(directory+'result_2.csv','w') as newfile_:
    headerfields=['Border','Date','Measure','Value']
    csv_writer=csv.DictWriter(newfile_,fieldnames=fieldnames)
    csv_writer.writeheader()
    for month,measure,border in product(months_,measures,borders):
        csv_writer.writerow({'Border':border,'Date':month,'Measure':measure,\
                             'Value':monthly_totals(month,measure,border,directory+'update_Border_Crossing_Entry_Data.csv')})

            
#sort measure column and cumulative sum of values into dictionary; key and values pairs respectively
with open(directory+'result_2.csv','r') as readcsv:
    csv_reader=csv.DictReader(readcsv)
    emptysum={}
    for i in sorted(measures):
        emptysum[i]=[0]
    for line in csv_reader: #it only goes through once
        for i,j in emptysum.items():
            if line['Measure']==i:
                currentrow=int(line['Value'])
                emptysum[i].append(emptysum[i][len(emptysum[i])-1]+currentrow)
                
                
#unravel the dictionary to list, calculate the cumulative sum and running average
totals_list=[]
averages_list=[]
for keys,values in emptysum.items():
    sum=0
    count=0
    for i in range(0,len(values[1:])):
        sum+=values[1:][i]
        count+=1
        totals_list.append(values[1:][i])
        averages_list.append(int(sum/count))
       
    
#sort by measure column
filename='result_2'
key1='Measure'
reader = csv.DictReader(open(directory+filename+'.csv','r'))
result = sorted(reader, reverse=False,key=lambda d:(d[key1]))
newfile=directory+filename+'_.csv'
writer = csv.DictWriter(open(newfile,'w'), reader.fieldnames)
writer.writeheader()
writer.writerows(result)


#add cumulative sum and average to table
with open(directory+'result_2_.csv','r') as csvfile:
    csvreader=csv.DictReader(csvfile)
    
    with open(directory+'result_2_sum_ave.csv','w') as newfile_:
        fieldnames=['Border','Date','Measure','Value','Average']
        csvwriter=csv.DictWriter(newfile_,fieldnames=fieldnames)
        csvwriter.writeheader()
        count=0
        for line in csvreader:
            del line['Value']
            csvwriter.writerow({'Border':line['Border'],'Date': line['Date'],'Measure':line['Measure'],'Value':int(totals_list[count]),'Average':averages_list[count]})
            count+=1

            
sort_column('Date','Value','Measure','Border',directory+'result_2_sum_ave')


directory_output='/home/asmsclique/insight/output/'
#try:
#    with open(directory_output+'report.csv','r') as readcsv:
#        csvreader=csv.DictReader(csvfile)
#except:    
with open(directory+'result_2_sum_ave_.csv','r') as csvfile:
    csvreader=csv.DictReader(csvfile)

    with open(directory_output+'report.csv','w') as newfile_:
        fieldnames=['Border','Date','Measure','Value','Average']
        csvwriter=csv.DictWriter(newfile_,fieldnames=fieldnames)
        csvwriter.writeheader()
        count=0
        for line in csvreader:
            csvwriter.writerow({'Border':line['Border'],'Date':\
                                date_str(line['Date']),'Measure':line['Measure'],'Value':int(line['Value']),'Average':line['Average']})
            count+=1
        
