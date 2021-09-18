from django.shortcuts import render
from django.db.models import query
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.response import Response
from rest_framework.permissions import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import *
from .serializers import *
from .code import tf_idf as bot
from . import add_data
from .permission import *
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny
import datetime
import json, os
import pandas as pd
from django.conf import settings
from pathlib import Path 
from django.template.loader import render_to_string
from dotenv import dotenv_values
from django.contrib.auth import logout

# Initialise environment variables
ENV_FILE = Path(os.getcwd(), 'environments','.env.dev')
env = dotenv_values(ENV_FILE)

class DomainList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Domains.objects.all()
        serializer = DomainsSerializer(queryset, many=True)
        
        # serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)

class DomainsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        predomain = Domains.objects.filter(domain=request.data['domain'], client='psb')
        if predomain:
            return Response({"status": status.HTTP_208_ALREADY_REPORTED})
        else:
            serializer = DomainsSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"errors": "Invalid data format","X-Content-Type-Options":'nosniff'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
            return Response(serializer.data)


class DomainsViews(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        domain = self.kwargs.get('domain', None)
        try:
            queryset = Domains.objects.get(domain=domain)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DomainsSerializer(queryset, data=request.data)
        if not serializer.is_valid():
            return Response({"errors": "Invalid data format","X-Content-Type-Options":'nosniff'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        domain = self.kwargs.get('doamin', None)
        try:
            queryset = Domains.objects.get(domain=domain)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset.delete()

        return Response(domain)

class IntentList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        queryset = Intents.objects.all()
        serializer = IntentsSerializer(queryset, many=True)
        for i in serializer.data:
            domain = Domains.objects.get(id=i['domain'])
            i['domain'] = domain.domain
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)

class IntentsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        request.data._mutable
        try:
            domain = Domains.objects.filter(
                domain=request.data['domain']).last().id
        except ObjectDoesNotExist as e:
            return Response({"status": status.HTTP_404_NOT_FOUND})
        
        if '"' in request.data['user_say']:
            request.data['user_say'].replace('"',"'")
        if '"' in request.data['response']:
            request.data['response'].replace('"',"'")
        serializer = IntentsSerializer(data={"intent":request.data['intent'],"user_say":request.data["user_say"],"response":request.data['response'],"domain":domain})
        if not serializer.is_valid():
            return Response({"errors": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        data = [{"message":request.data['user_say'], "response":request.data['response']}]
        file = env['PSB_JSON_FILE']
        tfidf_vectorizer_pikle_path = "code/previous_tfidf_vectorizer.pickle"
        tfidf_matrix_train_path = "code/previous_tfidf_matrix_train.pickle"
        add_data.append_new_intent(data, file)
        chatbot = bot.Bot()
        chatbot.train_chat(file, tfidf_vectorizer_pikle_path, tfidf_matrix_train_path)
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)


class IntentsViews(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        intents = self.kwargs.get('intents', None)
        try:
            queryset = Intents.objects.get(intents=intents)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = IntentsSerializer(queryset, data=request.data)
        if not serializer.is_valid():
            return Response({"errors": "Invalid data format","X-Content-Type-Options":'nosniff'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        intents = self.kwargs.get('doamin', None)
        try:
            queryset = Intents.objects.get(intents=intents)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset.delete()

        return Response(intents)

class EntityList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        queryset = Entity.objects.all()
        serializer = EntitySerializer(queryset, many=True)
        for i in serializer.data:
            intent = Intents.objects.get(id=i['intents'])
            i['intents'] = intent.intent
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)

class EntityView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            request.data['intents'] = Intents.objects.filter(
                intent=request.data['intent']).last().id
        except ObjectDoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND})
        serializer = EntitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": "Invalid data format","X-Content-Type-Options":'nosniff'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)


class EntityViews(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        entity = self.kwargs.get('entity', None)
        try:
            queryset = Entity.objects.get(entity=entity)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EntitySerializer(queryset, data=request.data)
        if not serializer.is_valid():
            return Response({"errors": "Invalid data format","X-Content-Type-Options":'nosniff'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        entity = self.kwargs.get('doamin', None)
        try:
            queryset = Entity.objects.get(entity=entity)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset.delete()

        return Response(entity)

class ConversationsList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        queryset = Conversations.objects.all()
        serializer = ConversationSerializer(queryset, many=True)
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)

class ConversationsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            queryset = Conversations.objects.filter(
                datetime__range=[request.data['startdate'], request.data['enddate']])
        except ObjectDoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND})
        serializer = ConversationSerializer(queryset, many=True)
        for i in serializer.data:
            i['count'] = len(serializer.data)
            i['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)


class MessageView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            query = Conversations.objects.filter(
                user_id=request.data['user_id'], datetime=request.data['date']).last()
            queryset = Message.objects.filter(conversation=query.id)
        except ObjectDoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND})
        serializer = MessageSerializer(queryset, many=True)
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)


class ConversationsViews(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        startdate = self.kwargs.get('startdate')
        enddate = self.kwargs.get('enddate')
        try:
            queryset = Conversations.objects.filter(
                datetime__range=[startdate, enddate])
        except ObjectDoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND})
        serializer = ConversationSerializer(queryset, many=True)
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        try:
            queryset = Conversations.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        queryset.delete()
        return Response({"status": "Success"})


