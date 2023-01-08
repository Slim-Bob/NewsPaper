from django.core.management.base import BaseCommand, CommandError
from ...models import Post, Category


class Command(BaseCommand):
    help = 'Deletes all news in the category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        del_category = options["category"]
        answer = input(f'Delete all news from the {del_category} category? y/n')

        if answer != 'y':
            self.stdout.write(self.style.ERROR('Cancelled'))

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'All news from the {category.name} category has been successfully deleted'))
        except category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Couldn\'t find the {del_category} category'))