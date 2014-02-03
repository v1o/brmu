import pickledb
import time
#generate some records
#load romania.db
db = pickledb.load("DB/romania.db", False)

f = open("DB/orase.txt", 'r')

#insert cities

db.dcreate("cities_list")
for line in f:
	db.dadd("cities_list", (line.lower().strip() , dict([('searches', 0)])))	
f.close()

f = open("DB/beers.txt", 'r')
#insert beers

db.dcreate("beers_list")
for line in f:
	db.dadd("beers_list", (line.lower().strip() , dict([('searches', 0)])))
f.close()

f = open("DB/places_cluj.txt", 'r')
#insert cluj places

db.dcreate("cluj-napoca_places")
for line in f:
	timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")	
	db.dadd("cluj-napoca_places", (line.lower().strip() , dict([('searches', 0), ('datetime_added', timestamp)])))
f.close()

f = open("DB/cluj_places_beers.txt", 'r')

db.dcreate("cluj-napoca_places_beers")
for line in f:
	timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")	
	db.dadd("cluj-napoca_places_beers", (line.lower().strip() , dict([('searches', 0), ('price', 0), ('datetime_added', timestamp)])))	
f.close()

db.dump()