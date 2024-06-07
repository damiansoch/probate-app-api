from django.core.management import BaseCommand

from core.models import ApplicationStatus


class Command(BaseCommand):
    help = 'Populates the ApplicationStatusId table with initial data'

    def handle(self, *args, **options):
        data = {
            0: 'Unknown',
            1: 'Active Application',
            2: 'Application Cancelled',
            3: 'Borrower Declined',
            4: 'Fraud Risk',
            5: 'Fraud',
            6: 'Loan Paid Out',
            7: 'Settled',
        }

        for id, name in data.items():
            ApplicationStatus.objects.update_or_create(id=id, defaults={'name': name})
