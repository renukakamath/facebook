from flask import *
from database import *
import uuid



api=Blueprint('api',__name__)



@api.route('/userregister')
def userregister():
    
    data={}
 
  
    fname=request.args['fname']
    lname=request.args['lname']
    place=request.args['place']
    phone=request.args['phone']
    email=request.args['email']

    uname=request.args['username']
    passw=request.args['password']
    q="select * from login where username='%s'"%(uname)
    print(q)
    res=select(q)
    if res:
        data['status']='duplicate'
    else:
        q="insert into login values(null,'%s','%s','user')"%(uname,passw)
        print(q)
        id=insert(q)
        q="insert into user values(null,'%s','%s','%s','%s','%s','%s')"%(id,fname,lname,place,phone,email)
        print(q)
        insert(q)
        data['status']='success'
    return str(data)

@api.route('/login')
def login():
    data={}
    username=request.args['username']
    password=request.args['password']

    q="select * from login where username='%s' and password='%s'"%(username,password)
    res=select(q)
    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']="failed"
    return str(data)


@api.route('/viewpost')
def viewpost():
    data={}
    q="select * from post inner join user using (user_id)"
    res=select(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']='failed'
    return str(data)


@api.route('/Viewusers')
def Viewusers():
    data={}
    q="select * from user"
    res=select(q)
    if res:
        data['status']="success"
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewusers'
    return str(data)



@api.route('/uploadfile',methods=['get','post'])
def uploadfile():
    data={}
    image=request.files['image'];
    lid=request.form['lid'];
    details=request.form['details']
    
    path="static/uploads/"+str(uuid.uuid4())+image.filename
    image.save(path)

    q="insert into post values(null,(select user_id from user where login_id='%s'),'%s','%s',curdate(),'active','%s')" %(lid,path,path,details)
    res=insert(q)
    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='uploadfile'

    return str(data)


@api.route("/chatdetail")
def chatdetail():
	sid=request.args['sender_id']
	rid=request.args['receiver_id']
	
	data={}
	q="select * from message where (sender_id='%s' and receiver_id='%s') or (sender_id='%s' and receiver_id='%s') group by message_id "%(sid,rid,rid,sid)
	
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		
		data['status']="failed"
	data['method']='chatdetail'
	
	return str(data)



@api.route("/chat")
def chat():
	data={}
	sid=request.args['sender_id']
	rid=request.args['receiver_id']
	det=request.args['details']
	
	
	q="insert into message values(null,'%s','%s','%s',curdate())"%(sid,rid,det)
	insert(q)
	data['status']='success'
	data['method']='chat'
	return str(data)


@api.route('/likepost')
def likepost():
    data={}
    lid=request.args['lid']
    postid=request.args['postid']
    q="insert into `like` values(null,'%s',(select user_id from user where login_id='%s'),'liked')"%(postid,lid)
    print(q)
    insert(q)
    data['status']='success'
    data['method']='likepost'
    return str(data)



@api.route('/viewreply')
def viewreply():
    data={}
    id=request.args['id']
    q="select * from complaint inner join user using(user_id) where complaint.user_id=(select user_id from user where login_id='%s')"%(id)
    res=select(q)
    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    return str(data)



@api.route('/sendcomplaint')
def sendcomplaint():
    data={}
    id=request.args['id']
    complaint=request.args['complaint']
    q="insert into complaint values(null,(select user_id from user where login_id='%s'),'%s','pending',curdate())"%(id,complaint)
    insert(q)
    data['status']='success'
    return str(data)




@api.route('/viewuserss',methods=['get','post'])
def viewuserss():
	data={}
	loginid=request.args['lid']
	search="%"+request.args['search']+"%"
	q="select *,concat (fname,' ',lname) as names from user where (fname like '%s' and  login_id != '%s') " %(search,loginid)
	print(q)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']='viewusers'
	return  str(data)






@api.route('/view_request',methods=['get','post'])
def view_request():
	data={}
	loginid=request.args['loginid']
	q="SELECT * FROM `user` INNER JOIN `friends` USING(user_id) where friend_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s') and status ='pending'" %(loginid)
	print(q)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']='view_request'
	return  str(data)


@api.route('/user_send_request',methods=['get','post'])
def user_send_request():
	data={}
	loginid=request.args['loginid']
	friend_id=request.args['friend_id']
	q="SELECT * FROM `friends` WHERE `friend_id`='%s' AND `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(friend_id,loginid)
	print(q)
	res=select(q)
	if res:
		data['status']='duplicate'
		data['method'] ='user_send_request'
	else:
		q="INSERT INTO `friends` VALUES(NULL,'%s',(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),NOW(),'pending')"%(friend_id,loginid)
		print(q)
		id=insert(q)
		if id>0:
			data['status'] ='success'
		else:
			data['status'] ='failed'
		data['method'] ='user_send_request'
		return  str(data)



	
@api.route('/request_accept',methods=['get','post'])
def request_accept():
	data={}
	frnd_id=request.args['frnd_id']
	q="UPDATE `friends` SET `status`='Accept' WHERE `friends_id`='%s'"%(frnd_id)
	print(q)
	id=update(q)
	if id>0:
		data['status'] ='success'
	else:
		data['status'] ='failed'
	data['method'] ='request_accept'
	return  str(data)





@api.route('/reject_request',methods=['get','post'])
def reject_request():
	data={}
	frnd_id=request.args['frnd_id']
	q="DELETE FROM `friends` WHERE `friends_id`='%s'"%(frnd_id)
	print(q)
	id=update(q)
	if id>0:
		data['status'] ='success'
	else:
		data['status'] ='failed'
	data['method'] ='reject_request'
	return  str(data)




@api.route('/view_friends',methods=['get','post'])
def view_friends():
	data={}
	loginid=request.args['loginid']
	# friend_id=request.args['friend_id']
	q="SELECT * FROM `user` WHERE user_id IN(SELECT IF(user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s'),friend_id,user_id) FROM friends WHERE (friend_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s') AND STATUS='Accept') OR (user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')  AND STATUS='Accept'))" %(loginid,loginid,loginid)
	print(q)
	res=select(q)
	print(res)
	if res:
		data['status']='success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method'] ='view_friends'
	return  str(data)





