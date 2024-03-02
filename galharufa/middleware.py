from sys import stdout
import logging
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(stdout))


class RequestMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # your middleware logic here
        logger.info(request.headers)
        logger.info("Host: " + request.get_host())
        if request.method in {'POST', 'PUT', 'PATCH'}:
            logger.info(request.body)
        response = self.get_response(request)
        return response


class ResponseMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Replace '*' with your specific allowed origin(s) or a function to determine the allowed origin
        response['Access-Control-Allow-Origin'] = ['127.0.0.1', 'localhost',
                                                   'galharufa-frontend-load-balancer-56051477.sa-east-1.elb.amazonaws.com']
        response['Access-Control-Allow-Methods'] = 'GET, PATCH, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization'
        response['Access-Control-Allow-Credentials'] = 'true'
        logger.info(response.items())
        return response
