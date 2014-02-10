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
		db = db_operation(config.permanent_db)
		web.header('Content-Type', 'application/json')
		return json.dumps(db.get_all_keys_from_dict(config.cities_list))

class get_beers:

	def GET(self):
		db = db_operation(config.permanent_db)
		web.header('Content-Type', 'application/json')
		return json.dumps(db.get_all_keys_from_dict(config.beers_list))


class get_places:

	def GET(self):
		db = db_operation(config.permanent_db)
		get_input = web.input(_method='get')

		try:
			web.header('Content-Type', 'application/json')
			return json.dumps(db.get_all_keys_from_dict(get_input.data+config.places_suffix))
		except:
			return "Not Found !"


class search_places_beers:
	
	def GET(self):
		db = db_operation(config.permanent_db)

		get_input = web.input(_method='get')

		city_name, place_name, beer_name = get_input.data.split("_")

		all_dict_keys = db.get_all_keys_from_dict(city_name+config.places_beers_suffix)

		if place_name+"-"+beer_name in all_dict_keys:
			#increment city searches
			db.increment_search("cities_list", city_name, "searches")
			#increment city_beer searches
			db.increment_search(city_name+config.places_beers_suffix, place_name+"-"+beer_name, "searches")
			#increment beer searches
			db.increment_search(config.beers_list, beer_name, "searches")
			#increment places
			db.increment_search(city_name+config.places_suffix, place_name, "searches")
			#save DB
			db.save()
			return "Found !"
		else:
			return "Not Found !"


class add_place_beer:

	def POST(self):
		db = db_operation(config.permanent_db)
		#get value from POST
		get_input = web.input(_method='post')
		city_name, place_name, beer_name, beer_price = get_input.data.split("_")

		timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")
		record = place_name+"-"+beer_name

		#verify if place exists
		try:
			places = db.get_all_keys_from_dict(city_name+config.places_suffix)
			if place_name in places:
				print "Place exists"
			else:
				db.add_to_dict(city_name+config.places_suffix, (place_name, config.new_record_place))
				db.save()
		except:
			db.create_dict(city_name+config.places_suffix)
			db.add_to_dict(city_name+config.places_suffix, (place_name, config.new_record_place))
			db.save()

		#verify if beer exists
		beers = db.get_all_keys_from_dict(config.beers_list)
		if beer_name in beers:
			print "Beer exists"
		else:
			db.add_to_dict(config.beers_list, (beer_name, config.new_record_beer))
			db.save()

		#verify if the pair place_beer exists
		try:
			places_beers = db.get_all_keys_from_dict(city_name+config.places_beers_suffix)
			if record in places_beers:
				return config.existing_record_message
			else:
				db.add_to_dict(city_name+config.places_beers_suffix, (record, dict([('searches', 0), ('price', beer_price), ('date_added', timestamp)])))
				db.save()
				return config.added_new_record_message
		except:
			db.create_dict(city_name+config.places_beers_suffix)
			db.add_to_dict(city_name+config.places_beers_suffix, (record, dict([('searches', 0), ('price', beer_price), ('date_added', timestamp)])))
			db.save()
			return config.added_new_record_message

class insert_feedback:

	def POST(self):
		db = db_operation(config.feedback_db)
		timestamp = time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M:%S")
		feedback = web.input(_method='post')
		db.insert_key_value(timestamp, feedback)
		db.save()		


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()