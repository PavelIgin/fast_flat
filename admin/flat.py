from sqladmin import ModelView

from flat.models import Flat

__all__ = ("FlatAdmin",)


class FlatAdmin(ModelView, model=Flat):
    column_list = [Flat.cost, Flat.floor, Flat.quadrature, Flat.address]
    column_searchable_list = [Flat.user_id, Flat.id]