@api.route('/like_or_not_post',methods=['get','post'])
def like_or_not_post():
	data={}
	loginid=request.args['lid']
	postid=request.args['postid']
	q="SELECT * FROM `like` WHERE `post_id`='%s' AND `user_id`=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(postid,loginid)
	print(q)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']='like_or_not_post'
	return  str(data)



@api.route('/profile',methods=['get','post'])
def profile():
	data={}
	loginid=request.args['lid']
	
	q="SELECT * FROM USER INNER JOIN post USING(user_id) WHERE user_id=(SELECT `user_id` FROM `user` WHERE `login_id`='%s')"%(loginid)
	print(q)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	
	return  str(data)


@api.route('/Viewcommets',methods=['get','post'])
def Viewcommets():
	data={}
	postid=request.args['post_id']
	
	q="SELECT* FROM `comment` INNER JOIN post USING(post_id) inner join user on(comment.user_id=user.user_id) where post_id='%s' order by comment_id desc"%(postid)
	print(q)
	res = select(q)
	print(res)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']='view'
	
	return  str(data)

@api.route('/comment',methods=['get','post'])
def comment():
	data={}
	lid=request.args['lid']
	msg=request.args['cmt']
	postid=request.args['postid']
	
	q="insert into comment values(null,'%s',(select user_id from user where login_id='%s'),'%s')"%(postid,lid,msg)
	print(q)
	res = insert(q)
	print(res)
	if res :
		data['status']  = 'success'
		
	else:
		data['status']	= 'failed'
	data['method']='add'
	
	return  str(data)



