from sqladmin import ModelView

from flat.models import Photo

__all__ = ("PhotoAdmin",)


class PhotoAdmin(ModelView, model=Photo):
    column_list = [Photo.id, Photo.flat, Photo.photo]
