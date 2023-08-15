from tkinter import *
from datetime import date
from datetime import datetime
import mysql.connector
from tabulate import tabulate
from PIL import Image, ImageTk
conn = mysql.connector.connect(user='root', password='h', host='localhost', database='banker')
cursor = conn.cursor()
today = date.today()


def clear_frame():
    for widget in top.winfo_children():
        widget.destroy()


def fill_account(write):
    if write == 'Withdrawal':
        sqq = "INSERT INTO "+str(username1)+"(det, amount, date) VALUES(%s, %s, %s)"
        value = (write, '- Rs.'+str(amount), today)
        cursor.execute(sqq, value)
        conn.commit()
    elif write == 'Deposit':
        sqq = "INSERT INTO "+str(username1)+"(det, amount, date) VALUES(%s, %s, %s)"
        value = (write, '+ Rs.'+str(amount), today)
        cursor.execute(sqq, value)
        conn.commit()
    elif write == 'Transfer':
        sqq = "INSERT INTO "+str(username1)+"(det, amount, date) VALUES(%s, %s, %s)"
        value = (write+' To '+nam, '- Rs.'+str(amount), today)
        cursor.execute(sqq, value)
        conn.commit()
        sqq1 = "INSERT INTO "+str(acco)+"(det, amount, date) VALUES(%s, %s, %s)"
        value1 = (write+' From '+nam1, '+ Rs.'+str(amount), today)
        cursor.execute(sqq1, value1)
        conn.commit()
    elif write == 'Fixed Deposit':
        sqq = "INSERT INTO "+str(username1)+"(det, amount, date) VALUES(%s, %s, %s)"
        value = (write, '- Rs.'+str(amount), today)
        cursor.execute(sqq, value)
        sqq1 = "UPDATE account SET fd = '"+str(amount)+"' WHERE username = "+username
        cursor.execute(sqq1)
        conn.commit()
    elif write == 'Loan':
        sqq = "INSERT INTO "+str(username1)+"(det, amount, date) VALUES(%s, %s, %s)"
        value = (write, '+ Rs.'+str(amount), today)
        cursor.execute(sqq, value)
        conn.commit()
        sqq1 = "UPDATE account SET loan = '"+str(amount)+"' WHERE username = "+username
        cursor.execute(sqq1)
        conn.commit()


def upd(able, column, data, sp_column, sp_data):
    update = ("UPDATE "+str(able)+" SET "+str(column)+" ="+"'"+data+"'"+"WHERE "+str(sp_column)+" = "+sp_data)
    cursor.execute(update)
    conn.commit()


def bal_check(acc):
    balance_extract = ("SELECT balance from account WHERE username = "+acc)
    cursor.execute(balance_extract)
    bal = cursor.fetchone()
    balance = float(bal[0])
    return balance


def new_account():
    clear_frame()
    Label(top, text='Welcome to AHN Bank\nThanks for choosing AHN', font=('Arial Black', 12), bg='Azure').place(x=70,
                                                                                                                y=0)
    Label(top, text='Write Your First Name:', bg='Azure').place(x=10, y=50)
    Label(top, text='Write Your Last Name:', bg='Azure').place(x=10, y=80)
    Label(top, text='Enter Your Date of Birth:', bg='Azure').place(x=10, y=110)
    global dob, cust_1name_entry, cust_2name_entry
    dob = Entry(top, width=30)
    dob.place(x=150, y=110)
    Label(top, text='(dd/mm/yyyy)', bg='Azure').place(x=260, y=110)
    cust_1name_entry = Entry(top, width=30)
    cust_1name_entry.place(x=150, y=50)
    cust_2name_entry = Entry(top, width=30)
    cust_2name_entry.place(x=150, y=80)
    Button(top, text='Submit', bg='Light Steel Blue', command=age).place(x=150, y=140)


