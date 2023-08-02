from resources import jsonify, Resource, TESTING, request, Response, render_template, reqparse
from datamgmt.dataframes import getDfSql
from config import vcdsPgSqlAlchemy
from pbi.datasets import pushToPowerBi
from test import catalogTemp


class Catalogue(Resource):
    """
    """
    path = '/sources'

    def get(self):
        # For Testing
        if TESTING:
            return jsonify({'message': 'Welcome to the DataHub Catalogue!'})
        else:
            return Response(response=render_template("catalog.html"), status=200)
            #return jsonify({'message': 'Welcome to the DataHub Catalogue!'})


class Query(Catalogue):
    """
    """
    path = Catalogue.path + '/info'

    def get(self):
        # For Testing
        if TESTING:
            return jsonify({'message': 'Here is the result of your query.'})
        else:
            return jsonify({'message': 'Here is the result of your query.'})


class DataSourceNew(Catalogue):
    """
    """
    path = Catalogue.path + '/source'

    def get(self):
        # For Testing
        if TESTING:
            return {'message': 'Please add a datasource!'}, 200
        else:
            return Response(response=render_template('newDatasource.html'), status=200)


class PowerBi(Catalogue):
    """
    """
    path = Catalogue.path + '/powerbi'

    def get(self):
        # For Testing
        if TESTING:
            return {'message': 'The query has been processed and pushed to Power BI.'}, 200
        else:
            return Response(response=render_template('powerbi.html'), status=200)


class PowerBiQuery(PowerBi):
    """
    """
    path = PowerBi.path + '/query'

    def post(self):
        # For Testing
        if TESTING:
            return {'message': 'The query has been processed and pushed to Power BI.'}, 200
        else:
            args = request.form.to_dict()
            
            # Return error if at least one key cannot be matched to a datasource.
            if 'keys' in args.keys():
                # Builds dictionary of dataframes.
                args['keys'] = args['keys'].split(',')
                dfs = {}
                for key in args['keys']:
                    for entry in catalogTemp:
                        if key == entry['key']:
                            dfs[key] = getDfSql(key, entry['cred'])

            else:
                return {'message': 'Catalog Keys corresponding to data must be supplied.'}, 400
            
            # Assign default dataset name
            if 'dsname' not in args.keys():
                args['dsname'] = 'DataHub'

            # Assign boolean for relationships
            if 'relationships' not in args.keys():
                args['relationships'] = None
            else:
                field = args['relationships']
                keys = []
                for key, df in dfs.items():
                    if field in df.columns:
                        keys.append(key)

                if len(keys) == 0:
                    args['relationships'] = None
                else:
                    args['relationships'] = {field: keys}
            
            pushToPowerBi(dfs=dfs, datasetName=args['dsname'], relationships=args['relationships'])
            return Response(response=render_template('powerbi_success.html'), status=201)
            try:
                pushToPowerBi(dfs=dfs, datasetName=args['dsname'], relationships=args['relationships'])
            except:
                return {'message': 'Something has gone wrong on our end.'}, 500
            else:
                return Response(response=render_template('powerbi_success.html'), status=201)
