#  Copyright (c) 2020 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#       openECOE-API is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       openECOE-API is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.

from flask_potion import ModelResource, fields
from flask_potion.routes import Route, ItemRoute
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals
from werkzeug.exceptions import Forbidden
from app.api import export

MainManager = principals(SQLAlchemyManager)


class OpenECOEResource(ModelResource):
    @ItemRoute.GET('/permissions')
    def item_permissions(self, item) -> fields.String():
        object_permissions = self.manager.get_permissions_for_item(item)
        return object_permissions

    @Route.GET('/permissions')
    def object_permissions(self) -> fields.String():
        object_permissions = self.manager.get_permissions_for_item(self)
        return object_permissions

    @ItemRoute.GET('/export',
                   rel="exportItem",
                   description="export data to file")
    def item_export(self, item):
        # Only can export if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(item)
        if 'manage' in object_permissions and object_permissions['manage'] is not True:
            raise Forbidden

        _filename = self.Meta.name

        _dict = {_filename: [item]}

        return export.book_dict(_dict, _filename)

    @Route.GET('/export',
               rel="export",
               description="export data to file")
    def object_export(self):
        # Only can export if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(self)
        if 'manage' in object_permissions and object_permissions['manage'] is not True:
            raise Forbidden

        _query = self.manager.instances().all()

        _columns = self.Meta.model.__table__.columns.keys()
        _filename = self.Meta.name

        _dict = {_filename: _query}

        return export.book_dict(_dict, _filename)

    class Meta:
        manager = MainManager
