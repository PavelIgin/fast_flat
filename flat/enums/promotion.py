from enum import IntEnum


class PromotionEnum(IntEnum):
    """
    Enum ordering Flat by Promotion
    """

    DEFAULT = 1
    MIDDLE = 2
    TOP = 3

    @staticmethod
    def get_count_elements():
        return len([i for i in PromotionEnum])
