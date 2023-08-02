from flask import jsonify, Response, render_template
from flask_restful import Resource, reqparse, request

from config import cache
from datamgmt.filemgmt import fileExists

# TESTING = True
TESTING = False

cacheIncoming = '/'.join([cache, 'incoming', ''])


if __name__ == '__main__':
    print(cacheIncoming)