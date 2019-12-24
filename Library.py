from datetime import *
from tkinter import *
from tkinter import messagebox
from sqlite3 import *

global conn, fineWin1, uid, eUID, payFineWin, retWin1, eBID, bks, bn, un
bn = 25
un = 10
def create_conn(db_file):
    try:
        conn = connect(db_file)
        messagebox.showinfo('LMS: Message','Connected To Database!')
        return conn
    except Error as e:
        messagebox.showerror('LMS: Error','Could Not Connect To Database!')
    return None


def finePaid () :
    global payFineWin, uid, conn
    with conn :
        cur = conn.cursor()
        query = """UPDATE USERINFO
        SET fine=?
        WHERE userID=?"""
        cur.execute(query,(0,uid))
        cur.execute("""SELECT booksBorrowed FROM USERINFO
        WHERE userID=?;""",(uid,))
        rn = cur.fetchall()
        for j in rn :
            bb = j[0]
        if bb == 1 :
            cur.execute("""SELECT days1 FROM USERBOOKS2
            WHERE userID=?;""",(uid,))
            d = cur.fetchall()
            for k in d :
                for l in k :
                    if l > 7 :
                        cur.execute("""UPDATE USERBOOKS2
                        SET days1=?
                        WHERE userID=?;""",(0,uid,))
        if bb == 2 :
            z = 0
            cur.execute("""SELECT days1, days2 FROM USERBOOKS2
            WHERE userID=?;""",(uid,))
            d = cur.fetchall()
            for k in d :
                for l in k :
                    if l > 7 :
                        if z == 0 :
                            cur.execute("""UPDATE USERBOOKS2
                            SET days1=?
                            WHERE userID=?;""",(0,uid,))
                        if z == 1 :
                            cur.execute("""UPDATE USERBOOKS2
                            SET days2=?
                            WHERE userID=?;""",(0,uid,))
                        z = z + 1
        if bb == 3 :
            z = 0
            cur.execute("""SELECT days1, days2, days3 FROM USERBOOKS2
            WHERE userID=?;""",(uid,))
            d = cur.fetchall()
            for k in d :
                for l in k :
                    if l > 7 :
                        if z == 0 :
                            cur.execute("""UPDATE USERBOOKS2
                            SET days1=?
                            WHERE userID=?;""",(0,uid,))
                        if z == 1 :
                            cur.execute("""UPDATE USERBOOKS2
                            SET days2=?
                            WHERE userID=?;""",(0,uid,))
                        if z == 2 :
                            cur.execute("""UPDATE USERBOOKS2
                            SET days3=?
                            WHERE userID=?;""",(0,uid,))
                        z = z + 1
    messagebox.showinfo("LMS: Message","Fine Paid!")
    payFineWin.destroy()


def checkPayFine() :
    global fineWin1, uid, eUID, payFineWin
    uid = eUID.get()
    if not ( uid.isdigit() ) :
        messagebox.showerror('LMS','INVALID ENTRY!')
        fineWin1.destroy()
        pfWin()
        return
    if uid == '' :
        messagebox.showwarning('LMS','FIELD EMPTY!')
        fineWin1.destroy()
        pfWin()
        return
    if int(uid) > un or int(uid) < 1 :
        messagebox.showwarning('LMS','INVALID USER ID!')
        fineWin1.destroy()
        pfWin()
        return
    try :
        fineWin1.destroy()
        fine1 = retrieveFine(uid)
        payFineWin = Tk()
        payFineWin.geometry('200x100')
        payFineWin.title('PAY FINE')
        l = Label(payFineWin, text=('Fine To Be Paid: Rs.'+str(fine1)))
        l.place(x=35, y=20)
        payBt = Button(payFineWin, text='PAY', command=finePaid)
        payBt.place(x=75, y=60)
        payFineWin.mainloop()
    except UnboundLocalError :
         pass


def retrieveFine (uid) :
    global conn
    cur = conn.cursor()
    cur.execute("SELECT fine FROM USERINFO WHERE userID=?",(uid,))
    fine1=cur.fetchall()
    for i in fine1 :
        for j in i :
            fineAmt = j
    return fineAmt


