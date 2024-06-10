from flask import *
from database import *

public=Blueprint('public',__name__)

@public.route('/')
def home():

    return render_template('index.html')



@public.route('/login',methods=['get','post'])
def login():
    data={}
    if 'login' in request.form:
        uname=request.form['uname']
        passw=request.form['pass']
        q="select * from login where user_name='%s' and password='%s'"%(uname,passw)
        print(q)
        res=select(q)
        if res:
            session['logid']=res[0]['login_id']
            utype=res[0]['user_type']

            if utype=='admin':
                return redirect(url_for('admin.adhome'))

            elif utype=='user':
                q="select * from user where login_id='%s'"%(session['logid'])
                rs=select(q)
                session['uid']=rs[0]['user_id']        
                return redirect(url_for('user.uhome'))
        else:
            flash("invalid username or password")
            return redirect (url_for("public.login"))
    return render_template("login.html")



@public.route('/user_reg',methods=['get','post'])
def user_reg():
	data={}
	

	if 'reg' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		place=request.form['pl']
		phone=request.form['ph']
		email=request.form['email']
		uname=request.form['uname']
		pword=request.form['passw']
		q2="SELECT * FROM login WHERE user_name='%s' OR password='%s' "%(uname,pword)
		res=select(q2)

		if res:
			flash("USERNAME OR PASSWORD ALREADY EXISTS")
		else:

			q1="insert into login values(null,'%s','%s','user')"%(uname,pword)
			id=insert(q1)
			q="insert into user values(null,'%s','%s','%s','%s','%s','%s')"%(id,fname,lname,place,phone,email)
			insert(q)
			flash("INSERTED SUCCESSFULLY")
			return redirect(url_for('public.login'))


	return render_template('user_reg.html',data=data)

