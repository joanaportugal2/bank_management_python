from os import path
from datetime import datetime

ACCOUNTS_FILE = "./accounts.txt"
TRANSACTIONS_FILE = "./transactions.txt"

def check_id_existence(id):
    has_id = False
    if path.exists(ACCOUNTS_FILE):
        f = open(ACCOUNTS_FILE, "r")
        for line in f:
            line_seperated = line.split(";")
            if line_seperated[0] == id:
                has_id = True
                break
        f.close()
    return has_id

def check_balance(id, value):
    bigger_than_balance = False
    f = open(ACCOUNTS_FILE, "r")
    for line in f:
        line_seperated = line.split(";")
        if line_seperated[0] == id:
            if int(line_seperated[3]) < value:
                bigger_than_balance = True
            break
    f.close()
    return bigger_than_balance

def get_date():
    return str(datetime.date(datetime.now()))

def get_time():
    return str(datetime.time(datetime.now()))

def create_account():
    account_id = input("Account holder id: ")
    account_name = input("Account holder name: ")
    account_phone = input("Account holder phone number: ")
    account_initial = input("Account initial amount: ")
    if check_id_existence(account_id):
        print("Holder id already exists!")
    elif int(account_initial) < 0:
        print("Initial amount has to be positive and cannot be 0!")
    else:
        fa = open(ACCOUNTS_FILE, "a")
        fa.write(account_id + ";" + account_name + ";" + account_phone + ";" + account_initial + "\n")
        fa.close()
        ft = open(TRANSACTIONS_FILE, "a")
        ft.write(account_id + ";" + get_date() + ";" + get_time() + ";" + "DEPOSIT" + ";" + account_initial + "\n")
        ft.close()
        print("Account created!\n\n")

def read_all_accounts():
    if path.exists(ACCOUNTS_FILE):
        print("HOLDER'S ID\t | HOLDER'S NAME\t | HOLDER'S PHONE | HOLDER'S BALANCE")
        f = open(ACCOUNTS_FILE, "r")
        for line in f:
            line_seperated = line.split(";")
            print(line_seperated[0] + "\t | " + line_seperated[1] + "\t | " + line_seperated[2] + "\t  | " + line_seperated[3][:-1])
        f.close()
    else:
        print("No accounts saved!\n")

def read_one_account():
    if path.exists(ACCOUNTS_FILE):
        account_id = input("Account holder id: ")
        if check_id_existence(account_id):
            f = open(ACCOUNTS_FILE, "r")
            for line in f:
                line_seperated = line.split(";")
                if line_seperated[0] == account_id:
                    print("HOLDER'S ID\t | HOLDER'S NAME\t | HOLDER'S PHONE | HOLDER'S BALANCE")
                    print(line_seperated[0] + "\t | " + line_seperated[1] + "\t | " + line_seperated[2] + "\t  | " + line_seperated[3])
                    break
            f.close()
        else:
            print("No account found!\n")
    else:
        print("No account found!\n")

def read_one_account_transactions():
    if path.exists(ACCOUNTS_FILE):
        account_id = input("Account holder id: ")
        if check_id_existence(account_id):
            ft = open(TRANSACTIONS_FILE, "r")
            print("DATE\t   | TIME\t\t| TRANSACTION")
            for line in ft:
                line_seperated = line.split(";")
                if line_seperated[0] == account_id:
                    movement = ""
                    if line_seperated[3] == "DEPOSIT":
                        movement = "+"
                    else:
                        movement = "-"
                    print(line_seperated[1] + " | " + line_seperated[2] + "\t| " + movement + line_seperated[4][:-1])
            ft.close()
            fa = open(ACCOUNTS_FILE, "r")
            for line in fa:
                line_seperated = line.split(";")
                if line_seperated[0] == account_id:
                    print("HOLDER'S BALANCE: " + line_seperated[3])
                    break
            fa.close()
        else:
            print("No account found!\n")
    else:
        print("No account found!\n")

