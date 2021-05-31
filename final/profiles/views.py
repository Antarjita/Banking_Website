#sys.path defines paths from which imports can be made

import sys, os
print(os.getcwd())
sys.path.append(os.getcwd()+'/profiles/utils')

from django.shortcuts import render, redirect
from profiles.models import Customer_Data, Account_Data,Transactions,ECS_Data,Bills
import random
from django.http import HttpResponse
import Classes

cur_customer = None #Stores customer obj

# Create your views here.
def randomGen():
    # return a 6 digit random number
    return int(random.uniform(100000, 999999))

def display_menu(request):
    global cur_customer
    user_log_in = Classes.Login_Details(request.user.username, request.user.password)
    #Check if customer is a new or existing customer
    cust_details = Customer_Data.objects.filter(Name = user_log_in.username)
    print("cust_details", cust_details)
    if(cust_details):
       print("Existing Customer")
       customer = Classes.Customer(user_log_in)
       print("customer obj", customer)
    else:
        print("Making New Customer")
        customer = Classes.New_Customer(user_log_in, user_log_in.username, '9999999999', 'saa@gmail.com')
    print("Customer name:", customer.customer_data.Name)
    cur_customer = customer
    return render(request, 'profiles/user_account.html', 
    {'customer':customer})
  
def account_management(request):
    accounts = cur_customer.accounts
    user_accnos = list(accounts.keys())
    print("user_accnos", user_accnos)
    return render(request, 'profiles/account_details.html', 
    {'customer':cur_customer, 'accounts':accounts, 'can_close_accnos':user_accnos})


def withdraw(request):
    accounts = cur_customer.accounts
    msg="<br>Enter a valid account no. and also check for ur balance!</p><br>"
    if request.method == "POST":
        acc_num=int(request.POST.get('acc_no'))
        amount=int(request.POST.get('amount'))
        print('requestPOST=',acc_num,type(acc_num))
        #print('account dict:',accounts.keys())
        if acc_num in accounts:
            #acc_obj= accounts[acc_num]
            acc_q=Account_Data.objects.get(Accno=acc_num)
            balance=acc_q.Balance
            print("balance:",balance)
            if(balance>=amount):
                trans=Classes.Account(acc_q)
                trans.create_transaction(amount,"withdraw")
                balance-=amount
                acc_q.Balance=balance
                print("balance:",acc_q.Balance)
                acc_q.save()
                cur_customer.accounts[acc_num].account_details.Balance-=amount
                msg="<td>Withdrawn Successfully!</td><br>"
            else:
                msg="<td>Not sufficient balance!</td><br>"
            
        else:
            msg="<p>Invalid account number</p><br>"
    return render(request, 'profiles/withdraw.html',{'customer':cur_customer, 'accounts':accounts,'msg':msg})
    #'customer':cur_customer, 'accounts':accounts

def deposit(request):
    accounts = cur_customer.accounts
    msg="<br>Enter a valid account no. and also check for ur balance!</p><br>"
    if request.method == "POST":
        acc_num=int(request.POST.get('acc_no'))
        amount=int(request.POST.get('amount'))
        print('requestPOST=',acc_num,type(acc_num))
        #print('account dict:',accounts.keys())
        if acc_num in accounts:
            #acc_obj= accounts[acc_num]
            acc_q=Account_Data.objects.get(Accno=acc_num)
            balance=acc_q.Balance
            print("balance:",balance)
            trans=Classes.Account(acc_q)
            trans.create_transaction(amount,"deposit")
            balance+=amount
            acc_q.Balance=balance
            print("balance:",acc_q.Balance)
            acc_q.save()
            cur_customer.accounts[acc_num].account_details.Balance+=amount
            msg="<td>Deposited Successfully!</td><br>"
        else:
            msg="<p>Invalid account number</p><br>"
    return render(request, 'profiles/deposit.html',{'customer':cur_customer, 'accounts':accounts,'msg':msg})

def stat_gen(request):
    accounts = cur_customer.accounts
    print(accounts)
    msg=""
    all_transactions = {}
    for acc in accounts:
        print("acc_no:",acc)
        acc_q=Account_Data.objects.get(Accno=int(acc))
        trans=Classes.Account(acc_q)
        #trans_rec=Transactions.objects.filter(Accno_id=int(acc))
        #print("trans_rec:",trans_rec)
        transaction=trans.get_transaction_log()
        trans_objs_list = list(transaction.values())
        all_transactions[acc] = all_transactions.get(acc, [])+trans_objs_list
        print("trans:",transaction)
    return render(request, 'profiles/stat_gen.html',{'customer':cur_customer, 'accounts':accounts, 'transaction':all_transactions,'msg':msg})

