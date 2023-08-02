from flask import request, send_from_directory
import werkzeug
import uuid
import json
from datamgmt.filemgmt import deleteFile, stageJsonFile

from resources import jsonify, Resource, TESTING, cacheIncoming, fileExists, Response, reqparse
from test import testPost, testGet


class DataSource(Resource):
    """
    """
    path = '/sources/source/<string:catalogKey>'

    def get(self, catalogKey):
        # For Testing
        if TESTING:
            return jsonify({'message': 'Here is the content of DataSource {}.'.format(catalogKey)})
        else:
            string = testGet(catalogKey)
            try:
                string = testGet(catalogKey)
            except:
                return {'message': 'Something has gone wrong on our end.'}, 500
            else:
                if string is None:
                    return {'message': 'Key is not matched to a datasource.'}, 404
                
                path, file = stageJsonFile(string, catalogKey)
                return send_from_directory(path, file)


class Metadata(DataSource):
    """
    """
    path = DataSource.path + '/metadata'

    def get(self, catalogKey):
        # For Testing
        if TESTING:
            return jsonify({'message': 'Here is the metadata of DataSource {}.'.format(catalogKey)})
        else:
            return jsonify({'message': 'Here is the metadata of DataSource {}.'.format(catalogKey)})


class New(DataSource):
    """
    """
    path = '/sources/source/new'

    def post(self):
        # For Testing
        if TESTING:
            return jsonify({'message': 'DataSource {} Successfully Added.'.format(catalogKey)})
        else:
            parse = reqparse.RequestParser()
            parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='file')
            args = parse.parse_args()
            file = args['file']
            print(args)
            fileName = cacheIncoming + str(uuid.uuid4()) + '.xlsx'
            while fileExists(fileName):
                fileName = cacheIncoming + str(uuid.uuid4()) + '.xlsx'
            
            print(fileName)
            try:
                file.save(fileName)
            except AttributeError:
                return {'message': 'File could not be retrieved. Please try again.'}, 422
            except:
                return {'message': 'Something has gone wrong on our end.'}, 500
            else:
                catalogKey = request.form.to_dict()['key']
                try:
                    testPost(catalogKey, fileName.split('/')[-1])
                except:
                    return {'message': 'Something has gone wrong on our end.'}, 500
                else:
                    return {'message': 'File has been received and is linked with Catalog Key {}!'.format(catalogKey)}, 201


class Update(DataSource):
    """
    """
    path = DataSource.path + '/update/<string:filePath>'

    def put(self, catalogKey, filePath):
        # For Testing
        if TESTING:
            return jsonify({'message': 'DataSource {} Successfully Updated from file path {}.'.format(catalogKey, filePath)})
        else:
            return jsonify({'message': 'DataSource {} Successfully Updated from file path {}.'.format(catalogKey, filePath)})


class Remove(DataSource):
    """
    """
    path = DataSource.path + '/remove'

    def delete(self, catalogKey):
        # For Testing
        if TESTING:
            return jsonify({'message': 'DataSource {} Successfully Removed.'.format(catalogKey)})
        else:
            return jsonify({'message': 'DataSource {} Successfully Removed.'.format(catalogKey)})


class ChangePermissions(DataSource):
    """
    """
    path = DataSource.path + '/perms/<string:query>'

    def put(self, catalogKey, query):
        # For Testing
        if TESTING:
            return jsonify({'message': 'Permissions Have Been Modified for DataSource {} based on {}.'.format(catalogKey, query)})
        else:
            return jsonify({'message': 'Permissions Have Been Modified for DataSource {} based on {}.'.format(catalogKey, query)})


