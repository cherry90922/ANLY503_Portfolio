library(dplyr)
library(tidyverse)
##############################################################################################################
####################################### 1. Ingesting data ####################################################
##############################################################################################################

# accounts contains information about the bank's accounts.
accounts <- read_csv("data/accounts.csv")
head(accounts)

# clients contain information about the bank's customers. A client (customer) can have several accounts.
clients <- read_csv("data/clients.csv")
head(clients)

# links contains information that links customers to accounts, 
# and whether a customer is the owner or a user in a given account.
links <- read_csv("data/links.csv")
head(links)

# transactions contains all of the bank's transactions.
transactions <- read_csv("data/transactions.csv")
head(transactions)

# payment_orders contains information about orders for payments to other banks via bank transfers. 
# A customer issues an order for payment and the bank executes the payment. 
# These payments should also be reflected in the transactions.csv data as debits.
payment_orders <- read_csv("data/payment_orders.csv")
head(payment_orders)

# cards contains information about credit cards issued to clients. 
# Accounts can have more than one credit card.
cards <- read_csv("data/cards.csv")
head(cards)

# loans contains information about loans associated with accounts. 
# Only one loan is allowed per account.
loans <- read_csv("loans_r.csv")
loans <- loans %>%
  select(-X1)
head(loans)

# districts contains demographic information and characteristics about the districts 
# where customers and branches are located.
districts <- read_csv("districts_r.csv")
districts <- districts %>%
  select(-X1)
head(districts)


##############################################################################################################
####################################### 2. Cleaning data #####################################################
##############################################################################################################

# Build an analytical dataset by combining (joining) the data from the different tables as you see fit, 
# which will be used for the purposes of exploratory data analysis, visualization and reporting. 
# The unit of analysis is the account. 
# This dataset must contain the following information for each account using the following field names:
# 
# account_id: Account number      <- accounts.id
# open_date: Date when account was opened     <- accounts.date
# statement_frequency: The frequency that statements are generated for the account   
# <- accounts.statement_frequency

# district_name: Name of the district where the account is     
# <- districts.name, accounts.district_id = districts_r.id
# create a new df that has everything in accounts, and only district name from districts
# accounts left joins districts on accounts.district_id = districts_r.id

customers <- accounts %>%
  left_join(districts[, c("id", "name")], by = c("district_id" = "id")) %>%
  rename(district_name = name) %>%
  select(-district_id)

customers %>% glimpse()


# num_customers: The total number of clients associated with the account (owner and users) 
# <- count(links.client_id) accounts.id = links.account_id

customers <- links %>%
  count(account_id, name = "num_customers") %>% # group_by account_id and count total clients
  right_join(customers, by = c("account_id"="id"))


# credit_cards: Number of credit cards for an account or zero if none  
# <- count(cards.id) cards.link_id = links.id, links.account_id = accounts.id
# note links need to be joined as well
customers <- links %>%
  inner_join(cards, by=c("id" = "link_id")) %>%
  count(account_id, name = "credit_cards") %>% #group_by account_id and count total clients
  right_join(customers, by="account_id") %>%
  mutate(credit_cards = ifelse(is.na(credit_cards), 0, credit_cards))


cards %>% glimpse()
# to replace NA with 0 in the entire df, use either of below 2 options:
# customers[is.na(customers$credit_cards)] <- 0
# df %>% mutate_each( funs_( interp( ~replace(., is.na(.),0) ) ) )

# loan: T/F if the account has a loan  
# <- accounts.id = loans_r.id
# assume loans.id is the account_id
# since loan does not exist in any df 
# need to create a new column loan, which will depend on values in other columns in loans df
customers$loan = NA

# loan_amount: The amount of the loan if there is one, NA if none  <- loans.amount, accounts.id = loans_r.id
# loan_payments: The amount of the loan payment if there is one, NA if none   <- loans.payments, accounts.id = loans_r.id
# loan_term: The duration of loan in months, NA if none  <- 
# loan_status: The status of the loan (current or expired), NA if none
# loan_default: T/F if the loan is in default, or NA if none
customers <- customers %>%
  left_join(loans[, c("account_id", "amount", "payments", "loan_term", "loan_status", "loan_default")], by = "account_id") %>%
  rename(loan_amount = amount, loan_payments = payments, open_date = date) %>% # rename column names, note its new_name=old_name, not the other way around
  mutate(loan = ifelse(is.na(loan_amount), "F", "T")) # fill values into new column loan


# max_withdrawal: Maximum amount withdrawn for the account
# min_withdrawal: Minimum amount withdrawn for the account

# transactions %>%
#   select(account_id, type, amount) %>%
#   group_by(account_id, type) %>%
#   filter(type == 'credit', amount == max(amount)) %>%
#   glimpse()
# 
# transactions %>%
#   select(account_id, type, amount) %>%
#   group_by(account_id, type) %>%
#   slice(type == 'credit', which.max(amount)) %>%
#   glimpse()

customers <- transactions %>% 
  filter(type == 'debit') %>% # debit == withdrawl
  group_by(account_id) %>%
  summarize(min_withdrawal = min(amount), max_withdrawal = max(amount)) %>%
  right_join(customers, by="account_id")

transactions %>% glimpse()
# cc_payments: Count of credit payments for the account for all cards
customers <- transactions %>%
  filter(type=='credit') %>%
  count(account_id, name = "cc_payments") %>%
  right_join(customers, by="account_id")

# max_balance: Maximum balance in the account
# min_balance: Minimum balance in the account
customers <- transactions %>%
  group_by(account_id) %>%
  summarize(min_balance = min(balance), max_balance = max(balance)) %>%
  right_join(customers, by="account_id")

customers %>% glimpse()

# save the result as a csv
write.csv(customers, "customers_r.csv")
