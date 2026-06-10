from tools import *
import os

class FileManager:
    path:str="files"
    logger:Logger
    que:Que

    def __init__(self,que:Que,path="files",logger:Logger=Logger()):
        self.path = path
        self.logger = logger
        self.que = que
        try:
            os.mkdir(self.path)
            self.logger.log("Created files path!")
        except FileExistsError:
            pass
    def save_file(self, file:bytes, name:str):
        self.que.query("SELECT uid FROM files")
        uid = gen_uid()
        print(uid)
        open(f"{self.path}/{uid}", "wb").write(file)
        self.logger.log("File stored in path!")
        self.que.query("INSERT INTO files VALUES (?, ?)", (uid, name, ))
        self.logger.log("File stored in database!")
        return uid
    def get_file(self, uid):
        self.que.query("SELECT filename FROM files WHERE uid=?", (uid, ))
        res = self.que.cur.fetchall()
        if len(res) == 0: return "File not found!"
        return {"filename": res[0][0], "uid":uid}
    def remove_file(self, uid):
        self.que.query("SELECT filename FROM files WHERE uid=?", (uid, ))
        res = self.que.cur.fetchall()
        if len(res) == 0: return "File not found!"
        self.que.query("DELETE FROM files WHERE uid=?", (uid, ))
        os.remove(f"{self.path}/{uid}")
        return "File removed!"