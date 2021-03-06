# coding: utf-8
from textblob import TextBlob
import nltk
from textblob import Word
import sys
import json

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)


def genQuestion(line):
    if type(line) is str:
        line = TextBlob(line)
    bucket = {}
    for i,j in enumerate(line.tags):
        if j[1] not in bucket:
            bucket[j[1]] = i
    question = ' '            # Create an empty string 

    l1 = ['NNP', 'VBG', 'VBZ', 'IN']
    l2 = ['NNP', 'VBG', 'VBZ']


    l3 = ['PRP', 'VBG', 'VBZ', 'IN']
    l4 = ['PRP', 'VBG', 'VBZ']
    l5 = ['PRP', 'VBG', 'VBD']
    l6 = ['NNP', 'VBG', 'VBD']
    l7 = ['NN', 'VBG', 'VBZ']

    l8 = ['NNP', 'VBZ', 'JJ']
    l9 = ['NNP', 'VBZ', 'NN']

    l10 = ['NNP', 'VBZ']
    l11 = ['PRP', 'VBZ']
    l12 = ['NNP', 'NN', 'IN']
    l13 = ['NN', 'VBZ']

    if all(key in  bucket for key in l1): 
        question = 'What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NNP']]+ ' '+ line.words[bucket['VBG']] + '?'
    elif all(key in  bucket for key in l2):
        question = 'What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NNP']] +' '+ line.words[bucket['VBG']] + '?'
    elif all(key in  bucket for key in l3): 
        question = 'What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['PRP']]+ ' '+ line.words[bucket['VBG']] + '?'
    elif all(key in  bucket for key in l4): 
        question = 'What ' + line.words[bucket['PRP']] +' '+  ' does ' + line.words[bucket['VBG']]+ ' '+  line.words[bucket['VBG']] + '?'
    elif all(key in  bucket for key in l7): 
        question = 'What' + ' ' + line.words[bucket['VBZ']] +' '+ line.words[bucket['NN']] +' '+ line.words[bucket['VBG']] + '?'

    elif all(key in bucket for key in l8): 
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NNP']] + '?'

    elif all(key in bucket for key in l9): 
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NNP']] + '?'

    elif all(key in bucket for key in l11): 
        if line.words[bucket['PRP']] in ['she','he']:
            question = 'What' + ' does ' + line.words[bucket['PRP']].lower() + ' ' + line.words[bucket['VBZ']].singularize() + '?'

    elif all(key in bucket for key in l10): 
        question = 'What' + ' does ' + line.words[bucket['NNP']] + ' ' + line.words[bucket['VBZ']].singularize() + '?'

    elif all(key in bucket for key in l13): 
        question = 'What' + ' ' + line.words[bucket['VBZ']] + ' ' + line.words[bucket['NN']] + '?'

    if 'VBZ' in bucket and line.words[bucket['VBZ']] == "’":
        question = question.replace(" ’ ","'s ")

# Print the genetated questions as output.
    if question != '':        
        return json.dumps(question)


class User(Resource):
    def get(self, string):
        txt = TextBlob(string)
        for sentence in txt.sentences:
            info=json.loads(genQuestion(sentence))
            return "hey man"



api.add_resource(User, "/user/<string:string>")
app.run(debug=True)