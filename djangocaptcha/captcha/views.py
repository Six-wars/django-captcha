from django.shortcuts import render, render_to_response

def login_page(request, template_name="login.html"):
    context = {'title': 'Login Page'}
    return render_to_response(template_name, context)
