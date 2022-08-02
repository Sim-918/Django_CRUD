from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt

nextid=4
topics=[
    {'id':1,'title':'first','body':'First is ...'},
    {'id':2,'title':'second','body':'Second is ...'},
    {'id':3,'title':'third','body':'Third is ...'},
]


def htmlTemplate(articleTag,id=None):
    global topics
    contextUI=''
    if id != None:
        contextUI=f'''
        <li>
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li> 
            <li><a href="/update/{id}">update</a></li>     
        '''
    ol=''
    for topic in topics:
        ol+= f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'

    return f'''
    <html>
    <body>
        <a href="/"><h1>Django</a></h1>
        <ul>
            {ol}
        </ul>
        {articleTag}
        <ul>
            <li><a href="/create/">create</a></li>
            {contextUI}                 
        </ul>
    </body>
    </html>
    '''
    


# Create your views here.
def index(request):

    article='''
    <h2>Sim</h2>
    Hello,Welcome
    '''
    return HttpResponse(htmlTemplate(article))

    
def read(request,id):
    global topics
    article=''
    for topic in topics:
        if topic['id']==int(id):
            article=f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(htmlTemplate(article,id))
    
@csrf_exempt

def create(request):                        #메서드의 방식이 POST방식인가, GET방식인가
    #print("request.method",request.method)
    global nextid
    if request.method=='GET':
        article='''
            <form action="/create/" method="post">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(htmlTemplate(article))
    elif request.method=='POST':
        title=request.POST['title']
        body=request.POST['body']
        newTopic={"id":nextid,"title":title,"body":body}
        topics.append(newTopic)
        url='/read/'+str(nextid)
        nextid+=1
        return redirect(url)


@csrf_exempt
def update(request,id):
    global topics
    if request.method=='GET':
        for topic in topics:
            if topic['id']==int(id):
                selectedTopic={"title":topic['title'],
                                "body":topic['body']
                                }

        article=article=f'''
            <form action="/update/{id}/" method="post">
                <p><input type="text" name="title" placeholder="title" value={selectedTopic["title"]}></p>
                <p><textarea name="body" placeholder="body">{selectedTopic["body"]}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(htmlTemplate(article,id))
    elif request.method=='POST':
        title=request.POST['title']
        body=request.POST['body']
        for topic in topics:
            if topic['id']==int(id):
                topic['title']=title
                topic['body']=body
        return redirect(f'/read/{id}')


@csrf_exempt
def delete(request):
    global topics
    if request.method=='POST':
        id=request.POST['id']
        newTopics=[]
        for topic in topics:
            if topic['id']!=int(id):
                newTopics.append(topic)
        topics=newTopics
        return redirect('/')
