from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

from code import currencies


scheduler = AsyncIOScheduler(timezone='Asia/Almaty')
scheduler.add_job(
    currencies.update_currency,
    trigger='cron',
    minute=0,
    hour=12,
    max_instances=1,
    replace_existing=True,
)

scheduler.start()

asyncio.get_event_loop().run_forever()
