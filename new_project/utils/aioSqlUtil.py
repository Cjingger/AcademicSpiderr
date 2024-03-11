# !/usr/bin/python3
# -*- coding:utf-8 -*-
import asyncio
import os
import aiomysql
from common.logs import Logs
from common.Files import Files

log = Logs()
# path = r"E:\project\new_project"
ylFile = Files()
MYSQL_items = ylFile.getConfigDict("Mysql-Config-ali")
MYSQL_HOST = MYSQL_items['host']
MYSQL_DB = MYSQL_items['db']
MYSQL_PORT = int(MYSQL_items['port'])
MYSQL_USER = MYSQL_items['usr']
MYSQL_PASSWORD = MYSQL_items['code']



class sqlAlchemyUtil():

    def __init__(self):
        # self.engine = create_async_engine(f'mysql+asyncmy://{MYSQL_USER}@{MYSQL_HOST}/{MYSQL_DB}',
        #                pool_size=80, max_overflow=0, pool_recycle=1500)
        # self.async_session = sessionmaker(self.engine, class_=AsyncSession)
        pass

    async def get_mysql_pool(self):
        return await aiomysql.create_pool(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
                                          password=MYSQL_PASSWORD,
                                          db=MYSQL_DB,
                                          loop=asyncio.get_event_loop(), autocommit=False,
                                          maxsize=5,
                                          minsize=1,
                                          pool_recycle=5)

    async def create_table(self, t):
        # async with self.async_session() as session:
        #     async with session.begin():
                conn = await aiomysql.connect(
                    host=MYSQL_HOST,
                    port=MYSQL_PORT,
                    user=MYSQL_USER,
                    password=MYSQL_PASSWORD,
                    db=MYSQL_DB,
                    loop=asyncio.get_event_loop()
                )
                cur = await conn.cursor()
                try:
                    await cur.execute(f'''CREATE TABLE IF NOT EXISTS {t} (
                        `id` varchar(64) NOT NULL,
                        `author` varchar(64) NOT NULL,
                        `article` varchar(1000) NOT NULL,
                        `abstract` text,
                        `url` varchar(1000) NOT NULL,
                        `time` INT,
                        `data_from` varchar(20) NOT NULL,
                        `keyword` varchar(300),
                        `is_qikan` INT default 0,
                        `email` varchar(100) NOT NULL,
                        `area` varchar(100) NOT NULL,
                        `is_ch` INT,
                        `classify` varchar(300) NOT NULL,
                        `discipline` varchar(300),
                        `subdiscipline` varchar(300),
                        `conference` varchar(1000),
                        `journal` varchar(300),
                        `create_time` DATETIME NOT NULL,
                        PRIMARY KEY(`id`),
                        UNIQUE (`id`, `email`)
                        ) ENGINE=innodb, CHARSET=utf8mb4;
        ''')
                    await conn.commit()
                    conn.close()
                except Exception as e:
                    log.error(f'''SQL execution error,
                                hint:\n {e}\n,''')
                    await conn.rollback()
                    await cur.close()

    async def insert_data(self, t: str, d: dict):
        # async with self.async_session() as session:
        #     async with session.begin():
                conn = await aiomysql.connect(
                    host=MYSQL_HOST,
                    port=MYSQL_PORT,
                    user=MYSQL_USER,
                    password=MYSQL_PASSWORD,
                    db=MYSQL_DB,
                    loop=asyncio.get_event_loop()
                )
                cur = await conn.cursor()
                try:
                    await cur.execute(f'''replace into {t} (id, author, article, abstract, url, time, data_from, keyword, is_qikan, email, area, is_ch, classify, discipline, subdiscipline, conference, journal, create_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                                          ({d['id']}, {d['author']}, {d['article']}, {d['abstract']}, {d['url']}, {d['time']}, {d['data_from']}, {d['keyword']}, {d['is_qikan']}, {d['email']}, {d['area']}, {d['is_ch']}, {d['classify']}, {d['discipline']}, {d['subdiscipline']}, {d['conference']}, {d['journal']}, {d['create_time']}))
                    await conn.commit()
                    log.info("数据插入/更新成功")
                    conn.close()
                except Exception as e:
                    log.error(f'''SQL execution error, hint:\n {e}\n,''')
                    await conn.rollback()
                    await cur.close()

    async def query_data(self, **kwargs):
        task = [
            asyncio.ensure_future(self.get_mysql_pool())
        ]
        await asyncio.wait(task)
        pool = [t.result() for t in task]
        pool = pool[0]
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
        # conn = await aiomysql.connect(
        #     host=MYSQL_HOST,
        #     port=MYSQL_PORT,
        #     user=MYSQL_USER,
        #     password=MYSQL_PASSWORD,
        #     db=MYSQL_DB,
        #     loop=asyncio.get_event_loop()
        # )
        # cur = await conn.cursor()
                try:
                    sql = f'''SELECT author, article, abstract, url, `time`, data_from, keyword, is_qikan, email, area, classify, discipline, subdiscipline, conference, journal FROM {kwargs.get('t')} WHERE 1=1 and is_ch=1 and journal = "{kwargs.get('journal')}"'''
                    # sql = f'''-- SELECT author, article, abstract, url, `time`, data_from, keyword, is_qikan, email, area, classify, discipline, subdiscipline, conference, journal FROM {kwargs.get('t')} WHERE 1=1 and (is_ch = 0 or is_ch = 2 and journal = "{kwargs.get('journal')}");'''
                    await cur.execute(sql)
                    ret = await cur.fetchall()

                    # await cur.close()
                    # conn.close()
                    return ret
                except Exception as e:
                    await conn.ping()
                    log.error(f'''SQL QUERT err, \n {e}\n''')
                    await conn.rollback()
                    await cur.close()
                finally:
                    await cur.close()
                    conn.close()
