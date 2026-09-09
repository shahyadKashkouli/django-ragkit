from abc import ABC

from django.conf import settings


class BaseProvider(ABC):
    settings_key = None
    DEFAULT_CONFIG = {}
    @property
    def config(self):
        user_config = settings.RAGKIT.get(self.settings_key, {})

        return {
            **self.DEFAULT_CONFIG,
            **user_config,
        }

    @property
    def model(self):
        return self.config["MODEL"]

    @property
    def base_url(self):
        return self.config["BASE_URL"]
    @property
    def provider(self):
        return self.config["PROVIDER"]

    @property
    def api_key(self):
        return self.config["API_KEY"]