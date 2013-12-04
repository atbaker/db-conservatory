from django.core.management.base import BaseCommand
from ...models import Database, Container
from ...utils import get

class Command(BaseCommand):
    help = 'Verifies that all images and containers are available on spin-docker host'

    def handle(self, *args, **options):
        self.stdout.write('Checking images')
        spin_docker_images = get('images')
        self.stdout.write('%s images in spin-docker' % len(spin_docker_images))

        dbc_images = Database.objects.all()
        self.stdout.write('%s databases in DBC' % len(dbc_images))

        for database in dbc_images:
            if database.image not in spin_docker_images:
                self.stdout.write('Deactivating image for %s' % database)
                database.active = False
                database.save()
        self.stdout.write('Database audit complete')

        self.stdout.write('Checking containers')
        spin_docker_containers = get('containers')
        spin_docker_containers = [c['id'] for c in spin_docker_containers]
        self.stdout.write('%s containers in spin-docker' % len(spin_docker_containers))

        dbc_containers = Container.objects.all()
        self.stdout.write('%s containers in DBC' % len(dbc_containers))

        for container in dbc_containers:
            if container.container_id not in spin_docker_containers:
                self.stdout.write('Deactivating container %s' % container)
                container.active = False
                container.save()

        self.stdout.write('Container audit complete')