def age():
    global dater, cust_1name, cust_2name
    dater = dob.get()
    cust_1name = cust_1name_entry.get()
    cust_2name = cust_2name_entry.get()
    clear_frame()
    try:
        dater = datetime.strptime(dater, "%d/%m/%Y")
        Label(top, text='Set a Username:', bg='Azure').place(x=10, y=10)
        global username1, password1
        username1 = Entry(top, width=30)
        username1.place(x=150, y=10)
        Label(top, text='Set A password:', bg='Azure').place(x=10, y=40)
        password1 = Entry(top, width=30)
        password1.place(x=150, y=40)
        Button(top, text="Submit", command=submit, bg='Light Steel Blue').place(x=160, y=80)
    except:
        Label(top, text='Invalid Credential').pack()


def submit():
    username = username1.get()
    password = password1.get()
    clear_frame()
    cursor.execute("SELECT username FROM account")
    users = cursor.fetchall()
    if (username,) in users:
        Label(top, text='Username Taken Already', font=('Arial Black', 15), bg='Azure').pack()
    else:
        my_sql = "INSERT INTO account(username, cust_fname, cust_sname, date, password, balance, fd, loan) " \
                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        val = username, cust_1name, cust_2name, dater, password, float(0), float(0), float(0)
        cursor.execute(my_sql, val)
        value = username, float(0), today
        cursor.execute("INSERT INTO fd(username, amount, date) VALUES(%s, %s, %s)", value)
        cursor.execute("INSERT INTO loan(username, amount, date) VALUES(%s, %s, %s)", value)
        cursor.execute("CREATE TABLE " + str(username) + " (det VARCHAR(300), amount VARCHAR(300), date DATE)")
        conn.commit()
        Label(top, text='Account Created Successfully', font=('Arial Black', 15), bg='Azure').pack()
        Label(top, text=str(cust_1name)+'\nThanks For Joining AHV Bank', font=('Arial Black', 15), foreground='red',
              bg='Azure').place()


def login():
    clear_frame()
    top.geometry("300x200")
    Label(top, text='Username:', font=("Times New Roman", 12), bg='Azure').place(x=20, y=20)
    Label(top, text='Password:', font=("Times New Roman", 12), bg='Azure').place(x=20, y=50)
    global user, passw
    user = Entry(top, width=30)
    user.place(x=90, y=25)
    passw = Entry(top, width=30, show='*')
    passw.place(x=90, y=55)
    Button(top, text='Login', command=nex, bg='Light Steel Blue').place(x=140, y=90)


def nex():
    global username, password, username1, password1
    username1 = user.get()
    username = "'" + username1 + "'"
    password1 = passw.get()
    password = "'" + password1 + "'"
    top.geometry("260x140")
    cursor.execute("SELECT username FROM account")
    r = cursor.fetchall()
    cursor.execute("SELECT password FROM account WHERE username = " + username)
    p = cursor.fetchone()
    if ((username1,) in r) and ((password1,) == p):
        clear_frame()
        cursor.execute("SELECT cust_fname FROM account WHERE username = " + username)
        nam = cursor.fetchone()
        nam1 = nam[0]
        texter = 'Money\nTransfer'
        texter1 = 'Balance &\nHistory'
        Label(top, text='Welcome '+nam1, font=('Arial Black', 10), foreground='red', bg='Azure').place(x=68, y=10)
        Button(top, text='Deposit', height=2, width=10, command=deposit, bg='Light Steel Blue').place(x=10, y=50)
        Button(top, text='Withdrawal', height=2, width=10, command=withdrawal, bg='Light Steel Blue').place(x=88, y=50)
        Button(top, text='Fixed Deposit', height=2, width=10, command=fd, bg='Light Steel Blue').place(x=10, y=90)
        Button(top, text=texter, height=2, width=10, command=transfer, bg='Light Steel Blue').place(x=166, y=50)
        Button(top, text='Loan', height=2, width=10, command=loan, bg='Light Steel Blue').place(x=88, y=90)
        Button(top, text=texter1, height=2, width=10, command=history, bg='Light Steel Blue').place(x=166, y=90)
    else:
        clear_frame()
        Label(top, text='Invalid Credential', font=('Segoe Script', 10), bg='Azure').pack()


