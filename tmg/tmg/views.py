from django.shortcuts import render, render_to_response

def page_not_found(request, **kwargs):
    response = render_to_response('html/404.html', {})
    response.status_code = 404
    return response
    # return render(request, 'html/404.html')