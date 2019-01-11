from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from sklearn.feature_extraction.text import TfidfTransformer
import nltk,string, numpy
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy.exc import DBAPIError

from ..models import (
     MyModel,
     Student,
     Teacher,
     Test
  )
#global d = {'testname','qno'}


@view_config(route_name='first', renderer='../templates/first.jinja2')
def first(request):
    try:
        session = request.session
        session['user'] = "0"
        return render_to_response('../templates/first.jinja2',{},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='signin', renderer='../templates/signin.jinja2')

@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(MyModel)
        one = query.filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'Answer_Evaluation'}



@view_config(route_name='register')
def view(request):
    try:
        session = request.session
        session['user'] = request.params['user']

        return render_to_response('../templates/register.jinja2',{'session' : session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'Answer_Evaluation'}


@view_config(route_name='page')
def page(request):
    try:
        query1 = request.dbsession.query(Teacher)
        query2 = request.dbsession.query(Student)

        session = request.session
        name = request.params['name']
        username = request.params['username']
        password = request.params['password']
        email = request.params['email']
        if session['user'] == "teacher":
            subject = request.params['subject']
            obj = Teacher()
            obj.subject = subject
        else:
            obj = Student()

        obj.name = name
        obj.username = username
        obj.password = password
        obj.email_id = email

        request.dbsession.add(obj)
        return render_to_response('../templates/signin.jinja2',{},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    #return {'one': one, 'project': 'Answer_Evaluation'}


@view_config(route_name='pg')
def pg(request):
    try:
        k=0
        username = request.params['username_value']
        password = request.params['password_value']

        session = request.session
        if session['user'] == "teacher":
            tabledata = request.dbsession.query(Teacher)
            name = tabledata.filter(Teacher.username == username and Teacher.password == password).all()
        else:
            tabledata = request.dbsession.query(Student)
            name = tabledata.filter(Student.username == username and Student.password == password).all()
        session['username'] = username
        for i in name:
            if i.username == username and i.password == password:
                if session['user'] == "teacher":
                    session['user_id'] = i.teacher_id
                if session['user'] == "student":
                    session['user_id'] = i.student_id
                k=1

        if k == 1:
            return render_to_response ('../templates/page.jinja2', {'session':session}, request=request)
        else:
            return render_to_response ('../templates/error.jinja2',{},request=request)

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)



@view_config(route_name='nxt', renderer='../templates/display.jinja2')
def next(request):
    try:
        global num,test
        session = request.session
        test = request.params['test_name']
        num = int(request.params['desc_no'])

        return render_to_response('../templates/display.jinja2',{'session':session,'test_name':test,'desc_no':num},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

@view_config(route_name='createtest', renderer='../templates/createtest.jinja2')
def createtest(request):
    try:
        session = request.session
        return render_to_response('../templates/createtest.jinja2',{'session':session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)




@view_config(route_name='save', renderer='../templates/saved.jinja2')
def save(request):
    try:
        session = request.session

        for i in range(0,int(num)):
            query = request.dbsession.query(Test)

            ques_temp = str('Question'+str(i+1))
            ans_temp = str('Answer_key'+str(i+1))
            testname = test
            question_id = 1+i
            question = request.params[ques_temp]
            answer = request.params[ans_temp]

            obj = Test()
            obj.question_id = question_id
            obj.question = question
            obj.answer_key = answer
            obj.test_name = testname
            obj.teach_id = session['user_id']
            request.dbsession.add(obj)
        return render_to_response('../templates/saved.jinja2',{'session':session},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='taketest', renderer='../templates/taketest.jinja2')
def taketest(request):
    try:
        session = request.session
        tabledata = request.dbsession.query(Teacher)
        table = tabledata.all()
        teacher_id=[]
        username=[]
        tablelist=[teacher_id,username]

        for i in table:
            teacher_id.append(i.teacher_id)
            username.append(i.username)
        return render_to_response('../templates/taketest.jinja2',{'session':session,'tablenew':tablelist},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='3t', renderer='../templates/writetest.jinja2')
def t(request):
    try:
        global tablelis
        session = request.session
        test_name = request.params['test_name']
        tabledata = request.dbsession.query(Test)
        table = tabledata.filter(Test.test_name == test_name).all()
        test_name = []
        question_id = []
        question = []
        answer_key = []
        teach_id = []
        tablelis=[test_name,question_id,question,answer_key,teach_id]
        for i in table:
            test_name.append(i.test_name)
            question_id.append(i.question_id)
            question.append(i.question)
            answer_key.append(i.answer_key)
            teach_id.append(i.teach_id)
        count = len(question_id)

        return render_to_response('../templates/writetest.jinja2',{'session':session,'tablenew':tablelis,'count':count},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)


@view_config(route_name='tt', renderer='../templates/displaytest.jinja2')
def tt(request):
    try:
        session = request.session
        teacher_id = request.params['teacher_name']
        tabledata = request.dbsession.query(Test)
        table = tabledata.filter(Test.teach_id == teacher_id).all()
        test_name = []
        question_id = []
        question = []
        answer_key = []
        tablelist=[test_name,question_id,question,answer_key]
        for i in table:
            test_name.append(i.test_name)
            question_id.append(i.question_id)
            question.append(i.question)
            answer_key.append(i.answer_key)

        print(tablelist)

        return render_to_response('../templates/displaytest.jinja2',{'session':session,'tablenew':tablelist},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)




#@view_config(route_name='5t', renderer='../templates/score.jinja2')
@view_config(route_name='4t', renderer='../templates/score.jinja2')
def tttttt(request):
    try:
        score =[]
        ans=[]
        ques=[]
        mark_list=[]
        session = request.session
        #tablelis[][]
        for i in range(0,len(tablelis[0])):
            answer_key = tablelis[3][i]
            answer = str(request.params['Answer_key'+str(i+1)])
            ans.append(ans)
            print (answer)
            ques.append(tablelis[2][i])
            print (answer_key)
            documents = [answer_key,answer]
            documents = list(map(str, documents))
            print (documents)
            print ("1")
            lemmer = nltk.stem.WordNetLemmatizer()
            print ("2")

            '''lemmer = nltk.stem.WordNetLemmatizer()
            def LemTokens(tokens):
                return [lemmer.lemmatize(token) for token in tokens]
            remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
            def LemNormalize(text):
                return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))'''




            def LemTokens(tokens):
                print ("3")
                return [lemmer.lemmatize(token) for token in tokens]

            def LemNormalize(text):
                print ("4")
                tokens = nltk.word_tokenize(text)
                words = [w.lower() for w in tokens if w.isalnum()]
                return LemTokens(words)
            print ("5")
            TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
            print ("6")
            def cos_similarity(textlist):
                print(textlist)
                print ("7")
                tfidf = TfidfVec.fit_transform(textlist)
                return (tfidf * tfidf.T).toarray()
            print ("8")
            print(documents)
            tf_matrix = cos_similarity(documents)
            print ("9")
            tfidfTran = TfidfTransformer(norm="l2")
            print ("10")
            tfidfTran.fit(tf_matrix)
            print ("12")
            tfidf_matrix = tfidfTran.transform(tf_matrix)
            cos_similarity_matrix = (tfidf_matrix * tfidf_matrix.T).toarray()
            score = cos_similarity_matrix[0][1]*10
            mark = int(round(score))

            mark_list.append(mark)
            print (mark)
            leng = int(len(mark_list))


        return render_to_response('../templates/score.jinja2',{'session':session,'leng':leng ,'score':mark_list ,'ans':ans, 'ques':ques},request=request)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)



db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_Answer_Evaluation_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