def nex_back():
    clear_frame()
    cursor.execute("SELECT cust_fname FROM account WHERE username =" + username)
    nam = cursor.fetchone()
    nam1 = nam[0]
    texter = 'Money\nTransfer'
    texter1 = 'Balance &\nHistory'
    Label(top, text='Welcome ' + nam1, font=('Arial Black', 10), foreground='red', bg='Azure').place(x=68, y=10)
    Button(top, text='Deposit', height=2, width=10, command=deposit, bg='Light Steel Blue').place(x=10, y=50)
    Button(top, text='Withdrawal', height=2, width=10, command=withdrawal, bg='Light Steel Blue').place(x=88, y=50)
    Button(top, text='Fixed Deposit', height=2, width=10, command=fd, bg='Light Steel Blue').place(x=10, y=90)
    Button(top, text=texter, height=2, width=10, command=transfer, bg='Light Steel Blue').place(x=166, y=50)
    Button(top, text='Loan', height=2, width=10, command=loan, bg='Light Steel Blue').place(x=88, y=90)
    Button(top, text=texter1, height=2, width=10, command=history, bg='Light Steel Blue').place(x=166, y=90)


def deposit():
    clear_frame()
    top.geometry('360x140')
    Label(top, text='AHN DEPOSIT CENTRE', font=('Times New Roman', 12), bg='Azure').place(x=92, y=10)
    Label(top, text='Enter Amount To Deposit:', bg='Azure').place(x=8, y=50)
    global amo
    amo = Entry(top, width=30)
    amo.place(x=152, y=50)
    Button(top, text='Deposit', command=dep, bg='Light Steel Blue').place(x=140, y=80)
    Button(top, text='Back', command=nex_back, bg='Light Steel Blue').place(x=200, y=80)


def dep():
    try:
        global amount
        amount = float(amo.get())
        bal = bal_check(username)
        global bal_update
        bal_update = str(bal + amount)
        clear_frame()
        top.geometry('250x70')
        Button(top, text='Confirm', command=depc, bg='Light Steel Blue').pack()
        Label(top, text="To Quit press above cross 'x'", bg='Azure', font=('Times New Roman', 10)).pack()
    except:
        clear_frame()
        top.geometry("360x300")
        Label(top, text='Invalid Amount', font=('Arial Black', 10), foreground='Blue', bg='Azure').pack()


def depc():
    top.geometry('300x70')
    new_bal = ("UPDATE account SET balance = '"+bal_update+"' WHERE username = "+username)
    cursor.execute(new_bal)
    conn.commit()
    Label(top, text='Your Balance is Rs.'+bal_update, font=('Times New Roman', 10), bg='Azure').pack()
    fill_account('Deposit')


def withdrawal():
    clear_frame()
    top.geometry('390x140')
    top.title('AHN Bank')
    top.iconbitmap('icon.ico')
    top['bg'] = 'Azure'
    Label(top, text='AHN WITHDRAWAL CENTRE', font=('Times New Roman', 12), bg='Azure').place(x=95, y=10)
    Label(top, text='Enter Amount To Withdraw: Rs.', bg='Azure').place(x=10, y=50)
    global amo
    amo = Entry(top, width=30)
    amo.place(x=180, y=50)
    Button(top, text='Withdraw', command=withdraw, bg='Light Steel Blue').place(x=140, y=80)


