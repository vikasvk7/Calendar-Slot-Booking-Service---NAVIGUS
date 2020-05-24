from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from PIL import Image
from PIL import ImageTk
import sqlite3

root = Tk()
root.geometry('500x500')
root.title("Registration Form")

db = sqlite3.connect('Meet.db')


#Variables
user = StringVar()
passw = StringVar()
var = IntVar()
desig = StringVar()
ppl = StringVar()
meetingmsg = StringVar()
meetingtitle = StringVar()
durn = StringVar()

login_name = StringVar()
pass_w = StringVar()




def control():
	db.execute("CREATE TABLE IF NOT EXISTS USERDATA(USERNAME CHAR[40], PASSWORD CHAR[50], GENDER CHAR[6], DESIGNATION CHAR[50])")
	# db.execute("DROP TABLE MEETING")
	db.execute("CREATE TABLE IF NOT EXISTS MEETING(USER1 CHAR[40], USER2 CHAR[40], TITLE CHAR[50], MESSAGE CHAR[50], DURATION CHAR[5], DATE1 CHAR[15], TIME_FROM CHAR[15], TIME_TO CHAR[15])")

def debug():
	crsr = db.execute("SELECT * FROM USERDATA")
	c = 0
	print("\n")
	print("COMPANY OFFICALS\n")
	for row in crsr:
		if(c==0):
			print("USERNAME      PASSWORD           GENDER              DESIGNATION")

		print(row[0],"     ", row[1], "          ", row[2], "            ", row[3], "             ")
		c+=1

	c=0
	crsr2 = db.execute("SELECT * FROM MEETING")
	print("\n\n")
	print("MEETING DETAILS\n")
	for row in crsr2:
		if(c==0):
			print("USER1    USER2     TITLE        MESSAGE           DURATION       DATE1      TIME_FROM          TIME_TO  ")
		print(row[0],"    ", row[1], "       ", row[2], "          ", row[3], "         ", row[4],"   ", row[5],"         ", row[6],"       ", row[7],"        ")
		c+=1

def checkAvailabilty():
	print('de')


def calen():
	def print_date():
		print(my_name)
		global meetingdate
		meetingdate = cal.get_date()
		if(available==1):
			print("yes")
			db.execute("INSERT INTO MEETING (USER1,USER2,TITLE,MESSAGE,DURATION,DATE1,TIME_FROM,TIME_TO) VALUES(?,?,?,?,?,?,?,?)",(my_name,name,meetingtitle.get(),meetingmsg.get(),durn.get(),meetingdate,"09:00:00","17:00:00"))
			db.commit()
			return
		else:
			checkAvailabilty()

	top = Toplevel(msg)
	Label(top, text='Choose date').pack(padx=10, pady=10)

	cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
	cal.pack(padx=10, pady=10)

	Button(top, text = "Ok",command=print_date).pack()


def message_window():

	global msg
	global available
	global my_name

	available = 0
	client_name = name
	my_name = title_name 

	msg = Toplevel(account)
	msg.title(f"{client_name} - Let's Meet")
	msg.geometry("350x550")

	Label(msg,text = "Meeting Title",font=("Helvetica",12)).place(x=30,y=30)
	meeting_title = Entry(msg, textvariable = meetingtitle,width="30")
	meeting_title.place(x=30,y=70)
	Label(msg,text = "Message",font=("Helvetica",12)).place(x=30,y=110)
	msg_entry = Entry(msg, textvariable = meetingmsg,width="30")
	msg_entry.place(x=30,y=150)

	Label(msg,text = "Duration",font=("Helvetica",12)).place(x=30,y=190)
	dur = Entry(msg, textvariable = durn,width="30")
	dur.place(x=30,y=230)

	Label(msg,text = "My Meetings ",font=("Helvetica",12)).place(x=30,y=270)

	crsr = db.execute("SELECT * FROM MEETING WHERE USER1 = (?)", (my_name,))
	row = crsr.fetchone()
	#Check if there is no scheduled meeting
	if(row == None):
		teller = Label(msg,text = "There are currently no meeting scheduled for you",fg="red")
		teller.place(x=30, y= 300)

		available = 1
	else:
		crsr = db.execute("SELECT * FROM MEETING WHERE USER1 = (?)", (my_name,))
		for r in crsr:
			with_whom = r[1]
			m_title = r[2]
			m_mesg = r[3]
			m_dur = r[4]
			m_date = r[5]
			m_from = r[6]
			m_to = r[7]

		Label(msg, text = f"Meeting Title : {m_title}",fg="indigo").place(x=30, y= 320)
		Label(msg,text = f"Your meeting is scheduled with {with_whom}",fg="red").place(x=30, y= 340)
		Label(msg, text = f"Duration : {m_dur}",fg="indigo").place(x=30, y= 360)

	s = ttk.Style(msg)
	s.theme_use('clam')

	Button(msg, text='Choose Meeting Date', command=calen).place(x=60,y=380)




