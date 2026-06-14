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
    def save_file(self, file, owner_ip:str):
        name = file.filename
        self.que.query("SELECT uid FROM files")
        uid = gen_uid()
        print(uid)
        file.save(f"{self.path}/{uid}")
        self.logger.log(f"File stored in path for {owner_ip}!")
        self.que.query("INSERT INTO files VALUES (?, ?, ?)", (uid, name, owner_ip, ))
        self.logger.log(f"File stored in database for {owner_ip}!")
        return uid
    def get_file(self, uid):
        self.que.query("SELECT filename FROM files WHERE uid=?", (uid, ))
        res = self.que.cur.fetchall()
        if len(res) == 0: return "File not found!"
        return {"filename": res[0][0], "uid":uid}
    def remove_file(self, uid, owner_ip):
        self.que.query("SELECT filename FROM files WHERE uid=? AND owner_ip=?", (uid, owner_ip, ))
        res = self.que.cur.fetchall()
        if len(res) == 0: return {"result": 404}
        self.que.query("DELETE FROM files WHERE uid=?", (uid, ))
        os.remove(f"{self.path}/{uid}")
        return {"result": 200}
    def get_files(self, owner_ip):
        self.que.query("SELECT uid, filename FROM files WHERE owner_ip=?", (owner_ip, ))
        res = self.que.cur.fetchall()
        pack = []
        for i in res:
            pack.append({"uid": i[0], "name": i[1]})
        return {"result":pack}
