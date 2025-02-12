
import os

def username_context(request):
    return {
        'username': os.getlogin().split('\\')[-1].replace('.', ' ')
    }