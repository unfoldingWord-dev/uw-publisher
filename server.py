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
from flask import Flask, request, abort
from subprocess import *

app = Flask(__name__)
# source_root = ""
# port = ""
#
# # reads in the config file
# def loadConfig(config_path):
#     global source_root, port
#
#     if not os.path.isfile(config_path):
#         print("the configuration file is missing")
#         exit()
#
#     # load settings from the config file
#     json_data = open(config_path)
#     try:
#         data = json.load(json_data)
#     except ValueError:
#         print("the configuration file could not be parsed")
#         exit()
#     json_data.close()
#
#     # validate configuration
#     if 'port' not in data or 'source_root' not in data:
#         print("missing some configuration details")
#         exit()
#
#     source_root = str(data['source_root'])
#     port = str(data['port'])
#
#     # validate configuration values
#     if source_root == "" or port == "":
#         print("invalid configuration values")
#         exit()
#
#     # make sure directories exist
#     if not os.path.isdir(source_root):
#         print('--------------------------------------------------------------')
#         print('Configuration warning:')
#         print('could not locate the source path please make sure it exists')
#         print('path: '+source_root)
#         print('--------------------------------------------------------------\n')

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

    if request.method == 'GET':
        return json.dumps({'ok':''})

    elif request.method == 'POST':
        # load payload
        try:
            payload = request.json['data']
        except Exception as e:
            return json.dumps({'error': e.message,
                               'request': request.json})

        # read fields
        if 'slug' not in payload:
            return json.dumps({'error':'missing the "slug"'})
        slug = payload['slug']

        if 'sig' not in payload:
            return json.dumps({'error':'missing the "sig"'})
        sig = payload['sig']

        if 'content' not in payload:
            return json.dumps({'error':'missing the "content"'})
        content = payload['content']


        return json.dumps({'ok':'We are done'})

if __name__ == "__main__":
    try:
        port_number = int(sys.argv[1])
    except:
        port_number = 80
    # global port
    # loadConfig('{0}/config.json'.format(sys.argv[0].rsplit('/', 1)[0]))
    is_dev = os.environ.get('ENV', None) == 'dev'
    # if os.environ.get('USE_PROXYFIX', None) == 'true':
    #     from werkzeug.contrib.fixers import ProxyFix
    #     app.wsgi_app = ProxyFix(app.wsgi_app)

    # show OpenSSL version
    command_str = 'openssl version'
    command = shlex.split(command_str)
    com = Popen(command, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = com.communicate()
    print out

    print('--------------------------')
    print('Publishing Server')
    print('Listening on port: '+ str(port_number))
    print('--------------------------\n')

    app.run(host='0.0.0.0', port=port_number, debug=is_dev)