def schedule():

	global name
	selected = ppl.get()
	if(selected == "Clients"):
		status = Label(account,text = "Please select someone to schedule",fg="red")
		status.place(x=70, y= 420)
		status.after(1000,lambda : status.destroy())
		return

	name = selected.split(" : ")[0]   #Name will be get from here
	message_window()

def accept():
	timm = t.get()
	timm = timm.split("-")
	newtime = int(timm[0][:2]) + int(m_dur)
	newtime = str(newtime)+":00:00"

	db.execute("INSERT INTO MEETING (USER1,USER2,TITLE,MESSAGE,DURATION,DATE1,TIME_FROM,TIME_TO) VALUES(?,?,?,?,?,?,?,?)",(title_name,from_whom,m_title,"",m_dur,m_date,timm[0],newtime))
	db.commit()
	return 
def myAccount():

	global account
	global propic
	global myf
	global title_name
	global t

	pflag = 0
	title_name = login_name.get()
	account = Toplevel(login_win)
	account.title(f"{title_name} - Let's Meet")
	account.geometry("350x550")

	crsr = db.execute("SELECT * FROM USERDATA WHERE USERNAME =(?)", (title_name,))
	
	for row in crsr:
		job = row[3]

	propic = Image.open("prof.jpg")
	propic = propic.resize((120,125), Image.ANTIALIAS)
	myf = ImageTk.PhotoImage(propic)

	
	Label(account, image = myf, anchor = "w").pack(fill="both")
	Label(account,text = f"{job}",font=("Helvetica",9,"bold"),fg = "#3b5998").place(x=10,y=140)
	Label(account,text = f"Welcome {title_name}!",font=("Helvetica",12,"bold"),fg = "#3b5998").place(x=140,y=20)

	Label(account,text = "Meeting Requests",font=("Helvetica",12,"bold"),fg = "#3b5998").place(x=70,y=160)

	timings = []
	crsr = db.execute("SELECT * FROM MEETING WHERE USER2 = (?)", (title_name,))

	prow = crsr.fetchone()

	if(prow == None):
		Label(account,text = f"No meeting requests!",fg="red").place(x=30, y= 180)
		pflag = 1


	global from_whom
	global m_title
	global m_msg
	global m_dur
	global m_date
	global m_start
	global m_end

	if(pflag==0):
		crsr = db.execute("SELECT * FROM MEETING WHERE USER2 = (?)", (title_name,))
		for row in crsr:
			from_whom = row[0]
			m_title = row[2]
			m_msg = row[3]
			m_dur = row[4]
			m_date = row[5]
			m_start = row[6]
			m_end = row[7]

			Label(account, text = f"Meeting Title : {m_title}",fg="indigo").place(x=30, y= 200)
			Label(account,text = f"Meeting request from {from_whom}",fg="red").place(x=30, y= 220)
			Label(account, text = f"Duration : {m_dur} hr",fg="indigo").place(x=30, y= 240)
			Label(account, text = f"Date : {m_date}",fg="indigo").place(x=30, y= 260)

			m_start = int(m_start[:2])
			m_end = int(m_end[:2])
			timings.append([m_start,m_end])

		#Sort the time intervals 
		possible = []
		options = []

		
		timings.sort()
		start = 9
		# end = start+m_dur
		i =1 

		#Possible timings that the user can attend
		while(i<len(timings)):
			possible.append([timings[i-1][1], timings[i][0]])
			i+=1
		for tim in possible:
			if(tim[1] - tim[0] <=dur):
				options.append(f"{tim[0]}:00:00 - {tim[0]+dur}:00:00")

		t = StringVar()

		if(len(timings)==1):
			ti = ["09:00:00 - 17:00:00"]
			droplist1=OptionMenu(account,t, *ti)
			droplist1.config(width=25)
			t.set('Choose the timings') 
			droplist1.place(x=30,y=280)
		else:
			droplist1=OptionMenu(account,t, *options)
			droplist1.config(width=25)
			t.set('Choose the timings') 
			droplist1.place(x=70,y=280)

		Button(account, text='Accept',width=6,bg='brown',fg='white',command = accept).place(x=240,y=280)

		

	Label(account,text = "Schedule a meeting",font=("Helvetica",12,"bold"),fg = "#3b5998").place(x=70,y=330)
	crsr = db.execute("SELECT USERNAME, DESIGNATION FROM USERDATA")

	list2 = []
	for row in crsr:
		if(row[0] != title_name):
			list2.append(f"{row[0]} : {row[1]}")

	droplist=OptionMenu(account,ppl, *list2)
	droplist.config(width=25)
	ppl.set('Clients') 
	droplist.place(x=70,y=350)

	Button(account, text='Schedule',width=6,bg='brown',fg='white',command = schedule).place(x=100,y=430)