class Train_bot(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # request.data['client']="psb"
        if self.request.query_params.get('domain'):
            request.data['domain']=self.request.query_params.get('domain')
        try:
            domain = Domains.objects.filter(
                client="PSB", domain=request.data['domain']).last()
        except ObjectDoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = Intents.objects.all().filter(domain=domain.id)
        file = env['PSB_JSON_FILE']
        tfidf_vectorizer_pikle_path = "previous_tfidf_vectorizer.pickle"
        tfidf_matrix_train_path = "previous_tfidf_matrix_train.pickle"
        add_data.append_new_data(data, file)
        chatbot = bot.Bot()
        chatbot.train_chat(
            file, tfidf_vectorizer_pikle_path, tfidf_matrix_train_path)
        return Response({"status": status.HTTP_202_ACCEPTED})
 


class Train_bot_csv(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def make_json(self, csvFilePath):
        # create a dictionary
        data = []
        jsonFilePath = env['PSB_JSON_FILE']
        # Open the csv file and read as a dataframe
        with open(csvFilePath, encoding='utf-8') as csvf:
            df = pd.read_csv(csvFilePath, names=['Questions', 'Answers'])

        f = open(env['PSB_JSON_FILE'],
                 encoding="utf-8", mode='r+')
        dataprev = json.load(f)
        count = 0
        # coonverting the rows of the dataframe into list of dictionaries
        for i in df.index:
            d = {}
            d['message'] = df['Questions'][i]
            d['response'] = df['Answers'][i]
            data.append(d)

        # function to dump data
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))

        return jsonFilePath

    def post(self, request, *args, **kwargs):
        try:
            request.data['client']="psb"
            if 'domain' not in request.data:
                request.data['domain'] = self.request.query_params.get("domain")
            query = TrainFiles.objects.filter(
                client=request.data['client'], domain=request.data['domain']).last()
            file_read = Path(settings.MEDIA_ROOT, query.trainfile.name)
            if file_read.split('.')[1] == 'csv':
                file = self.make_json(file_read)
            elif file_read.split('.')[1] == 'json':
                file = file_read
            tfidf_vectorizer_pikle_path = "previous_tfidf_vectorizer.pickle"
            tfidf_matrix_train_path = "previous_tfidf_matrix_train.pickle"
            chatbot = bot.Bot()
            chatbot.train_chat(
                file, tfidf_vectorizer_pikle_path, tfidf_matrix_train_path)

            return Response({"status": status.HTTP_202_ACCEPTED})
        except ObjectDoesNotExist:
            return Response({"status": status.HTTP_400_BAD_REQUEST})

class ChatrunList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        queryset = Conversations.objects.get(user_id=request.data['user_id'])
        serializer = ConversationSerializer(queryset)
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)

