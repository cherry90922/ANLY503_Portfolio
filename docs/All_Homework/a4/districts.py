#!/usr/bin/env python
# coding: utf-8

# Make the district.csv data tidy. You must account for all the information contained in each record (row).

# In[3]:


import pandas as pd


# In[5]:


districts = pd.read_csv("data/districts.csv")
districts.head()


# In[6]:


districts.info()


# In[16]:


# remove brackets from the beginning and the end of 3 columns
districts['municipality_info'] = districts['municipality_info'].str.strip('[]')
districts['unemployment_rate'] = districts['unemployment_rate'].str.strip('[]')
districts['commited_crimes'] = districts['commited_crimes'].str.strip('[]')


# In[22]:


# split col ['municipality_info'] into 4 columns, save it into a temp df
# and combine it with original df
tmp1 = districts['municipality_info'].str.split(',', expand=True)
tmp1.columns = ["Population500", "Population500to1999", "Population2000to9999", "Population10000"]
districts_py = pd.concat([districts.drop('municipality_info', axis=1), tmp1.iloc[:, 0:4]], axis=1) 
# note tmp1.iloc is 0:4, not 1:4 or 0:3


# In[25]:


# do the same to columns unemployment_rate & committed_crimes
# split col ['municipality_info'] into 4 columns, save it into a temp df
# and combine it with original df
tmp2 = districts['unemployment_rate'].str.split(',', expand=True)
tmp2.columns = ["unemployment_rate_1995", "unemployment_rate_1996"]
districts_py = pd.concat([districts_py.drop('unemployment_rate', axis=1), tmp2.iloc[:, 0:3]], axis=1) 


# split col ['municipality_info'] into 4 columns, save it into a temp df
# and combine it with original df
tmp3 = districts['commited_crimes'].str.split(',', expand=True)
tmp3.columns = ["commited_crimes_1995", "commited_crimes_1996"]
districts_py = pd.concat([districts_py.drop('commited_crimes', axis=1), tmp3.iloc[:, 0:3]], axis=1) 


# In[26]:


districts_py.head()


# In[27]:


districts_py.info()


# In[32]:


# convert newly split columns into floats
districts_py['Population500']=[float(x) for x in districts_py['Population500']]
districts_py['Population500to1999']=[float(x) for x in districts_py['Population500to1999']]
districts_py['Population2000to9999']=[float(x) for x in districts_py['Population2000to9999']]
districts_py['Population10000']=[float(x) for x in districts_py['Population10000']]
# districts_py['unemployment_rate_1995']=[float(x) for x in districts_py['unemployment_rate_1995']]
districts_py['unemployment_rate_1996']=[float(x) for x in districts_py['unemployment_rate_1996']]
# districts_py['commited_crimes_1995']=[float(x) for x in districts_py['commited_crimes_1995']]
districts_py['commited_crimes_1996']=[float(x) for x in districts_py['commited_crimes_1996']]


# In[33]:


districts_py.info()


# In[36]:


districts_py.to_csv("districts_py.csv", index=False, header=True)


# In[ ]:




