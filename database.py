import pymysql
import math
import xml.dom.minidom as mdom
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

db = pymysql.Connect(host="localhost", user="root", passwd="******", db="minibbs", port=3306, charset='utf8')

cursor = db.cursor()

if __name__ == '__main__':
    def make_user_data():
        basicExpr = 'insert into User (UserName, Gender, Birthday, Password, Email) '
        for i in range(50):
            insertExpr = "values ('User"+str(i)+"','Male','1998-01-01','123','user"+str(i)+"@pku.edu.cn');"
            cursor.execute(basicExpr+insertExpr)
        for i in range(50, 100):
            insertExpr = "values ('User"+str(i)+"','Female','1998-12-12','321','user"+str(i)+"@pku.edu.cn');"
            cursor.execute(basicExpr+insertExpr)
        try:
            db.commit()
        except:
            db.rollback()
        row = cursor.fetchall()
    def make_post_data():
        basicExpr = 'insert into Post (UserNo, SectionNo, Title, Content)'
        '''for i in range(50):
            insertExpr = "values ("+str(i+306)+",1,'Hello world!','I am new here. Lets start chatting!');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i+306)+",2,'Good lecture!','I want to attend this lecture~');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i+306)+",3,'Looking for jobs.','I am looking for jobs.');"
            cursor.execute(basicExpr+insertExpr)
        for i in range(50,100):
            insertExpr = "values ("+str(i+306)+",1,'Hello world!','I am new here. Lets start chatting!');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i+306)+",4,'Studying','Come on and study together!');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i+306)+",5,'Good game','Peking University Sports Events are so great!');"
            cursor.execute(basicExpr+insertExpr)'''
        for i in range(10):
            insertExpr = "values ("+str(i+306)+",1,'Hello world!!!','I am really new here. Lets start chatting!');"
            cursor.execute(basicExpr+insertExpr)

        try:
            db.commit()
        except:
            db.rollback()
        row = cursor.fetchall()
    def make_reply_data():
        basicExpr = 'insert into Reply (PostNo, UserNo, ReplyContent)'
        '''for i in range(1, 301):
            insertExpr = "values ("+str(i)+",1,'Good Post!');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i)+",2,'Good Post!');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i)+",3,'Good Post!');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i)+",306,'Good Post!');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i)+",307,'Good Post!');"
            cursor.execute(basicExpr+insertExpr)'''
        for i in range(1, 50):
            insertExpr = "values ("+str(i)+",400,'Good Post!');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i)+",401,'Good Post!');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i)+",402,'Good Post!');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i)+",403,'Good Post!');"
            cursor.execute(basicExpr+insertExpr)
            insertExpr = "values ("+str(i)+",404,'Good Post!');"
            cursor.execute(basicExpr+insertExpr)
            
        try:
            db.commit()
        except:
            db.rollback()
        row = cursor.fetchall()
    db.close()

def calculate_level(EXP):
    EXP = int(EXP)
    return '0' if EXP == 0 else str(int(math.log(EXP,2)))

def calculate_age(birthday):
    birthday = str(birthday)
    year, month, day = int(birthday[0:4]), int(birthday[5:7]), int(birthday[8:10])
    current_time = datetime.datetime.now()
    now_year, now_month, now_day = current_time.year, current_time.month, current_time.day
    age = now_year-year
    if now_month < month:
        age = age-1
    elif now_month == month and now_day < day:
        age = age-1
    return '0' if age < 0 else str(age)




def valid_login(account, password):
    is_admin = False
    is_master = []
    userID = 0
    sql = "SELECT UserName, Password, Admin, UserNo FROM User WHERE UserName = '"+account+"';"
    cursor.execute(sql)
    row = cursor.fetchall()
    if cursor.rowcount == 0:
        return 'User not existed!', is_admin, is_master, userID
    elif row[0][1] == password:
        is_admin = True if row[0][2] == 1 else False
        userID = int(row[0][3])
        checkMaster = "SELECT SectionNo FROM Section WHERE Master = "+str(userID)+";"
        cursor.execute(checkMaster)
        row = cursor.fetchall()
        if cursor.rowcount != 0:
            for i in row:
                is_master.append(str(i[0]))
        return False, is_admin, is_master, userID
    else:
        return 'Password Error.', is_admin, is_master, userID

def valid_register(request):
    username = request.form["username"]
    password = request.form["password"]
    rpassword = request.form["rpassword"]
    email = request.form["email"]
    gender = request.form["gender"]
    birthday = request.form["birthday"]
    if password != rpassword:
        return '', username, 'Two passwords are not the same!'
    sql = """insert into User (UserName, Gender, Birthday, Password, Email)
    values ('%s','%s','%s','%s','%s');"""
    data = (username, gender, birthday, password, email)
    try:
        expr = sql%data
        cursor.execute(expr)
        cursor.execute("SELECT UserNo FROM User WHERE UserName= '%s';" % username)
        row = cursor.fetchall()

        db.commit()
        return row[0][0], username, None
    except:
        db.rollback()
        return '', username, 'This username has been used. Please try another.'

def get_sections():
    '''
    return type:
    [{'number': ,
        'name': ,
        'description': ,
        'master': ,
        'posts':['','',''] # with ...
        }]
    '''
    return_section = []
    sql = "SELECT SectionNo, SectionName, SectionDesc, Master FROM Section;"
    cursor.execute(sql)
    row = cursor.fetchall()
    for Block in row:
        addblock = {}
        addblock['number']=Block[0]
        addblock['name']=Block[1]
        addblock['description']=Block[2]
        addblock['posts']=[]
        sql = "SELECT UserName FROM User WHERE UserNo = '%s'" % Block[3]
        cursor.execute(sql)
        mod = cursor.fetchall()

        addblock['master']=mod[0][0]
        sql = "SELECT Content FROM Post WHERE Post.SectionNo = %s ORDER BY Post.PostTime desc limit 0, 3;" %addblock['number']
        cursor.execute(sql)
        pos = cursor.fetchall()
        for i in pos:
            temp_post = i[0]
            if len(temp_post) > 70:
                temp_post = temp_post[0:70] + '...'
            addblock['posts'].append(temp_post)
        return_section.append(addblock)
    return return_section

def search_in_db(searching):
    ''' return the post that contains searching 搜索包含searching字符串的post
    return type:
    [{
        'post_id': ,
        'section': ,
        'user': ,
        'time': ,  # YYYY-MM-DD
        'title' : ,
        'content': ,
        'clicks' : ,
        'replies' : , # number
        }]
    '''
    return_section = []
    sql = "select * from Post where Title like '%%%s%%' or Content like '%%%s%%';" %(searching, searching)
    cursor.execute(sql)
    row = cursor.fetchall()
    for pos in row:
        addblock = {}
        addblock['post_id'] = pos[0]
        sql = "SELECT UserName FROM User WHERE UserNo = %s;" % pos[1]
        cursor.execute(sql)
        UserNo = cursor.fetchall()
        addblock['user'] = UserNo[0][0]
        sql = "SELECT SectionName FROM Section WHERE SectionNo = %s;" % pos[2]
        cursor.execute(sql)
        SectionNo = cursor.fetchall()
        addblock['section'] = SectionNo[0][0]
        addblock['title']=pos[3]
        addblock['content']=pos[4]
        addblock['clicks']=pos[5]
        addblock['time']=pos[6]
        addblock['replies']=pos[7]
        return_section.append(addblock)
    return return_section

def get_top10clicks_post():
# 返回点击量前十的post，返回格式同上
    return_section = []
    sql = "SELECT * from Post ORDER BY Clicks DESC LIMIT 0, 10;"
    cursor.execute(sql)
    row = cursor.fetchall()
    for pos in row:
        addblock = {}
        addblock['post_id'] = pos[0]
        sql = "SELECT UserName FROM User WHERE UserNo = %s;" % pos[1]
        cursor.execute(sql)
        UserNo = cursor.fetchall()
        addblock['user'] = UserNo[0][0]
        sql = "SELECT SectionName FROM Section WHERE SectionNo = %s;" % pos[2]
        cursor.execute(sql)
        SectionNo = cursor.fetchall()
        addblock['section'] = SectionNo[0][0]
        addblock['title']=pos[3]
        addblock['content']=pos[4]
        addblock['clicks']=pos[5]
        addblock['time']=pos[6]
        addblock['replies']=pos[7]
        return_section.append(addblock)
    return return_section

def get_top10replies_post():
#返回回复量前十的post，返回格式同上
    return_section = []
    sql = "SELECT * from Post ORDER BY Replies DESC LIMIT 0, 10;"
    cursor.execute(sql)
    row = cursor.fetchall()
    for pos in row:
        addblock = {}
        addblock['post_id'] = pos[0]
        sql = "SELECT UserName FROM User WHERE UserNo = %s;" % pos[1]
        cursor.execute(sql)
        UserNo = cursor.fetchall()
        addblock['user'] = UserNo[0][0]
        sql = "SELECT SectionName FROM Section WHERE SectionNo = %s;" % pos[2]
        cursor.execute(sql)
        SectionNo = cursor.fetchall()
        addblock['section'] = SectionNo[0][0]
        addblock['title']=pos[3]
        addblock['content']=pos[4]
        addblock['clicks']=pos[5]
        addblock['time']=pos[6]
        addblock['replies']=pos[7]
        return_section.append(addblock)
    return return_section

