from sqladmin import ModelView

from flat.models import Promotion

__all__ = ("RentingAdmin",)


class RentingAdmin(ModelView, model=Promotion):
    column_list = [
        Promotion.id,
        Promotion.type,
    ]
