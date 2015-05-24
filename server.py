#!/usr/bin/env python

import sys
import json
import os.path
import logging
from subprocess import call
from twisted.internet import protocol, reactor, endpoints

# global variables
api_version = "1.0.0"
source_root = ""
port = ""

# reads in the config file
def loadConfig(config_path):
    global source_root, port

    if not os.path.isfile(config_path):
        print("the configuration file is missing")
        exit()

    # load settings from the config file
    json_data = open(config_path)
    try:
        data = json.load(json_data)
    except ValueError:
        print("the configuration file could not be parsed")
        exit()
    json_data.close()

    # validate configuration
    if 'port' not in data or 'source_root' not in data:
        print("missing some configuration details")
        exit()

    source_root = str(data['source_root'])
    port = str(data['port'])

    # validate configuration values
    if source_root == "" or port == "":
        print("invalid configuration values")
        exit()

    # make sure directories exist
    if not os.path.isdir(source_root):
        print('--------------------------------------------------------------')
        print('Configuration warning:')
        print('could not locate the source path please make sure it exists')
        print('path: '+source_root)
        print('--------------------------------------------------------------\n')

class ResponseHandler(protocol.Protocol):
    global source_root, api_version

    # sends an error message to the client
    def sendError(self, message):
        response = '{"version":"'+api_version+'","error":"'+message+'"}'
        self.transport.write(response)

    # sends a ok message to the client
    def sendOk(self, message):
        response = '{"version":"'+api_version+'","ok":"'+message+'"}'
        self.transport.write(response)

    # saves the data sent by the client
    def processData(self, data):
        # TODO: only select files chosen by user
        path = source_root + "/test/*"
        # docx
        # pandoc -f html -t docx -o translation.docx /Users/joel/git/Door43/book_renderer/source/test/*
        # latex
        # pandoc -f html -t latex -o translation.txt /Users/joel/git/Door43/book_renderer/source/test/*
        command = "/usr/local/bin/pandoc -f html -t epub -o /Users/joel/git/Door43/book_renderer/translation.epub " + path
        os.system(command)
        # TODO: return file to user
        self.sendOk("done")

    # handle responses
    def dataReceived(self, json_data):
        # expects {'key':'public key', 'udid':'device id', 'username':'an optional username'}
        try:
            data = json.loads(json_data)
        except ValueError:
            print("Unexpected error:", sys.exc_info()[0])
            self.sendError('invalid request')
            return

        # if 'key' not in data or data['key'] == "" or 'udid' not in data or data['udid'] == "":
        #     self.sendError('incomplete request')
        # else:
        self.processData(data)

class ResponseFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ResponseHandler()

loadConfig('{0}/config.json'.format(sys.argv[0].rsplit('/', 1)[0]))

print('--------------------------')
print('Translation Studio Server')
print('Version: '+api_version)
print('Listening on port: '+port)
print('--------------------------\n')

endpoints.serverFromString(reactor, 'tcp:'+port).listen(ResponseFactory())
reactor.run()