def pfWin () :
    global fineWin1, eUID
    fineWin1 = Tk()
    fineWin1.title('PAY FINE')
    fineWin1.geometry('200x100')
    labelUID = Label(fineWin1, text='ENTER USER ID: ')
    labelUID.place(x=10, y=20)
    eUID = Entry(fineWin1)
    eUID.place(x=120, y=18, width=60)
    checkFineBt = Button(fineWin1, text='ENTER', command=checkPayFine)
    checkFineBt.place(x=65, y=60)
    fineWin1.mainloop()


def borrowBK1 () :
    global brWin1, eUID
    brWin1 = Tk()
    brWin1.title('ISSUE')
    brWin1.geometry('200x100')
    labelUID = Label(brWin1, text='ENTER USER ID: ')
    labelUID.place(x=10, y=20)
    eUID = Entry(brWin1)
    eUID.place(x=120, y=18, width=60)
    borrowBt = Button(brWin1, text='ENTER', command=borrowBK2)
    borrowBt.place(x=65, y=60)
    brWin1.mainloop()


def borrowBK2 () :
    global eUID, uid, brWin1, brWin2, eBID
    uid = eUID.get()
    if not ( uid.isdigit() ) :
        messagebox.showerror('LMS','INVALID ENTRY!')
        brWin1.destroy()
        borrowBK1()
        return
    if uid == '' :
        messagebox.showwarning('LMS','FIELD EMPTY!')
        brWin1.destroy()
        borrowBK1()
        return
    if int(uid) > un or int(uid) < 1 :
        messagebox.showwarning('LMS','INVALID USER ID!')
        brWin1.destroy()
        borrowBK1()
        return
    brWin1.destroy()
    avail = checkUserAvail(uid)
    if avail == 1 :
        brWin2 = Tk()
        brWin2.geometry('200x100')
        brWin2.title('ISSUE')
        labelBID = Label(brWin2, text='ENTER BOOK ID: ')
        labelBID.place(x=10, y=20)
        eBID = Entry(brWin2)
        eBID.place(x=120, y=18, width=60)
        borrowBt = Button(brWin2, text='ISSUE', command=borrowBK3)
        borrowBt.place(x=65, y=60)
    elif avail == 2 :
        messagebox.showwarning('LMS: Message', 'Three Books Are Already Issued!')
    elif avail == 3 :
        messagebox.showwarning('LMS: Message', 'Pay Fine First!')


def checkUserAvail(uid) :
    global conn
    cur = conn.cursor()
    cur.execute("""SELECT booksBorrowed, fine FROM USERINFO
    WHERE userID=?""",(uid,))
    inf = cur.fetchall()
    for i in inf :
        bb = i[0]
        fn = i[1]
    if bb > 2 :
        return 2
    elif fn > 99 :
        return 3
    else :
        return 1         


def borrowBK3 () :
    global uid, eBID, bid, conn, brWin2
    bid = eBID.get()
    if not ( bid.isdigit() ) :
        messagebox.showerror('LMS','INVALID ENTRY!')
        brWin2.destroy()
        borrowBK1()
        return
    if bid == '' :
        messagebox.showerror('LMS',"FIELD EMPTY!")
        brWin2.destroy()
        borrowBK1()
        return
    if int(bid) < 1 or int(bid) > bn :
        messagebox.showerror('LMS',"INVALID BOOK ID!")
        brWin2.destroy()
        borrowBK1()
        return
    brWin2.destroy()
    with conn :
        cur = conn.cursor()
        cur.execute("""SELECT copies FROM BOOKS
        WHERE bookID = ?;""",(bid,))
        bc = cur.fetchall()
        for i in bc :
            for j in i :
                bc = j
        if bc > 0 :
            cur.execute("""SELECT book1, book2, booK3 FROM USERBOOKS1
            WHERE userID =?""",(uid,))
            d = cur.fetchall()
            for i in d:
                if i[0] == None :
                    cur.execute("""UPDATE USERBOOKS1
                    SET book1 = ?
                    WHERE userID = ?;""",(bid, uid,))
                    cur.execute("""UPDATE USERBOOKS2
                    SET days1 = ?
                    WHERE userID = ?;""",(0, uid,))
                elif i[1] == None :
                    cur.execute("""UPDATE USERBOOKS1
                    SET book2 = ?
                    WHERE userID = ?;""",(bid, uid,))
                    cur.execute("""UPDATE USERBOOKS2
                    SET days2 = ?
                    WHERE userID = ?;""",(0, uid,))
                elif i[2] == None :
                    cur.execute("""UPDATE USERBOOKS1
                    SET book3 = ?
                    WHERE userID = ?;""",(bid, uid,))
                    cur.execute("""UPDATE USERBOOKS2
                    SET days3 = ?
                    WHERE userID = ?;""",(0, uid,))
            cur.execute("""UPDATE BOOKS
            SET copies = copies - 1
            WHERE bookID = ?;""",(bid,))
            cur.execute("""UPDATE USERINFO
            SET booksBorrowed = booksBorrowed + 1
            WHERE userID = ?;""",(uid,))
            messagebox.showinfo('LMS: Message','Book Issued!')
        else :
            messagebox.showerror("LMS: Message","Sorry, No Copies Left!") 


