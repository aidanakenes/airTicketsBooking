import functools
import time


def with_connection(f):
    async def with_connection_(pool, *args, **kwargs):

        async with pool.acquire() as conn:
            transaction = conn.transaction()
            await transaction.start()
            try:
                result = await f(connection=conn, *args, **kwargs)

            except Exception as e:
                await transaction.rollback()
                raise
            else:
                await transaction.commit()

        return result

    return with_connection_


def retry(exc_to_check, tries: int = 5, delay: int = 3):
    def deco_retry(func):
        @functools.wraps(func)
        def func_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 0:
                try:
                    return func(*args, *kwargs)
                except exc_to_check as e:
                    time.sleep(mdelay)
                    mtries -= 1
            return func(*args, **kwargs)

        return func_retry

    return deco_retry
