import pickledb
import time
from database_operations import db_operations
#generate some records
#load romania.db
db = db_operations("DB/romania.db")

f = open("orase.txt", 'r')

#insert cities

for line in f:
	db.save_city(line.lower().strip())
	
f.close()