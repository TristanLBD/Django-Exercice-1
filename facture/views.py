from django.shortcuts import render
from datetime import datetime

# Create your views here.
def index(request):
    context = {
        'messages': [
            {
                'content': 'text',
                'username': 'Tristan',
                'created_at': datetime.now(),
            },
                        {
                'content': 'text',
                'username': 'Tristan',
                'created_at': datetime.now(),
            },
                        {
                'content': 'text',
                'username': 'Tristan',
                'created_at': datetime.now(),
            },
        ]
    }
    return render(request, 'index.html', context=context)
