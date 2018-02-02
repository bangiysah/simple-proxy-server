#Simple Multi-threaded proxy server with caching

This project was implemented in python.

1. In this project a client has to insert URL and the script parses that URL according to HTTP protocol.
2. It searches for the requested page in cache.If it is found it responses with the requested page.
3. Otherwise it tries to fetch the requested page from the server and sends responses
   to client and save one copy for its future referneces.
4. For caching we made use of dictionary in python.

#Testing:-

1. you can test the proxy server function using telent protocol

 EX:-
    telnet cis.poly.edu 80

	GET /~ross/ HTTP/1.1
	Host: cis.poly.edu

	This opens a TCP connection to port 80 of the host cis.poly.edu and then sends the 
	HTTP request message.You can see the raw base HTML files in the command prompt.

2. You can enter the url in the browser in the below format.

   http:// < ip-address >:< port_no >/ < URL >

 EX:-
    http://localhost:8888/www.google.com
 
 Note :- 
   1. This works only for HTTP protocol(not for HTTPS).
   2. The topic of proxy server was much elaborated in Kurose-Ross Computer-Networking textbook.
