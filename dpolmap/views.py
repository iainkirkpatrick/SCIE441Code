from django.shortcuts import render_to_response

def under_construction(request):
    cons = "under construction"
    oper = "operational"
    return render_to_response('dpolmap_main.html', {'working': cons})
