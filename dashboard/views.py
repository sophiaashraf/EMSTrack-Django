import logging
from django.views.generic.base import TemplateView
from rest_framework.authtoken.models import Token
import requests
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)

class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # if mode is dev, we directly call ucsd server, which has data
        # if mode is prod, we call ourselves, which will have nothing if 
        # running on local machine, but will have data when on ucsd server
        mode = "production" # run in dev if on local machine, change to prod when deploy
        if mode == "dev":
            SERVER = "UCSD"
            param = {
                'username': os.environ["DASHBOARD_USERNAME_" + SERVER],
                'password': os.environ["DASHBOARD_PASSWORD_" + SERVER],
            }
            url = os.environ["DASHBOARD_AUTHURL_" + SERVER]
            res = requests.post(url, data=param)
            res.raise_for_status()
            token = res.json()['token']
        elif mode == "production": # if running on your own computer, has empty data
            token, created = Token.objects.get_or_create(user=self.request.user)
        context['token'] = token

        return context