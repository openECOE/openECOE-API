from typing import Type
import uuid
from seedwork.domain.entities import Entity


class JSONDataMapper:
    """Used to serialize/deserialize entities from/to JSON data format"""

    def data_to_entity(self, data: dict, entity_class: Type[Entity]) -> Entity:
        """Creates business entity from dictionary with a `data` attribute"""
        entity_id = uuid.UUID(str(data.id))
        entity_dict = {
            "id": entity_id,
            **data.data,
        }
        return entity_class(**entity_dict)

    def entity_to_data(self, entity: Entity, model_class):
        """Stores entity attributes in dictionary with a `data` attribute"""
        data = dict(**entity.__dict__)
        entity_id = str(data.pop("id"))
        return model_class(
            **{
                "id": entity_id,
                "data": data,
            }
        )
