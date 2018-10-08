import statsmodels.api as sm
import pandas as pd
import numpy as np
import re, collections
import matplotlib.pyplot as plt
from mpldatacursor import datacursor
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression

class analysis():
	def __init__(self, num_data):
		self.num_data = num_data

	# clean up a row data 
	def clean_up(self, file_name): 
		with open(file_name) as infile:

			'''
			# replaceements 
			rep = {'%20':' ','%2F%2F':'://','%2F':'/',';':'\n','%3D%3D%3D%3D':'\n','png':'\n','%3A':''}

			rep = dict((re.escape(k),v) for k, v in rep.iteritems())
			pattern = re.compile("|".join(rep.keys()))
			text = pattern.sub(lambda m:rep[re.escape(m.group(0))], text)
			print(text)
			'''

			contents = infile.read()
			data = contents.replace('%20', ' ')
			d_slash = data.replace('%2F%2F','://')
			s_slash = d_slash.replace('%2F','/')
			info = s_slash.replace(';','\n')
			info = info.replace('%3D%3D%3D%3D','\n')
			info = info.replace('png','\n')
			info1 = info.replace('%3A','')
			#f = open("Nata.txt","a+")
			#f.write(info1 +"\n")
			#f.close()
		return info1

	'''
	website_list = pd.read_html("https://en.wikipedia.org/wiki/List_of_most_popular_websites")
	for each in website_list:
		web_address = pd.DataFrame(data=each[1], index=each[1])
	'''

	# change to list with in a dictionary 
	def prepare(self, file_name, from_file=False):
		collection = []
		data= collections.defaultdict(dict) 
		count_num_data = 0

		if from_file:
			with open(file_name,'r') as l_file:	
				content = l_file.read()
		else:
			content = file_name
		
		line = content.split('\n')

		# convert the data into one hot list
		for each in line:
			values = each.split(':')
			if len(values) == 3:
				key, value_1, value_2 = values
				value = value_1+":"+ value_2
				if key == 'web address':
					catagory = value
			elif len(values) == 2:
				key, value = values

			else:                   
			#	if count_num_data %100 == 0:
			#	print key, value, len(value)
				pass

				if key == 'Waterfall view':
					pattern = r'[0-9][0-9]'
					if re.search(pattern, value):
						x = re.findall(pattern,value)
						rep = re.compile(r'\s+')
						time = re.sub(rep,'',str(x[:3]).replace("'",""))
						
						value = time.replace('18','2018').replace('[', '').replace(']','').replace(',','-')
						key = 'date'
					count_num_data += 1

			data[catagory].setdefault(key,[]).append(value)
			
		cleaned_dict =  dict(data)
		for web in cleaned_dict.keys():
			#replace empty value with np.nan
			del cleaned_dict[web]['Waterfall view']
			del cleaned_dict[web]['web address']
			for x in cleaned_dict[web].keys():
				if '' in cleaned_dict[web][x]:
					for y in cleaned_dict[web][x]:
						cleaned_dict[web][x] = np.nan
			if cleaned_dict[web].has_key(''):
				del cleaned_dict[web]['']
			else:
				pass
		
		print "The number of data collected is: ", count_num_data

		return cleaned_dict
	
	def select(self, dataframe, param):
		dfT = dataframe.transpose() 
		print dfT
		# conver to frame
		df_2 = pd.DataFrame(data=dfT[param]).dropna() #, columns=['webaddress',param]).dropna()
		s = df_2.apply(lambda x: pd.Series(x[param]), axis = 1).transpose().max()
		s.name = param
 		# conver serias to DataFrame
		#df = pd.DataFrame(data=s ) #columns=['webaddress', param])
		df = df_2.drop(param, axis=1).join(s)

		return df	

	# produce tabel, chart, and graph
	def plot(self, dataframe, param, param2, color='red', label ='no', ax = None):
		df = self.select(dataframe, param) 
		df2 = self.select(dataframe, param2) 
		comb_df = df.join(df2)
		
		if label == 'no':
			comb_df.plot.scatter(x=param, y=param2, color=color,title=param+' Vs '+param2) 
			datacursor(hover=True, point_labels=comb_df.index)

			# getting the summary
			print df.describe() 
			print df2.describe()
			print comb_df
			plt.show()
			#return dataframe.plot()
		else:
			if ax == None:
				return comb_df.plot.scatter(x=param, y=param2, color=color, label=label) 
			else:
				comb_df.plot.scatter(x=param, y=param2, color=color, label=label, ax = ax, title=param+' Vs '+param2) 
				datacursor(hover=True, point_labels=comb_df.index)
				# getting the summary
				print df.describe() 
				print df2.describe()
				print comb_df
				plt.show()
			

	
	def prop(self, dataframe):
		return dataframe.columns

if __name__ == '__main__':
	
	test = analysis(1)

# import from a the cleaned data
#value =  test.prepare('Nata.txt', True)
#print value 

alexa = test.clean_up('./Test_results/alexa_data3.txt')

alexa_dic = test.prepare(alexa)

alexa_df = pd.DataFrame(data=alexa_dic)

alexa_df.to_excel("parafortop100.xlsx")

"""
# import row file 
usa = test.clean_up('./Test_results/test_result.txt')
Italy = test.clean_up('./Test_results/Milan_Italy_test_result.txt')
alexa = test.clean_up('./Test_results/alexa_test_result.txt')

alexa_v = test.prepare(alexa)
df_a = pd.DataFrame(data=alexa_v)


USA_v = test.prepare(usa)
Italy_v = test.prepare(Italy)
###############################################################################
# u'(Doc complete) Byets in', u'(Doc complete) Requests',
# u'(Fully loaded) Bytes in', u'(Fully loaded) Requests',
# u'(Fully loaded) Time', u'DOM elements', u'First byte', u'Load time',
# u'Speed Index', u'Start render', u'date'],
###############################################################################
""" 
'''
df2 = pd.DataFrame.from_dict({(i,j):value[i][j]
							for i in value.keys()
							for j in value[i].keys()},
							orient = 'index')
'''

"""
df_u = pd.DataFrame(data=USA_v)
df_i = pd.DataFrame(data=Italy_v)

#test.plot(df_u, u'Speed Index', u'Load time')

dat = test.plot(df_u, u'Speed Index', u'Load time',color='lightBlue', label="USA")
test.plot(df_i, u'Speed Index', u'Load time',color='DarkBlue',label="Italy", ax=dat)

# linear regression 
p1 = test.select(df_u, u'Speed Index')
p2 = test.select(df_u, u'Load time')
p3 = test.select(df_u, u'Start render')
p4 = test.select(df_u, u'DOM elements')

X = p1.join(p2).join(p3).join(p4)
y = test.select(df_u, u'First byte')


# spliting the date to test and train 
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

lm = LinearRegression()
lm.fit(X_train, y_train)
accuracy = lm.score(X_test, y_test)
print "Accuracy: ", accuracy

model = sm.OLS(y, X).fit()
predictions = model.predict(X)
print model.summary()
plt.title( "Ordinary Least Squares")	
plt.xlabel("Web addresses")
plt.ylabel('First byte')
plt.plot(predictions, 'bo',markersize=9, label='PREDICTION')
plt.plot(y, 'ko',markersize=6, label='TARGET') 

Y = -0.7179*p1 + 0.5839*p2 +0.7944*p3 +-1.3634*p4

plt.plot(y, '--')

datacursor(hover=True, point_labels=predictions.index)
plt.legend()
plt.show()
"""
