import re
import string
import pickle
import newspaper
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .apps import CompaniesConfig
# Create your views here.

@api_view(['GET'])#ye function ki property ko change karta hai decorator
def test_article(request):
    text = request.query_params.get('article')
    text = wordopt(text)
    if len(text)==0:# apna model empty ko false bolega
        return Response('Could not process the article', status=400)
    return Response(predict(text))

@api_view(['GET'])
def test_url(request):
    url = request.query_params.get('url')
    article = newspaper.Article(url = url)
    try:
        article.download()
        article.parse()
    except:
        return Response('Could not fetch the URL', status=400)
    text = article.text
    # text = "abcd"
    if len(text)==0:
        return Response('Could not process the article', status=400)
    return Response(predict(text))

def predict(text):
    prediction = CompaniesConfig.trained_model.predict([text])[0]
    if prediction == 0:
        result = False
    else:
        result = True
    return {'result': result}

def wordopt(text):#puntuation aur link hata dega thoda cleen karega
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text