def check():

	crsr = db.execute("SELECT * FROM USERDATA")
	flag = 0
	for row in crsr:
		if(row[0]== login_name.get() and row[1]==pass_w.get()):
			flag = 1
			print(f"{login_name.get()} is online")
	
	if(flag==1):
		myAccount()

	else:
		status = Label(login_win,text = "Username or Password Incorrect! Try Again",fg="red")
		status.place(x=70, y= 420)
		status.after(1000,lambda : status.destroy())

	ue1.delete(0,END)
	pe1.delete(0,END)



def login():
	global login_win
	global ue1
	global pe1

	login_win = Toplevel(root)
	login_win.title("Login Page")
	login_win.geometry("350x550")
	# login_win.wm_iconbitmap("fb.ico")

	user1 = Label(login_win, text="Username",width=20,font=("bold", 10))
	user1.place(x=10,y=180)


	ue1 = Entry(login_win, textvariable = login_name)
	ue1.place(x=140,y=180)

	pass1 = Label(login_win, text="Password",width=20,font=("bold", 10))
	pass1.place(x=10,y=250)

	pe1 = Entry(login_win, textvariable = pass_w,show="*")
	pe1.place(x=140,y=250)


	Button(login_win, text='Login',width=10,bg='brown',fg='white',command = check).place(x=140,y=380)


def register():

	user_name = user.get()
	pass_word = passw.get()
	gender = var.get()
	job = desig.get()

	if(gender==1):
		gndr = "MALE"
	else:
		gndr = "FEMALE"

	if(user_name == "" or pass_word == "" or job == "Select your Designation" or (gender!=1 and gender!=2)):
		warn = Label(text = "Please Fill The details!",fg="red")
		warn.place(x=190,y=320)
		warn.after(2000, lambda: warn.destroy())
		return 
		
	db.execute("INSERT INTO USERDATA (USERNAME,PASSWORD,GENDER,DESIGNATION) VALUES(?,?,?,?)",(user_name,pass_word,gndr,job))
	db.commit()


header = Label(root, text="Registration form",width=20,font=("bold", 20))
header.place(x=90,y=53)


user1 = Label(root, text="Username",width=20,font=("bold", 10))
user1.place(x=80,y=130)


ue1 = Entry(root, textvariable = user)
ue1.place(x=240,y=130)

pass1 = Label(root, text="Password",width=20,font=("bold", 10))
pass1.place(x=68,y=180)


pe1 = Entry(root, textvariable = passw,show="*")
pe1.place(x=240,y=180)

gen = Label(root, text="Gender",width=20,font=("bold", 10))
gen.place(x=70,y=230)

Radiobutton(root, text="Male",padx = 5, variable=var, value=1).place(x=235,y=230)
Radiobutton(root, text="Female",padx = 20, variable=var, value=2).place(x=290,y=230)


desn = Label(root, text="Designation",width=20,font=("bold", 10))
desn.place(x=70,y=280)

list1 = ['Software Engineer','Senior Software Engineer','Manager','HR','Graphic Designer','CEO'];

droplist=OptionMenu(root,desig, *list1)
droplist.config(width=25)
desig.set('Select your Designation') 
droplist.place(x=240,y=280)

Button(root, text='Submit',width=20,bg='brown',fg='white',command = register).place(x=180,y=380)
Button(root, text='Login',width=20,bg='brown',fg='white',command = login).place(x=180,y=440)



control()
debug()
root.mainloop()