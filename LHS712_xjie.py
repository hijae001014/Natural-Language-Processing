#!/usr/bin/env python
# coding: utf-8

# In[867]:


import re
import pandas as pd
from datetime import datetime


# In[868]:

# # Task 1
# Load data & create a dataframe
doc = []
with open("WN24_dates.txt") as file:
    for line in file:
        doc.append(line)
        
df = pd.Series(doc)
df.head(10)


# # Extract date having regular format with / or -

# In[869]:


#define a function that will add '19' to Year with two digits
def add19ToTwoDigitYear(dateStr): 
    match = re.search(r'\d{1,2}[/-]\d{1,2}[/-]\d{2}$', dateStr)
    if match:
        original_date = match.group(0)
        dateWith19 = original_date[:-2] + '19' + original_date[-2:]
        return dateWith19
    else:
        return dateStr

format1 = dict()
#find matched date
for ind,vals in dict(df.apply(lambda x:re.search('\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',x))).items():
    if vals:
        #replace'-' with '/'
        format1[ind]=re.sub(r'(-)','/',vals.group())
        for index, date in format1.items():
            #use function: if find two digits year, add 19 to year
            format1[index] = add19ToTwoDigitYear(date)


print(format1)
#print(len(format1))


# In[873]:


# convert into normalized datetime using datetime
from datetime import datetime

#define a function that can convert value of date to datetime format
def convertToDateTime(format_Dict):
    format_datetime = dict()
    for index, date in format_Dict.items():
        newDate = datetime.strptime(date, '%m/%d/%Y')
        format_datetime[index] = newDate
    return format_datetime

format1_dateTime = convertToDateTime(format1)
# print(format1_dateTime[10].date())
print(format1_dateTime[6].date())
print(len(format1_dateTime))


# # Extract date having alphabet

# In[876]:


#find matched date and add them to the dictionary 
format2 = dict()

for ind, vals in dict(df.apply(lambda x:re.search(
    r'(?:\d{1,2}[^\S\t\n\r])?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|August|Sep|Oct|Nov|Dec)[a-zA-Z.]*(?:\d{1,2})?,? \d{2,4}',
    x))).items():
    if vals and (ind not in list(format1.keys())):
        format2[ind] = vals.group() 
        
print(format2)
print(len(format2))


# In[877]:


#convert alphabet to numbers

month_abbreviations = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

format2_Num = dict()

for index, date in format2.items():
    # find all match of word month
    match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zA-Z.]*',date);
    if match:
        # get month in number
        monthNum = month_abbreviations.index(match.group()[:3])
        # replace word month that has space before to /
        dateNoMonth = re.sub(r'\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zA-Z.]*\s?','/',date)
        # replace word month with no space before to ''
        dateNoMonth1 = re.sub(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zA-Z.]*\s?','',dateNoMonth)
        # add month number to front
        dateWithNumMonth = str(monthNum+1) + '/' + dateNoMonth1
        # replace ,space or space with /
        format2_Num[index] = re.sub(r',?\s','',dateWithNumMonth)
            
print(format2_Num)


# In[840]:


# add 01 to dates that have no day

def add01ToNoDay(dateStr):
    #match date only have months
    match = re.search(r'^\d{1,2}[/]\d{2,4}$',dateStr)
    if match:
        # replace / with /01/
        dateWith01 = re.sub(r'[/]','/01/',match.group());
        return dateWith01
    else:
        return dateStr;


format2_Num_with01 = dict()
for index, date in format2_Num.items():
    format2_Num_with01[index] = add01ToNoDay(date)

print(format2_Num_with01)
    
# add 19 if year has only two digit
format2_Num_with01_4DigitYear = dict()
for index, date in format2_Num_with01.items():
    format2_Num_with01_4DigitYear[index] = add19ToTwoDigitYear(date);
    
# print(format2_Num_with01_4DigitYear)


# In[881]:


# convert format2 to datetime
format2_dateTime = convertToDateTime(format2_Num_with01_4DigitYear)

print(format2_dateTime[0].date()) #in datetime format
print(len(format2_dateTime))


# # Extract date in month/year format

# In[885]:


format3 = dict()

#match dates in the format of those in month/year
for ind, vals in dict(df.apply(lambda x:re.search(r'\d{1,2}[/]\d{4}',x,re.M|re.I))).items():
    if vals and (ind not in list(format1.keys())) and (ind not in list(format2.keys())):
        format3[ind] = vals.group()
# print(format3)
# print(len(format3))


format3_Num_with01 = dict()
for index, date in format3.items():
    # add 01 as day between month and year using defined add01ToNoDay function
    format3_Num_with01[index] = add01ToNoDay(date)
# print(format3_Num_with01)


# convert to datetime
format3_dateTime = convertToDateTime(format3_Num_with01)
print(format3_dateTime[361].date())
print(len(format3_dateTime))


# # extract dates in the format of those only have year

# In[848]:


format4 = dict()
for ind, vals in dict(df.apply(lambda x:re.search(r'\d{4}',x))).items():
    if vals and (ind not in list(format1.keys())) and (ind not in list(format2.keys())) and (ind not in list(format3.keys())):
        format4[ind] = vals.group()


# add 01/01 as month & day
def add01ToMonth(dateStr):
    match = re.search(r'\d{4}',dateStr)
    if match:
        date = '01/01/' + match.group()
        return date
    else:
        return dateStr


format4_withMonthDay = dict()
for index, date in format4.items():
    format4_withMonthDay[index] = add01ToMonth(date)


print(format4_withMonthDay)
print(len(format4_withMonthDay))


#convert to datetime
format4_dateTime = convertToDateTime(format4_withMonthDay)
print(format4_dateTime[13].date())


# # Task 2: push 40 days back and put it after the original one

# In[886]:


#build a new dictionary with all days
merged_dict = format1_dateTime.copy()
for key, value in format2_dateTime.items():
    merged_dict[key] = value
    
merged_dict2 = merged_dict.copy()
for key, value in format3_dateTime.items():
    merged_dict2[key] = value

merged_all = merged_dict2.copy()
for key, value in format4_dateTime.items():
    merged_all[key] = value


#push 40 days back using datetime
from datetime import datetime

add40days = dict()
for index, date in merged_sorted.items():
    new_date = date + timedelta(days=40)
    #have second column of new dataframe to the first one
    add40days[index] = [str(date.date()), new_date.strftime('%Y-%m-%d')]
print(add40days)


# In[888]:


# write dictionary into text file
with open('LHS712-Assg1-xjie.txt ', 'w') as file:
    for index, dates in add40days.items():
        file.write(f"{index}\t{dates[0]}\t{dates[1]}\n")


# In[ ]:




