import web
import pickledb
import json
import time
import config
from database_interaction import db_operation

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
		records = db_operation(config.permanent_db)
		web.header('Content-Type', 'application/json')
		return json.dumps(records.get_all_keys_from_dict(config.cities_list))

class get_beers:

	def GET(self):
		records = db_operation(config.permanent_db)
		web.header('Content-Type', 'application/json')
		return json.dumps(records.get_all_keys_from_dict(config.beers_list))


class get_places:

	def GET(self):
		records = db_operation(config.permanent_db)
		get_input = web.input(_method='get')

		try:
			web.header('Content-Type', 'application/json')
			return json.dumps(records.get_all_keys_from_dict(get_input.data+config.places_suffix))
		except:
			return "Not Found !"


class search_places_beers:
	
	def GET(self):
		records = db_operation(config.permanent_db)

		get_input = web.input(_method='get')

		city_name, place_name, beer_name = get_input.data.split("_")

		all_dict_keys = records.get_all_keys_from_dict(city_name+config.places_beers_suffix)

		if place_name+"-"+beer_name in all_dict_keys:
			#increment city searches
			records.increment_search("cities_list", city_name, "searches")
			#increment city_beer searches
			records.increment_search(city_name+config.places_beers_suffix, place_name+"-"+beer_name, "searches")
			#increment beer searches
			records.increment_search(config.beers_list, beer_name, "searches")
			#increment places
			records.increment_search(city_name+config.places_suffix, place_name, "searches")
			#save DB
			records.save()
			return "Found !"
		else:
			return "Not Found !"


class add_place_beer:

	def POST(self):
		records = db_operation(config.permanent_db)
		#get value from POST
		get_input = web.input(_method='post')
		city_name, place_name, beer_name, beer_price = get_input.data.split("_")

		timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")
		record = place_name+"-"+beer_name

		#verify if place exists
		try:
			places = records.get_all_keys_from_dict(city_name+config.places_suffix)
			if place_name in places:
				print "Place exists"
			else:
				records.add_to_dict(city_name+config.places_suffix, (place_name, dict([('searches', 0), ('date_added', timestamp)])))
				records.save()
		except:
			records.create_dict(city_name+config.places_suffix)
			records.add_to_dict(city_name+config.places_suffix, (place_name, dict([('searches', 0), ('date_added', timestamp)])))
			records.save()
		#verify if beer exists

		beers = records.get_all_keys_from_dict(config.beers_list)
		if beer_name in beers:
			print "Beer exists"
		else:
			records.add_to_dict(config.beers_list, (beer_name, dict([('searches', 0), ('date_added', timestamp)])))
			records.save()

		#verify if the pair place_beer exists
		try:
			places_beers = records.get_all_keys_from_dict(city_name+config.places_beers_suffix)
			if record in places_beers:
				return "Already exists !"
			else:
				records.add_to_dict(city_name+config.places_beers_suffix, (record, dict([('searches', 0), ('price', beer_price), ('date_added', timestamp)])))
				records.save()
				return "Added new record to existing list !"
		except:
			records.create_dict(city_name+config.places_beers_suffix)
			records.add_to_dict(city_name+config.places_beers_suffix, (record, dict([('searches', 0), ('price', beer_price), ('date_added', timestamp)])))
			records.save()
			return "Added new record !"

class insert_feedback:

	def POST(self):
		record = db_operation(config.feedback_db)
		timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")
		feedback = web.input(_method='post')
		record.insert_key_value(timestamp, feedback)
		record.save()		


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()