def get_transaction_action(request):
    accounts = cur_customer.accounts
    print("got:", request.GET)
    msg="filter"
    button_action = request.GET['account_action']
    all_transactions = {}
    if(button_action == 'withdraw'):
        for acc in accounts:
            transaction=Transactions.objects.filter(Accno_id=int(acc),Type="withdraw")
            print("withdraw:",transaction)
            all_transactions[acc] = list(transaction)
    elif(button_action == 'deposit'):
        for acc in accounts:
            transaction=Transactions.objects.filter(Accno_id=int(acc),Type="deposit")
            all_transactions[acc] = list(transaction)
    elif(button_action == 'all'):
        return redirect('profiles:stat_gen')
    #print("Account created successfully")
    print("all_trans:", all_transactions)
    return render(request,'profiles/stat_gen.html',{'customer':cur_customer, 'accounts':accounts, 'transaction':all_transactions,'msg':msg});

def get_function_chosen(request):
    print(request.GET) 
    #print("Got menu") 
    menu_chosen = request.GET['function_chosen']
    if(menu_chosen=='view_accounts'):
        return redirect('profiles:account_management') #name of view given in urls.py
    elif(menu_chosen=='withdraw'):
        return redirect('profiles:withdraw') #name of view given in urls.py
    elif(menu_chosen=='deposit'):
        return redirect('profiles:deposit') #name of view given in urls.py
    elif(menu_chosen=='stat_gen'):
        return redirect('profiles:stat_gen') #name of view given in urls.py
    elif(menu_chosen=='start_ecs'):
        return redirect('profiles:show_ecs_options')
    
def get_account_action(request):
    print("got:", request.GET)
    account_action = request.GET['account_action']
    #err_msg=""
    if(account_action == 'create'):
        cur_customer.create_account()
    elif(account_action == 'close'):
        print(request.GET)
        print("account:", cur_customer.accounts)
        close_accno = int(request.GET['close_accno'])
        #if(close_accno not in accounts):
        #    err_msg = "Invalid Account number!"
        #else:
        cur_customer.close_account(close_accno)
    else:
        print("Got neither create nor close")
    #print("Account created successfully")
    return redirect('profiles:account_management')

def show_ecs_options(request):
    return render(request, "profiles/ecs.html")
    
def redirect_ecs(request):
    ecs_option = request.GET['ecs_option']
    print("ecs_option", ecs_option)
    if(ecs_option == "new_ecs"):
        return redirect('profiles:start_ecs')
    if(ecs_option == 'view_ecs'):
        return redirect('profiles:show_due_bills')
        
def start_ecs(request):
    msg=""
    return render(request, 'profiles/set_up_ecs.html', {"msg":msg})
    
def store_new_ecs_data(request):
    #Make a class for ECS
    payer_name = request.GET['payer_name']
    upper_limit = request.GET['upper_limit']
    accno = int(request.GET['accno'])
    acc_obj = cur_customer.accounts[accno]
    ecs_obj = Classes.New_ECS(payer_name, acc_obj, upper_limit)
    msg = "New ECS Created Successfully!"
    return render(request, 'profiles/set_up_ecs.html', {"msg":msg})
    
def show_due_bills(request):
    accounts = cur_customer.accounts
    bills_list = []
    for acc_obj in accounts.values():
        ecs_list = ECS_Data.objects.filter(Account = acc_obj.account_details)
        for ecs in ecs_list:
            bills_for_cur_ecs = Bills.objects.filter(ECS_ID = ecs).filter(Completed = False)
            for bill in bills_for_cur_ecs:
                bill_details = [bill.id, ecs.Payer_Name, acc_obj.account_no, bill.Amount, ecs.Upper_Limit]
                if(bill.Amount<=ecs.Upper_Limit):
                    bill_details.append("yes")
                else:
                    bill_details.append("NO")
                #bills_list.extend(list(bills_for_cur_ecs))
                bills_list.append(bill_details)
    print(bills_list)
    return render(request, 'profiles/ecs_show_bills.html', {'bills_list':bills_list});
    
def pay_bill(request):
    bill_id = request.GET['bill_id']
    print("bill_id", bill_id)
    bill_obj = Bills.objects.get(id=bill_id);
    bill_obj.Completed = True
    bill_obj.save()
    return redirect('profiles:show_due_bills')
           
'''    
def test_classes(request):
    print("got to test classes")
    login_obj = Classes.Login_Details('anj', 'anj123')
    cust_obj = Classes.Customer(login_obj)
    acc_obj = Classes.Account(1111)
    new_acc_obj = Classes.New_Account(111, cust_obj)
    new_cust_obj = Classes.New_Customer(login_obj, 'anjali', 'addr1', '99880')
'''    
    

        