def moreposts(seca, secb):
    ''' 返回在seca版块比secb版块帖子发的更多的用户（包含admin、master）
    return type:
    [{
    'id': ,
    'name': ,
    'level': ,
    'postA': ,
    'postB': ,
    }]
    '''
    sql = "SELECT * FROM Section WHERE SectionName = '%s';" % seca
    cursor.execute(sql)
    row = cursor.fetchall()
    if cursor.rowcount == 0:
        return [], 'Section %s not found.' % seca
    sql = "SELECT * FROM Section WHERE SectionName = '%s';" % secb
    cursor.execute(sql)
    row = cursor.fetchall()
    if cursor.rowcount == 0:
        return [], 'Section %s not found.' % secb
    return_user = []
    sql = "SELECT * FROM UserSection WHERE SectionName = '%s'" % seca
    cursor.execute(sql)
    row1 = cursor.fetchall()
    sql = "SELECT * FROM UserSection WHERE SectionName = '%s'" % secb
    cursor.execute(sql)
    row2 = cursor.fetchall()


    cursor.execute("create temporary table SecA(UserNo INT, Posts INT);")
    cursor.execute("create temporary table SecB(UserNo INT, Posts INT);")
    cursor.execute("select UserNo, Posts from UserSection where SectionName = '%s';" % seca)
    ans1 = cursor.fetchall()
    cursor.execute("select UserNo, Posts from UserSection where SectionName = '%s';" % secb)
    ans2 = cursor.fetchall()
    cursor.executemany("insert into SecA values (%s, %s)", ans1)
    cursor.executemany("insert into SecB values (%s, %s)", ans2)
    sql = "select SecA.UserNo, SecA.Posts, SecB.Posts from (SecA inner join SecB on SecA.UserNo = SecB.UserNo) " \
          "where SecA.Posts>SecB.Posts order by SecB.Posts desc, SecA.Posts desc;"
    cursor.execute(sql)
    row = cursor.fetchall()
    for i in row:
        sql = 'SELECT UserName, EXP FROM User WHERE UserNo = %s' % i[0]
        cursor.execute(sql)
        data = cursor.fetchall()
        adduser={}
        adduser['id'] = i[0]
        adduser['name'] = data[0][0]
        adduser['postA'] = i[1]
        adduser['postB'] = i[2]
        adduser['level'] = calculate_level(data[0][1])
        return_user.append(adduser)
    sql = "select UserNo, Posts from SecA where SecA.UserNo not in (select UserNo from SecB) order by Posts desc;"
    cursor.execute(sql)
    row = cursor.fetchall()
    for i in row:
        sql = 'SELECT UserName, EXP FROM User WHERE UserNo = %s' % i[0]
        cursor.execute(sql)
        data = cursor.fetchall()
        adduser={}
        adduser['id'] = i[0]
        adduser['name'] = data[0][0]
        adduser['postA'] = i[1]
        adduser['postB'] = '0'
        adduser['level'] = calculate_level(data[0][1])
        return_user.append(adduser)
    cursor.execute("drop temporary table if exists SecA;")
    cursor.execute("drop temporary table if exists SecB;")
    return return_user, None

def sec_information(section_id):
    ''' 返回版块的信息 master是版主的意思
    return type:
    {
    'name': ,
    'master': ,
    'description': ,
    }
    '''
    section = {}
    sql = "SELECT SectionName, Master, SectionDesc FROM Section WHERE SectionNo = %s" % section_id
    cursor.execute(sql)
    row = cursor.fetchall()
    section['name'] = row[0][0]
    section['master'] = row[0][1]
    section['description'] = row[0][2]
    return section

def update_section(section_id, sec):
    # 返回error，默认为None，传入的sec格式同上
    error = None
    if 'master' in sec.keys():
        data = (sec['name'], sec['description'], sec['master'], section_id)
        sql = "UPDATE Section SET SectionName = '%s', SectionDesc = '%s', Master = %s WHERE SectionNo = %s" % data
        try:
            cursor.execute(sql)
            db.commit()
            return error
        except:
            db.rollback()
            error = "Update failed! Maybe section name has been used or master ID is invalid. "
            return error
    else:
        data = (sec['name'], sec['description'], section_id)
        sql = "update Section set SectionName = '%s', SectionDesc = '%s' where SectionNo = %s" % data
        try:
            cursor.execute(sql)
            db.commit()
            return error
        except:
            db.rollback()
            error = "Update failed! Maybe section name has been used or master ID is invalid. "
            return error


def add_sectionTo(sec):
    # 返回section_id 和 error，默认为None，传入的sec格式同上
    error = None
    data = (sec['name'], sec['description'], sec['master'])
    sql = "insert into Section (SectionName, SectionDesc, Master) values ('%s', '%s', '%s')" % data
    try:
        cursor.execute(sql)
        cursor.execute("select SectionNo from Section where SectionName = '%s';" % sec['name'])
        section_id = cursor.fetchall()
        db.commit()
        return section_id[0][0], error
    except:
        db.rollback()
        error = "Add failed! Maybe section name has been used or master ID is invalid."
        return -1, error

def delete_sectionFromDB(id):
    sql = "delete from Section where SectionNo = %s" % id
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


def get_all_users():
    ''' 返回所有的用户（包括admin、master）
    return type:
    [{
    'id': ,
    'name': ,
    'gender': ,
    'level': ,
    'birthday': ,
    'reg_time': ,
    'email': ,
    'power': ,
    }]
    '''
    return_user = []
    sql = "SELECT * FROM User;"
    cursor.execute(sql)
    users = cursor.fetchall()
    sql = "SELECT Master FROM Section;"
    cursor.execute(sql)
    masters_wrap = cursor.fetchall()
    masters = []
    for i in masters_wrap:
        masters.append(i[0])
    for user in users:
        adduser = {}
        adduser['id'] = str(user[0])
        adduser['name'] = user[1]
        adduser['gender'] = user[2]
        adduser['level'] = calculate_level(user[6])
        adduser['birthday'] = str(user[3])
        adduser['reg_time'] = str(user[8])[0:10]
        adduser['email'] = user[5]
        if user[7] == 1:
            adduser['power'] = 'admin'
        elif user[0] in masters:
            adduser['power'] = 'master'
        else:
            adduser['power'] = 'user'
        return_user.append(adduser)
    return return_user

