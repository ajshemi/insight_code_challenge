import csv
import datetime
import os
from itertools import product
from border_analysis_functions_script import *

directory=os.getcwd()+'/input/'

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
            
#%%time
border_dict={'Date':[],'Border':[],'Measure':[],'Value':[]}
with open(directory+'update_Border_Crossing_Entry_Data.csv','r') as read_csv:
    csv_reader=csv.DictReader(read_csv)
    for line in csv_reader:
        border_dict['Border'].append(line['Border'])
        border_dict['Date'].append(line['Date'])
        border_dict['Measure'].append(line['Measure'])
        border_dict['Value'].append(line['Value']) 
#%%time
#new dictionary for US-Canada Border
border_dict_={'Date':[],'Measure':[],'Value':[]}
for month,measure in product(months_,measures):
    for i in range(len(border_dict['Date'])):
        if(border_dict['Date'][i]==month and border_dict['Measure'][i]==measure and border_dict['Border'][i]=='US-Canada Border'):
            border_dict_['Date'].append(border_dict['Date'][i])
            border_dict_['Measure'].append(border_dict['Measure'][i])
            border_dict_['Value'].append(border_dict['Value'][i])
#%%time
#new dictionary for US-Mexico Border
border_dict_1={'Date':[],'Measure':[],'Value':[]}
for month,measure in product(months_,measures):
    for i in range(len(border_dict['Date'])):
        if(border_dict['Date'][i]==month and border_dict['Measure'][i]==measure and border_dict['Border'][i]=='US-Mexico Border'):
            border_dict_1['Date'].append(border_dict['Date'][i])
            border_dict_1['Measure'].append(border_dict['Measure'][i])
            border_dict_1['Value'].append(border_dict['Value'][i])
#%%time
#monthly sum per measure for US-Canada Border
sum_array=[]
for j,k in product(measures,months_):
    sum=0
    for i in range(len(border_dict_['Measure'])):
        if border_dict_['Measure'][i]==j and border_dict_['Date'][i]==k:
            sum=sum+int(border_dict_['Value'][i])
    sum_array.append(sum)

#%%time
#monthly sum per measure for US-Mexico Border
sum_array_=[]
for j,k in product(measures,months_):
    sum=0
    for i in range(len(border_dict_1['Measure'])):
        if border_dict_1['Measure'][i]==j and border_dict_1['Date'][i]==k:
            sum=sum+int(border_dict_1['Value'][i])
    sum_array_.append(sum)

#%%time
border_US_Canada={'Border':[],'Date':[],'Measure':[],'Value':[]}
border_US_Mexico={'Border':[],'Date':[],'Measure':[],'Value':[]}
count=0
for j,k in product(measures,months_):
    border_US_Canada['Border'].append('US-Canada Border')
    border_US_Canada['Measure'].append(j)
    border_US_Canada['Date'].append(k)
    border_US_Canada['Value'].append(sum_array[count])

    border_US_Mexico['Border'].append('US-Mexico Border')
    border_US_Mexico['Measure'].append(j)
    border_US_Mexico['Date'].append(k)
    border_US_Mexico['Value'].append(sum_array_[count])
    count+=1


both_border=border_US_Mexico.copy()
both_border['Border'].extend(border_US_Canada['Border'])
both_border['Date'].extend(border_US_Canada['Date'])
both_border['Measure'].extend(border_US_Canada['Measure'])
both_border['Value'].extend(border_US_Canada['Value'])

with open('result_sum.csv','w') as newfile_:
    fieldnames=['Border','Date','Measure','Value']
    csvwriter=csv.DictWriter(newfile_,fieldnames=fieldnames)
    csvwriter.writeheader()
    for i in range(len(both_border['Date'])):
        csvwriter.writerow({'Border':both_border['Border'][i],'Date': both_border['Date'][i],'Measure':both_border['Measure'][i],'Value':both_border['Value'][i]})

#table with monthly sum and running average for each measure for US_Canada border
with open(directory+'result_sum_ave.csv','w') as newfile_:
    fieldnames=['Border','Date','Measure','Value','Average']
    csvwriter=csv.DictWriter(newfile_,fieldnames=fieldnames)
    csvwriter.writeheader()
    for j in measures:
        start=measures.index(j)*len(months_)
        end=start+len(months_)
        count=1;
        sum=0
        average_array=[0]
        for k in range(start,end):
            sum=sum+border_US_Canada['Value'][k]
            average=round(sum/count)
            average_array.append(average)
            #print(border_US_Canada['Value'][k],border_US_Canada['Measure'][k],sum,average_array[count-1])
            csvwriter.writerow({'Border':border_US_Canada['Border'][k],'Date': border_US_Canada['Date'][k],'Measure':border_US_Canada['Measure'][k],'Value':border_US_Canada['Value'][k],'Average':average_array[count-1]})
            count+=1
        average_array.clear()

#append to table. add monthly sum and running average for each measure for US_Mexico border
with open(directory+'result_sum_ave.csv','a') as newfile_:
    fieldnames=['Border','Date','Measure','Value','Average']
    csvwriter=csv.DictWriter(newfile_,fieldnames=fieldnames)
    for j in measures:
        start=measures.index(j)*len(months_)
        end=start+len(months_)
        count=1
        sum=0
        average_array=[0]
        for k in range(start,end):
            sum=sum+border_US_Mexico['Value'][k]
            average=round(sum/count)
            average_array.append(average)
            csvwriter.writerow({'Border':border_US_Mexico['Border'][k],'Date': border_US_Mexico['Date'][k],'Measure':border_US_Mexico['Measure'][k],'Value':border_US_Mexico['Value'][k],'Average':average_array[count-1]})
            count+=1
        average_array.clear()

#sort table by Date, Value, Measure and Border            
sort_column('Date','Value','Measure','Border',directory+'result_sum_ave')


#change date format, then save table to output file
directory_output=os.getcwd()+'/output/'
#try:
#    with open(directory_output+'report.csv','r') as readcsv:
#        csvreader=csv.DictReader(csvfile)
#except:    
with open(directory+'result_sum_ave_.csv','r') as csvfile:
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
        