class Chatrun(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    runbot = bot.Bot()

    def post(self, request, *args, **kwargs):
        request.data['datetime'] = str(datetime.date.today())
        serializer = ConversationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": "Invalid data format","X-Content-Type-Options":'nosniff'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response({"user_id": serializer.data['user_id'],"status": status.HTTP_201_CREATED})

    def put(self, request, *args, **kwargs):
        request.data['datetime'] = str(datetime.date.today())
        try:
            queryset = Conversations.objects.filter(
                user_id=request.data['user_id'], datetime=request.data['datetime'])
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ConversationSerializer(queryset, data=request.data)
        if not serializer.is_valid():
            return Response({"errors": "Invalid data format","X-Content-Type-Options":'nosniff'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response({'response': "Thanks for your feedback"})


class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    runbot = bot.Bot()

    def post(self, request, *args, **kwargs):
        request.data['datetime'] = str(datetime.date.today())
        response = self.runbot.runbot(request.data['msg'])
        
        if response == "":
            response = "Apologies! I did not get you. Please bear with me I'm still learning. Alternatively you can call on Toll Free Number - (1800-419-8300)"
        
        elif type(response) == list:
            response = '<br><br>'.join(response)

        request.data['response'] = response
        
        if request.data['msg'].capitalize() in ['Hi', 'Hello', 'Hey']:
            quicklinks = ["Loan", "Pay Bills/Recharge", "Balance Enquiry",
                          "Interest Rate", "Card Block", "Services", "Mobile Banking", "Branch"]
        else:
            quicklinks = []

        if "user_id" in request.data:
            try:
                Conversations.objects.get(user_id=request.data['user_id'], datetime=request.data['datetime'])
            except ObjectDoesNotExist:
                return Response({"error": "Please enter your details first."})
        else:
            serializers = ConversationSerializer(data=request.data)
            if not serializers.is_valid():
                return Response({"errors": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)
            serializers.save()
            request.data['user_id'] = serializers.data['user_id']
            return Response({"user_id": serializers.data['user_id'],"response":response, "quicklinks":quicklinks}, status=status.HTTP_201_CREATED)

        serializer = MessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": "Invalid data format","X-Content-Type-Options":'nosniff'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(conversation=Conversations.objects.get(
            user_id=request.data['user_id'], datetime=request.data['datetime']))
        return Response({"response": response, "quicklinks": quicklinks, "X-Content-Type-Options":'nosniff'})

class FilesaveList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        client = self.kwargs.get('id')
        queryset = TrainFiles.objects.get(client=client)
        serializer = TrainFilesSerializer(queryset, many=True)
        serializer.data[0]['X-Content-Type-Options'] = 'nosniff'
        return Response(serializer.data)

class FilesaveView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        request.data['client'] = "psb"
        request.data['upload_date'] = datetime.date.today()
        name, ext = os.path.splitext(request.data['trainfile'])
        if ext!='.csv':
            return Response({"errors":"Incorrect file format, csv required "+ext+" given.", "X-Content-Type-Options":'nosniff'})
        serializer = TrainFilesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"errors": "Invalid data format","X-Content-Type-Options":'nosniff'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"status": status.HTTP_201_CREATED})


class SaveQuicklinks(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        f = open(env['PSB_JSON_FILE'],
                 encoding="utf-8", mode='r+')
        data = json.load(f)
        data['X-Content-Type-Options'] = 'nosniff'
        return Response(data)


def get_chatwindow(request):
    file = Path(os.getcwd(), 'chatbox','static','chatbot.html')
    print(render_to_string(file))

class FAQViews(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        f = open(env['PSB_JSON_FILE'], encoding="utf-8", mode='r+')
        data = json.load(f)
        return Response({"data":data})

    def put(self, request, *args, **kwargs):
        f = open(env['PSB_JSON_FILE'], encoding="utf-8", mode='r+')
        data = json.load(f)
        for i in data:
            if i['message']==request.data['message'] and i['response']==request.data['response']:
                i['message']=request.data['newmessage']
                i['response']=request.data['newresponse']
        with open(env['PSB_JSON_FILE'], 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))
        tfidf_vectorizer_pikle_path = "previous_tfidf_vectorizer.pickle"
        tfidf_matrix_train_path = "previous_tfidf_matrix_train.pickle"
        chatbot = bot.Bot()
        chatbot.train_chat(env['PSB_JSON_FILE'], tfidf_vectorizer_pikle_path, tfidf_matrix_train_path)
        return Response({"data":data, "status":"updated successfully","X-Content-Type-Options":'nosniff'}, status=status.HTTP_202_ACCEPTED)

class DownloadView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def post(self, request, *args, **kwargs):
        df = pd.read_json(env['PSB_JSON_FILE'])
        response = HttpResponse(df.to_csv(header=False, index=False),content_type='text/csv', secure=True, httponly=True)
        response['Content-Disposition'] = 'attachment; filename=data.csv'
        response['X-Content-Type-Options'] = 'nosniff'
        return response

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "success", 'code': status.HTTP_200_OK, 'detail': "logout success","X-Content-Type-Options":'nosniff'})

def chatbot(request):
    return render(request, "contents/psbchatbot.html") 