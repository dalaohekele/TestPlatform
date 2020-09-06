from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # 注册signals
    def ready(self):
        import users.signals