from flat.models import Flat, Promotion, Renting
from users.models import User

from .base_model import Base

__all__ = ["Base", "User", "Flat", "Renting", "Promotion"]