def returnBK1 () :
    global retWin1, eUID, eBID
    retWin1 = Tk()
    retWin1.title('RETURN')
    retWin1.geometry('200x125')
    labelUID = Label(retWin1, text='ENTER USER ID: ')
    labelUID.place(x=10, y=20)
    eUID = Entry(retWin1)
    eUID.place(x=120, y=18, width=60)
    labelBID = Label(retWin1, text='ENTER BOOK ID: ')
    labelBID.place(x=12, y=50)
    eBID = Entry(retWin1)
    eBID.place(x=120, y=48, width=60)
    retBt = Button(retWin1, text='RETURN', command=returnBK2)
    retBt.place(x=65, y=85)
    retWin1.mainloop()


def returnBK2 () :
    global retWin1, eUID, eBID, conn
    uid = eUID.get()
    bid = eBID.get()
    if not ( uid.isdigit() and bid.isdigit() ) :
        messagebox.showerror('LMS','INVALID ENTRY!')
        retWin1.destroy()
        returnBK1()
        return
    if uid == '' or bid == '' :
        messagebox.showwarning('LMS',"FIELDS EMPTY!")
        retWin1.destroy()
        returnBK1()
        return
    if int(uid) < 0 or int(uid) > un :
        messagebox.showerror('LMS','INVALID USER ID!')
        retWin1.destroy()
        returnBK1()
        return
    if int(bid) < 0 or int(bid) > bn :
        messagebox.showerror('LMS','INVALID BOOK ID!')
        retWin1.destroy()
        returnBK1()
        return
    retWin1.destroy()
    dict1 = {
        'one' : None ,
        'two' : uid
    }
    with conn :
        bk = 0
        cur = conn.cursor()
        cur.execute("""SELECT book1, book2, book3 FROM USERBOOKS1
        WHERE userID=?""",(uid,))
        d = cur.fetchall()
        for i in d :
            for j in i :
                if int(bid) == j :
                    bk = i.index(j) + 1
        if bk == 0 :
            messagebox.showerror('LMS','INVALID BOOK ID!')
        if bk == 1 :
            cur.execute("""UPDATE USERBOOKS1
            SET book1 = ?
            WHERE userID=?""",list(dict1.values()))
            cur.execute("""UPDATE USERBOOKS2
            SET days1 = ?
            WHERE userID=?""",list(dict1.values()))
        if bk == 2 :
            cur.execute("""UPDATE USERBOOKS1
            SET book2 = ?
            WHERE userID=?""",list(dict1.values()))
            cur.execute("""UPDATE USERBOOKS2
            SET days2 = ?
            WHERE userID=?""",list(dict1.values()))
        if bk == 3 :
            cur.execute("""UPDATE USERBOOKS1
            SET book3 = ?
            WHERE userID=?""",list(dict1.values()))
            cur.execute("""UPDATE USERBOOKS2
            SET days3 = ?
            WHERE userID=?""",list(dict1.values()))
        cur.execute("""UPDATE USERINFO
        SET booksBorrowed = booksBorrowed - 1
        WHERE userID=?""",(uid,))
        cur.execute("""UPDATE BOOKS
        SET copies = copies + 1
        WHERE bookID=?""",(bid,))
    messagebox.showinfo('LMS', 'BOOK RETURNED!')


def bkSearch1 () :
    global bks, eBT
    bks = Tk()
    bks.title('SEARCH')
    bks.geometry('280x100')
    labelBT = Label(bks, text='ENTER BOOK TITLE : ')
    labelBT.place(x=10, y=20)
    eBT = Entry(bks)
    eBT.place(x=140, y=18, width=120)
    srchBt = Button(bks, text='SEARCH', command=bkSearch2)
    srchBt.place(x=100, y=60)
    bks.mainloop()


