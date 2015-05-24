#!/usr/bin/env python

import os
import sys
import json
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

@app.route("/", methods=['GET', 'POST'])
def index():
    global source_root, temp_root
    # if request.method == 'GET':
    #     return json.dumps({'ok':''})

    if request.method == 'POST' or request.method == 'GET':
        print("we got something!")
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
        if 'resource' not in payload:
            return json.dump({'error':'missing the "resource" parameter'})

        # read fields
        if 'format' in payload:
            format = payload['format']
        else:
            format = "epub"
        books = payload['books']
        lang = payload['lang']
        resource = payload['resource']
        chapters = []
        if 'chapters' in payload and isinstance(books, list) and len(books) is 1:
            chapters = payload['chapters']
            if 'start' not in chapters or 'end' not in chapters:
                chapters = []

        filename = "translation." + format
        output_path = temp_root + "/" + filename
        command = "/usr/local/bin/pandoc -f html -t " + format + " -o " + output_path
        input_path = source_root + "/" + lang + "/" + resource + "/"

        # TODO: select the proper source
        if not isinstance(books, list):
            # TODO: add all the books to the command
            pass
        else:
            for b in books:
                print("loading book: " + b)
                if len(chapters) == 2:
                    for i in range(chapters["start"], chapters["end"]):
                        print("loading chapter: " + str(i))
                        # add selected chapters
                        command += " " + input_path + b + "/" + str(i) + ".html"
                else:
                    # add all the chapters
                    command += " " + input_path + b + "/*"

        # docx
        # pandoc -f html -t docx -o translation.docx /Users/joel/git/Door43/book_renderer/source/test/*
        # latex
        # pandoc -f html -t latex -o translation.txt /Users/joel/git/Door43/book_renderer/source/test/*
        #command = "/usr/local/bin/pandoc -f html -t epub -o " + output + " " + path

        # debug the command
        print(command)
        os.system(command)
        if(os.path.isfile(output_path)):
            try:
                with open(output_path, 'r') as content_file:
                    response = Response(content_file.read(),  content_type='application/octet-stream')
                    response.content_disposition = 'attachment; filename="export.epub"'
                    response.headers['Content-Disposition'] = 'attachment; filename="export.epub"'
                    return response
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