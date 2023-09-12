from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def check_table_bot(self):
        sql = "SELECT * FROM usersmanage_bot "
        await self.execute(sql, execute=True)

    async def get_setting(self):
        sql = "SELECT * FROM usersmanage_bot"
        return await self.execute(sql, fetch=True)


    async def create_table_setting(self, token, username):
        sql = 'SELECT * FROM "usersmanage_bot"'
        text_bot = await self.execute(sql, fetch=True)
        if not text_bot:
            sql = '''INSERT INTO "usersmanage_bot" (token, name, admins, support) VALUES($1, $2, $3, $4)'''
            await self.execute(sql, token, username, '1', '1',  fetchrow=True)
        elif text_bot[0].get('token') != token:
            await self.execute('UPDATE "usersmanage_bot" SET token=$1', token, execute=True)
            await self.execute('UPDATE "usersmanage_bot" SET name=$1', username, execute=True)