def bkSearch2 () :
    global bks, eBT, conn
    bktitle = eBT.get()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM BOOKS
    WHERE title = ?""",(bktitle,))
    d = cur.fetchall()
    if len(d) == 0 :
        messagebox.showerror('LMS', 'BOOK NOT FOUND!')
        bks.destroy()
    else :
        bks.destroy()
        p = d[0]
        bks2 = Tk()
        bks2.title('BOOK DETAILS')
        bks2.geometry('250x140')
        tLabel1 = Label(bks2, text='  TITLE    :')
        tLabel1.place(x=10, y=20)
        tLabel2 = Label(bks2, text=p[1].upper())
        tLabel2.place(x=75, y=20)
        idLabel1 = Label(bks2, text='     ID      :')
        idLabel1.place(x=10 , y=40)
        idLabel2 = Label(bks2, text=p[0])
        idLabel2.place(x=75, y=40)
        aLabel1 = Label(bks2, text='AUTHOR  :')
        aLabel1.place(x=9, y=60)
        aLabel2 = Label(bks2, text=p[2].upper())
        aLabel2.place(x=75, y=60)
        cLabel1 = Label(bks2, text='COPIES   :')
        cLabel1.place(x=11, y=80)
        cLabel2 = Label(bks2, text=p[3])
        cLabel2.place(x=75, y=80)
        okBt = Button(bks2, text='OK', command=bks2.destroy)
        okBt.place(x=100, y= 100)
        bks2.mainloop()


def reIssue1 () :
    global conn, reIsWin1, eUID, eBID
    reIsWin1 = Tk()
    reIsWin1.title('RETURN')
    reIsWin1.geometry('200x125')
    labelUID = Label(reIsWin1, text='ENTER USER ID: ')
    labelUID.place(x=10, y=20)
    eUID = Entry(reIsWin1)
    eUID.place(x=120, y=18, width=60)
    labelBID = Label(reIsWin1, text='ENTER BOOK ID: ')
    labelBID.place(x=12, y=50)
    eBID = Entry(reIsWin1)
    eBID.place(x=120, y=48, width=60)
    reIssueBt = Button(reIsWin1, text='RETURN', command=reIssue2)
    reIssueBt.place(x=65, y=85)
    reIsWin1.mainloop()

def reIssue2 () :
    global conn,reIsWin1, eUID, eBID
    flag = 0
    uid = eUID.get()
    bid = eBID.get()
    if not ( uid.isdigit() and bid.isdigit() ) :
        messagebox.showerror('LMS','INVALID ENTRY!')
        reIsWin1.destroy()
        reIssue1()
        return
    if uid == '' or bid == '' :
        messagebox.showwarning('LMS',"FIELDS EMPTY!")
        reIsWin1.destroy()
        reIssue1()
        return
    if int(uid) < 0 or int(uid) > un :
        messagebox.showerror('LMS','INVALID USER ID!')
        reIsWin1.destroy()
        reIssue1()
        return
    if int(bid) < 0 or int(bid) > bn :
        messagebox.showerror('LMS','INVALID BOOK ID!')
        reIsWin1.destroy()
        reIssue1()
        return
    with conn :
        cur = conn.cursor()
        cur.execute("""SELECT book1, book2, book3 FROM USERBOOKS1
        WHERE userID = ?""",(uid,))
        d = cur.fetchall()
        for i in d :
            for j in i :
                if j == int(bid) :
                    flag = 1
                    cl = i.index(j) + 1
                    break
        if flag == 0 :
            reIsWin1.destroy()
            messagebox.showerror('LMS','INVALID BOOK ID!')
        elif cl == 1 :
            cur.execute("""UPDATE USERBOOKS2
            SET days1 = ?
            WHERE userID = ?""",(0,uid,))
            reIsWin1.destroy()
            messagebox.showinfo('LMS','BOOK RETURNED!')
        elif cl == 2 :
            cur.execute("""UPDATE USERBOOKS2
            SET days2 = ?
            WHERE userID = ?""",(0,uid,))
            reIsWin1.destroy()
            messagebox.showinfo('LMS','BOOK RETURNED!')
        elif cl == 3 :
            cur.execute("""UPDATE USERBOOKS2
            SET days3 = ?
            WHERE userID = ?""",(0,uid,))
            reIsWin1.destroy()
            messagebox.showinfo('LMS','BOOK RETURNED!')


def updateFine (diff) :
    global conn
    with conn :
        cur = conn.cursor()
        cur.execute("""SELECT userID from USERINFO;""")
        rn = cur.fetchall()
        maxID = 0
        for i in rn :
            maxID = max(i)
        for i in range(1,maxID+1) :
            cur.execute("""SELECT booksBorrowed FROM USERINFO
            WHERE userID=?;""",(i,))
            rn = cur.fetchall()
            for j in rn :
                bb = j[0]
            if bb == 1 :
                cur.execute("""UPDATE USERBOOKS2
                SET days1=days1+?
                WHERE userID=?;""",(diff,i,))
                cur.execute("""SELECT days1 FROM USERBOOKS2
                WHERE userID=?;""",(i,))
                d = cur.fetchall()
                for k in d :
                    for l in k :
                        if l > 7 :
                            fnd = l - 7
                            cur.execute("""UPDATE USERINFO
                            SET fine = ?
                            WHERE userID = ?;""",(fnd*10 , i,))
            if bb == 2 :
                cur.execute("""UPDATE USERBOOKS2
                SET days1=days1+? ,
                days2=days2+?
                WHERE userID=?;""",(diff,diff,i,))
                fnd=0
                cur.execute("""SELECT days1, days2 FROM USERBOOKS2
                WHERE userID=?;""",(i,))
                d = cur.fetchall()
                for k in d :
                    for l in k :
                        if l > 7 :
                            fnd = fnd + (l-7)
                cur.execute("""UPDATE USERINFO
                SET fine = ?
                WHERE userID = ?;""",(fnd*10 , i,))
            if bb == 3 :
                cur.execute("""UPDATE USERBOOKS2
                SET days1=days1+?,
                days2=days2+?,
                days3=days3+?
                WHERE userID=?;""",(diff,diff,diff,i,))
                fnd=0
                cur.execute("""SELECT days1, days2 FROM USERBOOKS2
                WHERE userID=?;""",(i,))
                d = cur.fetchall()
                for k in d :
                    for l in k :
                        if l > 7 :
                            fnd = fnd + (l-7)
                cur.execute("""UPDATE USERINFO
                SET fine = ?
                WHERE userID = ?;""",(fnd*10 , i,))


def updateDate(y1, m1, d1) :
    global conn
    with conn :
        cur = conn.cursor()
        cur.execute("""UPDATE LASTUPDATE
        SET year = ? ,
        month = ? ,
        day = ?
        WHERE pointer = ?;""",(y1,m1,d1,1,))


home = Tk()
home.geometry('480x325')
home.title('Library Management System')
file1=PhotoImage(file='pic.png')
picLabel = Label(home,image=file1, width=200,height=300)
picLabel.place(x=0,y=5)
brBt = Button(home, text='ISSUE' ,height=2, width=20, command=borrowBK1)
brBt.place(x=230,y=25)
rtBt = Button(home, text='RETURN' ,height=2, width=20, command=returnBK1)
rtBt.place(x=230,y=90)
srBt = Button(home, text='SEARCH' ,height=2, width=20, command=bkSearch1)
srBt.place(x=230,y=155)
pfBt = Button(home, text='PAY FINE' ,height=2, width=20, command=pfWin)
pfBt.place(x=230,y=220)
reIsBt = Button(home, text='RE-ISSUE', command=reIssue1)
reIsBt.place(x=250,y=280)
exBt = Button(home, text='EXIT', command=home.destroy)
exBt.place(x=380,y=280)
conn = create_conn('library.db')
today=date.today()
y = today.year
m = today.month
d = today.day
cur = conn.cursor()
query = """SELECT year, month, day
FROM LASTUPDATE
WHERE pointer = 1"""
cur.execute(query)
dt=cur.fetchall()
oy = dt[0][0]
om = dt[0][1]
od = dt[0][2]
diff = 0
if (oy!=y) or (om!=m) or (od!=d) :
    d2=date(oy,om,od)
    delta = today - d2
    diff = delta.days
if diff > 0 :
    updateFine(diff)
    updateDate(y,m,d)
home.mainloop()