def delete_user(id):
# 用于删除用户（此用户不含admin、master），返回error默认为None
    try:
        sql = "DELETE FROM User WHERE UserNo = %s" % id
        cursor.execute(sql)
        db.commit()
        return None
    except:
        db.rollback()
        return "Delete failed! "

def update_user(request, userID):
    password = request.form["password"]
    rpassword = request.form["rpassword"]
    email = request.form["email"]
    gender = request.form["gender"]
    birthday = request.form["birthday"]
    if password != rpassword:
        return 'Two passwords are not the same!'
    sql = """update User set Gender = '%s', Birthday = '%s', Password = '%s', Email = '%s' where UserNo = %s;"""
    data = (gender, birthday, password, email, userID)
    try:
        expr = sql%data
        cursor.execute(expr)
        db.commit()
        return None
    except:
        db.rollback()
        return 'Update failed!'

def get_user_info(id):
    cursor.execute("SELECT * FROM User WHERE UserNo = %s" % id)
    user_db = cursor.fetchall()
    user = {}
    user['gender'] = user_db[0][2]
    user['birthday'] = user_db[0][3]
    user['username'] = user_db[0][1]
    user['email'] = user_db[0][5]
    return user


def make_user_xml(id):
    sql = "SELECT * FROM User WHERE UserNo = %s" % id
    cursor.execute(sql)
    user = cursor.fetchall()
    sql = "SELECT * FROM Post WHERE UserNo = %s ORDER BY PostTime Desc" % id
    cursor.execute(sql)
    posts = cursor.fetchall()
    sql = "SELECT * FROM Reply WHERE UserNo = %s ORDER BY ReplyTime Desc" % id
    cursor.execute(sql)
    replies = cursor.fetchall()


    doc = mdom.Document()
    doctype = mdom.DocumentType('User')
    doctype.systemId = "userprofile.dtd"
    doctype.publicId = None

    doc.appendChild(doctype)


    root = doc.createElement('User')
    doc.appendChild(root)

    node_username = doc.createElement('UserName')
    node_username.appendChild(doc.createTextNode(str(user[0][1])))
    root.appendChild(node_username)
    node_info = doc.createElement('Info')
    node_basicinfo = doc.createElement('BasicInfo')
    node_gender = doc.createElement('Gender')
    node_gender.appendChild(doc.createTextNode(str(user[0][2])))
    node_age = doc.createElement('Age')
    node_age.appendChild(doc.createTextNode(calculate_age(user[0][3])))
    node_level = doc.createElement('Level')
    node_level.appendChild(doc.createTextNode(calculate_level(user[0][6])))
    node_birth = doc.createElement('Birthday')
    node_birth.appendChild(doc.createTextNode(str(user[0][3])))
    node_email = doc.createElement('Email')
    node_email.appendChild(doc.createTextNode(str(user[0][5])))
    node_basicinfo.appendChild(node_gender)
    node_basicinfo.appendChild(node_age)
    node_basicinfo.appendChild(node_level)
    node_basicinfo.appendChild(node_birth)
    node_basicinfo.appendChild(node_email)
    node_info.appendChild(node_basicinfo)

    node_otherinfo = doc.createElement('OtherInfo')
    node_posts = doc.createElement('Posts')
    node_replies = doc.createElement('Replies')

    for x in posts:
        node_post = doc.createElement('Post')
        node_No = doc.createElement('No')
        node_No.appendChild(doc.createTextNode(str(x[0])))
        node_block = doc.createElement('Block')
        sql = "select SectionName from Section where SectionNo = %s" % x[2]
        cursor.execute(sql)
        sec = cursor.fetchall()
        node_block.appendChild(doc.createTextNode(str(sec[0][0])))
        node_postuser = doc.createElement('PostUser')
        node_postuser.appendChild(doc.createTextNode(str(user[0][1])))
        node_title = doc.createElement('Title')
        node_title.appendChild(doc.createTextNode(str(x[3])))
        node_content = doc.createElement('Content')
        node_content.appendChild(doc.createTextNode(str(x[4])))
        node_posttime = doc.createElement('PostTime')
        node_posttime.appendChild(doc.createTextNode(str(x[6])))
        node_clicks = doc.createElement('Clicks')
        node_clicks.appendChild(doc.createTextNode(str(x[5])))
        node_replynum = doc.createElement('ReplyNum')
        node_replynum.appendChild(doc.createTextNode(str(x[7])))
        node_post.appendChild(node_No)
        node_post.appendChild(node_block)
        node_post.appendChild(node_postuser)
        node_post.appendChild(node_title)
        node_post.appendChild(node_content)
        node_post.appendChild(node_posttime)
        node_post.appendChild(node_clicks)
        node_post.appendChild(node_replynum)
        node_posts.appendChild(node_post)
    for x in replies:
        node_reply = doc.createElement('Reply')
        sql = "select * from Post where PostNo = %s" % x[2]
        cursor.execute(sql)
        temp_post = cursor.fetchall()
        node_title = doc.createElement('Title')
        node_title.appendChild(doc.createTextNode(str(temp_post[0][3])))
        sql = "select UserName from User where UserNo = %s" % temp_post[0][1]
        cursor.execute(sql)
        temp_user = cursor.fetchall()
        node_postuser = doc.createElement('PostUser')
        node_postuser.appendChild(doc.createTextNode(str(temp_user[0][0])))
        node_postid = doc.createElement('PostID')
        node_postid.appendChild(doc.createTextNode(str(x[2])))
        node_original = doc.createElement('OriginalNo')
        node_original.appendChild(doc.createTextNode(str(x[0])))
        node_floor = doc.createElement('Floor')
        node_floor.appendChild(doc.createTextNode(str(x[1])))
        node_replyuser = doc.createElement('ReplyUser')
        node_replyuser.appendChild(doc.createTextNode(str(user[0][1])))
        node_replycontent = doc.createElement('ReplyContent')
        node_replycontent.appendChild(doc.createTextNode(str(x[4])))
        node_replytime = doc.createElement('ReplyTime')
        node_replytime.appendChild(doc.createTextNode(str(x[5])))
        node_praisenum = doc.createElement('PraiseNum')
        node_praisenum.appendChild(doc.createTextNode(str(x[6])))
        node_reply.appendChild(node_title)
        node_reply.appendChild(node_postuser)
        node_reply.appendChild(node_postid)
        node_reply.appendChild(node_original)
        node_reply.appendChild(node_floor)
        node_reply.appendChild(node_replyuser)
        node_reply.appendChild(node_replycontent)
        node_reply.appendChild(node_replytime)
        node_reply.appendChild(node_praisenum)
        node_replies.appendChild(node_reply)

    node_otherinfo.appendChild(node_posts)
    node_otherinfo.appendChild(node_replies)
    node_info.appendChild(node_otherinfo)
    root.appendChild(node_info)

    filepath = './static/xml/user_%s.xml' % user[0][1]

    xmlfile = open(filepath, 'w', encoding='utf-8')
    doc.writexml(xmlfile, indent='\t', addindent='\t', newl='\n', encoding='UTF-8')

    xmlfile.close()

