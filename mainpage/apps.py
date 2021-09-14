from django.apps import AppConfig




class MainpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainpage'
    def ready(self):
        from mainpage.VSBLogic import Scanner
        import colorama
        from colorama import Fore, Back, Style
        colorama.init(autoreset=True)