def withdraw():
    try:
        global amount
        amount = float(amo.get())
        bal = bal_check(username)
        global bal_update
        bal_update = str(bal - amount)
        global t3
        clear_frame()
        top.geometry('250x70')
        top.title('Confirmation')
        top.iconbitmap('icon.ico')
        top['bg'] = 'Azure'
        Button(top, text='Confirm', command=withdrawc, bg='Light Steel Blue').pack()
        Label(top, text="To Quit press above cross 'x'", bg='Azure', font=('Times New Roman', 10)).pack()
    except:
        clear_frame()
        top.geometry("360x300")
        top.title("AHN Bank")
        top['bg'] = 'Azure'
        Label(top, text='Invalid Amount', font=('Arial Black', 10), foreground='Blue', bg='Azure').pack()


def withdrawc():
    clear_frame()
    top.geometry('300x70')
    top.title('AHN Bank')
    top['bg'] = 'Azure'
    top.iconbitmap('icon.ico')
    new_bal = ("UPDATE account SET balance = '"+bal_update+"' WHERE username = "+username)
    cursor.execute(new_bal)
    conn.commit()
    Label(top, text='Your Balance is Rs.'+bal_update, font=('Times New Roman', 15), bg='Azure').pack()
    fill_account('Withdrawal')
    top.mainloop()


def transfer():
    clear_frame()
    cursor.execute("SELECT transfercount FROM dataset where username =" + username)
    fd_count = cursor.fetchone()
    fd_count = fd_count[0]
    cursor.execute("UPDATE dataset SET transfercount = '" + str(fd_count + 1) + "' WHERE username = " + str(username))
    conn.commit()
    top.geometry('360x200')
    top['bg'] = 'Azure'
    top.title('AHN Bank')
    top.iconbitmap('icon.ico')
    Label(top, text='AHN MONEY TRANFER CENTRE', font=('Times New Roman', 12), bg='Azure').place(x=65, y=10)
    Label(top, text='Trasferee Username:', bg='Azure').place(x=10, y=50)
    Label(top, text='Enetr Amount To Deposit:', bg='Azure').place(x=10, y=80)
    global account, amo
    account = Entry(top, width=30)
    amo = Entry(top, width=30)
    account.place(x=150, y=50)
    amo.place(x=160, y=80)
    Button(top, text='Transfer', command=transf, bg='Light Steel Blue').place(x=140, y=110)


def transf():
    global amount, acco
    amount = float(amo.get())
    acco = account.get()
    clear_frame()
    print("t_amount")
    cursor.execute("SELECT transferamount FROM dataset where username =" + username)
    t_amount = cursor.fetchone()
    t_amount = t_amount[0]
    cursor.execute(
        "UPDATE dataset SET transferamount = '" + str(t_amount + amount) + "' WHERE username = " + str(username))
    conn.commit()
    if bal_check(username) > amount:
        aco = "'" + acco + "'"
        try:
            msq = "SELECT cust_fname FROM account WHERE username = '" + str(acco) + "'"
            cursor.execute(msq)
            global nam
            nam = cursor.fetchone()
            nam = nam[0]
            msq1 = "SELECT cust_fname FROM account WHERE username = " + str(username)
            cursor.execute(msq1)
            global nam1
            nam1 = cursor.fetchone()
            nam1 = nam1[0]
            bal = bal_check(username)
            bal1 = bal_check(aco)
            global bal_update1, bal_update2
            bal_update1 = str(bal - amount)
            bal_update2 = str(bal1 + amount)
            top.geometry('300x70')
            top.title('Confirmation')
            top.iconbitmap('icon.ico')
            top['bg'] = 'Azure'
            Button(top, text='Confirm', command=transfc, bg='Light Steel Blue').pack()
            Label(top, text="Transfering to " + nam + " of Rs." + str(amount), font=('Arial Black', 10),
                  foreground='Blue', bg='Azure').pack()
            Label(top, text="To Quit press above cross 'x'", bg='Azure').pack()
        except:
            top.geometry('300x70')
            top.title('AHN Bank')
            top.iconbitmap('icon.ico')
            top['bg'] = 'Azure'
            Label(top, text='No Account Named: ' + str(aco) + ' found', font=('Arial Black', 10), foreground='Blue',
                  bg='Azure').pack()
    else:
        top.geometry('150x70')
        top.title('AHN Bank')
        top.iconbitmap('icon.ico')
        top['bg'] = 'Azure'
        Label(top, text='Insufficient Balance', font=('Arial Black', 10), foreground='Blue', bg='Azure').pack()


