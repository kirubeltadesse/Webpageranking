import pandas as pd
import numpy as np
import re, collections
from sklearn import preprocessing

import os.path
from os.path import dirname, join


class helper:

    BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    RESOURCE_DIR = os.path.join(BASE_DIR, 'modeldata.csv')

    def __init__(self, num_data):
        self.num_data = num_data

    def write_model_toCSV(self, dic_para):
        # list_of_params = list(dic_para)
        # list_of_params[1:-1]
        data = pd.DataFrame(dic_para, index=[0])
        data.to_csv(helper.RESOURCE_DIR)
        print("The file writing successful")

    def get_data(self, file='resource'):
        if(file=='resource'):
            df = pd.read_csv(str(helper.RESOURCE_DIR))
            nor_to = pd.read_csv(self.get_data(file='alexasite.csv'))
            return self.normal(df, 'testclass', nor_to)
        else:
            return os.path.join(helper.BASE_DIR, file)

    # clean up a row data
    def clean_up(self, file_name):
        rep = {'%20': ' ','%2F%2F':'://', '%2F':'/',';':'\n','.png':'.png \n','%3A':''}

        with open(file_name) as infile:
            contents = infile.read()
            # replacements
            for i, j in rep.items():
                contents = contents.replace(i, j)

        return contents

    # change to list with in a dictionary
    def prepare(self, file_name, from_file=False):
        collection = []
        data = collections.defaultdict(dict)
        count_num_data = 0

        # checking for expernal or internal file source
        if from_file:
            with open(file_name, 'r') as l_file:
                content = l_file.read()
                print(type(content))
        else:
            content = file_name
            #     print(content)

            #     separate each param and add to list
        line = content.split('\n')

        for each in line:

            values = each.split(':')

            # forming params and value pairs
            if len(values) == 2:
                key, value = values
            elif len(values) == 3:
                key, value_1, value_2 = values
                value = value_1+":"+value_2
                if key == 'web address':
                    catagory = value
            else:
                pass

            # put the value for each param of single website together
            data[catagory].setdefault(key,[]).append(value)
            #if key not in ['web address', 'Waterfall view']:
               # print data[catagory].setdefault(key)

            cleaned_dict = dict(data)

        for web in cleaned_dict.keys():
            count_num_data = count_num_data + 1
            #print count_num_data
            #print web
            del cleaned_dict[web]['Waterfall view']
            del cleaned_dict[web]['web address']

            for x in cleaned_dict[web].keys():
                if '' in cleaned_dict[web][x]:
                    for y in cleaned_dict[web][x]:
                        cleaned_dict[web][x] = np.nan
            if '' in cleaned_dict[web]:
                 del cleaned_dict[web]['']

            else:
                pass
        #print "The number of data collected is: ", count_nam_data

        return cleaned_dict

    def select(self, dataframe, param):
        dfT = dataframe.transpose()
        # conver to frame
        df_2 = pd.DataFrame(data=dfT[param]).dropna() #, columns=['webaddress',param]).dropna()
        s = df_2.apply(lambda x: pd.Series(x[param]), axis = 1).transpose().max()
        s.name = param
        # conver serias to DataFrame
        #df = pd.DataFrame(data=s ) #columns=['webaddress', param])
        df = df_2.drop(param, axis=1).join(s)
        return df

    def table(self, df):
        params = ['(Doc complete) Byets in', '(Doc complete) Requests','(Fully loaded) Bytes in','(Fully loaded) Requests',
              '(Fully loaded) Time','DOM elements','First byte','Load time','Speed Index','Start render',]

        df_list = [select(df, param) for param in params]

        for indx, i in enumerate(df_list):

            # first time run
            if indx == 0:
                joined = i

            if indx < len(df_list) -1:

                joined = joined.join(df_list[indx+1])
        joined.index.names = ['Site name']

        return joined

    def catagory(self, df, cata):
        if(cata == 'time'):
            df_ret = df.drop(['(Doc complete) Byets in', '(Doc complete) Requests', '(Fully loaded) Bytes in', '(Fully loaded) Requests'
                    ], axis = 1)
        elif(cata == 'request'):
            df_ret = df[['(Fully loaded) Requests','(Doc complete) Requests']]
        elif(cata == 'bytes'):
            df_ret = df[['(Doc complete) Byets in','(Fully loaded) Bytes in']]

        return df_ret


    def normal(self, df_set, name, nor_to = "Not passed"):

        min_max_scaler = preprocessing.MinMaxScaler()

        if(isinstance(nor_to, pd.DataFrame)):
            # reordering the columne of the input
            new_order = new_order = [1,8,7,11,10,9,6,3,2,5,4,]
            df_set = df_set[df_set.columns[new_order]]
            # renaming the index
            df_set = df_set.rename(columns = {'web_address': 'Site name'})
            data = df_set[list(df_set.columns)[1:]]
            x = nor_to[list(nor_to.columns)[1:]]
            scaled = min_max_scaler.fit(x)

            x_scaled = min_max_scaler.transform(data)
            Columns = [list(nor_to.columns)[1:]]

        else:
            x = df_set[list(df_set.columns)[1:]]
            x_scaled = min_max_scaler.fit_transform(x)
            Columns = [list(df_set.columns)[1:]]


        df = pd.DataFrame(x_scaled,index=df_set[list(df_set.columns)[0]], columns=Columns)
        df.to_csv(os.path.join(helper.BASE_DIR, name))
        return df


if __name__ == '__main__':
    test = helper(1)
    # test = analysis(1)

# import from a the cleaned data
#value =  test.prepare('Nata.txt', True)

# alexa = test.clean_up('./Test_results/alexa_data3.txt')
# alexa_dic = test.prepare(alexa)
# alexa_df = pd.DataFrame(data=alexa_dic)
# data = pd.read_csv("D://Project//Webpageranking/bokeh_app/data/alexasite.csv")
#
# df =catagory(data, 'time')
# normal(df, "testomgkdsm")
