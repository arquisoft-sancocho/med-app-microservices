from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def test_url_resolution(request):
    """Simple test view to check if URL routing works"""
    return HttpResponse("URL routing works!", content_type="text/plain")

@login_required
def index(request):
    try:
        logger.info(f"Index view called by user: {request.user}")
        
        # Try to render the template
        return render(request, 'index.html')
        
    except Exception as e:
        logger.error(f"Error in index view: {str(e)}")
        return create_fallback_response(request, f"Error: {str(e)}")


# Microservice redirect views for seamless navigation
@login_required
def examenes_redirect(request):
    """Redirect to examenes microservice"""
    exams_url = settings.EXAMS_SERVICE_URL.rstrip('/')
    # Extract the path after /examenes/
    full_path = request.get_full_path()
    if full_path.startswith('/examenes/'):
        path = full_path[len('/examenes/'):]
    elif full_path == '/examenes':
        path = ''
    else:
        path = full_path
    
    # Ensure path starts with /
    if path and not path.startswith('/'):
        path = '/' + path
    elif not path:
        path = '/'
        
    redirect_url = f"{exams_url}{path}"
    logger.info(f"Redirecting to examenes service: {redirect_url}")
    return HttpResponseRedirect(redirect_url)

@login_required
def diagnosticos_redirect(request):
    """Redirect to diagnosticos microservice"""
    diagnosis_url = settings.DIAGNOSIS_SERVICE_URL.rstrip('/')
    # Extract the path after /diagnosticos/
    full_path = request.get_full_path()
    if full_path.startswith('/diagnosticos/'):
        path = full_path[len('/diagnosticos/'):]
    elif full_path == '/diagnosticos':
        path = ''
    else:
        path = full_path
    
    # Ensure path starts with /
    if path and not path.startswith('/'):
        path = '/' + path
    elif not path:
        path = '/'
        
    redirect_url = f"{diagnosis_url}{path}"
    logger.info(f"Redirecting to diagnosticos service: {redirect_url}")
    return HttpResponseRedirect(redirect_url)

@login_required
def cirugias_redirect(request):
    """Redirect to cirugias microservice"""
    surgery_url = settings.SURGERY_SERVICE_URL.rstrip('/')
    # Extract the path after /cirugias/
    full_path = request.get_full_path()
    if full_path.startswith('/cirugias/'):
        path = full_path[len('/cirugias/'):]
    elif full_path == '/cirugias':
        path = ''
    else:
        path = full_path
    
    # Ensure path starts with /
    if path and not path.startswith('/'):
        path = '/' + path
    elif not path:
        path = '/'
        
    redirect_url = f"{surgery_url}{path}"
    logger.info(f"Redirecting to cirugias service: {redirect_url}")
    return HttpResponseRedirect(redirect_url)


def create_fallback_response(request, error_message=""):
    """Create a fallback HTML response when template rendering fails"""
    
    # Basic HTML template with inline CSS
    fallback_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Medical System</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .container {{
                text-align: center;
                padding: 40px;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                max-width: 500px;
                margin: 20px;
            }}
            .logo {{
                font-size: 4em;
                margin-bottom: 20px;
            }}
            .title {{
                color: #333;
                font-size: 2.5em;
                margin-bottom: 10px;
                font-weight: 300;
            }}
            .subtitle {{
                color: #666;
                font-size: 1.2em;
                margin-bottom: 30px;
            }}
            .user-info {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            }}
            .error-info {{
                background: #fff3cd;
                color: #856404;
                padding: 10px;
                border-radius: 5px;
                font-size: 0.9em;
                margin-top: 20px;
            }}
            .navigation {{
                margin-top: 30px;
            }}
            .nav-link {{
                color: #007bff;
                text-decoration: none;
                margin: 0 15px;
                padding: 10px 20px;
                border: 1px solid #007bff;
                border-radius: 5px;
                display: inline-block;
                transition: all 0.3s;
            }}
            .nav-link:hover {{
                background: #007bff;
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🏥</div>
            <h1 class="title">Medical System</h1>
            <p class="subtitle">Healthcare Management Platform</p>
            
            <div class="user-info">
                <strong>Welcome, {request.user.username if request.user.is_authenticated else 'Guest'}!</strong>
                {f'<br><small>Email: {request.user.email}</small>' if request.user.is_authenticated and request.user.email else ''}
            </div>
            
            <div class="navigation">
                <a href="/admin/" class="nav-link">Admin Panel</a>
                <a href="/logout/" class="nav-link">Logout</a>
            </div>
            
            {f'<div class="error-info">Note: {error_message}</div>' if error_message else ''}
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(fallback_html)

