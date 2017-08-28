
# coding: utf-8

# In[2]:


import pandas as pd
import re

input = pd.read_csv('phase1.csv')


# Removing companies with null values
input = input[pd.notnull(input['Attributes'])]


#Seperate the CDS Text 

input = input[input['Attributes'] == 'CDS Text']

#Drop the attributes column
input.drop('Attributes',axis=1,inplace = True)

#Since we only have cds text in values column rename it
input.rename(columns={'Values': 'CDS Text'},inplace = True)
input.to_csv('phase2.csv')

#--------------------------------------------------------------------------------------------------------
#Match words in each cds text and overwrite the underlying column
c = 0

input["Underlying"] = ''
for i in input['CDS Text']:
    words = input['CDS Text'][c].split(' ')
    #print(words)
    for i in range(0,len(words)):
        if words[i] == 'default' and words[i+1] == 'of':
            print(words[i+2] +' '+ words[i+3])
            input['Underlying'][c] = words[i+2] +' '+ words[i+3]
        if words[i] == 'default' and words[i+2] == 'of':
            print(words[i+3] + ' '+ words[i+4])
            input['Underlying'][c] = words[i+3] + ' '+ words[i+4]
    c = c+1

#--------------------------------------------------------------------------------------------------------
#Match words in each cds text and overwrite the Counterparty column

c = 0

input["Counter Party"] = ''
for i in input['CDS Text']:
    words = input['CDS Text'][c].split(' ')
    #print(words)
    for i in range(0,len(words)-6):
        if words[i] == 'pay':
            if words[i+1]== 'to':
                i = i+1
            print(words[i+1] +' '+ words[i+2])
            input['Counter Party'][c] = words[i+1] +' '+ words[i+2]
            if words[i+1] == 'Bank':
                print(words[i+1] +' '+ words[i+2]+ ' '+ words[i+3])
                input['Counter Party'][c] = words[i+1] +' '+ words[i+2]+ ' '+ words[i+3]

    c = c+1

#--------------------------------------------------------------------------------------------------------
#Match words in each cds text and overwrite the Exact Underlying column
# use regular expressions to find %
c = 0

pattern = re.compile('%$')
input["Exact Underlying"] = ''
for i in input['CDS Text']:
    words = input['CDS Text'][c].split(' ')
    for i in range(0,len(words)-3):
        if words[i] == 'notional' and words[i+1] == 'amount' and words[i+2] == 'of':
            for x in words[i+3:]:
                f = pattern.findall(x)
                if len(f):
                    input['Exact Underlying'][c] = input['Underlying'][c] +' '+ x
                    print(input['Exact Underlying'][c])
    c = c+1

#--------------------------------------------------------------------------------------------------------
#use regular expressions to find dates

c = 0
pattern = re.compile('\D\d\d$')
for i in input['CDS Text']:
    words = input['CDS Text'][c].split(' ')
    for i in range(0,len(words)-3):
        if words[i] == 'notional' and words[i+1] == 'amount' and words[i+2] == 'of':
            for x in words[i+3:]:
                f = pattern.findall(x)
                if len(f):
                    input['Exact Underlying'][c] = input['Underlying'][c] +' '+ x
                    print(input['Exact Underlying'][c])
    c = c+1



input['CDS Transaction']=''
for i in input['CDS Text']:
	words = input['CDS Text'][c].split(' ')
	for j in words:
		if 'buy' in j.lowercase():
			input['CDS Transaction']='Buy'
		if 'sell' in j.lowercase():
			input['CDS Transaction']='Sell'
input.to_excel('phase2.xlsx')
input1= pd.read_csv('phase1.csv')
input1.to_excel('phase1.xlsx')






# In[ ]:




