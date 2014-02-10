import pickledb

class db_operation:
	def __init__(self, database_file):
		self.db = pickledb.load(database_file, False)

	def get_all_keys_from_dict(self, dict_name):
		all_keys = self.db.dgetall(dict_name).keys()
		return all_keys

	def add_to_dict(self, dict_name, pair):
		self.db.dadd(dict_name, pair)

	def create_dict(self, dict_name):
		self.db.dcreate(dict_name)

	def insert_key_value(self, key, value):
		self.db.set(key, value)

	def get_key_value(self, key, value):
		return self.db.dget(key, value)

	def increment_search(self, dict, key, item):
		city_key = self.db.dget(dict, key)
		city_key[item] += 1

	def save(self):
		self.db.dump()