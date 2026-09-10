from django.apps import AppConfig


class DjangoRagkitConfig(AppConfig):
    name = 'django_ragkit'

    def ready(self):
        import django_ragkit.signals