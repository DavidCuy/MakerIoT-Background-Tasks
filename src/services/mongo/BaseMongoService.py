
from typing import List, Tuple, Type, cast

from src.data.models.mongo import BaseMongoModel

class BaseMongoService:
    def __init__(self, model: Type) -> None:
        self.model = model
    
    def get_all(self, paginate = False, page = 1, per_page = 10) -> Tuple[Type[BaseMongoModel], BaseMongoModel]:
        """ Obtiene todos los elementos del modelo de datos especificado

        Args:
            self (class): Class
            paginate (bool, optional): Flag to paginate results. Defaults to False.
            page (int, optional): Pagenumber to return. Defaults to 1.
            per_page (int, optional): Number of elements per page. Defaults to 10.

        Returns:
            List: Lista de objectos de base de datos
        """
        if paginate is True:
            return cast(BaseMongoModel, self.model).get_paginated(page, per_page)
        return cast(BaseMongoModel, self.model).all()
    
    def get_one(self, id: str):
        """ Search an element by id

        Args:
            self (class): Class
            id (str): Database identifier

        Returns:
            ORMClass: Devuelve un objeto de la base de datos
        """
        return cast(BaseMongoModel, self.model).find(id)
    
    def filter_by_column(self, column_name: str, column_value, paginate = False, page = 1, per_page = 10, first: bool = False):
        return cast(BaseMongoModel, self.model).filter_by(column_name, column_value, paginate, page, per_page, first)

    def get_by_column(self, column_name: str, column_value):
        """ Get an element according with the specified colum name and value

        Args:
            self (class): Class
            column_name (str): Column name
            value (Any): Value to mach

        Returns:
            ORMClass: First coincidence of the search
        """
        return cast(BaseMongoModel, self.model).get_one(column_name, column_value)
    
    def multiple_filters(self, filters: List[dict], paginate = False, page = 1, per_page = 10, first: bool = False):
        return cast(BaseMongoModel, self.model).filters(filters, paginate, page, per_page, first)
    
    def insert_register(self, input_data: dict):
        input_params = {}
        for ipKey in input_data.keys():
            if ipKey in self.get_model_keys():
                input_params[ipKey] = input_data[ipKey]
        obj = self.model(**input_params)
        return cast(BaseMongoModel, obj).save_document(**input_data)
    
    def update_register(self, id: str, update_data: dict):
        obj = self.get_one(id)
        return cast(BaseMongoModel, obj).update_document(update_data)
    
    def delete_register(self, id: int):
        obj = self.get_one(id)
        return cast(BaseMongoModel, obj).delete_document()
    
    def get_model_keys(self) -> List[str]:
        return cast(BaseMongoModel, self.model).get_keys()
    
    def get_display_members(self) -> List[str]:
        return cast(BaseMongoModel, self.model).display_members()

    def get_filter_columns(self) -> List[str]:
        return cast(BaseMongoModel, self.model).filter_columns

    def get_relationship_names(self) -> List[str]:
        return cast(BaseMongoModel, self.model).relationship_names
    
