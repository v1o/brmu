import web
import pickledb

urls = (
    '/', 'index',
    '/cities', 'get_cities'
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
		return all_keys


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()