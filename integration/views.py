from django.shortcuts import render
from django.conf import settings
import requests, json
from .models import Team
from django.http import HttpResponse


def index(request):
    client_id = settings.SLACK_CLIENT_ID
    return render(request, 'slack_landing.html', {'client_id': client_id})


def slack_oauth(request):
    code = request.GET['code']
    
    params = { 
        'code': code,
        'client_id': settings.SLACK_CLIENT_ID,
        'client_secret': settings.SLACK_CLIENT_SECRET
    }
    url = 'https://slack.com/api/oauth.access'
    json_response = requests.get(url, params)
    data = json.loads(json_response.text)
    Team.objects.create(
        name=data['team_name'], 
        team_id=data['team_id'],
        bot_user_id=data['bot']['bot_user_id'],     
        bot_access_token=data['bot']['bot_access_token'],
        chat_type="slack"
    )
    return HttpResponse('Bot added to your Slack team!')