def make_section_xml(id):
    sql = "SELECT * FROM Section WHERE SectionNo = %s" % id
    cursor.execute(sql)
    section = cursor.fetchall()
    sql = "SELECT * FROM Post WHERE SectionNo = %s ORDER BY PostTime Desc" % id
    cursor.execute(sql)
    posts = cursor.fetchall()
    postNum = cursor.rowcount

    doc = mdom.Document()
    doctype = mdom.DocumentType('Section')
    doctype.systemId = "secprofile.dtd"
    doctype.publicId = None

    doc.appendChild(doctype)


    root = doc.createElement('Section')
    doc.appendChild(root)

    node_info = doc.createElement('Info')
    node_secid = doc.createElement('SecId')
    node_secid.appendChild(doc.createTextNode(str(id)))
    node_secname = doc.createElement('SecName')
    node_secname.appendChild(doc.createTextNode(str(section[0][1])))
    node_master = doc.createElement('Master')
    sql = "SELECT UserName FROM User WHERE UserNo = %s" % section[0][3]
    cursor.execute(sql)
    master_name = cursor.fetchall()
    node_master.appendChild(doc.createTextNode(str(master_name[0][0])))
    node_postnum = doc.createElement('PostNum')
    node_postnum.appendChild(doc.createTextNode(str(postNum)))
    node_desc = doc.createElement('Description')
    node_desc.appendChild(doc.createTextNode(str(section[0][2])))
    node_info.appendChild(node_secid)
    node_info.appendChild(node_secname)
    node_info.appendChild(node_master)
    node_info.appendChild(node_postnum)
    node_info.appendChild(node_desc)
    root.appendChild(node_info)

    node_posts = doc.createElement('Posts')

    for x in posts:

        node_post = doc.createElement('Post')
        node_No = doc.createElement('No')
        node_No.appendChild(doc.createTextNode(str(x[0])))
        node_postuser = doc.createElement('PostUser')
        sql = "SELECT UserName FROM User WHERE UserNo = %s" %  x[1]
        cursor.execute(sql)
        username = cursor.fetchall()
        node_postuser.appendChild(doc.createTextNode(str(username[0][0])))
        node_title = doc.createElement('Title')
        node_title.appendChild(doc.createTextNode(str(x[3])))
        #print(node_title.getElementsByTagName('Title')[0])
        node_content = doc.createElement('Content')
        node_content.appendChild(doc.createTextNode(str(x[4])))
        node_posttime = doc.createElement('PostTime')
        node_posttime.appendChild(doc.createTextNode(str(x[6])))
        node_clicks = doc.createElement('Clicks')
        node_clicks.appendChild(doc.createTextNode(str(x[5])))

        node_replies = doc.createElement('Replies')

        sql = "SELECT * FROM Reply WHERE PostNo = %s ORDER BY ReplyTime Desc LIMIT 0, 3" % x[0]
        cursor.execute(sql)
        replies = cursor.fetchall()

        for y in replies:
            node_reply = doc.createElement('Reply')
            node_floor = doc.createElement('Floor')
            node_floor.appendChild(doc.createTextNode(str(y[1])))
            node_replyuser = doc.createElement('ReplyUser')
            sql = "SELECT UserName FROM User WHERE UserNo = %s" % y[3]
            cursor.execute(sql)
            replyuser = cursor.fetchall()
            node_replyuser.appendChild(doc.createTextNode(str(replyuser[0][0])))
            node_replycontent = doc.createElement('ReplyContent')
            original_content = str(y[4])
            reply_content = original_content[0:80]+'...' if len(original_content) > 80 else original_content
            node_replycontent.appendChild(doc.createTextNode(reply_content))
            node_replytime = doc.createElement('ReplyTime')
            node_replytime.appendChild(doc.createTextNode(str(y[5])))
            node_praisenum = doc.createElement('PraiseNum')
            node_praisenum.appendChild(doc.createTextNode(str(y[6])))
            node_reply.appendChild(node_floor)
            node_reply.appendChild(node_replyuser)
            node_reply.appendChild(node_replycontent)
            node_reply.appendChild(node_replytime)
            node_reply.appendChild(node_praisenum)
            node_replies.appendChild(node_reply)


        node_post.appendChild(node_No)
        node_post.appendChild(node_postuser)
        node_post.appendChild(node_title)
        node_post.appendChild(node_content)
        node_post.appendChild(node_posttime)
        node_post.appendChild(node_clicks)
        node_post.appendChild(node_replies)
        node_posts.appendChild(node_post)


    root.appendChild(node_posts)

    filepath = './static/xml/sec_%s.xml' % section[0][0]

    xmlfile = open(filepath, 'w', encoding='utf-8')

    doc.writexml(xmlfile, indent='\t', addindent='\t', newl='\n', encoding='UTF-8')

    xmlfile.close()

