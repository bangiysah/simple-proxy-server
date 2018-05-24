#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
import socket
import itertools
import signal
import argparse
from time import sleep
from socket import socket as Socket
from threading import *
from HTTP_request_handler import *

BUFFER_SIZE = 4096
REMOTE_PORT = 80


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('--port', '-p', default=8888, type=int, help='Port to use')
	args = parser.parse_args()
	global Threads

	try:
		server_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		server_socket.bind(('', args.port))
		server_socket.listen(100)

		cache_dict = {}
		print "Proxy server is running.....\n"

		while True:			
			try:
				connection_socket , connection_addr = server_socket.accept()

				t = Thread(target = http_request_parse, args = (cache_dict , connection_socket ,))
				print "Connected client :" , connection_addr
				t.setDaemon(1)
				t.start()
				t.join()
				signal.signal(signal.SIGINT,exit_handler)
				signal.pause()
			except socket.error as e:
				print e
			finally:
				connection_socket.close()

	except KeyboardInterrupt as msg:
		print msg
		sys.exit()
	finally:
		server_socket.close()
    

def http_request_parse(cache_dict , connection_socket):

	request_string = connection_socket.recv(BUFFER_SIZE).decode('utf-8','ignore')
	request = HTTPRequest(request_string)

	method = request.command
	uri = request.path

	if method == "GET":
		pass
	else:
		print "It is not GET method"
		sys.exit()
	    
	try:
		useless, full_url, path = uri.split('/',2)
	except ValueError:
		useless = None
		l,full_url = uri.split('/',1)
		path = ''

	search_key = request.path

	if search_key in cache_dict:
		cached_page = cache_dict.get(search_key)
		print "Got page from", search_key ,"cache\n\n"
		
	else:
		cached_page = http_response(full_url , path)
		print(cached_page)
		cache_dict[search_key] = cached_page
		print "Serving page from", search_key ,"and cached it\n\n"
		
	connection_socket.send(cached_page.encode('utf-8'))



def http_response(full_url , path):

	global reply

	try:
		remote_ip = socket.gethostbyname( full_url )
		print(remote_ip)		
	except socket.gaierror:
		print "Hostname could not be resolved. Exiting"
		sys.exit()

	client_socket = Socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((remote_ip, REMOTE_PORT))

	if path is None:
		message = "GET / " +"HTTP/1.0\r\nHost: " +  full_url+"\r\n\r\n"
	else:
		message = "GET /" + path +" HTTP/1.0\r\nHost: " + full_url+"\r\n\r\n"

	try :
		client_socket.sendall((message).encode('utf-8'))
	except socket.gaierror:
		print "Send failed"
		sys.exit()

	reply = client_socket.recv(4096).decode('utf-8','ignore')
	client_socket.close()

	return reply

def exit_handler(signal , frame):
	print "Main thread exitted successfully"
	sys.exit()


if __name__ == '__main__':
	main()
	sys.exit()   
