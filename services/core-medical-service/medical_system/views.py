from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

@login_required
def index(request):
    try:
        logger.info(f"Index view called by user: {request.user}")
        return render(request, 'index.html')
    except Exception as e:
        logger.error(f"Error in index view: {str(e)}")
        # Return a simple response if template rendering fails
        return HttpResponse(f"<h1>Welcome to Medical System</h1><p>User: {request.user}</p><p>Error: {str(e)}</p>")