def make_post_xml(id):
    sql = "SELECT * FROM Post WHERE PostNo = %s;" % id
    cursor.execute(sql)
    target_post = cursor.fetchall()[0]
    sql = "SELECT * FROM Reply WHERE PostNo = %s ORDER BY ReplyNo Asc;" % id
    cursor.execute(sql)
    replies = cursor.fetchall()
    replyNum = cursor.rowcount

    doc = mdom.Document()
    doctype = mdom.DocumentType('Post')
    doctype.systemId = "postprofile.dtd"
    doctype.publicId = None

    doc.appendChild(doctype)


    root = doc.createElement('Post')
    doc.appendChild(root)


    node_No = doc.createElement('No')
    node_No.appendChild(doc.createTextNode(str(target_post[0])))
    node_postuser = doc.createElement('PostUser')
    sql = "SELECT UserName FROM User WHERE UserNo = %s" %  target_post[1]
    cursor.execute(sql)
    username = cursor.fetchall()
    node_block = doc.createElement('Block')
    sql = "select SectionName from Section where SectionNo = %s" % target_post[2]
    cursor.execute(sql)
    node_block.appendChild(doc.createTextNode((str(cursor.fetchall()[0][0]))))
    node_postuser.appendChild(doc.createTextNode(str(username[0][0])))
    node_title = doc.createElement('Title')
    node_title.appendChild(doc.createTextNode(str(target_post[3])))
    node_content = doc.createElement('Content')
    node_content.appendChild(doc.createTextNode(str(target_post[4])))
    node_posttime = doc.createElement('PostTime')
    node_posttime.appendChild(doc.createTextNode(str(target_post[6])))
    node_clicks = doc.createElement('Clicks')
    node_clicks.appendChild(doc.createTextNode(str(target_post[5])))
    node_replynum = doc.createElement('ReplyNum')
    node_replynum.appendChild(doc.createTextNode(str(replyNum)))

    node_replies = doc.createElement('Replies')

    for y in replies:
        node_reply = doc.createElement('Reply')
        node_floor = doc.createElement('Floor')
        node_floor.appendChild(doc.createTextNode(str(y[1])))
        node_orino = doc.createElement('OriginalNo')
        node_orino.appendChild(doc.createTextNode(str(y[0])))
        node_replyuser = doc.createElement('ReplyUser')
        sql = "SELECT UserName FROM User WHERE UserNo = %s" % y[3]
        cursor.execute(sql)
        replyuser = cursor.fetchall()
        node_replyuser.appendChild(doc.createTextNode(str(replyuser[0][0])))
        node_replycontent = doc.createElement('ReplyContent')
        original_content = str(y[4])
        reply_content = original_content[0:80] + '...' if len(original_content) > 80 else original_content
        node_replycontent.appendChild(doc.createTextNode(reply_content))
        node_replytime = doc.createElement('ReplyTime')
        node_replytime.appendChild(doc.createTextNode(str(y[5])))
        node_praisenum = doc.createElement('PraiseNum')
        node_praisenum.appendChild(doc.createTextNode(str(y[6])))
        node_reply.appendChild(node_floor)
        node_reply.appendChild(node_orino)
        node_reply.appendChild(node_replyuser)
        node_reply.appendChild(node_replycontent)
        node_reply.appendChild(node_replytime)
        node_reply.appendChild(node_praisenum)
        node_replies.appendChild(node_reply)

    root.appendChild(node_No)
    root.appendChild(node_postuser)
    root.appendChild(node_block)
    root.appendChild(node_title)
    root.appendChild(node_content)
    root.appendChild(node_posttime)
    root.appendChild(node_clicks)
    root.appendChild(node_replynum)
    root.appendChild(node_replies)

    filepath = './static/xml/post_%s.xml' % target_post[0]

    xmlfile = open(filepath, 'w', encoding='utf-8')
    doc.writexml(xmlfile, indent='\t', addindent='\t', newl='\n', encoding='UTF-8')

    xmlfile.close()

