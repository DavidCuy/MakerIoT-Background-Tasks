from __future__ import annotations
import json
from json.encoder import JSONEncoder
import Environment as env
from typing import Any, Dict, List, Type, cast
from typing import List
from datetime import datetime
from mongoengine import Document, connect
from src.utils.encoders import CustomJSONDecoder
from src.config.database import config

## Database connection string
config_mongo = config[env.MONGODB_DRIVER]
connect(
    config_mongo['database'],
    host=config_mongo['host'],
    port=config_mongo['port'],
    username=config_mongo['username'],
    password=config_mongo['password'],
    authentication_source='admin'
)



class BaseMongoModel(Document):
    """ Base model for a child classes implementations

    Args:
        Base (Any): SQLAlchemy declarative base

    Raises:
        e: Exceptions for not implemented functions

    Returns:
        BaseModel: Instace of BaseModel class
    """

    ## Indicate it is an abstract class (not 100% completed y going to be done in child classes)
    __abstract__ = True
    
    filter_columns = []
    relationship_names = []
    search_columns = []
    meta = {'allow_inheritance': True}


    @property
    def attrs(self) -> List[str]:
        """ Returns a list of the attributes of an object

        Returns:
            List[str]: Attributes
        """
        preliminar = list(filter(lambda prop: not str(prop).startswith('_'), type(self).__dict__.keys()))
        display_member = self.display_members()
        return list(set(preliminar) & set(display_member)) if len(display_member) > 0 else display_member
    
    @classmethod
    def filters(cls_, filters: List[dict], paginated: bool = False, page: int = 1, per_page: int = 10, first: bool = False):
        """ Gets all documents that match with the multiple filters specified in dict (and logic)

        Args:
            cls_ (class): Child class method

        Returns:
            List[Type[BaseModel]]: List of elements that match with the multiple filters
        """
        query_dict = {}
        for filter in filters:
            key = list(filter.keys())[0]
            query_dict.update({key: filter[key]})
        
        if first:
            return cls_, cls_.objects(__raw__=query_dict).first()
        
        if paginated:
            init_element = (page - 1) * (per_page)
            end_element = init_element + per_page - 1
            return cls_, cls_.objects(__raw__=query_dict)[init_element:end_element]
        return cls_, cls_.objects(__raw__=query_dict)

    @classmethod
    def all(cls_):
        """ Get all documents from a table

        Args:
            cls_ (cls): Type of class

        Returns:
            List[Type[BaseModel]]: List of elements mapped from database table
        """
        return cls_, cls_.objects
    
    @classmethod
    def get_paginated(cls_, page: int = 1, per_page: int = 10):
        return cls_.filters([], paginated=True, page=page, per_page=per_page)
    
    @classmethod
    def filter_by(cls_, column_name: str, value, paginated: bool = False, page: int = 1, per_page: int = 10, first = False):
        """ Gets all documents that match with the specified filter

        Args:
            cls_ (class): Child class method
            column_name (str): Column name to filter
            value (Any): Value to match

        Returns:
            List[Type[BaseModel]]: List of elements that match with filter
        """
        filter_dict = {
            column_name: value
        }
        return cls_.filters([filter_dict], paginated, page, per_page, first)
    
    @classmethod
    def find(cls_, id: str):
        """ Search a document by id

        Args:
            cls_ (class): Child class method
            id (int): document identifier

        Returns:
            Type[BaseModel]: The document that have a coincidence with the identifier
        """
        return cls_.objects.get(id=id)
    
    @classmethod
    def get_one(cls_, column_name: str, value):
        """ Gets the first document that matches the filter

        Args:
            cls_ (class): Child class method
            session (Session): Database session
            column_name (str): Column name to filter
            value (Any): Value to match

        Returns:
            Type[BaseModel]: First register that match with filter
        """
        filter_dict = {
            column_name: value
        }
        return cls_.filters([filter_dict], first=True)

    def before_save(self, *args, **kwargs):
        """ Method to execute before save a document in database (polimorfism)
        """
        pass

    def after_save(self, *args, **kwargs):
        """ Method to execute after save a document in database (polimorfismo)
        """
        pass
    
    def save_document(self, *args, **kwargs):
        """ Save a register in database

        Args:
            session (Session): Database session
            commit (bool, optional): Indicate if the changes will make in database. Defaults to True.

        Raises:
            e: In case of error, the register will be erased and raise an Exception
        """
        self.before_save(*args, **kwargs)
        self.save()

        self.after_save(*args, **kwargs)
        return self

    def before_update(self, *args, **kwargs):
        """ Method to execute before update a document in database (polimorfism)
        """
        pass

    def after_update(self, *args, **kwargs):
        """ Method to execute after update a document in database (polimorfism)
        """
        pass

    def update_document(self, object: dict, *args, **kwargs):
        """ Update a specified register in database

        Args:
            session (Session): Database session
            object (dict): Dictionary with only the field to update
        """
        self.before_update(*args, **kwargs, **object)
        keys = self.get_keys()
        for key in keys:
            if key in object:
                update_dict = {key: object[key]}
                self.update(**update_dict)
        self.reload()
        self.after_update(*args, **kwargs)
        return self
    
    def before_delete(self, *args, **kwargs):
        """ Method to execute before update a document in database (polimorfism)
        """
        pass

    def after_delete(self, *args, **kwargs):
        """ Method to execute after update a document in database (polimorfism)
        """
        pass

    def delete_document(self, *args, **kwargs):
        """ Delete a specified register in database

        Args:
            session (Session): Database session
            commit (bool, optional): Indicate if the changes will make in database. Defaults to True.
        """
        self.before_delete(*args, **kwargs)
        self.delete()
        self.after_delete(*args, **kwargs)

    
    @classmethod
    def get_keys(cls_: Type[BaseMongoModel]) -> List[str]:
        """ Get all attributes of class

        Args:
            cls_ (Type[BaseModel]): Child class method

        Returns:
            List[str]:  Attributes
        """
        return list(filter(lambda prop: not str(prop).startswith('_'), cls_.__dict__.keys()))
    
    @classmethod
    def display_members(cls_) -> List[str]:
        """Get only de properties to display to end user

        Returns:
            List[str]: List of properties
        """
        return []
    
    def to_dict(self, jsonEncoder: JSONEncoder = CustomJSONDecoder, circular: bool = True, encoder_extras: dict = {}) -> dict:
        dict_element: dict = json.loads(self.to_json())
        for key in dict_element.keys():
            if isinstance(dict_element[key], dict):
                if '$oid' in dict_element[key]:
                    dict_element[key] = dict_element[key]['$oid']
                if '$date' in dict_element[key]:
                    dict_element[key] = datetime.fromtimestamp(int(dict_element[key]['$date']/1000))
        return dict_element


    def __repr__(self) -> str:
        """ Model representation

        Returns:
            str: Model output string formatted
        """
        attr_array = [f"{attr}={self.__getattribute__(attr)}" for attr in self.attrs]
        args_format = ",".join(attr_array)
        return f"<{type(self).__name__}({args_format})>"


