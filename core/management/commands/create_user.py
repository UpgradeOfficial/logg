from django.core.management.base import BaseCommand
from user.models import User

class Command(BaseCommand):
    help = 'create users'

    def add_arguments(self, parser):
        parser.add_argument('email', nargs='+', type=int, help='User ID')

    def handle(self, *args, **kwargs):
        users_ids = kwargs['user_id']

        for user_id in users_ids:
            try:
                user = User.objects.get(pk=user_id)
                user.delete()
                self.stdout.write(self.style.SUCCESS('User "%s (%s)" deleted with success!' % (user.username, user_id)))
            except User.DoesNotExist:
                self.stdout.write(self.style.WARNING('User with id "%s" does not exist.' % user_id))