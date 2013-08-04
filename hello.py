import cherrypy, os, json as libjson, pidora, template
current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
cherrypy.engine.autoreload.unsubscribe()
class Pidora():

	data = dict(pianobar=None)

	@cherrypy.expose
	def index(self):
		songData = pidora.getSongData()
		return template.index(songData)

	@cherrypy.expose
	def api(self, json=None):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		reply = pidora.api(self.data, json)
		return reply["json"]

	@cherrypy.expose
	def start(self):
		if self.data['pianobar'] is None:
			pidora.api(self.data, '{"method":"Pianobar.Start", "id":1}')
			return "<html><head><title>Pianobar has started</title></head><body><p>Pianobar is starting</p></body></html>"
		else:
			return "<html><head><title>Pianobar is already running</title></head><body><p>Pianobar is already running</p></body></html>"

	@cherrypy.expose
	def quit(self):
		if self.data['pianobar']:
			pidora.api(self.data, '{"method":"Pianobar.Quit", "id":1}')
			return "<html><head><title>Pianobar has quit</title></head><body><p>Pianobar has quit</p></body></html>"
		else:
			return "<html><head><title>Pianobar is not running</title></head><body><p>Pianobar is not running</p></body></html>"

	@cherrypy.expose
	def mobile(self):
		songData = pidora.getSongData()
		return template.mobile(songData)
	m = mobile

cherrypy.quickstart(Pidora(), config=current_dir + "cpy.conf")