from django.core.mail import EmailMessage, send_mail, mail_admins, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
import requests
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
import logging

# @cache_page(5*60)
# def say_hello(request):
    # try:
        # send_mail('subject', 'message', 'info@haribuy.com', ['bob@haribuy.com'])

        # mail_admins("subject", "message", html_message='message')

        # message = EmailMessage('subject', 'message', 'from@haribuy.com', ['john@haribuy.com'])
        # message.attach_file('playground/static/images/hari.jpg')
        # message.send()

        # message = BaseEmailMessage(
        #     template_name='emails/hello.html',
        #     context = {'name':'Harish'}
        # )
        # message.send(['john@haribuy.com'])
    # except BadHeaderError:
    #     pass

    # requests.get('https://httpbin.org/delay/2')
    # return render(request, 'hello.html', {'name': 'Harish'})


    #for caching process using low level api
    # key = 'httpbin_result'
    # if cache.get(key) is None:
    #     response = requests.get('https://httpbin.org/delay/2')
    #     data = response.json()
    #     cache.set(key, data)
    # return render(request, 'hello.html', {'name': cache.get(key)})

    #cashing views
    # response = requests.get('https://httpbin.org/delay/2')
    # data = response.json()
    # return render(request, 'hello.html', {'name': data})


# class HelloView(APIView):
#     @method_decorator(cache_page(5*60))
#     def get(self, request):
#         response = requests.get('https://httpbin.org/delay/2')
#         data = response.json()
#         return render(request, 'hello.html', {'name': 'Harish'})

#for logging 
logger = logging.getLogger(__name__)

class HelloView(APIView):
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Received the response')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('httpbin is offline')

        return render(request, 'hello.html', {'name': 'Harish'})