def delete_postOf(id):
    sql = "delete from Post where PostNo = %s" % id
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()


def add_click(post_id):
    sql = "update Post set Clicks = Clicks+1 where PostNo = %s" % post_id
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

def add_praiseTo(reply_id):
    sql = "update Reply set PraiseNum=PraiseNum+1 where ReplyNo = %s" % reply_id
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

def get_postFromReply(reply_id):
    cursor.execute("select PostNo from Reply where ReplyNo = %s" % reply_id)
    result = cursor.fetchall()
    return result[0][0]

def add_replyTo(userID, post_id, reply):
    if '"' in reply:
        sql = "insert into Reply(PostNo, UserNo, ReplyContent) values (%s, %s, '%s');" % (post_id, userID, reply)
    else:
        sql = 'insert into Reply(PostNo, UserNo, ReplyContent) values (%s, %s, "%s");' % (post_id, userID, reply)
    try:
        cursor.execute(sql)

        db.commit()
    except:
        db.rollback()

def add_postTo(user_id, section_id, title, content):
    sql = "insert into Post(UserNo, SectionNo, Title, Content) values "
    if '"' in title and '"' in content:
        sql += "(%s, %s, '%s', '%s');" % (user_id, section_id, title, content)
    elif '"' in title and "'" in content:
        sql += "(%s, %s, '%s', \"%s\");" % (user_id, section_id, title, content)
    elif '"' in content:
        sql += "(%s, %s, \"%s\", '%s');" % (user_id, section_id, title, content)
    else:
        sql += "(%s, %s, \"%s\", \"%s\");" % (user_id, section_id, title, content)
    try:
        cursor.execute(sql)
        db.commit()
        check_anomalies()
    except:
        db.rollback()

def get_active_users(section_id, sortedByPosts):
    '''
    return:
    sectionName
    active_user: type:
    [{
    'id'
    'name'
    'level'
    'gender'
    'age'
    'posts'
    'replies'
    }]
    '''
    cursor.execute("select SectionName from Section where SectionNo = %s;" % section_id)
    sectionName = cursor.fetchall()[0][0]

    cursor.execute("drop view if exists PostNum;")
    cursor.execute("drop view if exists ReplyNum;")
    cursor.execute("drop view if exists ActiveUsers;")

    sql = 'create view PostNum as select UserNo as pUserNo, count(PostNo) as Posts from Post where SectionNo = %s group by UserNo;' % section_id
    cursor.execute(sql)

    sql = '''create view ReplyNum as select Reply.UserNo as rUserNo, count(*) as Replies from
            ((select PostNo, UserNo from Post where SectionNo = %s) as Post inner join 
            (select ReplyNo, UserNo, PostNo from Reply) as Reply on Post.PostNo = Reply.PostNo) group by rUserNo;''' % section_id
    cursor.execute(sql)
    sql = '''create view ActiveUsers as select pUserNo as UserNo, IfNull(Posts,0) as Posts, IfNull(Replies,0) as Replies from
            (select * from PostNum left join ReplyNum on PostNum.pUserNo = ReplyNum.rUserNo union select * from
             PostNum right join ReplyNum on PostNum.pUserNo = ReplyNum.rUserNo) as t;'''
    cursor.execute(sql)
    active_users = []
    if sortedByPosts:
        cursor.execute("select UserNo, Posts, Replies from ActiveUsers order by Posts desc, Replies desc;")
    else:
        cursor.execute("select UserNo, Posts, Replies from ActiveUsers order by Replies desc, Posts desc;")

    row = cursor.fetchall()
    for x in row:
        if x[0] == None: continue
        temp_user = {}
        temp_user['id'] = str(x[0])
        temp_user['posts'] = str(x[1])
        cursor.execute(
            "select UserName, EXP, Gender, timestampdiff(year, Birthday, current_timestamp) from User where UserNo = %s" %
            x[0])
        row2 = cursor.fetchall()[0]
        temp_user['name'] = str(row2[0])
        temp_user['level'] = calculate_level(row2[1])
        temp_user['gender'] = str(row2[2])
        temp_user['age'] = str(row2[3])
        temp_user['replies'] = str(x[2])
        active_users.append(temp_user)
    cursor.execute("drop view if exists PostNum;")
    cursor.execute("drop view if exists ReplyNum;")
    cursor.execute("drop view if exists ActiveUsers;")

    return sectionName, active_users


