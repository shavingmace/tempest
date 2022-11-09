from django.apps import AppConfig



class TempestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tempest'
    
    def ready(self):
        from .forecastUpdater import climateupdate  # AppConfig 객체의 ready()를 오버라이드 할 때는 꼭 내부에서 임포트해야한다!!!
        climateupdate()
