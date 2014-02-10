import web
import pickledb
import json

urls = (
    '/', 'moderate'
)

class moderate:

	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self, name=None):
		return self.render.moderate()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()