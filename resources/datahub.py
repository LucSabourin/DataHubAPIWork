from resources import jsonify, Resource, TESTING

class DataHub(Resource):
    """
    """
    path = '/'

    def get(self):
        # For Testing
        if TESTING:
            return jsonify({'message': 'Connection Successful.'})
        else:
            return jsonify({'message': 'Connection Successful.'})


