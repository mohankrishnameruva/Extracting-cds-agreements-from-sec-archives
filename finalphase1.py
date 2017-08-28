
# coding: utf-8

import pandas as pd
import numpy
import urllib.request
import bs4 as bs
import re

#Read Input from excel file
input = pd.read_excel('Input.xlsx')

#'catch' column will be used to replicate company rows required to accomodate available attributes
input['catch'] = 1

#'values'  and 'attr' lists will contain all values and attributes that are available for all the companies
#if a company doesn't have any cds attributes lists will have 'NA' for those companies
val = []
attr = []

#This variable is used to keep track of companies while passing through loop
p=0


for each in input['URL']:

#Grab the webpage using the url and parse it using BeautifulSoup

	print('Downloading the file ......')
	sauce = urllib.request.urlopen(each)
	print('Brewing Soup..........')
	soup = bs.BeautifulSoup(sauce,'lxml')
#-------------------------------------------------------------------------------------------------------------
	print('preparing Soup1..........')
	if input['Form Type'][p]=='N-Q':
		searchtext = re.compile(r'Credit default swap',re.IGNORECASE)
		foundtext = soup.find('p',text=searchtext)
		table = foundtext.findNext('table')
		soup1 = table.find_all('tr')

	else:
		soup1 = soup.find_all('tr')
		
#----------------------------------------------------------------------------------------------------------------
	
	print('extracting text..........')
	data=[]
	for each in soup1:
		data.append(each.text.rstrip())
	data = [x for x in data if x]
	print('got the text')
	cds=False
	for i in data:
		if 'Credit Default Swap' in i:
			cds = True
		
	#~ if cds==False:
		#~ p=p+1   
		#~ print('no cds...')
		#~ continue
	
	print('Matching index..........')
	#print(data)
	table_data= data
	match_index = []
	if input['Form Type'][p] !='N-Q':
		for i in table_data:
			if 'Credit Default Swap' in i:
				print(table_data.index(i))
				match_index.append(table_data.index(i))
				del table_data[table_data.index(i)]	
		print('index found')
		print(match_index)
	if input['Form Type'][p] == 'N-Q':
		for j in data:
			if 'Description' in j:
				del data[data.index(j)]
		del data[-1]
		for j in data:
			match_index.append(1)

		print(match_index)
	print('index found')


#-------------------------------------------------------------------------------------------------------------------------------------------------

	print('appending values.........')
	if input['Form Type'][p] !='N-Q': ## change back to  input['Form Type'][p]!
		for j in match_index:
			words = data[j].split()
			unrealised = words[-2]+words[-1]
			notion = words[-4]+words[-3]
			exp = words[-6]+' '+words[-5]
			cdstext = ' '.join(i for i in words[0:-7])
			val.append(cdstext)
			val.append(exp)
			val.append(notion)
			val.append(unrealised)
			attr.append('CDS Text')
			attr.append('Expiration Date')
			attr.append('Notional Amount (000s)')
			attr.append('Unrealized Appreciation/ (Depreciation) (000s)')
	if input['Form Type'][p] == 'N-Q':
		for j in range(0,len(data)):
			words=data[j].split()
			for i in words:
				if i =='$':
					del words[words.index(i)]
			unrealised = words[-1]
			notion = words[-2]
			exp = words[-3]+' '+words[-4]
			cdstext = ' '.join(i for i in words[0:-6])
			val.append(cdstext)
			val.append(exp)
			val.append(notion)
			val.append(unrealised)
			attr.append('CDS Text')
			attr.append('Expiration Date')
			attr.append('Notional Amount (000s)')
			attr.append('Unrealized Appreciation/ (Depreciation) (000s)')

###-------------------------------------------------------------------------------------------------------------------------------------------
# Replicating rows of each company accordingly		
	if len(match_index):
		input['catch'][p]= 4*len(match_index)
	if len(match_index)==0:
		attr.append('NA')
		val.append('NA')

	p=p+1
	#print(comp)
	print('_'*100)
	print('processed '+str(p)+'companies')
	
#------------------------------------------------------------------------------------------------------------------------------------------------
inputf = pd.DataFrame([input.loc[idx] for idx in input.index for _ in range(input.loc[idx]['catch'])]).reset_index(drop=True)

comp = pd.DataFrame()
comp['attributes'] = attr
comp['values'] = val

result = inputf
result = result.drop('catch',axis =1)
result['Attributes'] = comp['attributes']
result['Values'] = comp['values']

result.rename(columns={'Unnamed: 0':'ID'},inplace=True)
#----------------------------------------------------------------------------------------------------------------------------------------------
#reset the ID cof companies
id=1
pcik=35315
com=0
pft='N-CSR'
for i in result['CIK']:
    if i==pcik and result['Form Type'][com] == pft:
        result['ID'][com]=id
    else:
        id = id + 1
        result['ID'][com]=id
        pcik = i
        pft = result['Form Type'][com]
    com= com+1



result.to_csv('phase1.csv')
print(result)

