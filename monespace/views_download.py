import csv
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import StatusUsersLocations, Location
from .functions_global import forbidden_to_user


@forbidden_to_user
@login_required(login_url='/login/')
def download_users_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="monespace_benevoles.csv"'},
    )

    writer = csv.writer(response)
    all_users=[]

    try:
        request.GET['site']
        location = Location.objects.get(pk=request.GET['site'])
    except:
        all_users = StatusUsersLocations.objects.filter(status=1) | StatusUsersLocations.objects.filter(status=2)
    else:
        if location in Location.objects.filter(location_managers=request.user):
            all_users = StatusUsersLocations.objects.filter(status=1, location=location) | StatusUsersLocations.objects.filter(status=2, location=location)
        else:
            return redirect('index')
    finally:
        writer.writerow(['Nom utilisateur', 'Email', 'Prénom', 'Nom', 'Site', 'Status dans ce site'])
        for i in all_users:
                writer.writerow([i.user.username, i.user.email, i.user.first_name , i.user.last_name, i.location.name, i.status])

    return response