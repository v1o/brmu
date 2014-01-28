import pickledb
#generate some records
#load romania.db
db = pickledb.load("DB/romania.db", False)

f = open("DB/orase.txt", 'r')

#insert cities
db.lcreate("cities_list")

for line in f:
	db.ladd("cities_list", line.lower().strip())
	print line.lower()

f.close()

f = open("DB/beers.txt", 'r')
#insert beers
db.lcreate("beers_list")
for line in f:
	db.ladd("beers_list", line.lower().strip())
	print line.lower()

f.close()

f = open("DB/places_cluj.txt", 'r')
#insert cluj places
db.lcreate("cluj_places")
for line in f:
	db.ladd("cluj_places", line.lower().strip())
	print line.lower()

f.close()

f = open("DB/cluj_places_beers.txt", 'r')

db.lcreate("cluj_places_beers")
for line in f:
	db.ladd("cluj_places_beers", line.lower().strip())

f.close()

db.dump()