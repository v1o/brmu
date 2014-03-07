import pickledb
import config

class db_operations:
	def __init__(self, database_file):
		self.db = pickledb.load(database_file, False)

	def get_all_dicts_from_root(self):
		return self.db.dgetall("root")

	def get_all_keys_from_root_dict(self, dictionary):
		return self.db.dget("root", dictionary).keys()

	def get_all_dicts_from_root_dict(self, dictionary):
		return self.db.dget("root", dictionary)

	def save_feedback(self, feedback):
		timestamp = config.timestamp
		self.db.set(timestamp, feedback)
		self.db.dump()		

	def increment_searches(self, bucket, entity):
		all_keys_from_bucket = self.db.dget("root", bucket)
		all_keys_from_bucket[entity]['searches'] += 1
		self.db.dump()

	def delete_entry(self, sequence_of_values):
		city_place_beer = sequence_of_values[0]
		place_beer = sequence_of_values[1]
		beer_type = sequence_of_values[2]

		all_keys_from_places_beers = self.db.dget("root", city_place_beer)
		#delete beer_type entry
		#print len(all_keys_from_places_beers[place_beer])
		del all_keys_from_places_beers[place_beer][beer_type]
		self.db.dump()
		#if dict is empty, delete it
		if len(all_keys_from_places_beers[place_beer]) == 0:
			del all_keys_from_places_beers[place_beer]
			self.db.dump()		

		return "done"

	def save_city(self, city_name):
		all_keys_from_root = self.db.dgetall("root").keys()
		print "all_keys_from_root"
		print all_keys_from_root

		if config.cities_list in all_keys_from_root:
			print "cities_list exists. going deeper"
			all_dicts_from_cities_list = self.db.dget("root", config.cities_list)
			all_keys_from_cities_list = self.db.dget("root", config.cities_list).keys()
			print "all_keys_from_cities_list"
			print all_keys_from_cities_list
			#if beer name exists
			if city_name in all_keys_from_cities_list:
				print "city exists. do nothing"
			else:
				#add beer name
				print "city didn't exist. added."
				all_dicts_from_cities_list.update( dict([[ city_name, dict([('searches', 0)]) ]]) )
				self.db.dump()					
		else:
			#add beers_list + beer name
			self.db.dadd("root", (config.cities_list,  dict([[ city_name, dict([('searches', 0)]) ]])  ))
			self.db.dump()			

	def save_beer(self, beer_name, searches, datetime_added):
		all_keys_from_root = self.db.dgetall("root")
		if "beers_list" in all_keys_from_root:
			print "beer exists. do nothing"
			all_keys_from_beers_list = self.db.dget("root", "beers_list")
			#if beer name exists
			if beer_name in all_keys_from_beers_list:
				print "beer exists. do nothing"
			else:
				#add beer name
				print "beer didn't exist. added."
				all_keys_from_beers_list.update( dict([[beer_name, dict( [('searches', searches), ('datetime_added', datetime_added) ] ) ]]) )
				self.db.dump()					
		else:
			#add beers_list + beer name
			self.db.dadd("root", (config.beers_list,  dict([[beer_name, dict( [('searches', searches), ('datetime_added', datetime_added) ] ) ]])  ))
			self.db.dump()			

	def save_city_name_place(self, city_name, place_name, searches, datetime_added):
		all_keys_from_root = self.db.dgetall("root")
		if city_name+"_places" in all_keys_from_root:
			all_keys_from_city_places = self.db.dget("root", city_name+"_places")
			#if place name exists
			if place_name in all_keys_from_city_places:
				print "place exists. do nothing"
			else:
				#add place name
				print "place didn't exist. added."
				all_keys_from_city_places.update( dict([[place_name, dict( [('searches', searches), ('datetime_added', datetime_added) ] ) ]]) )
				self.db.dump()				
		else:
			#add city-name_places + place_name
			self.db.dadd("root", (city_name+"_places",  dict([[place_name, dict( [('searches', searches), ('datetime_added', datetime_added) ] ) ]])  ))
			self.db.dump()

	def save_city_name_place_beer(self, sequence_of_values):
		#print len(sequence_of_values)
		print "sequence_of_values"
		print sequence_of_values
		city_place_beer = sequence_of_values[0]
		place_beer = sequence_of_values[1]
		beer_type = sequence_of_values[2]
		beer_price = sequence_of_values[3]
		datetime_added = sequence_of_values[4]

		city_name_place_beer_array = sequence_of_values[0].split("_")
		place_beer_array = sequence_of_values[1].split("-")
		city_name = city_name_place_beer_array[0]
		place_name = place_beer_array[0]
		beer_name = place_beer_array[1]

		#try to get all keys from root
		try:
			all_keys_from_root = self.db.dgetall("root").keys()
		except:
			#create root dictionary
			self.db.dcreate("root")
			self.db.dump()	

		all_keys_from_root = self.db.dgetall("root").keys()
		print "all_keys_from_root"
		print all_keys_from_root
		#city-name_place_beer section -------------
		#add to existing dictionaries in self.db
		#verify if _places_beers dictionary exists in root
		if city_place_beer in all_keys_from_root:
			
			#if exists, get all keys from it
			all_keys_from_places_beers = self.db.dget("root", city_place_beer)
			print "all_keys_from_places_beers"
			print all_keys_from_places_beers
			#search for specific place-beer key
			if place_beer in all_keys_from_places_beers:
				#get all beer_types		
				print "place_beer exists"
				#if found, return beer types
				beer_types_array = all_keys_from_places_beers[place_beer].keys()
				print "beer_types_array"
				print beer_types_array
				w = False
				if beer_type in beer_types_array:
					print "go deeper to the price"
					if all_keys_from_places_beers[place_beer][beer_type]['price'] == beer_price:
						print "same price. do nothing"
					else:
						all_keys_from_places_beers[place_beer][beer_type]['price'] = beer_price
						self.db.dump()
				else:
					print "adding beer type"
					all_keys_from_places_beers[place_beer].update(dict([[ beer_type, dict( [('price', beer_price), ('datetime_added', datetime_added) ] )  ]]))
					self.db.dump()
			#add place_beer_key+beer_type
			else:
				print "added place_beer_key+beer_type"
				self.db.dadd("root", (city_place_beer, dict([[place_beer, dict([[beer_type, dict([('price', beer_price),('datetime_added', datetime_added)])]]) ]]) ))
				self.db.dump()


		else:
			print "fuck you !!"
			self.db.dadd("root", (city_place_beer, dict([[place_beer, dict([[beer_type, dict([('price', beer_price),('datetime_added', datetime_added)]) ]] ) ]]) ))
			self.db.dump()

		#city-name_places section ------------
		self.save_city_name_place(city_name, place_name, 0, datetime_added)

		#beers_list section ---------------
		self.save_beer(beer_name, 0, datetime_added)