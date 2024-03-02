from django.core.mail import send_mail
from django.views import View
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from django.middleware.csrf import get_token


def csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})


class EmailSenderView(View):
    @swagger_auto_schema(
        responses={200: "Email enviado com sucesso!"},
        operation_description="Send email",
        tags=['email'],
        security=[],
    )
    def post(self, request):
        if request.method == 'POST':
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            recipient = request.POST.get('recipient')

            send_mail(
                subject=subject,
                message=message,
                from_email=None,  # set to default email defined in settings.py
                recipient_list=[recipient],
                fail_silently=False,
            )

            return HttpResponse('Email enviado com sucesso!')
        return HttpResponse('Erro ao enviar email.', status=405)
