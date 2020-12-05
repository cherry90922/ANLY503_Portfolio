# Static Visualization Assignment

## Introduction & Data

In the previous assignment, you started working with the raw data dumps from the bank's systems, you tidied (is that even a verb?!?) some datasets, and you created an _analytical dataset_. An _analytical dataset_ may be tidy or not -there is somewhat of a gray area there- however, it is a dataset that can be used for both data visualization and modeling.

We are providing an extended _analytical_ dataset, with one record per _account_ and many different variables/measurements/features for each account.

We are also providing the `transactions.csv` data as well so you can build some visualizations from the raw data.

The data for this assignment is contained in the `data.zip` file included in this repository. **You must unzip the file**, which will create a `data/` directory inside this repository as well, and this directory is ignored by git. 

---

The `transactions.csv` contains all of the bank's transactions.

| Field Name | Description |
|:-----------|:------------|
| `id`| Unique record identifier |
| `account_id` | Account identifier | 
| `date` | Transaction date |
| `type` | Debit or Credit |
| `amount` | Amount of transaction |
| `balance` | Account balance after the transaction is excuted
| `bank` | The two letter code of the other bank if the transaction is a bank transfer | `account` | The account number of the other bank if the transaction is a bank transfer |
| `method` | Method of transaction: can be bank transfer, cash, or credit card | 
| `category` | What the transaction was for |

---

The `accounts_analytical.csv` file contains the following information for every account. There is one record per account. 4,500 rows and 64 columns.

|Field Name                                      |Description ||:-----------------------------------------------|:-----------||`account_id`                                    | Account number           ||`acct_creation_date`                            | Date when account was opened           ||`statement_frequency`                           | The frequency that statements are generated for the account
|`account_district`                              | Name of the district where the account is           ||`num_customers`                                 | The total number of clients associated with the account (owner and users) |
|`credit_cards`                                  | Number of credit cards for an account or zero if none           ||`loan_date`                                     | The date the loan was issued           ||`loan_amount`                                   | The amount of the loan           ||`loan_payment`                                  | The amount of the loan payment           ||`loan_term`                                     | The duration of loan in months           ||`loan_status`                                   | The status of the loan (current or expired)           ||`loan_default`                                  | T/F if the loan is in default           ||`max_withdrawal`                                | Maximum debit amount for the account           ||`min_withdrawal`                                | Minimum debit amount for the account           ||`max_balance`                                   | Maximum balance for the account           ||`min_balance`                                   | Minimum balance for the account           ||`credit_xxxxx_yyyyy_zzzzz`             | Summary statistics for all types of **credit** type transactions where: <br/> * `xxxxx` can be: cash, bank transfer or other <br/> * `yyyyy` can be: pension benefit, interest credit, or other <br/> * `zzzzz` can be transaction count (txn\_ct), transaction totals (txn\_tot) or average transaction amount (avg_txn) ||`debit_xxxxx_yyyyy_zzzzz`             | Summary statistics for all types of **debit** type transactions where: <br/> * `xxxxx` can be: cash, bank transfer or credit card <br/> * `yyyyy` can be: household payment, insurance payment, loan payment, negative balance charge, statement charge, or other <br/> * `zzzzz` can be transaction count (txn\_ct), transaction totals (txn\_tot) or average transaction amount (avg_txn)           ||`pmt_order_ct`                                  | Number of payment orders for the account           ||`pmt_order_avg_amt`                             | The average amount for the payment orders           ||`owner_client_id`                               | Client ID           ||`gender`                                        | Client gender           ||`birth_date`                                    | Client birth date           ||`owner_district`                                | Client district           |


## Instructions & Tasks 

Use the data provided in the files above to create analysis and visualizations that answer the posed question or complete the task.

1. Explore all accounts. Create visualizations that combine or these account characteristics:
	* Whether an account has a credit card or not
	* Whether an account has a loan or not
	* The **average** balance for the account
1. What is the distribution of all loans and what are their characteristics?
1. Is there a relationship between a good or bad loan and the time between an account is opened an the loan is created? Is there a specific set of accounts that seem to be at higher or lower risk of defaulting?
1. For the account with the highest number of transactions, make a time series line plot for the behavior of the account over time, including all debits and credits, the different methods, and the with the different categories.
1. Explore the validity of the data for the case whether or not an account has a credit card and whether or not they have associated credit card transactions. Is there anything worth noting?

 
You will use RMarkdown to create five `.Rmd` and `.html` files named `task1` through `task5`. Within the markdown files, you will use **both** `R` and `Python`. You are free to use each language as you see fit, _but you must have at least one task with each language._

**The `.html` files will become part of your portfolio.** We will provide a tutorial on how to use RMarkdown to create the html documents and run both `R` and `Python`, and how to set this up in your portfolio.

The files to be committed and pushed to the repository for this assignment are:

* 5 `.Rmd` files
* 5 `.html` files

### Good design practices

We would like to see you apply good design practices and make choices that support them. Think about the first three weeks of the course and use the frameworks we discussed as guidelines for making great visualizations for your audience. 

### Submitting the Assignment

Make sure you commit and push to GitHUb **only the files requested above**! Although you can upload files to GitHub using the website, we would prefer if you get in the habit of cloning your repisitory to your local machine, and using git to push back to GitHub using commit messages. 

### Grading Criteria

The assginment will be graded holistically considering the following:

* The work is complete
* All output is correct and the code runs and does what it is expected to do
* There is discussion on specifics of the analysis, and analysis decisions are justified
* The visualization choices are justified and are designed for the right audience
* The deliverable is professional and properly formatted, has clean presentation, reasonable design choices, and no spelling/grammatical errors

You will receive full credit if your submission meets all of the above criteria. If not, you will receive partial credit where applicable. However, points **will** be deducted for **any** of the following reasons:

- The instructions are not followed
- There are missing sections of the assignment
- The visualizations are sloppy
- The overall presentation and/or writing is sloppy
- There are no comments in your code
- There are more files in the repository than those requested
- There are absolute filename links in your code
- The repository structure is altered
- You include data files in the repository
- You perform the visualizations and analysis just for the sake of doing it, without thinking through and providing analytical justification

and last, but not least

- You use Excel for your charts
- You create a pie chart with 100 categories
- Your visuals look like those we've seen created by Fox News