def transfc():
    clear_frame()
    top.geometry('300x70')
    top.title('AHN Bank')
    top.iconbitmap('icon.ico')
    top['bg'] = 'Azure'
    new_bal = ("UPDATE account SET balance = '"+bal_update1+"' WHERE username = "+username)
    cursor.execute(new_bal)
    conn.commit()
    new_ball = ("UPDATE account SET balance = '"+bal_update2+"' WHERE username = '"+acco+"'")
    cursor.execute(new_ball)
    conn.commit()
    Label(top, text='Your Balance is Rs.'+bal_update1, font=('Times New Roman', 10), bg='Azure').pack()
    top.mainloop()
    fill_account('Transfer')


def fd():
    clear_frame()
    cursor.execute("SELECT fdcount FROM dataset where username =" + username)
    fd_count = cursor.fetchone()
    fd_count = fd_count[0]
    cursor.execute("UPDATE dataset SET fdcount = '" + str(fd_count + 1) + "' WHERE username = " + str(username))
    conn.commit()
    top.geometry('360x150')
    top.title('AHN Bank')
    top['bg'] = 'Azure'
    top.iconbitmap('icon.ico')
    Label(top, text='AHN Fix Deposit CENTRE\nInterest rate: 6% per annum', font=('Times New Roman', 12), bg='Azure').place(x=75, y=10)
    Label(top, text='Enetr Amount To Deposit:', bg='Azure').place(x=10, y=60)
    global amo
    amo = Entry(top, width=30)
    amo.place(x=150, y=60)
    Label(top, text='To Break Fixed Deposit: ', bg='Azure').place(x=10, y=125)
    Label(top, text='***Only One FD at a time', bg='Azure').place(x=200, y=90)
    Button(top, text='Break', command=fdb, bg='Light Steel Blue').place(x=150, y=120)
    Button(top, text='Deposit', command=fds, bg='Light Steel Blue').place(x=140, y=90)


def fdb():
    clear_frame()
    top.geometry('360x150')
    top.title('AHN Bank')
    top.iconbitmap('icon.ico')
    top['bg'] = 'Azure'
    ms5 = "SELECT fd from account WHERE username = "+str(username)
    cursor.execute(ms5)
    global fd_amount
    fd_amount = float(cursor.fetchone()[0])
    mss1 = "SELECT date from fd WHERE username = "+str(username)
    cursor.execute(mss1)
    global d
    d = cursor.fetchone()
    d = d[0]
    global fdn
    fdn = ((int((today - d).days))*fd_amount*(6/100)*(1/360))+ fd_amount
    if fd_amount == 0:
        Label(top, text='No Fixed Deposit Sanctioned', font=('Times New Roman', 9), bg='Azure').pack()
    else:
        Label(top, text='Confirm To Break Fixed Deposit of Amount Rs.'+str(fdn), bg='Azure').pack()
        Button(top, text='Confirm', command=fdbc, bg='Light Steel Blue').pack()


def fdbc():
    clear_frame()
    top.title('AHN Bank')
    top.iconbitmap('icon.ico')
    top.geometry('250x70')
    top['bg'] = 'Azure'
    mq = "UPDATE account SET fd = '"+str(0.0)+"' WHERE username = "+str(username)
    mqq = "UPDATE account SET balance = '"+str(bal_check(username)+fdn)+"' WHERE username = "+str(username)
    cursor.execute(mq)
    cursor.execute(mqq)
    conn.commit()
    Label(top, text='Fixed Deposit of amount Rs.'+str(fdn)+' Received\nNew Balance is Rs.'+str(bal_check(username)),
          font=('Times New Roman', 12), bg='Azure').pack()
    sqq = "INSERT INTO "+str(username)+"(det, amount, date) VALUES(%s, %s, %s)"
    value = 'Fixed Deposit Break', '+ Rs.'+str(fdn), today
    cursor.execute(sqq, value)
    conn.commit()


