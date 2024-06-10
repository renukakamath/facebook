from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/adhome')
def adhome():

    return render_template('admin_home.html')

@admin.route('/view_user')
def view_usre():
    data={}
    q="select * from user"
    data['user']=select(q)
    return render_template('admin_view_user.html',data=data)


@admin.route('/viewpost')
def viewpost():
    data={}
    q="select * from post inner join user using(user_id) order by post_id desc"
    data['post']=select(q)

   
    q="SELECT * FROM `comment` INNER JOIN post USING(post_id) INNER JOIN `user` ON(comment.`user_id`=user.`user_id`)"
    data['cmt']=select(q)
    return render_template('admin_view_post.html',data=data)

@admin.route('/viewcomplaint',methods=['get','post'])
def viewcomplaint():
    data={}
    q="select * from complaint inner join user using(user_id)"
    data['viewc']=select(q)

    if 'id' in request.args:
        id=request.args['id']
        data['viewc1']=1

    if 'send' in request.form:
        id=request.args['id']
        reply=request.form['reply']
        q="update complaint set reply='%s' where complaint_id='%s'"%(reply,id)
        update(q)
        flash("Reply Sent Successfull")
        return redirect(url_for('admin.viewcomplaint'))
    return render_template('admin_view_complaints.html',data=data)