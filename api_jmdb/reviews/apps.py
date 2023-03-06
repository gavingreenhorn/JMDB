from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate

from reviews.utils import get_csv_data, set_by_id


class ReviewsConfig(AppConfig):
    name = 'reviews'
    verbose_name = name.capitalize()

    def post_migration(self, sender, **kwargs):
        """Code to run after migration is completed."""
        verbosity = kwargs['verbosity']
        self.setup_permissions(verbosity=verbosity)
        self.prepopulate_database(verbosity=verbosity)

    def setup_permissions(self, **kwargs) -> None:
        """Get and set permissions for the groups that should have them."""
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth.models import Group, Permission

        verbosity = kwargs['verbosity']
        if verbosity >= 1:
            print('Setting up permissions for all user roles.')
        review = self.get_model('Review')
        comment = self.get_model('Comment')
        review_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(review))
        comment_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(comment))
        Group.objects.get_or_create(name='user')
        moderators, created = Group.objects.get_or_create(name='moderator')
        if verbosity >= 2:
            print('Setting up moderator permissions.')
        moderator_permissions = (
            list(filter(
                lambda perm: perm.codename in (
                    'delete_review',
                    'change_review'),
                review_permissions))
            + list(filter(
                lambda perm: perm.codename in (
                    'delete_comment',
                    'change_comment'),
                comment_permissions))
        )
        moderators.permissions.add(*moderator_permissions)
        admins, created = Group.objects.get_or_create(name="admin")
        if verbosity >= 2:
            print('Setting up administrator permissions.')
        admins.permissions.set(Permission.objects.all())

    def prepopulate_database(self, verbosity) -> None:
        """Fill database with data from included csv files."""
        from django.contrib.auth.models import Group

        if verbosity >= 1:
            print('Populating database with test data.')

        def load_model_data(self, source, modelname, related_field=None):
            """Get data from csv source, create model instances from it"""
            if verbosity >= 2:
                print(f'Creating {modelname} objects.')
            data = get_csv_data(source=source)
            model = self.get_model(modelname)
            for payload in data:
                if related_field:
                    set_by_id(payload, related_field)
                if not model.objects.filter(id=payload['id']).exists():
                    model.objects.get_or_create(**payload)

        user = get_user_model()

        Group.objects.get_or_create(name='user')
        Group.objects.get_or_create(name='moderator')
        Group.objects.get_or_create(name='admin')

        user_data = get_csv_data(source='users')
        for payload in user_data:
            user.objects.get_or_create(**payload)

        load_model_data(self, 'genre', 'Genre')
        load_model_data(self, 'category', 'Category')
        load_model_data(self, 'titles', 'Title', 'category')
        load_model_data(self, 'review', 'Review', 'author')
        load_model_data(self, 'comments', 'Comment', 'author')

        genre_title_data = get_csv_data(source='genre_title')
        for payload in genre_title_data:
            title = self.get_model('Title')
            through = title.genre.through
            if not through.objects.filter(id=payload['id']).exists():
                through.objects.create(**payload)

    def ready(self) -> None:
        post_migrate.connect(self.post_migration, sender=self)
