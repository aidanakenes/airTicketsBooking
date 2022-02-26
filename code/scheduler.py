from apscheduler.schedulers.asyncio import AsyncIOScheduler

import currencies


scheduler = AsyncIOScheduler(timezone='Asia/Almaty')

scheduler.add_job(
    currencies.update_currency,
    trigger='cron',
    minute=10,
    hour=19,
    max_instances=1,
    replace_existing=True,
)

scheduler.start()
