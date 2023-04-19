from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RSS_Feed_KeyowrdsSerializer, RSS_Feed_DatabaseSerializer, RSS_Feed_Name_IconSerializer
from .models import RSS_Feed_Keyowrds, RSS_Feed_Database, RSS_Feed_Name_Icon,RSS_Feed_Temp
from django.http import HttpResponseNotFound
from django.http import HttpResponse
import urllib

import openai
openai.api_key = settings.OPENAI_API_KEY

def custom_404_view(request, exception):
    return HttpResponseNotFound('<h1>404 Page Not Found</h1>')
    
    
@api_view(['GET'])
def getRoutes(request):
    homepage=[
        {
            'Endpoint':'nameicon',
            'method':'GET',
            'body':{
                'ID':'1',
                'name':'sample_name',
                'icon':'http://sample.icon.link'
            },
            'description':'shows all colums from table RSS_Feed_Name_Icon'

        },
    ]
    return Response(homepage)

@api_view(['GET'])
def getKeywordsAll(request):
	keywords = RSS_Feed_Keyowrds.objects.all().order_by('-id')
	serializer = RSS_Feed_KeyowrdsSerializer(keywords, many=True)
	return Response(serializer.data)

    
@api_view(['GET'])
def getDatabaseAll(request):
	database = RSS_Feed_Database.objects.all().order_by('-publishedDate')
	serializer = RSS_Feed_DatabaseSerializer(database, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def getNameIconAll(request):
	nameicon = RSS_Feed_Name_Icon.objects.all().order_by('-feedFrequency_accepted')
	serializer = RSS_Feed_Name_IconSerializer(nameicon, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def getFeedArticles(request, feedname):
    feedname = urllib.parse.unquote(feedname)
    try:
        name_icon = RSS_Feed_Name_Icon.objects.get(feedName=feedname)
    except RSS_Feed_Name_Icon.DoesNotExist:
        return Response({'error': 'Feed name not found'})
        
    databases = RSS_Feed_Database.objects.filter(feedName=feedname)
    articles = []
    for database in databases:
        articles.append(database)

    serializer = RSS_Feed_DatabaseSerializer(articles, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def reject_article(request):
    return HttpResponse("<h2>Article is Rejected , chech Admin Panel for more detail</h2>")
    
@api_view(['GET'])
def accept_article(request, title):
    try:
        try:
            article = RSS_Feed_Temp.objects.get(title=urllib.parse.unquote(title))

        except RSS_Feed_Temp.DoesNotExist:
            return HttpResponse("<h2>Article not found in Database, or already accepted</h2>")


        database_article = RSS_Feed_Database.objects.create(
            title=article.title,
            link=article.link,
            publishedDate=article.publishedDate,
            feedName=article.feedName,
            summary=article.summary,
        )

        article.delete()

        return HttpResponse("<h2>Article accepted successfully</h2>")
    except RSS_Feed_Temp.DoesNotExist:
        return HttpResponse("<h2>Article not found</h2>")
        
        
def chatbot(input):
    if input:
        messages=[
        {"role": "system", "content": "You are a helpful assistant in cybersecurity filed."},
        {"role": "user", "content": "What is cybersecurity?"},
        {"role":"user","content":"What is the math behind cybersecurity expert"},
        ]
        message={"role":"user","content":input}
        messages.append(message)
        response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=messages)
        reply = response["choices"][0]["message"]["content"]
        return reply

@api_view(['POST'])
def generate_response(request):
    # try:
        prompt = request.data.get('prompt', '')
        response = chatbot(prompt)
        return Response({'response': response})
    # except:
        return Response({'error': 'An error occurred'})
