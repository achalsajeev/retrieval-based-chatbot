from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Domains)
admin.site.register(Intents)
admin.site.register(Entity)
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Company)
admin.site.register(Human_agent)
admin.site.register(Admin)
admin.site.register(Bot_agent)
admin.site.register(Conversations)
admin.site.register(Message)
admin.site.register(TrainFiles)