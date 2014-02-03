import web
import pickledb
import json
import time

urls = (
    '/', 'index',
    '/cities', 'get_cities',
    '/beers', 'get_beers',
    '/places', 'get_places',
    '/search', 'search_places_beers',
    '/add', 'add_place_beer',
    '/add_feedback', 'insert_feedback'
)

class index:

	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self, name=None):
		return self.render.index()

class get_cities:

	def GET(self):
		db = pickledb.load("DB/romania.db", False)
		all_keys = db.dgetall("cities_list").keys()
		web.header('Content-Type', 'application/json')
		return json.dumps(all_keys)

class get_beers:

	def GET(self):
		db = pickledb.load("DB/romania.db", False)
		all_keys = db.dgetall("beers_list").keys()
		web.header('Content-Type', 'application/json')
		return json.dumps(all_keys)

class get_places:

	def GET(self):
		db = pickledb.load("DB/romania.db", False)
		get_input = web.input(_method='get')
		
		try:
			all_keys = db.dgetall(get_input.data + "_places").keys()
		except:
			all_keys = "Not Found !"
		web.header('Content-Type', 'application/json')
		return json.dumps(all_keys)

class search_places_beers:
	
	def GET(self):
		db = pickledb.load("DB/romania.db", False)
		#get value from POST
		get_input = web.input(_method='get')
		#POST data comes as "city_place_beer" -> split in array after "_"
		search_data = get_input.data.split("_")
		city_name = search_data[0]
		place_name = search_data[1]
		beer_name = search_data[2]
		
		criteria = place_name+"-"+beer_name

		all_keys = db.dgetall(city_name+"_places_beers").keys()
		print all_keys

		if criteria in all_keys:
			#increment searches for city
			city_key = db.dget("cities_list", city_name)
			print city_key
			city_key['searches'] += 1
			#increment searches for city_beer
			city_beer_key = db.dget(city_name+"_places_beers", criteria)
			city_beer_key['searches'] += 1
			#increment searches for beer
			beer_key = db.dget("beers_list", beer_name)
			beer_key['searches'] += 1
			#save searches
			db.dump()
			return "Found !"
 		else:
			return "Not Found !"		

class add_place_beer:

	def POST(self):
		db = pickledb.load("DB/romania.db", False)
		#get value from POST
		get_input = web.input(_method='post')

		add_data = get_input.data.split("_")
		city_name = add_data[0]
		place_name = add_data[1]
		beer_name = add_data[2]
		beer_price = add_data[3]

		record = place_name+"-"+beer_name

		#verify if place exists
		try:
			places_keys = db.dgetall(city_name+"_places")
			if place_name in keys:
				print "Exists place !"
			else:
				timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")
				db.dadd(city_name+"_places", (place_name, dict([('searches', 0), ('date_added', timestamp)])))
				db.dump()
		except:
			db.dcreate(city_name+"_places")
			timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")
			db.dadd(city_name+"_places", (place_name, dict([('searches', 0), ('date_added', timestamp)])))
			db.dump()

		#verify if beer exists
		beers_keys = db.dgetall("beers_list")
		if beer_name in beers_keys:
			print "Exists beer !"
		else:
			timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")
			db.dadd("beers_list", (beer_name, dict([('searches', 0), ('date_added', timestamp)])))
			db.dump()

		#try adding the pair place_beer
		try:
			all_keys = db.dgetall(city_name+"_places_beers")

			if record in all_keys:
				return "Already exists !"
			else:
				timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")
				db.dadd(city_name+"_places_beers", (record, dict([('searches', 0), ('price', beer_price), ('date_added', timestamp)])))
				db.dump()
				return "Added new record to existing list !"
		except:
			db.dcreate(city_name+"_places_beers")
			timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")
			db.dadd(city_name+"_places_beers", (record, dict([('searches', 0), ('price', beer_price), ('date_added', timestamp)])))
			db.dump()
			return "Added new record !"

class insert_feedback:

	def POST(self):
		db = pickledb.load("DB/feedback.db", False)
		timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")
		feedback = web.input(_method='post')
		db.set(timestamp, feedback)
		db.dump()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()