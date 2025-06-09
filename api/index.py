from todolist.wsgi import application
from vercel_python import VercelHandler

handler = VercelHandler(application)
