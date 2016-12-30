from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from os import curdir, sep
import cgi
import utils.ui_utils as ui_utils
import html_functions
import cgi

hostName = "localhost"
hostPort = 8080

class MyServer(BaseHTTPRequestHandler):


	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		str_request = html_functions.return_states()
		self.wfile.write(bytes(str_request,"utf8"))

		return

	def do_POST(self):
		
		form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })

		if self.path=="/cities":
			str_response = html_functions.return_cities(form["state"].value)

		if self.path=="/shapes":
			str_response = html_functions.return_shapes(form["city"].value)

		if self.path=="/airports":
			str_response = html_functions.return_airports(form["shape"].value)
		if self.path=="/date":
			str_response = html_functions.return_date(form["airport"].value)
		if self.path=="/result":
			str_response = html_functions.return_results(form["datepicker"].value)

		self.send_response(200)
		self.end_headers()
		self.wfile.write(bytes(str_response,"utf8"))

		return			
		

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
