import os, datetime, random

class Logger:
    path:str="logs"
    console_print:bool=False
    def __init__(self,path="logs",console_print=False):
        self.path = path
        self.console_print = console_print
        try:
            os.mkdir(self.path)
            self.log("Created logs path!")
        except FileExistsError:
            pass
    def log(self, txt):
        file_path = f"{self.path}/{datetime.datetime.now().date()}"
        if not os.path.exists(file_path):
            open(file_path, "w").write("")
        time_txt = f"[{str(datetime.datetime.now().time()).split(".")[0]}]: "
        past_txt = open(file_path, "r").read()
        fin_text = f"{past_txt}{time_txt}{txt}\n"
        open(file_path, "w").write(fin_text)
        if self.console_print: print(f"{time_txt}{txt}")

class Que:
    def __init__(self, con, cur, logger:Logger=Logger()):
        self.con = con
        self.cur = cur
        self.logger = logger
    def query(self, q, a=()):
        try:
            self.cur.execute(q, a)
            self.con.commit()
            self.logger.log(f"Made query: {q}, {a}")
        except Exception as e:
            self.logger.log(f"Error in query: {q}, {a}, {e}")
            self.con.rollback()

def gen_uid(length=30):
        characters = [i for i in "qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM"]
        uid = ""
        for i in range(length):
            uid+=random.choice(characters)
        return uid