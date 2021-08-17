from typing import Any, Callable, List
from abc import ABC

class _PaamBaseDescriptor(ABC):
    def __init__(self, obj: Any) -> None:
        self.is_setter  = isinstance(obj, Setter)  or isinstance(self, Setter)
        self.is_getter  = isinstance(obj, Getter)  or isinstance(self, Getter)
        self.is_deleter = isinstance(obj, Deleter) or isinstance(self, Deleter)

        self._obj = obj


    def __get__(self, owner_instance, owner_cls=None):
        raise ValueError(
            f"{owner_instance if owner_cls is None else owner_cls} is not gettable"
        )

    def __set__(self, owner_instance, value):
        raise ValueError(
            f"{owner_instance} is not settable"
        )

    def __delete__(self, owner_instance):
        raise ValueError(
            f"{owner_instance} is not deletable"
        )

class Setter(_PaamBaseDescriptor):
    def __set__(self, owner_instance, value):
        self._obj = value

class Getter(_PaamBaseDescriptor):
    def __get__(self, owner_instance, owner_cls=None):
        return self._obj

class Deleter(_PaamBaseDescriptor):
    def __delete__(self, owner_instance):
        del self._obj

class _PropertyAccessModifierFactory:
    def __init__(self, cls: type) -> None:
        self.cls = cls

    def __ror__(self, other: Any) -> _PaamBaseDescriptor:
        if issubclass(other.__class__, _PaamBaseDescriptor):
            class Both(self.cls, other.__class__):
                pass
            return Both(other._obj)
        return self.cls(other)

SET = _PropertyAccessModifierFactory(Setter)
GET = _PropertyAccessModifierFactory(Getter)
DEL = _PropertyAccessModifierFactory(Deleter)

# read https://dev.to/mattconway1984/python-creating-instance-properties-2ej0
# for more
class PaamBase:
    def __setattr__(self, attr_name: str, value: Any) -> None:
        try:
            attr = super().__getattribute__(attr_name) # avoid recursion this way
        except AttributeError: # must be "normal" attribute
            super().__setattr__(attr_name, value)
        else:
            if issubclass(type(attr), _PaamBaseDescriptor):
                attr.__set__(self, value)
            else:
                super().__setattr__(attr_name, value) # if "normal" attribute

    def __getattribute__(self, attr_name: str) -> Any:
        attr = super().__getattribute__(attr_name)
        if issubclass(type(attr), _PaamBaseDescriptor):
            return attr.__get__(self, self.__class__)
        return attr

    def __delattr__(self, attr_name: str) -> None:
        attr = super().__getattribute__(attr_name)
        if issubclass(type(attr), _PaamBaseDescriptor):
            attr.__delete__(self)
        del attr
