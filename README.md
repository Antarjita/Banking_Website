# Banking_Website
The Online Bank System has the following functionalities :
  1. Login/Logout
       Login as existing user or new user .
       Existing user logs in with username and password.
       While new user creates a username and password.

  2. Account Management
       Create or delete accounts ,View account details , account balance , view number of accounts of each user and their respective details.
       For new users , on account creation - a random account number is generated and provided.

  3. Transaction Management
       Withdraw, Deposit

  4. Statement Generation 
       based on specified criteria (credit transactions, debit transactions over the given period)

  5. Electronic Clearance Service


Requirements: 
  1. Django 3.x
  2. Mysql

Create a DB in MYSQL with name:- Bank_DB

For demo:- https://youtu.be/wj67Cao1DeA

Steps to run the code :
       
  ```
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
  ```

Go to browser and run url - 
Online Bank -  http://127.0.0.1:8000/accounts/login/




