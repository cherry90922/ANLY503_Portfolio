#!/usr/bin/env python
# coding: utf-8

# Build an analytical dataset by combining (joining) the data from the different tables as you see fit, which will be used for the purposes of exploratory data analysis, visualization and reporting. The unit of analysis is the account. This dataset must contain the following information for each account using the following field names:
# 
# - account_id: Account number
# - district_name: Name of the district where the account is
# - open_date: Date when account was opened
# - statement_frequency: The frequency that statements are generated for the account
# - num_customers: The total number of clients associated with the account (owner and users)
# - credit_cards: Number of credit cards for an account or zero if none
# - loan: T/F if the account has a loan
# - loan_amount: The amount of the loan if there is one, NA if none
# - loan_payments: The amount of the loan payment if there is one, NA if none
# - loan_term: The duration of loan in months, NA if none
# - loan_status: The status of the loan (current or expired), NA if none
# - loan_default: T/F if the loan is in default, or NA if none
# - max_withdrawal: Maximum amount withdrawn for the account
# - min_withdrawal: Minimum amount withdrawn for the account
# - cc_payments: Count of credit payments for the account for all cards
# - max_balance: Maximum balance in the account
# - min_balance: Minimum balance in the account

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# read in tables
accounts = pd.read_csv("data/accounts.csv")
districts = pd.read_csv("districts_py.csv")
loans = pd.read_csv("loans_py.csv")
clients = pd.read_csv("data/clients.csv")
links = pd.read_csv("data/links.csv")
transactions = pd.read_csv("data/transactions.csv", low_memory=False)
payment_orders = pd.read_csv("data/payment_orders.csv")
cards = pd.read_csv("data/cards.csv")


# In[3]:


accounts.head()


# In[18]:


# create a new dataframe customers to fill in with values from accounts
customers = pd.DataFrame()
customers[['account_id','open_date','statement_frequency', 'district_id']] = accounts[['id','date','statement_frequency', 'district_id']]


# In[19]:


# customers left join districts to get district_name
customers = customers.merge(districts[["id", "name"]], how='left', left_on='district_id', right_on='id')


# In[20]:


# drop columns that are not needed
customers.drop(['district_id', 'id'], axis=1, inplace=True)


# In[21]:


# credit_cards: Number of credit cards for an account or zero if none  
# <- count(cards.id) cards.link_id = links.id, links.account_id = accounts.id
# note links need to be joined as well
# links inner join cards to count number of credit cards per account_id, generate a table tmp1
tmp1 = links[['account_id', 'id']].merge(cards[['link_id', 'id']], how='inner', left_on='id', right_on='link_id').groupby(by='account_id').count()


# In[22]:


tmp1.head()


# In[23]:


# customers left join tmp1 to extract number of credit cards per account_id
customers = customers.merge(tmp1['link_id'], how='left', left_on='account_id', right_on='account_id')
customers['link_id'] = customers['link_id'].fillna(0)


# In[24]:


# rename link_id to credit_cards
# rename name to district_name
customers.rename(columns={'link_id': 'credit_cards', 'name': 'district_name'}, inplace=True)


# In[25]:


# loan: T/F if the account has a loan  
# <- accounts.id = loans_r.id
# assume loans.id is the account_id
# since loan does not exist in any df 
# need to create a new column loan, which will depend on values in other columns in loans df
customers['loan'] = 'NA'

# loan_amount: The amount of the loan if there is one, NA if none  <- loans.amount, accounts.id = loans_r.id
# loan_payments: The amount of the loan payment if there is one, NA if none   <- loans.payments, accounts.id = loans_r.id
# loan_term: The duration of loan in months, NA if none  <- 
# loan_status: The status of the loan (current or expired), NA if none
# loan_default: T/F if the loan is in default, or NA if none
customers = customers.merge(loans[["account_id", "amount", "payments", "loan_term", "loan_status", "loan_default"]],                 how='left', left_on='account_id', right_on='account_id')


# In[12]:


customers.head()


# In[26]:


# update customers['loan'] 
customers.loc[customers.loan_default.isnull(), 'loan'] = "0"
customers.loc[customers.loan_default.notnull(), 'loan'] = "1"


# In[27]:


# update column names
customers.rename(columns={'amount':'loan_amount', 'payments':'loan_payments'}, inplace=True)


# In[59]:


# update customers['loan'] 
customers.loc[customers.loan_amount.isnull(), 'loan_amount'] = "NA"

# update customers['loan'] 
customers.loc[customers.loan_payments.isnull(), 'loan_payments'] = "NA"

# update customers['loan'] 
customers.loc[customers.loan_term.isnull(), 'loan_term'] = "NA"

# update customers['loan'] 
customers.loc[customers.loan_status.isnull(), 'loan_status'] = "NA"

# update customers['loan'] 
customers.loc[customers.loan_default.isnull(), 'loan_default'] = "NA"


# In[34]:


customers.head()


# In[29]:


# max_withdrawal: Maximum amount withdrawn for the account
tmp2 = transactions[transactions['type']=='debit'].groupby(by='account_id')['amount'].max()
tmp2.head()


# In[36]:


customers = customers.merge(tmp2, how='left', on='account_id')
customers.rename(columns={'amount': 'max_withdrawal'}, inplace=True)


# In[40]:


# min_withdrawal: Minimum amount withdrawn for the account
customers = pd.merge(left=customers, how='left', on='account_id', right=transactions[transactions['type']=='debit'].groupby(by='account_id')['amount'].min())
customers.rename(columns={'amount': 'min_withdrawal'}, inplace=True)


# In[43]:


# cc_payments: Count of credit payments for the account for all cards
customers = pd.merge(left=customers, how='left', on='account_id',          right=transactions[transactions['type']=='credit'].groupby(by='account_id')['id'].count())


# In[44]:


customers.rename(columns={'id': 'cc_payments'}, inplace=True)


# In[47]:


# max_balance: Maximum balance in the account
customers = pd.merge(left=customers, how='left', on='account_id',          right=transactions[['account_id','balance']].groupby(by='account_id')['balance'].max())


# In[48]:


customers.rename(columns={'balance': 'max_balance'}, inplace=True)


# In[49]:


# min_balance: Minimum balance in the account
customers = pd.merge(left=customers, how='left', on='account_id',          right=transactions[['account_id','balance']].groupby(by='account_id')['balance'].min())


# In[50]:


customers.rename(columns={'balance': 'min_balance'}, inplace=True)


# In[55]:


# num_customers: The total number of clients associated with the account (owner and users)
# <- count(links.client_id) accounts.id = links.account_id
customers = pd.merge(left=customers, how='left', on='account_id', right=links[['account_id','id']].groupby(by='account_id').count())


# In[56]:


customers.rename(columns={'id': 'num_customers'}, inplace=True)


# In[60]:


# save the df to a csv
customers.to_csv("customers_py.csv", index=False, header=True)

