from sqladmin import ModelView

from flat.models import Renting

__all__ = ("RentingAdmin",)


class RentingAdmin(ModelView, model=Renting):
    column_list = [
        Renting.id,
        Renting.cost,
    ]
