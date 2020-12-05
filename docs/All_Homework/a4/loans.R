# # You need to perform the tasks above in both R and Python. 
# For each task above, you need to write scripts (*.R or *.py file) and output within this repository 
# that read the source files using relative paths and produce the required output. 
# For each task, you will procude four files: 2 script and 2 output for a total of 12 files:
# # 
# # loans.R, loans.py, loans_r.csv, loans_py.csv
# # district.R, district.py, district_r.csv, district_py.csv
# # customers.R, customers.py, customers_r.csv, customers_py.csv
# 
# # Since we realize that you may have a preference for a particular language, 
#   you will tell us which language will receive 70% of the weight for this assignment. 
# You still need to do the work in both languages. 
# Create a single-line text file called language.txt in this repository where you will enter R or Python.
getwd()

library(tidyverse)


##############################################################################################################
####################################### 1. Ingesting data ####################################################
##############################################################################################################

# loans.csv contains information about loans associated with accounts. 
# Only one loan is allowed per account.
loans <- read_csv("data/loans.csv")
head(loans)


##############################################################################################################
####################################### 2. Cleaning data #####################################################
##############################################################################################################

### 2.1 clean dataset: loans
library(dplyr)
glimpse(loans)

# convert pivot loan status columns and make them rows
loans_r <- loans %>%
  pivot_longer(cols = `24_A`:`60_A`, names_to = 'loan_info')

# since one account only has one loan, delete repetitive accounts with no payment status info
loans_r <- loans_r[!(loans_r$value=='-'),] 

# write it in wrangling?
# loans_r <- loans_r %>%
#   filter(loans_r$value!='-')


# separate loan_info into
# * loan_term: The duration of loan in months, NA if none
# * loan_status: The status of the loan (current or expired), NA if none
# * loan_default: T/F if the loan is in default, or NA if none

# A stands for an expired loan that was paid in full
# B stands for an expired loan that was not paid in full (it was in default)
# C stands for a current loan where all payments are being made
# D stands for a current loan in default due to not all payments being made

loans_r <- loans_r %>%
  separate(loan_info, 
           into = c("loan_term", "loan_other"),
           sep = "_") %>%
  glimpse()

# add two new columns to fill in extracted values with
loans_r$loan_status = NA
loans_r$loan_default = NA

for (i in 1:nrow(loans_r)){
  if (loans_r$loan_other[i] == 'A'){
    loans_r$loan_status[i] = 'expired'
    loans_r$loan_default[i] = 'F'
  } else if (loans_r$loan_other[i] == 'B'){
    loans_r$loan_status[i] = 'expired'
    loans_r$loan_default[i] = 'T'
  } else if (loans_r$loan_other[i] == 'C'){
    loans_r$loan_status[i] = 'current'
    loans_r$loan_default[i] = 'F'
  }
  else{
    loans_r$loan_status[i] = 'current'
    loans_r$loan_default[i] = 'T'
  }
}


# delete columns value & loan_other which are not useful anymore
# loans_r$value <- NULL
# loans_r$loan_other <- NULL

loans_r <- loans_r %>%
  select(-c(value, loan_other))

glimpse(loans_r)

write.csv(loans_r, 'loans_r.csv')







