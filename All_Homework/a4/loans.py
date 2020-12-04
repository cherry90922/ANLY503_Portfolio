#!/usr/bin/env python
# coding: utf-8

# ### Make the loans.csv data tidy. You must account for all the information contained in each record (row) and that should be in their own field. Remember, for a dataset to be considered tidy, it must meet the following criteria:
# - Each variable must have its own column
# - Each observation must have its own row
# - Each type of observational unit forms a table

# In[1]:


import pandas as pd


# In[35]:


loans = pd.read_csv("data/loans.csv")
loans.head()


# In[13]:


loans.info()


# In[36]:


# change df from wide to long
# convert pivot loan status columns and make them rows
loans_py = loans.melt(var_name='loan_info', id_vars=["id", "account_id", "date", "amount", "payments"], value_name='loan_exist')


# In[38]:


# since one account only has one loan, delete repetitive accounts with no payment status info
loans_py = loans_py[loans_py['loan_exist'] != '-']
# also loan_exist is no longer useful
loans_py.drop('loan_exist', inplace=True, axis=1)


# In[39]:


loans_py.head()


# In[40]:


# separate loan_info into
# * loan_term: The duration of loan in months, NA if none
# * loan_status: The status of the loan (current or expired), NA if none
# * loan_default: T/F if the loan is in default, or NA if none

# A stands for an expired loan that was paid in full
# B stands for an expired loan that was not paid in full (it was in default)
# C stands for a current loan where all payments are being made
# D stands for a current loan in default due to not all payments being made
loans_py[["loan_term", "loan_other"]] = loans_py['loan_info'].str.split('_',n=1, expand=True)


# In[48]:


# add two new columns to fill in extracted values with
loans_py['loan_status'] = 'NA'
loans_py['loan_default'] = 'NA'

for i in range(len(loans)):
    if loans_py['loan_other'].iloc[i] == 'A':
        loans_py['loan_status'].iloc[i] = 'expired'
        loans_py['loan_default'].iloc[i] = 'F'
    elif loans_py['loan_other'].iloc[i] == 'B':
        loans_py['loan_status'].iloc[i] = 'expired'
        loans_py['loan_default'].iloc[i] = 'T'
    elif loans_py['loan_other'].iloc[i] == 'C':
        loans_py['loan_status'].iloc[i] = 'current'
        loans_py['loan_default'].iloc[i] = 'F'
    else:
        loans_py['loan_status'].iloc[i] = 'current'
        loans_py['loan_default'].iloc[i] = 'T'


# In[44]:


# another way of updating loans_py['loan_status'] and loans_py['loan_default']
# loans_py['loan_status'][loans_py['loan_other']=='A'] = 'expired'
# loans_py['loan_default'][loans_py['loan_other']=='A'] = 'F'
# loans_py['loan_status'][loans_py['loan_other']=='B'] = 'expired'
# loans_py['loan_default'][loans_py['loan_other']=='B'] = 'T'
# loans_py['loan_status'][loans_py['loan_other']=='C'] = 'current'
# loans_py['loan_default'][loans_py['loan_other']=='C'] = 'F'
# loans_py['loan_status'][loans_py['loan_other']=='D'] = 'current'
# loans_py['loan_default'][loans_py['loan_other']=='D'] = 'T'


# In[49]:


loans_py.head()


# In[50]:


# delete columns loan_info & loan_other which are not useful anymore
loans_py.drop(['loan_info', 'loan_other'], inplace=True, axis=1)


# In[51]:


loans_py.head()


# In[52]:


# save the cleaned df to a csv
loans_py.to_csv("loans_py.csv", index=False, header=True)

