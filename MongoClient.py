from pymongo import MongoClient


def writetodb(result):
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["testdb"]
    imagescol = mydb["images"]
    #toDB = imagescol.insert_one(result)


