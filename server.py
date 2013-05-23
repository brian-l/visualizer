import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import time, sys, os, json, psi, psi.process, pwd

from tornado import autoreload
from dispatcher import MethodDispatcher
from orm import Process, ProcessManager 
from threading import Thread, Timer

class ViewHandler(MethodDispatcher):
	def initialize(self):
		pass

	def _json_response(func):
		def wrap(self, *args, **kwargs):
			self.set_header('Content-Type', 'application/json')
			self.set_header('Access-Control-Allow-Origin', '*')
			func(self, *args, **kwargs)	
		return wrap

	@_json_response
	def processes(self, *args, **kwargs):
		users = []
		nodes = {}
		edges = {}
		for process in psi.process.ProcessTable().values():
			user = pwd.getpwuid(process.ruid).pw_name
			if user not in users:
				users.append(user)
			if not nodes.get(process.pid):
				nodes[process.pid] = dict()
			nodes[process.pid] = {'shape': 'dot', 'label': process.name, 'color': 'red'}
			edges[process.pid] = {user: {}}

		for user in users:
			nodes[user] = {'shape': 'dot', 'label': user, 'color': 'blue'}

		self.write(json.dumps({'nodes': nodes, 'edges': edges}))

	def index(self):
		self.render('html/graph.html')

worker = tornado.web.Application([
	(r'/static/js/(.*)', tornado.web.StaticFileHandler, {'path': './static/js'},),
	(r'/static/css/(.*)', tornado.web.StaticFileHandler, {'path': './static/css'},),
	(r'/.*', ViewHandler,),
])

if __name__ == '__main__':
	server = tornado.httpserver.HTTPServer(worker)
	running = True

	with open('/tmp/visualizer.pid', 'w') as pidfile:
		pidfile.write(str(os.getpid()))

	def getProcesses():
		manager = ProcessManager()
		while running:
			time.sleep(2)
			for process in psi.process.ProcessTable().values():
				manager.createProcess(Process(process.pid, process.name))

	try:
		port = 8080
		print "Listening on localhost:%d" % (port)
		server.listen(port)
		ioloop = tornado.ioloop.IOLoop.instance()
		autoreload.start(ioloop)
		ioloop.start()
	except KeyboardInterrupt:
		print '\nSIGTERM received.'
		running = False
		print 'Stopping server...'
		server.stop()
		print 'Stopping io loop...'
		tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 2, tornado.ioloop.IOLoop.instance().stop)
		sys.exit()

