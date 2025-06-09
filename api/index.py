from todolist.wsgi import application
from vercel_wsgi import handle_request

def handler(request, context):
    return handle_request(request, application)
