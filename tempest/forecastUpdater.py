from apscheduler.schedulers.background import BackgroundScheduler
from .data_api import record_sp_wthr

class bt_unit_provider:
    def __init__(self, set_bt=0):
        self.num = set_bt
    
    def __str__(self):
        print(f'current num: {self.num}')
        return
    
    def provide(self):
        temp = self.num
        if self.num > 7:
            self.num=0
        else: 
            self.num +=1
        return temp
        
def climateupdate():
    job_defaults = {
        'max_instances': 1
        }  
    scheduler = BackgroundScheduler()
    scheduler.configure(
        job_defaults=job_defaults,
        timezone='Asia/Seoul'
    )
    scheduler.add_job(record_sp_wthr, 'cron', hour='2,5,8,11,14,17,20,23',  minute='5')
    scheduler.start()