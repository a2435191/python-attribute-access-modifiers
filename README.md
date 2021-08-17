# python-attribute-access-modifiers

Tired of typing `@property` just to make a read-only instance variable? Find yourself wishing for C#'s `{get; set;}` syntax? Look no further than PAAM, which auto-generates property getters, setter, and deleters for you!

## Quickstart

Once installed, just use the overloaded `|` operator between an instance variable and one of the predefined constants `GET`, `SET`, or `DEL`. Make sure to subclass from `PaamBase`.

```python
from paam import SET, PaamBase

class Test(PaamBase):
    def __init__(self, a: int):
        self.a = a | GET # write to self.a (not self._a) because PAAM creates setters/getters/deleters *after* __init__ finishes

>>> obj = Test(15)
>>> obj.a
>>> 15
>>> obj.a = 5 # raises AttributeError: can't set attribute
```

Property access modifiers can also be chained (order doesn't matter):

```python
from paam import SET, GET, DEL, PaamBase

class Test(PaamBase):
    def __init__(self, a: int):
        self.a = a | GET | SET

>>> obj = Test(15)
>>> obj.a
>>> 15
>>> obj.a = 5
>>> obj.a
>>> 5
>>> del obj.a # raises AttributeError: can't delete attribute
```

## Caveats (all planned to be fixed in future release)
* The type of any variable "annotated" with `GET`, `SET`, or `DEL` is `_PropertyAccessModifierBase`. This means `mypy` support and IDE type hinting are most likely broken.
* No tests