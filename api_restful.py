from flask import Flask, request
from flask_restful import Api

from resources.datahub import DataHub
from resources.datasource import DataSource, Metadata, New, Update, Remove, ChangePermissions
from resources.catalogue import Catalogue, DataSourceNew, PowerBi, PowerBiQuery, Query

app = Flask(__name__)
api = Api(app)

# Data Hub Endpoints
api.add_resource(DataHub, DataHub.path)

# Data Source Endpoints
api.add_resource(DataSource, DataSource.path)
api.add_resource(New, New.path)
api.add_resource(Update, Update.path)
api.add_resource(Remove, Remove.path)
api.add_resource(Metadata, Metadata.path)
api.add_resource(ChangePermissions, ChangePermissions.path)

# Catalogue Endponts
api.add_resource(Catalogue, Catalogue.path)
api.add_resource(PowerBi, PowerBi.path)
api.add_resource(PowerBiQuery, PowerBiQuery.path)
api.add_resource(DataSourceNew, DataSourceNew.path)
api.add_resource(Query, Query.path)

if __name__ == '__main__':
    app.run(debug=True)