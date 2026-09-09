from django.apps import AppConfig


class DjangoRagkitConfig(AppConfig):
    name = 'django_ragkit'

    def ready(self):
        print("ready called")
        import django_ragkit.signals