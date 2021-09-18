from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # List of domains or create a domain
    path('domain', DomainsView.as_view(), name="DomainsList"),
    path('domainview', DomainList.as_view(), name="DomainsListView"),
    # update or delete a single domain
    path('domain/<str:domain>', DomainsViews.as_view(), name="Domainsperticular"),
    # List of intents or create an intent
    path('intent', IntentsView.as_view(), name="IntentsList"),
    path('intentview', IntentList.as_view(), name="IntentsListView"),
    # update or delete a single intent
    path('intent/<str:intents>', IntentsViews.as_view(), name="Intentsperticular"),
    # List of entity or create an entity
    path('entity', EntityView.as_view(), name="EntityList"),
    path('entityview', EntityList.as_view(), name="EntityList"),
    # update or delete a single entity
    path('entity/<str:entity>', EntityViews.as_view(), name="Entityperticular"),
    # List of all conversations
    path('conversation', ConversationsView.as_view(), name="ConversationInsert"),
    path('conversationview', ConversationsList.as_view(), name="ConversationInsertView"),
    # delete all conversations of an user 
    path('message', MessageView.as_view(), name="ConversationUpdate"),
    # to train the chatbot
    path('train', Train_bot.as_view(), name="Bot-Train"),
    # to train the chatbot
    path('train_file', Train_bot_csv.as_view(), name="Bot-Train-Csv"),
    # api to send message to bot and get response from bot as well as save the conversation
    path('chat', ChatView.as_view(), name="chat"),
    # save user info at the start of conversation
    path('chats', Chatrun.as_view(), name="chat-start"),
    path('chatsview', ChatrunList.as_view(), name="chat-startview"),
    # save client's file to train the bot
    path('file', FilesaveView.as_view(), name="File-Save"),
    path('fileview', FilesaveList.as_view(), name="File-Save view"),
    # quicklinks test
    path('quick', SaveQuicklinks.as_view(), name="Test-Quick_Links"),
    # FAQ data display
    path('faq', FAQViews.as_view(), name="FAQs"),
    # logout destroy token
    path('api/logout/', LogoutView.as_view(), name="Logout"),
    # For FAQs backup
    path('backup',DownloadView.as_view(), name="FAQ-Download"),
    path('window', get_chatwindow, name="chat-window"),
    path('psbbot', chatbot,  name="psbbot"),

]
