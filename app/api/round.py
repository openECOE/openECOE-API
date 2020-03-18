#  Copyright (c) 2019 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#      openECOE-API is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      openECOE-API is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.

from flask_potion import fields
from flask_potion.routes import Relation, ItemRoute
from app.model.Round import Round
from app.api.ecoe import EcoeChildResource


class RoundResource(EcoeChildResource):
    planners = Relation('planners')

    class Meta:
        name = 'rounds'
        model = Round
        natural_key = ('ecoe', 'round_code')

    class Schema:
        ecoe = fields.ToOne('ecoes')

    @ItemRoute.POST('/play')
    def chrono_play(self, round) -> fields.String():
        return round.ecoe.play(round.id)

    @ItemRoute.POST('/pause')
    def chrono_pause(self, round) -> fields.String():
        return round.ecoe.pause(round.id)