def fds():
    clear_frame()
    try:
        global amount
        amount = float(amo.get())
        top.geometry('250x70')
        top.title('Confirmation')
        top.iconbitmap('icon.ico')
        top['bg'] = 'Azure'
        bal = float(bal_check(username))
        ms5 = "SELECT fd from account WHERE username = "+str(username)
        cursor.execute(ms5)
        fd_amount = float(cursor.fetchone()[0])
        if fd_amount == 0.00:
            if bal > amount:
                global bal_update
                bal_update = str(bal - amount)
                Button(top, text='Confirm', command=fdc, bg='Light Steel Blue').pack()
                Label(top, text="To Quit press above cross 'x'", bg='Azure').pack()
            else:
                Label(top, text="Insufficient Balance in Your Account Only Rs."+str(bal), font=('Times New Roman', 12), bg='Azure').pack()
        else:
            Label(top, text="Already a Fixed Deposit of Amount Rs. "+str(fd_amount), font=('Times New Roman', 12), bg='Azure').pack()
    except:
        t3 = Tk()
        t3.geometry("360x300")
        t3.title("AHN Bank")
        t3.iconbitmap('icon.ico')
        t3['bg'] = 'Azure'
        Label(t3, text='Invalid Amount', font=('Arial Black', 10), foreground='Blue', bg='Azure').pack()


def fdc():
    clear_frame()
    top.geometry('300x70')
    top.title('AHN Bank')
    top.iconbitmap('icon.ico')
    top['bg'] = 'Azure'
    new_bal = ("UPDATE account SET balance = '"+bal_update+"' WHERE username = "+username)
    cursor.execute(new_bal)
    conn.commit()
    fill = "UPDATE fd SET amount = '"+str(amount)+"' WHERE username = "+username
    cursor.execute(fill)
    fil2 = "UPDATE fd SET date = '"+str(today)+"' WHERE username = "+username
    cursor.execute(fil2)
    conn.commit()
    Label(top, text='Your Balance is Rs.'+bal_update, font=('Times New Roman', 10), bg='Azure').pack()
    top.mainloop()
    fill_account('Fixed Deposit')


def loan():
    clear_frame()
    cursor.execute("SELECT lcount FROM dataset where username =" + username)
    fd_count = cursor.fetchone()
    fd_count = fd_count[0]
    cursor.execute("UPDATE dataset SET lcount = '" + str(fd_count+1) + "' WHERE username = " + str(username))
    conn.commit()
    top.geometry('360x160')
    top.title('AHN Bank')
    top.iconbitmap('icon.ico')
    top['bg'] = 'Azure'
    Label(top, text='AHN LOAN CENTRE\nInterest rate: 9% per annum', font=('Times New Roman', 12), bg='Azure').place(x=75, y=10)
    Label(top, text='Enetr Amount of Loan:', bg='Azure').place(x=10, y=60)
    global amo
    amo = Entry(top, width=30)
    amo.place(x=150, y=60)
    Label(top, text='To Repay Loan: ', bg='Azure').place(x=10, y=125)
    Label(top, text='***Only One Loan at a time', bg='Azure').place(x=200, y=90)
    Button(top, text='Repay', command=loanb, bg='Light Steel Blue').place(x=150, y=120)
    Button(top, text='Santion', command=loans, bg='Light Steel Blue').place(x=140, y=90)