def deposit_amount():
    if path.exists(ACCOUNTS_FILE):
        account_id = input("Account holder id: ")
        if check_id_existence(account_id) :
            amount = input("Amount to deposit: ")
            ft = open(TRANSACTIONS_FILE, "a")
            ft.write(account_id + ";" + get_date() + ";" + get_time() + ";" + "DEPOSIT" + ";" + amount + "\n")
            ft.close()
            account_lines = open(ACCOUNTS_FILE, "r")
            new_list = ""
            for line in account_lines:
                line_seperated = line.split(";")
                if line_seperated[0] == account_id:
                    line_seperated[3] = str(int(line_seperated[3]) + int(amount))
                new_list = new_list + ";".join(line_seperated)
            account_lines.close()
            fa = open(ACCOUNTS_FILE, "w")
            fa.write(new_list)
            fa.close()
            print("Deposit successfully done!")
        else:
            print("No account found!\n")
    else:
        print("No account found!\n")

def withdraw_amount():
    if path.exists(ACCOUNTS_FILE):
        account_id = input("Account holder id: ")
        if check_id_existence(account_id):
            amount = input("Amount to withdraw: ")
            if check_balance(account_id, int(amount)):
                print("Impossible to withdraw more than balance!\n")
            else:
                ft = open(TRANSACTIONS_FILE, "a")
                ft.write(account_id + ";" + get_date() + ";" + get_time() + ";" + "WITHDRAW" + ";" + amount + "\n")
                ft.close()
                account_lines = open(ACCOUNTS_FILE, "r")
                new_list = ""
                for line in account_lines:
                    line_seperated = line.split(";")
                    if line_seperated[0] == account_id:
                        line_seperated[3] = str(int(line_seperated[3]) - int(amount))
                    new_list = new_list + ";".join(line_seperated)
                account_lines.close()
                fa = open(ACCOUNTS_FILE, "w")
                fa.write(new_list)
                fa.close()
                print("Withdraw successfully done!")
        else:
            print("No account found!\n")
    else:
        print("No account found!\n")

def update_account():
    if path.exists(ACCOUNTS_FILE):
        account_id = input("Account holder id: ")
        if check_id_existence(account_id):
            account_name = input("Account holder name: ")
            account_phone = input("Account holder phone number: ")
            account_lines = open(ACCOUNTS_FILE, "r")
            new_list = ""
            for line in account_lines:
                line_seperated = line.split(";")
                if line_seperated[0] == account_id:
                    line_seperated[1] = account_name
                    line_seperated[2] = account_phone
                new_list = new_list + ";".join(line_seperated)
            account_lines.close()
            fa = open(ACCOUNTS_FILE, "w")
            fa.write(new_list)
            fa.close()
            print("Account updated!")
        else:
            print("No account found!\n")
    else:
        print("No account found!\n")

def delete_account():
    if path.exists(ACCOUNTS_FILE):
        account_id = input("Account holder id: ")
        if check_id_existence(account_id):
            account_lines = open(ACCOUNTS_FILE, "r")
            new_list = ""
            for line in account_lines:
                line_seperated = line.split(";")
                if line_seperated[0] != account_id:
                    new_list = new_list + ";".join(line_seperated)
            account_lines.close()
            fa = open(ACCOUNTS_FILE, "w")
            fa.write(new_list)
            fa.close()
            print("Account deleted!")
        else:
            print("No account found!\n")
    else:
        print("No account found!\n")

option = 1

while option != 0:
    print("********** BANK APP **********")
    print("1 - Open Account")
    print("2 - See All Accounts")
    print("3 - See One Account Information")
    print("4 - See One Account Transactions")
    print("5 - Deposit Amount Into An Account")
    print("6 - Withdraw Amount From An Account")
    print("7 - Update Information From An Account")
    print("8 - Close An Account")
    print("0 - Exit")
    print("******************************")
    option = int(input("Enter option: "))
    if option > 0 and option < 9:
        match option:
            case 1: create_account()
            case 2: read_all_accounts()
            case 3: read_one_account()
            case 4: read_one_account_transactions()
            case 5: deposit_amount()
            case 6: withdraw_amount()
            case 7: update_account()
            case _: delete_account()
