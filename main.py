from tools import Que, Logger
from flask import render_template, Flask, request
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
logger.log("File Manager initialised!")

app = Flask(__name__)
logger.log("Flask App initialised!")

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/getFiles", methods=["GET"])
def getFiles():
    return FileManager.get_files(request.remote_addr)

@app.route("/uploadFile", methods=["POST"])
def getFiles():
    
    return 0

@app.route("/removeFile/<uid>", methods=["DELETE"])
def getFiles(uid):
    return FileManager.remove_file(uid, request.remote_addr)

app.run()

logger.log("Shutting down...")