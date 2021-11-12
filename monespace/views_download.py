import csv
from django.http import HttpResponse
import datetime

from .models import StatusUsersLocations


def download_users_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="monespace_benevoles.csv"'},
    )

    writer = csv.writer(response)
    all_users = StatusUsersLocations.objects.filter(status=1) | StatusUsersLocations.objects.filter(status=2)
    writer.writerow(['Nom utilisateur', 'Email', 'Prénom', 'Nom', 'Site', 'Status dans ce site'])
    for i in all_users:
        writer.writerow([i.user.username, i.user.email, i.user.first_name , i.user.last_name, i.location.name, i.status])

    return response