def loanb():
    clear_frame()
    top.geometry('360x150')
    top.title('AHN Bank')
    top.iconbitmap('icon.ico')
    top['bg'] = 'Azure'
    mss = "SELECT loan from account WHERE username = "+str(username)
    cursor.execute(mss)
    global l_amount, d, ldn
    l_amount = cursor.fetchone()
    l_amount = float(l_amount[0])
    mss1 = "SELECT date from loan WHERE username = "+str(username)
    cursor.execute(mss1)
    d = cursor.fetchone()
    d = d[0]
    ldn = (int((d - today).days))*l_amount*(9/100)*(1/360)
    if l_amount == 0:
        Label(top, text='No Loan Sanctioned', font=('Times New Roman', 9), bg='Azure').pack()
    else:
        Label(top, text='How much To Pay: ', bg='Azure').place(x=10, y=30)
        global to_pay
        to_pay = Entry(top, width=25)
        to_pay.place(x=100, y=30)
        Label(top, text='Loan of Amount Rs.'+str(ldn), bg='Azure').place(x=10, y=70)
        Button(top, text='Confirm', command=loanbc, bg='Light Steel Blue').place(x=150,y=90)


def loanbc():
    clear_frame()
    try:
        to_pa = float(to_pay.get())
        top.title('AHN Bank')
        top.iconbitmap('icon.ico')
        top['bg'] = 'Azure'
        mq = "UPDATE account SET loan = '"+str(ldn - to_pa)+"' WHERE username = "+str(username)
        mqq = "UPDATE account SET balance = '"+str(bal_check(username) - to_pa)+"' WHERE username = "+str(username)
        cursor.execute(mq)
        cursor.execute(mqq)
        conn.commit()
        Label(top, text='Loan of amount Rs.'+str(to_pa)+' Payed\nNew Balance is Rs.'+str(bal_check(username)), font=('Times New Roman', 12), bg='Azure').pack()
        s1 = "UPDATE loan SET amount = '"+str(ldn - to_pa)+"' WHERE username = "+str(username)
        s2 = "UPDATE loan SET date = '"+str(today)+"' WHERE username = "+str(username)
        cursor.execute(s1)
        cursor.execute(s2)
        sqq = "INSERT INTO "+str(username)+"(det, amount, date) VALUES(%s, %s, %s)"
        value = 'Loan Repaid', '- Rs.'+str(to_pa), today
        cursor.execute(sqq, value)
        conn.commit()
    except:
        top.geometry("360x300")
        top.title("AHN Bank")
        top.iconbitmap('icon.ico')
        top['bg']='Azure'
        Label(top, text='Invalid Amount', font=('Arial Black', 10), foreground='Blue', bg='Azure').pack()


def loans():
    global amount
    amount = float(amo.get())
    bal = float(bal_check(username))
    mss = "SELECT loan from account WHERE username = "+str(username)
    cursor.execute(mss)
    l_amount = float(cursor.fetchone()[0])
    global t3
    clear_frame()
    top.geometry('270x70')
    top.title('Confirmation')
    top['bg'] = 'Azure'
    top.iconbitmap('icon.ico')
    try:
        if l_amount == 0.00:
            if bal*10 >= amount:
                global bal_update
                bal_update = str(bal + amount)
                Button(top, text='Confirm', command=loanc, bg='Light Steel Blue').pack()
                Label(top, text="To Quit press above cross 'x'", bg='Azure').pack()
            else:
                Label(top, text="Insufficient Balance in Your Account Only Rs."+str(bal), font=('Times New Roman', 12), bg='Azure').pack()
        else:
            Label(top, text="Already a loan of Rs."+str(l_amount), font=('Times New Roman', 12), bg='Azure').pack()
    except:
        Label(top, text='Invalid Amount', font=('Arial Black', 10), foreground='Blue', bg='Azure').pack()


