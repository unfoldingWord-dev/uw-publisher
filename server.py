#!/usr/bin/env python

import os
import sys
import json
import requests
import time
import urllib2
import urllib
import base64
import shlex
from flask import Flask, request, Response, abort
from subprocess import *

app = Flask(__name__)
source_root = ""
temp_root = ""
port = 88

# reads in the config file
def loadConfig(config_path):
    global source_root, temp_root, port

    if not os.path.isfile(config_path):
        print("the configuration file is missing")
        exit()

    # load settings from the config file
    json_data = open(config_path)
    data = {}
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
    temp_root = str(data['temp_root'])
    port = int(data['port'])

    # validate configuration values
    if source_root == "" or port == "" or temp_root == "":
        print("invalid configuration values")
        exit()

    # make sure directories exist
    if not os.path.isdir(source_root):
        print('--------------------------------------------------------------')
        print('Configuration warning:')
        print('could not locate the source path please make sure it exists')
        print('path: '+source_root)
        print('--------------------------------------------------------------\n')

# class ResponseHandler(protocol.Protocol):
#     global source_root, api_version
#
#     # sends an error message to the client
#     def sendError(self, message):
#         response = '{"version":"'+api_version+'","error":"'+message+'"}'
#         self.transport.write(response)
#
#     # sends a ok message to the client
#     def sendOk(self, message):
#         response = '{"version":"'+api_version+'","ok":"'+message+'"}'
#         self.transport.write(response)

    # saves the data sent by the client
    # def processData(self, data):
    #     # TODO: only select files chosen by user
    #     path = source_root + "/test/*"
    #     # docx
    #     # pandoc -f html -t docx -o translation.docx /Users/joel/git/Door43/book_renderer/source/test/*
    #     # latex
    #     # pandoc -f html -t latex -o translation.txt /Users/joel/git/Door43/book_renderer/source/test/*
    #     command = "/usr/local/bin/pandoc -f html -t epub -o /Users/joel/git/Door43/book_renderer/translation.epub " + path
    #     os.system(command)
    #     # TODO: return file to user
    #     self.sendOk("done")

    # handle responses
    # def dataReceived(self, json_data):
    #     # expects {'key':'public key', 'udid':'device id', 'username':'an optional username'}
    #     try:
    #         data = json.loads(json_data)
    #     except ValueError:
    #         print("Unexpected error:", sys.exc_info()[0])
    #         self.sendError('invalid request')
    #         return
    #
    #     # if 'key' not in data or data['key'] == "" or 'udid' not in data or data['udid'] == "":
    #     #     self.sendError('incomplete request')
    #     # else:
    #     self.processData(data)

# class ResponseFactory(protocol.Factory):
#     def buildProtocol(self, addr):
#         return ResponseHandler()

# loadConfig('{0}/config.json'.format(sys.argv[0].rsplit('/', 1)[0]))

# print('--------------------------')
# print('Translation Studio Server')
# print('Version: '+api_version)
# print('Listening on port: '+port)
# print('--------------------------\n')

# endpoints.serverFromString(reactor, 'tcp:'+port).listen(ResponseFactory())
# reactor.run()

@app.route("/", methods=['GET', 'POST'])
def index():
    global source_root, temp_root
    if request.method == 'GET':
        return json.dumps({'ok':''})

    elif request.method == 'POST':
        # load payload
        try:
            payload = json.loads(request.values['data']) #request.json['data']
        except Exception as e:
            return json.dumps({'error': e.message,
                               'request': request.json})

        if 'books' not in payload:
            return json.dumps({'error':'missing the "books" parameter'})
        if 'lang' not in payload:
            return json.dumps({'error':'missing the "lang" parameter'})

        # read fields
        books = payload['books']
        lang = payload['lang']
        chapters = []
        if 'chapters' in payload and isinstance(payload['books'], list) and len(payload['books']) is 1:
            chapters = payload['chapters']
            if 'start' not in chapters or 'end' not in chapters:
                chapters = []

        # TODO: place this in a config file
        path = source_root + "/test/*"
        filename = "translation.epub"
        output = temp_root + "/" + filename
        # docx
        # pandoc -f html -t docx -o translation.docx /Users/joel/git/Door43/book_renderer/source/test/*
        # latex
        # pandoc -f html -t latex -o translation.txt /Users/joel/git/Door43/book_renderer/source/test/*
        command = "/usr/local/bin/pandoc -f html -t epub -o " + output + " " + path
        os.system(command)
        if(os.path.isfile(output)):
            try:

                with open(output, 'r') as content_file:
                    return Response(content_file.read(),  mimetype='application/octet-stream')
            except Exception as e:
                return json.dumps({'error': e.message})
        else:
            return json.dumps({'ok':'We are done'})

if __name__ == "__main__":
    global port
    loadConfig('{0}/config.json'.format(sys.argv[0].rsplit('/', 1)[0]))

    is_dev = os.environ.get('ENV', None) == 'dev'

    print('--------------------------')
    print('Publishing Server')
    print('Listening on port: '+ str(port))
    print('--------------------------\n')

    app.run(host='0.0.0.0', port=port, debug=is_dev)