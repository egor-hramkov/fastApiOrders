import enum


class EnumContainsMixin(enum.EnumMeta):
    def __contains__(cls, item):
        return isinstance(item, cls) or item in list(cls.__members__.keys())
