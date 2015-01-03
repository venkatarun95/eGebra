import threading
import random
import json

import cas_manager.cas_manager_interface
import cas_manager.error_reporter

#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 8000+random.randrange(0, 100)

#This class will handles any incoming request from
#the browser 
class serverHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_OPTIONS(self):           
        self.send_response(200, "ok")       
        #self.send_header('Access-Control-Allow-Origin', '*')                
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')#, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With") 

    def do_GET(self):
        #print("got GET request: "+ self.path)

        if ".." in self.path:
            self.wfile.write("Please restrict to accessing relevant files. Do not use \'..\' anywhere.")
            return

        if self.path.endswith(".html") or self.path.endswith(".js"):
            #read file
            try:
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                requestedFile = open(self.path[1:], 'r')
                self.wfile.write(requestedFile.read())
            except IOError:
                self.send_error(404, "File not found: \'"+self.path+"\'")
        elif self.path.endswith(".css"): #css files will need to send a different header indicating it is css
            #read file
            try:
                self.send_response(200)
                self.send_header('Content-type','text/css')
                self.end_headers()
                requestedFile = open(self.path[1:], 'r')
                self.wfile.write(requestedFile.read())
            except IOError:
                self.send_error(404, "File not found: \'"+self.path+"\'")
        elif self.path[1:] == "listen":
            print "Sending GET Hello World"
            self.wfile.write("Hello World")
        else:
            self.wfile.write("Cannot understand GET request: \'"+self.path+"\'")

    def do_POST(self):
        query_url = self.path
        query_string = self.rfile.read(int(self.headers['Content-Length'])).encode('ascii', 'ignore')
        #print("do_POST: "+query_string + str(self.headers['Content-Length']))

        if query_url == "/listen":
            self.send_response(200)
            self.send_header('Content-type', 'json')
            self.end_headers()

            #see if there is a result available
            res = cas_manager.cas_manager_interface.popResult()
            if res == None:
                self.wfile.write("{\"message\": \"Nothing Yet\"}") #nothing yet
            else:
                #see if result evaluation was successful
                if res[1] == []:
                    self.wfile.write("{\"message\": \"Function could not be computed\"}")
                else:
                    resStr = json.dumps((res[0][1:], res[1].getRepresentativeObject()))
                    #print resStr
                    self.wfile.write(resStr)


        elif query_url == "/createSymbolObject":
            self.send_response(200)
            self.send_header('Content-type', 'json')
            self.end_headers()
            try:
                query_data = json.loads(query_string)
                symbolStr, stringLang = query_data["symbolStr"].encode('ascii', 'ignore'), query_data["stringLang"].encode('ascii', 'ignore')
            except:
                self.wfile.write("{\"message\": \"Error: Incorrect format of JSON object.\"}")
                return
            try:
                res=cas_manager.cas_manager_interface.createSymbolicObject(symbolStr, stringLang)
            except:
                self.wfile.write("{\"message\": \"Error while creating symbol.\"}")
                cas_manager.error_reporter.reportRuntimeWarning("server.py:server:do_POST :- Error while creating symbol")
                return #should never be reached because of error_reporter

            self.wfile.write("{\"message\": \"Symbol creation successful.\", \"symObj\":"+json.dumps(res.getRepresentativeObject())+"}")


        elif query_url == "/requestComputation":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            try:
                query_data = json.loads(query_string)
                keyStr, symObjKeys = query_data["keyStr"].encode('ascii', 'ignore'), query_data["symObjKeys"]
            except:
                self.wfile.write("Error: Incorrect format of JSON object.")
                return
            try:
                cas_manager.cas_manager_interface.pushComputation(keyStr, symObjKeys, 100) #priority 100 as it is from the user (super high priority)
            except:
                self.wfile.write("Error: Error while pushing computation. Please report this.")
                return
            self.wfile.write("Computation push successful.")


        elif query_url == "/requestListOfPossibleComputations":
            self.send_response(200)
            self.send_header('Content-type', 'json')
            self.end_headers()
            try:
                res = cas_manager.cas_manager_interface.getPossibleComputations()
            except:
                self.wfile.write("Error: Error while fetching data. Please report this.")
                return
            self.wfile.write(json.dumps(res))

        else:
            self.send_error(404, "POST request not understood: \'"+self.path+"\'")


'''The interface class for the server'''
class server(threading.Thread): 
    def run(self):
        try:
            #Create a web server and define the handler to manage the
            #incoming request
            self.server = HTTPServer(('', PORT_NUMBER), serverHandler)
            print 'Started httpserver on port ' , PORT_NUMBER
            #Wait forever for incoming http requests
            self.server.serve_forever()

        except KeyboardInterrupt:
            print '^C received, shutting down the web server'
            self.server.socket.close()

    def __del__(self):
        self.server.socket.close()