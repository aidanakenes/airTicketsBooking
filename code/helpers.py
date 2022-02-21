def with_connection(f):
    async def with_connection_(pool, *args, **kwargs):

        async with pool.acquire() as conn:
            transaction = conn.transaction()
            await transaction.start()
            try:
                result = await f(connection=conn, *args, **kwargs)

            except Exception as e:
                await transaction.rollback()
                print(e)
                raise
            else:
                await transaction.commit()

        return result

    return with_connection_
