from multiprocessing.sharedctypes import Value
import threading
import uuid
import json
import pandas as pd
from pandas import DataFrame

from catalog.config import ctlgPgSqlAlchemy, tagLimit, cache
from catalog.cleanup import cleanUpKey
from datamgmt.dataframes import storeDfSql, getDfSql, jsonifyDf
from datamgmt.filemgmt import deleteFile

class Catalog():
    """Class for a catalog of datasources logged with a data hub/data source management system.

    Atributes:
    ----------
    catalog: dict
        a dictionary referencing all registered datasources and their corresponding keys
    metadata: dict
        a dictionary with each datasource's metadata paired with the datasource's key
    tags: dict
        a dictionary with each datasource's tags
    fields: dict
        a dictionary with each datasource's fields only

    Methods:
    --------
    reserveKey(key: str) -> dict
        reserves a specific key for a dataset, if available, otherwise provided am
        alternative derived by the proposed key
    killKey(key: str)
        removes a key from the catalog, along with the data source information stored
        in the catalog associated with that key
    registerDataSource(msgs: dict, dataSource, key: str, tags: dict = None) -> str
        registers a datasource with the catalog so if can be queried in the future
    serialize()
        serializes the catalog to store when not active
    deserialize()
        sources the serialized catalog to re-instantiate the catalog for querying
    """

    __singleton_lock = threading.Lock()
    __singleton_instance = None
    attributes = ['catalog', 'metadata', 'tags', 'fields']

    def __init__(self):
        self.deserialize()

    # Verfies there is only ever one instance of a the Catalog class active at
    # any given time.
    @classmethod
    def instance(Catalog):
        if Catalog.__singleton_instance is None:
            with Catalog.__singleton_lock:
                if Catalog.__singleton_instance is None:
                    Catalog.__singleton_instance = Catalog()
        return Catalog.__singleton_instance

    def reserveKey(self, key: str) -> dict:
        """
        """

        cleanKey = cleanUpKey(key)
        catalogKey = cleanKey
        
        while True:
            if catalogKey not in [entry['key'] for entry in self.catalog]:
                self.catalog.append({'key': catalogKey, 'source_key': key})
                break
            else:
                catalogKey = cleanKey + '~' + str(uuid.uuid4())[0:4]
        
        response = {'key': catalogKey}
        if catalogKey != key:
            response['message'] = '\'{}\' was unavailable; \'{}\' was assigned instead.'.format(key, catalogKey)
        
        return response

    def killKey(self, key: str) -> None:
        """
        """
        
        killEntry = None
        for entry in self.catalog:
            if key == entry['key']:
                killEntry = entry
                break
        
        if killEntry is not None:
            self.catalog.remove(entry)

    def registerDataSource(self, msgs : dict, dataSource, key: str, tags: dict = None) -> str:
        """
        """
        
        entry = [entry for entry in self.catalog if entry['source_key'] == key]
        if len(entry) == 0:
            catalogKey = self._reserveDataSourceKey(key=key, msgs=msgs)

        else:
            entry = entry[0]
            if len([value for value in entry.values() if value is not None]) > 1:
                catalogKey = self._reserveDataSourceKey(key=key, msgs=msgs)

            else:
                catalogKey = key

        if tags is not None:
            self._addTags(key=catalogKey, tags=tags, msgs=msgs)

        serialized = json.loads(json.dumps(dataSource.serialize()))
        for num, entry in enumerate(self.catalog):
            if entry['source_key'] == catalogKey:
                break
        
        for field, value in serialized.items():
            if field == 'metadata':
                self._extractMetadata(catalogKey, value)
            else:
                if field not in self._catalogFields:
                    self._catalogFields.append(field)
                self.catalog[num][field] = value
        self.serialize()
        return catalogKey

    def serialize(self):
        """
        """

        for attribute in self.attributes:
            if attribute in ['catalog', 'metadata']:
                self._normalize(attribute)

            df = pd.read_json(json.dumps(self.__dict__[attribute]))
            jsonifyDf(df, attribute)
            storeDfSql(df, attribute, ctlgPgSqlAlchemy)
            deleteFile('{}/{}.json'.format(cache, attribute))

    def deserialize(self):
        """
        """
        
        for attribute in self.attributes:
            try:
                df = getDfSql(attribute, ctlgPgSqlAlchemy)
            except ValueError:
                if attribute in ['catalog', 'metadata']:
                    self.__dict__['_' + attribute + 'Fields'] = []
                self.__dict__[attribute] = []
            else:
                if attribute in ['catalog', 'metadata']:
                    self.__dict__['_' + attribute + 'Fields'] = df.columns[:]
                self.__dict__[attribute] = jsonifyDf(df)

    def _reserveDataSourceKey(self, key : str, msgs : dict) -> str:
        response = self.reserveKey(key)
        try:
            msgs['information'].append(response['message'])
        except KeyError:
            pass
        return response['key']

    def _addTags(self, key : str, tags : dict) -> None:
        for num, tag in enumerate(tags.values()):
            field, value = tag
            self.tags.append({'id': '{}.{}'.format(key, num), 'key': key, 'tag_name': field, 'tag_value': value, 'tag_num': num})

    def _buildTags(self):
        self.tags[-1]
        for num in range(0, tagLimit):
            self.tags['name_{}'.format(num)]
            self.tags['value_{}'.format(num)]

    def _extractMetaData(self, key : str, metadata : dict) -> None:
        self.metadata.append({'key': key})
        for field, value in metadata.items():
            if field not in self._metadataFields:
                self._metadataFields.append(field)

            if field == 'fields':
                self._buildFields(key, value)
            else:
                self.metadata[-1][field] = value
    
    def _buildFields(self, key : str, fields : dict) -> None:
        for num, field in enumerate(fields.items()):
            fieldName, valueType = field
            self.fields.append({'key': key, 'field_name': fieldName, 'field_value_type': valueType, 'field_num': num})

    def _normalize(self, attributeName : str) -> None:
        addFields = []
        for num, entity in enumerate(self.__dict__[attributeName]):
            missingFields = []
            for field in self.__dict__['_{}Fields'.format(attributeName)]:
                if field not in entity.keys():
                    missingFields.append(field)

            if len(missingFields) > 0:
                addFields.append((num, missingFields))

        for index, fields in addFields:
            for field in fields:
                self.__dict__[attributeName][index][field] = None
        