import pickledb
import time

db = pickledb.load("DB/t_dict.db", False)

db.dcreate("cluj_places")

db.dadd("cluj_places", ("euphoria" , dict([('searches', 0), ('date_added', '03-02-2014')])))
db.dadd("cluj_places", ("broadway" , dict([('searches', 0), ('date_added', '03-02-2014')])))


keys_1 = db.dgetall("cluj_places")
print keys_1
keys_a = db.dget("cluj_places", "euphoria")
keys_a['searches'] = 1
print keys_a['searches']
db.dump()
keys_1 = db.dgetall("cluj_places")
print keys_1