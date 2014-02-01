import web
import pickledb
import json

urls = (
    '/', 'index',
    '/cities', 'get_cities',
    '/beers', 'get_beers',
    '/places', 'get_places',
    '/search', 'search_places_beers',
    '/add', 'add_place_beer'
)

class index:

	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self, name=None):
		return self.render.index()

class get_cities:

	def GET(self):
		db = pickledb.load("DB/romania.db", False)
		all_keys = db.lgetall("cities_list")
		web.header('Content-Type', 'application/json')
		return json.dumps(all_keys)

class get_beers:

	def GET(self):
		db = pickledb.load("DB/romania.db", False)
		all_keys = db.lgetall("beers_list")
		web.header('Content-Type', 'application/json')
		return json.dumps(all_keys)

class get_places:

	def GET(self):
		db = pickledb.load("DB/romania.db", False)
		get_input = web.input(_method='get')
		
		try:
			all_keys = db.lgetall(get_input.data + "_places")
		except:
			all_keys = "Not Found !"
		web.header('Content-Type', 'application/json')
		return json.dumps(all_keys)

class search_places_beers:
	
	def GET(self):
		db = pickledb.load("DB/romania.db", False)
		get_input = web.input(_method='get')

		search_data = get_input.data.split("_")
		
		criteria = search_data[1]+"-"+search_data[2]

		all_keys = db.lgetall(search_data[0]+"_places_beers")

		if criteria in all_keys:
			return "Found !"
		else:
			return "Not Found !"		

class add_place_beer:

	def POST(self):
		db = pickledb.load("DB/romania.db", False)
		get_input = web.input(_method='post')

		add_data = get_input.data.split("_")

		record = add_data[1]+"-"+add_data[2]

		try:
			all_keys = db.lgetall(add_data[0]+"_places_beers")

			if record in all_keys:
				return "Already exists !"
			else:
				db.ladd(add_data[0]+"_places_beers", record)
				db.dump()
				return "Added new record to existing list !"
		except:
			db.lcreate(add_data[0]+"_places_beers")
			db.ladd(add_data[0]+"_places_beers", record)
			db.dump()
			return "Added new record !"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()