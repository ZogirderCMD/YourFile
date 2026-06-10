from tools import Que, Logger
from objects import *
import sqlite3

logger = Logger(console_print=True)
logger.log("Starting app...")

try:
    con = sqlite3.connect("database.db",check_same_thread=False)
    cur = con.cursor()
except Exception as e:
    logger.log(f"Failed connection to database! {e}")
    exit()

logger.log("Connected to database!")

que = Que(con, cur, logger)
logger.log("Query linked!")

que.query(open("tables.sql", "r").read())
logger.log("Tables created!")

FileManager = FileManager(logger=logger, que=que)

uid = FileManager.save_file(open("file.docx", "rb").read(), "Паспорт проекта")
print(uid)
input()
res = FileManager.get_file(uid)
print(res)
input()
res = FileManager.remove_file(uid)
print(res)

logger.log("Shutting down...")