def loanc():
    top.geometry('300x70')
    top.title('AHN Bank')
    top['bg'] = 'Azure'
    top.iconbitmap('icon.ico')
    top.destroy()
    new_bal = ("UPDATE account SET balance = '"+bal_update+"' WHERE username = "+username)
    cursor.execute(new_bal)
    conn.commit()
    Label(top, text='Your Balance is Rs.'+bal_update, font=('Times New Roman', 10), bg='Azure').pack()
    top.mainloop()
    fill_account('Loan')
    fill = "UPDATE loan SET amount = '"+str(amount)+"' WHERE username = "+username
    cursor.execute(fill)
    fil2 = "UPDATE loan SET date = '"+str(today)+"' WHERE username = "+username
    cursor.execute(fil2)
    conn.commit()


def history():
    clear_frame()
    top.title('AHN Bank')
    top.geometry('600x800')
    top['bg'] = 'Azure'
    top.iconbitmap('icon.ico')

    h1 = ("SELECT fd FROM account where username ="+username)
    cursor.execute(h1)
    fd_amo = cursor.fetchone()
    fd_amo = fd_amo[0]
    h2 = ("SELECT loan FROM account where username ="+username)
    cursor.execute(h2)
    loan_amo = cursor.fetchone()
    loan_amo = loan_amo[0]
    h3 = ("SELECT date FROM fd where username ="+username)
    cursor.execute(h3)
    fd_date = cursor.fetchone()
    h4 = ("SELECT date FROM loan where username ="+username)
    cursor.execute(h4)
    loan_date = cursor.fetchone()
    if loan_amo == 0.0 and fd_amo == 0.0:
        Label(top, text='\n\nBalance account:  Rs. '+str(bal_check(username))+'\n\n\nNo Loan Due\n\n\nNo Fixed Deposit',
              font=('Segoe Script', 12), bg='Azure').pack()
    elif loan_amo == 0.0:
        Label(top, text='\n\nBalance account:  Rs. '+str(bal_check(username))+'\n\n\nNo Loan Due\n\n\nFixed Deposit '
            'amount:Rs. ' + str(fd_amo)+'    issued on  '+str(fd_date[0]), bg='Azure', font=('Segoe Script', 12)).pack()
    elif fd_amo == 0.0:
        Label(top, text='\n\nBalance account:  Rs. '+str(bal_check(username))+'\n\n\nLoan amount:   Rs. '
                        +str(loan_amo)+'    issued on '+str(loan_date[0])+'\n\n\nNo Fixed Deposit'
              , font=('Segoe Script', 12), bg='Azure').pack()
    else:
        Label(top, text='\n\nBalance account:  Rs. '+str(bal_check(username))+'\n\n\nLoan amount:   Rs. '
                        +str(loan_amo)+'    issued on '+
                       str(loan_date[0])+'\n\n\nFixed Deposit amount:   Rs. '
                        +str(fd_amo)+'    issued on  '+str(fd_date[0]),
              font=('Segoe Script', 12), bg='Azure').pack()
    cursor.execute("SELECT det, amount, date FROM "+str(username1))
    tabl = cursor.fetchall()
    history_table = (tabulate(tabl[::-1], headers=['      Detail      ', '      Amount      ', '    Date     '], tablefmt='grid'))
    scrollbar = Scrollbar(top)
    scrollbar.pack(side=RIGHT, fill=Y)

    mylist = Listbox(top, yscrollcommand=scrollbar.set)
    mylist.insert(history_table)

    mylist.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command=mylist.yview)
    top.mainloop()


top = Tk()
top.geometry('380x200')
img = Image.open("iconer.png")
pi = img.resize((110, 80))
pic = ImageTk.PhotoImage(pi)
top.title('AHN Bank')
top.iconbitmap('icon.ico')
top['bg'] = 'Azure'
Label(top, image=pic).pack()
Label(top, text='Welcome to AHN Bank', font=("Times New Roman", 20), bg='Azure').pack()
Button(top, text="New Account", bg='Light Steel Blue', command=new_account).pack()
Button(top, text="Login", bg='Light Steel Blue', command=login).pack()
top.mainloop()