def get_hot_post(section_id):
    cursor.execute("select SectionName from Section where SectionNo = %s;" % section_id)
    sectionName = cursor.fetchall()[0][0]
    sql = "create view lastReply as select Post.PostNo as PostNo, Post.PostTime as PostTime, max(Reply.ReplyTime) as lastReplyTime " \
          "from ((select * from Post where SectionNo = %s) as Post natural join Reply) group by Post.PostNo;" % section_id
    cursor.execute(sql)
    sql = "select PostNo from lastReply where timediff(PostTime, lastReplyTime) >= " \
          "all (select timediff(PostTime, lastReplyTime) from lastReply); "
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.execute("select * from Post where PostNo = %s;" % result[0][0])
    result_post = cursor.fetchall()
    hotpost = {}
    hotpost['id'] = result_post[0][0]
    cursor.execute("select UserName from User where UserNo = %s;" % result_post[0][1])
    result_user = cursor.fetchall()
    hotpost['user'] = result_user[0][0]
    hotpost['title'] = result_post[0][3]
    hotpost['content'] = result_post[0][4]
    hotpost['clicks'] = result_post[0][5]
    hotpost['posttime'] = result_post[0][6]
    replies = []
    cursor.execute("select * from Reply where PostNo = %s;" % hotpost['id'])
    result_replies = cursor.fetchall()
    for reply in result_replies:
        addreply = {}
        addreply['floor'] = reply[1]
        cursor.execute("select UserName from User where UserNo = %s;" % reply[3])
        result_user = cursor.fetchall()
        addreply['user'] = result_user[0][0]
        addreply['time'] = reply[5]
        addreply['praises'] = reply[6]
        addreply['content'] = reply[4]
        replies.append(addreply)
    hotpost['replies'] = replies
    cursor.execute("drop view if exists lastReply;")
    return sectionName, hotpost

def get_target_posts(section_id, clicks):
    cursor.execute("select SectionName from Section where SectionNo = %s;" % section_id)
    sectionName = cursor.fetchall()[0][0]
    return_value = []
    if clicks:
        cursor.execute("select avg(Clicks) from Post where SectionNo = %s group by SectionNo;" % section_id)
        avgclicks = cursor.fetchall()[0][0]
        sql = "select * from Post where SectionNo = %s and Clicks >= (select avg(Clicks) " \
              "from Post where SectionNo = %s group by SectionNo) order by Clicks desc;" % (section_id, section_id)
        cursor.execute(sql)
        result = cursor.fetchall()
        for temp_post in result:
            addpost = {}
            addpost['id'] = temp_post[0]
            cursor.execute("select UserName from User where UserNo = %s;" % temp_post[1])
            result_user = cursor.fetchall()
            addpost['user'] = result_user[0][0]
            addpost['title'] = temp_post[3]
            addpost['content'] = temp_post[4]
            addpost['clicks'] = temp_post[5]
            addpost['posttime'] = temp_post[6]
            return_value.append(addpost)
        avgresult = avgclicks
    else:
        cursor.execute("drop view if exists replyNum;")
        sql = "create view replyNum as select Reply.UserNo as UserNo, count(Reply.ReplyNo) as Replies from " \
              "((select * from Section where SectionNo = %s) as Section natural join Reply) group by Reply.UserNo;" % section_id
        cursor.execute(sql)
        cursor.execute("select avg(Replies) from replyNum;")
        avgreplies = cursor.fetchall()[0][0]
        cursor.execute("select UserNo, Replies from replyNum where Replies >= (select avg(Replies) from replyNum) order by Replies desc;")
        result = cursor.fetchall()
        for x in result:
            adduser = {}
            cursor.execute("select UserNo, UserName, Gender, timestampdiff(year, Birthday, current_timestamp), EXP from User where UserNo = %s;" % x[0])
            temp_user = cursor.fetchall()[0]
            adduser['id'] = x[0]
            adduser['name'] = temp_user[1]
            adduser['gender'] = temp_user[2]
            adduser['age'] = temp_user[3]
            adduser['level'] = calculate_level(temp_user[4])
            adduser['replies'] = x[1]
            return_value.append(adduser)
        cursor.execute("drop view if exists replyNum;")
        avgresult = avgreplies
    return sectionName, avgresult, return_value

def check_anomalies():
    cursor.execute("select * from MailBox;")
    sender = "example@qq.com"
    if cursor.rowcount != 0:
        mails = cursor.fetchall()
        cursor.execute("select Email from User where admin = 1;")
        receivers = cursor.fetchall()
        for mail in mails:
            content = "Anomalies checked: User with ID %s posts too much in the last 10 minutes. " \
                      "Current Time: %s" % (mail[0], mail[1])
            message = MIMEText(content, 'plain', 'UTF-8')
            message['From'] = Header('minibbs', 'UTF-8')
            message['To'] = Header('admin', 'UTF-8')
            subject = 'Anomalies Warning from MiniBBS'
            message['Subject'] = Header(subject, 'UTF-8')
            for receiver in receivers:
                try:
                    smtpObj = smtplib.SMTP_SSL('smtp.qq.com', 465)
                    smtpObj.login(sender, "*******")
                    smtpObj.sendmail(sender, [str(receiver[0])], message.as_string())
                    smtpObj.quit()
                    print("Mail delivered successfully.")
                except smtplib.SMTPException:
                    print("Mail failed.")
        cursor.execute("delete from MailBox;")
        try:
            db.commit()
        except:
            db.rollback()

def get_usernameFromID(user_id):
    cursor.execute("select UserName from User where UserNo = %s" % user_id)
    return cursor.fetchall()[0][0]

def getSectionFromPost(post_id):
    cursor.execute("select SectionNo from Post where PostNo = %s" % post_id)
    return cursor.fetchall()[0][0]

