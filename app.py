import web
import pickledb
import json
import time
import config
from database_operations import db_operations

urls = (
    '/', 'index',
    '/cities', 'get_cities',
    '/beers', 'get_beers',
    '/places', 'get_places',
    '/search', 'search_places_beers',
    '/add', 'save_entry',
    '/add_feedback', 'insert_feedback'
)

class index:

	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self, name=None):
		return self.render.index()

class get_cities:
	def GET(self):
		db = db_operations(config.permanent_db)
		web.header('Content-Type', 'application/json')
		return json.dumps(db.get_all_keys_from_root_dict(config.cities_list))

class get_beers:
	def GET(self):
		db = db_operations(config.permanent_db)
		web.header('Content-Type', 'application/json')
		return json.dumps(db.get_all_keys_from_root_dict(config.beers_list))


class get_places:
	def GET(self):
		db = db_operations(config.permanent_db)
		get_input = web.input(_method='get')

		try:
			web.header('Content-Type', 'application/json')
			return json.dumps(db.get_all_keys_from_root_dict(get_input.data+config.places_suffix))
		except:
			return "Not Found !"


class search_places_beers:
	def GET(self):
		db = db_operations(config.permanent_db)

		get_input = web.input(_method='get')

		city_name, place_name, beer_name = get_input.data.split("_")

		all_dict_keys = db.get_all_keys_from_root_dict(city_name+config.places_beers_suffix)

		if place_name + "-" + beer_name in all_dict_keys:
			#increment city searches
			db.increment_searches(config.cities_list, city_name)
			#increment beer searches
			db.increment_searches(config.beers_list, beer_name)
			#increment places
			db.increment_searches(city_name+config.places_suffix, place_name)
			#return response
			response = db.get_all_dicts_from_root_dict(city_name+config.places_beers_suffix)[place_name+"-"+beer_name]
			#print response
			
		try:
			web.header('Content-Type', 'application/json')
			return json.dumps(response)		
		except:
			return "Not Found !"


class save_entry:
	def POST(self):
		get_record = web.input(_method='post')

		db = db_operations(config.temporary_db)

		record_array = get_record.data.split(";")
		#print len(record_array)
		db.save_city_name_place_beer(record_array)

		return "done"

class insert_feedback:
	def POST(self):
		db = db_operations(config.feedback_db)
		feedback = web.input(_method='post')
		db.save_feedback(feedback)		


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()