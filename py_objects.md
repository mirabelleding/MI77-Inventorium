# Python Object Model

*A practical reference for `object`, `type`, metaclasses, inheritance, class metadata, the `inspect` module, and Python dunder methods.*

## Table of Contents

- [1. The big picture: instance → class → metaclass](#1-the-big-picture-instance--class--metaclass)
  - [`object` versus `type`](#object-versus-type)
  - [What about `int`, `str`, and `list`?](#what-about-int-str-and-list)
- [2. Creating classes with a metaclass](#2-creating-classes-with-a-metaclass)
  - [Meaning of the four arguments](#meaning-of-the-four-arguments)
  - [Which line creates `table_name`?](#which-line-creates-table_name)
  - [Creation sequence](#creation-sequence)
- [3. One complete example: parent class + metaclass](#3-one-complete-example-parent-class--metaclass)
  - [An explicit override is possible](#an-explicit-override-is-possible)
  - [Metaclass conflicts](#metaclass-conflicts)
- [4. Inspecting a class versus inspecting an instance](#4-inspecting-a-class-versus-inspecting-an-instance)
  - [Quick reference](#quick-reference)
  - [`vars()` and `__dict__`: direct attributes](#vars-and-__dict__-direct-attributes)
  - [`dir()`: discover available names](#dir-discover-available-names)
  - [Useful special class attributes](#useful-special-class-attributes)
- [5. The `inspect` module: examples of each function](#5-the-inspect-module-examples-of-each-function)
  - [5.1 `inspect.getmembers(obj)` — names AND values](#51-inspectgetmembersobj--names-and-values)
  - [5.2 `inspect.getmembers(User, inspect.isfunction)` — Python functions](#52-inspectgetmembersuser-inspectisfunction--python-functions)
  - [5.3 `inspect.getmembers(User, inspect.ismethod)` — bound methods](#53-inspectgetmembersuser-inspectismethod--bound-methods)
  - [5.4 `inspect.signature(callable)` — parameters and return annotations](#54-inspectsignaturecallable--parameters-and-return-annotations)
  - [5.5 `inspect.getmro(Class)` — inheritance lookup order](#55-inspectgetmroclass--inheritance-lookup-order)
  - [5.6 `inspect.isclass(obj)` — is this object a class?](#56-inspectisclassobj--is-this-object-a-class)
  - [5.7 `inspect.getsource(obj)` — retrieve Python source](#57-inspectgetsourceobj--retrieve-python-source)
  - [5.8 `inspect.classify_class_attrs(Class)` — where did it come from?](#58-inspectclassify_class_attrsclass--where-did-it-come-from)
  - [5.9 `inspect.getmembers_static()` and `inspect.getattr_static()` — avoid triggering access](#59-inspectgetmembers_static-and-inspectgetattr_static--avoid-triggering-access)
- [6. Other useful `inspect` functions](#6-other-useful-inspect-functions)
- [7. A reusable class introspection helper](#7-a-reusable-class-introspection-helper)
- [8. Practical questions and the best tool](#8-practical-questions-and-the-best-tool)
- [9. Dunder methods — Python's data model](#9-dunder-methods--pythons-data-model)
  - [9.1 The mental model: syntax calls special methods](#91-the-mental-model-syntax-calls-special-methods)
  - [9.2 Object creation: `__new__()` and `__init__()`](#92-object-creation-__new__-and-__init__)
  - [9.3 Truthiness: `__bool__()` and `__len__()`](#93-truthiness-__bool__-and-__len__)
  - [9.4 Printing and debugging: `__repr__()`, `__str__()`, `__format__()`](#94-printing-and-debugging-__repr__-__str__-__format__)
  - [9.5 Container behavior: `__len__()`, `__getitem__()`, `__setitem__()`, `__contains__()`](#95-container-behavior-__len__-__getitem__-__setitem__-__contains__)
  - [9.6 Iteration: `__iter__()` and `__next__()`](#96-iteration-__iter__-and-__next__)
  - [9.7 Operators: `__add__()`, reflected methods, and in-place methods](#97-operators-__add__-reflected-methods-and-in-place-methods)
  - [9.8 Equality, ordering, and hashing](#98-equality-ordering-and-hashing)
  - [9.9 Attribute access: `__getattribute__()`, `__getattr__()`, `__setattr__()`](#99-attribute-access-__getattribute__-__getattr__-__setattr__)
  - [9.10 Descriptors: `__get__()`, `__set__()`, `__set_name__()`](#910-descriptors-__get__-__set__-__set_name__)
  - [9.11 Context managers: `__enter__()` and `__exit__()`](#911-context-managers-__enter__-and-__exit__)
  - [9.12 Callable instances: `__call__()`](#912-callable-instances-__call__)
  - [9.13 Subclass customization and special-method lookup](#913-subclass-customization-and-special-method-lookup)
  - [9.14 Quick selection guide](#914-quick-selection-guide)
- [10. Five ideas to remember](#10-five-ideas-to-remember)
  - [Mini practice exercises](#mini-practice-exercises)

---
## 1. The big picture: instance → class → metaclass

In Python, **classes are themselves objects**.

```text
user = User(1, "Alice")  ── instance of ──► User  ── instance of ──► TableMeta
                                                      (class)       (metaclass)
```

- **Instance:** an object created from a class (`user`).
- **Class:** defines behavior and creates instances (`User`).
- **Metaclass:** defines how class objects are created (`TableMeta`).
- **`type`:** Python's default metaclass.
- **`object`:** the root of the ordinary Python class inheritance hierarchy.

The two different relationships are important:

- **Instance-of:** `isinstance(value, SomeClass)` or `type(value)`.
- **Subclass-of:** `issubclass(Child, Parent)` or `Child.__mro__`.

### `object` versus `type`

```python
type(object) is type          # True: object is an instance of type
type(type) is type            # True: type is an instance of itself

issubclass(type, object)      # True: type inherits from object
issubclass(object, type)      # False: object does not inherit from type

isinstance(object, type)      # True
isinstance(type, object)      # True
```

**Memorize:** `object` is the base of the inheritance hierarchy; `type` is the default metaclass of class objects. Their apparent circularity combines **two distinct relationships**, not circular inheritance.

### What about `int`, `str`, and `list`?

```python
type(10) is int               # True
type(int) is type             # True
isinstance(int, type)         # True
issubclass(int, object)       # True
issubclass(int, type)         # False

# The same applies to str, list, dict, float, and most classes.
```

`int` is an **instance of `type`** and a **subclass of `object`**. It is **not** a subclass of `type`.

---

## 2. Creating classes with a metaclass

A metaclass commonly subclasses `type` and customizes `__new__`.

```python
class TableMeta(type):
    def __new__(mcls, name, bases, namespace):
        namespace.setdefault("table_name", name.lower())
        return super().__new__(mcls, name, bases, namespace)
```

### Meaning of the four arguments

| Parameter | Meaning | Example while creating `User` |
| --- | --- | --- |
| `mcls` | Metaclass being used | `TableMeta` |
| `name` | New class's name, as a string | `"User"` |
| `bases` | Tuple of direct parent classes | `(BaseModel,)` |
| `namespace` | Mapping of names defined by the class body | `{"category": "customer", ...}` |

**`name` is the class name string**, not the class object: `"User"` rather than `User`.

### Which line creates `table_name`?

```python
namespace.setdefault("table_name", name.lower())
```

For `User`, this behaves like:

```python
if "table_name" not in namespace:
    namespace["table_name"] = "user"
```

Then this line creates and returns the actual class object:

```python
return super().__new__(mcls, name, bases, namespace)
```

Here, `super().__new__` resolves to **`type.__new__`**.

> `table_name` is a Python **class attribute** (custom class metadata). This code does **not** create a real SQL database table.

### Creation sequence

```text
Execute class body
      ↓
Collect namespace (attributes, methods, etc.)
      ↓
Call TableMeta.__new__(mcls, name, bases, namespace)
      ↓
Add default table_name to namespace
      ↓
Call type.__new__(...) to construct the class object
      ↓
Assign the created class object to its name (e.g. User)
```

A metaclass can also implement `__prepare__`, `__init__`, and `__call__`; this example focuses on `__new__`, which customizes **class construction**. The metaclass's `__call__` can influence **instance creation**.

---

## 3. One complete example: parent class + metaclass

This example will be reused throughout the introspection section.

```python
import inspect

class TableMeta(type):
    def __new__(mcls, name, bases, namespace):
        namespace.setdefault("table_name", name.lower())
        return super().__new__(mcls, name, bases, namespace)


class BaseModel(metaclass=TableMeta):
    def save(self):
        return f"Saving to {self.table_name}"


class User(BaseModel):
    category = "customer"

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def greet(self):
        return f"Hello, {self.name}"

    @classmethod
    def get_category(cls):
        return cls.category

    @staticmethod
    def validate_id(value):
        return isinstance(value, int)


class Transaction(BaseModel):
    pass


user = User(1, "Alice")
```

Check what was created:

```python
User.table_name                 # 'user'
Transaction.table_name          # 'transaction'
user.greet()                    # 'Hello, Alice'
user.save()                     # 'Saving to user'

issubclass(User, BaseModel)      # True: inheritance
isinstance(User, TableMeta)     # True: metaclass relationship
type(User) is TableMeta         # True
issubclass(User, TableMeta)     # False: not inheritance

User.__bases__                  # (BaseModel,)
User.__mro__                    # (User, BaseModel, object)
```

**Why isn't `metaclass=TableMeta` repeated on `User`?** Python chooses a metaclass compatible with its bases. Since `BaseModel` already uses `TableMeta`, `User` uses it too.

### An explicit override is possible

```python
class AuditLog(BaseModel):
    table_name = "audit_entries"

AuditLog.table_name             # 'audit_entries'
```

`setdefault` does not replace an attribute already present in the class namespace.

### Metaclass conflicts

```python
class OtherMeta(type):
    pass

class OtherBase(metaclass=OtherMeta):
    pass

# class Mixed(BaseModel, OtherBase):
#     pass
# TypeError: metaclass conflict
```

The selected metaclass must be a subclass of (or identical to) the metaclasses of all direct bases. If appropriate, a combined metaclass can resolve the conflict:

```python
class CombinedMeta(TableMeta, OtherMeta):
    pass

class Mixed(BaseModel, OtherBase, metaclass=CombinedMeta):
    pass
```

---

## 4. Inspecting a class versus inspecting an instance

### Quick reference

| Expression | What it reveals |
| --- | --- |
| `type(obj)` | Object's exact class (or a class's metaclass) |
| `obj.__class__` | Class of the object |
| `vars(obj)` | Dictionary of attributes stored directly on the object |
| `obj.__dict__` | Direct attribute namespace, when available |
| `dir(obj)` | Names of attributes/methods available for lookup |
| `Class.__name__` | Class name |
| `Class.__qualname__` | Qualified class name |
| `Class.__module__` | Module name |
| `Class.__bases__` | Direct parent classes |
| `Class.__mro__` | Method resolution order / inheritance lookup order |
| `type(Class)` | Class's metaclass |

### `vars()` and `__dict__`: direct attributes

```python
vars(user)
# {'id': 1, 'name': 'Alice'}

# Selected entries from vars(User):
# {
#   'category': 'customer',
#   '__init__': <function User.__init__ ...>,
#   'greet': <function User.greet ...>,
#   'table_name': 'user',
#   ...
# }

user.__dict__                   # {'id': 1, 'name': 'Alice'}
User.__dict__                   # mappingproxy({...})
```

- `vars(user)` only shows attributes stored directly on that instance, not inherited class attributes.
- `vars(User)` shows attributes stored directly on the `User` class, including ones added by the metaclass during creation.
- `User.__dict__` is a read-only **mapping proxy** of the class's namespace; a normal instance's `__dict__` is a mutable dictionary.
- Some objects use `__slots__` or extension-defined storage and have no instance `__dict__`. In that case `vars()` may raise `TypeError`.

### `dir()`: discover available names

```python
[name for name in dir(user) if not name.startswith("__")]
# ['category', 'get_category', 'greet', 'id', 'name',
#  'save', 'table_name', 'validate_id']

'save' in dir(user)             # True (inherited)
'save' in vars(user)            # False (not stored on instance)
```

`dir()` typically includes inherited and dynamically advertised names, but it is **not guaranteed to be an exhaustive inventory**.

### Useful special class attributes

```python
User.__name__                   # 'User'
User.__qualname__               # 'User'
User.__bases__                  # (BaseModel,)
User.__mro__                    # (User, BaseModel, object)
User.__module__                 # Usually '__main__' in a script
User.__class__ is TableMeta     # True
```

---

## 5. The `inspect` module: examples of each function

All examples below refer to the `User` and `user` defined in Section 3.

### 5.1 `inspect.getmembers(obj)` — names AND values

```python
for name, value in inspect.getmembers(User):
    if not name.startswith("__"):
        print(name, ":", value)
```

Simplified output:

```text
category : customer
get_category : <bound method User.get_category of <class '...User'>>
greet : <function User.greet at 0x...>
save : <function BaseModel.save at 0x...>
table_name : user
validate_id : <function User.validate_id at 0x...>
```

`getmembers()` returns **sorted `(name, value)` pairs**. It includes inherited members, but ordinary attribute access can trigger properties and other descriptors.

### 5.2 `inspect.getmembers(User, inspect.isfunction)` — Python functions

```python
[name for name, _ in inspect.getmembers(User, inspect.isfunction)]
# ['__init__', 'greet', 'save', 'validate_id']
```

- `greet` is an ordinary instance method accessed **from a class**, so it appears as a function.
- `save` is an inherited ordinary method, also appearing as a function.
- `validate_id` is a `@staticmethod`, which appears as a function on access.
- `get_category` is a `@classmethod`: on access, it appears as a **bound method**, not a function.

### 5.3 `inspect.getmembers(User, inspect.ismethod)` — bound methods

```python
[name for name, _ in inspect.getmembers(User, inspect.ismethod)]
# ['get_category']
```

The difference depends on **where you access the method**:

| Expression | `inspect.isfunction(...)` | `inspect.ismethod(...)` |
| --- | --- | --- |
| `User.greet` | `True` | `False` |
| `user.greet` | `False` | `True` |
| `User.get_category` | `False` | `True` |
| `User.validate_id` | `True` | `False` |

A bound method exposes the object it is bound to:

```python
user.greet.__self__ is user         # True
user.greet.__func__ is User.greet  # True

User.get_category.__self__ is User # True
```

### 5.4 `inspect.signature(callable)` — parameters and return annotations

```python
str(inspect.signature(User))             # '(id, name)'
str(inspect.signature(User.__init__))    # '(self, id, name)'
str(inspect.signature(User.greet))       # '(self)'
str(inspect.signature(user.greet))       # '()'
str(inspect.signature(User.validate_id)) # '(value)'
```

The callable class `User` has signature `(id, name)` because callers use `User(id, name)`. A bound instance method hides its already-bound `self` parameter.

Inspect individual parameters:

```python
def calculate(amount: float, rate: float = 0.05) -> float:
    return amount * rate

sig = inspect.signature(calculate)

sig.parameters["rate"].default    # 0.05
sig.parameters["rate"].kind       # POSITIONAL_OR_KEYWORD
sig.return_annotation             # <class 'float'>
```

**Uses:** validation, dependency injection, CLI generation, decorators, and introspecting unfamiliar APIs.

### 5.5 `inspect.getmro(Class)` — inheritance lookup order

```python
inspect.getmro(User)
# (User, BaseModel, object)

[c.__name__ for c in inspect.getmro(User)]
# ['User', 'BaseModel', 'object']
```

Equivalent to `User.__mro__`. Especially helpful with **multiple inheritance**, where lookup order is governed by Python's MRO (C3 linearization).

### 5.6 `inspect.isclass(obj)` — is this object a class?

```python
inspect.isclass(User)        # True
inspect.isclass(BaseModel)   # True
inspect.isclass(TableMeta)   # True
inspect.isclass(int)         # True
inspect.isclass(type)        # True
inspect.isclass(object)      # True
inspect.isclass(user)        # False
inspect.isclass(User.greet)  # False
```

**Use:** discovering classes in a module or building a class registry.

### 5.7 `inspect.getsource(obj)` — retrieve Python source

```python
print(inspect.getsource(User))
print(inspect.getsource(User.greet))
```

When available, the first returns the original `class User(BaseModel): ...` source, and the second returns the source of `greet()`.

**Caveat:** `getsource()` may raise `OSError` or `TypeError` for built-ins, extension objects, dynamically defined objects, or interactive environments where source isn't available.

### 5.8 `inspect.classify_class_attrs(Class)` — where did it come from?

```python
for attr in inspect.classify_class_attrs(User):
    if not attr.name.startswith("__"):
        print(attr.name, attr.kind, attr.defining_class.__name__)
```

Output:

```text
category data User
get_category class method User
greet method User
save method BaseModel
table_name data User
validate_id static method User
```

This distinguishes **inherited members**, **ordinary methods**, **class methods**, and **static methods**.

### 5.9 `inspect.getmembers_static()` and `inspect.getattr_static()` — avoid triggering access

Consider a property with side effects:

```python
class Example:
    @property
    def expensive(self):
        print("PROPERTY EXECUTED")
        return 42

example = Example()

getattr(example, "expensive")               # Prints PROPERTY EXECUTED
inspect.getattr_static(example, "expensive") # Returns the property descriptor
```

`inspect.getmembers_static(example)` similarly inspects members without triggering normal descriptor access or dynamic attribute lookup. It is useful for debugging, although it can miss some dynamically produced attributes.

---

## 6. Other useful `inspect` functions

| Function | Purpose | Example |
| --- | --- | --- |
| `inspect.getfile(User)` | Find defining file, when known | `inspect.getfile(User)` |
| `inspect.getmodule(User)` | Find defining module | `inspect.getmodule(User)` |
| `inspect.getdoc(User)` | Read cleaned docstring | `inspect.getdoc(User)` |
| `inspect.isabstract(User)` | Check for abstract class | `inspect.isabstract(User)` |
| `inspect.isgeneratorfunction(f)` | Check generator function | `inspect.isgeneratorfunction(f)` |
| `inspect.iscoroutinefunction(f)` | Check `async def` function | `inspect.iscoroutinefunction(f)` |
| `inspect.isawaitable(x)` | Check whether object can be awaited | `inspect.isawaitable(x)` |
| `inspect.isdatadescriptor(x)` | Identify data descriptors | `inspect.isdatadescriptor(x)` |

```python
def counter():
    yield 1

async def fetch():
    return 1

inspect.isgeneratorfunction(counter)   # True
inspect.iscoroutinefunction(fetch)    # True
```

---

## 7. A reusable class introspection helper

```python
import inspect


def describe_class(cls):
    if not inspect.isclass(cls):
        raise TypeError("Expected a class")

    return {
        "name": cls.__name__,
        "module": cls.__module__,
        "metaclass": type(cls).__name__,
        "bases": [base.__name__ for base in cls.__bases__],
        "mro": [base.__name__ for base in inspect.getmro(cls)],
        "own_attributes": list(vars(cls)),
        "functions": [
            name for name, _ in inspect.getmembers(cls, inspect.isfunction)
        ],
        "bound_methods": [
            name for name, _ in inspect.getmembers(cls, inspect.ismethod)
        ],
        "origins": {
            member.name: member.defining_class.__name__
            for member in inspect.classify_class_attrs(cls)
            if not member.name.startswith("__")
        },
    }


metadata = describe_class(User)
print(metadata["metaclass"])   # TableMeta
print(metadata["mro"])         # ['User', 'BaseModel', 'object']
print(metadata["origins"]["save"])  # BaseModel
```

For a **particular instance**:

```python
def describe_instance(obj):
    cls = type(obj)
    return {
        "class": cls.__name__,
        "metaclass": type(cls).__name__,
        "instance_attrs": vars(obj) if hasattr(obj, "__dict__") else None,
        "available_names": [n for n in dir(obj) if not n.startswith("__")],
    }

print(describe_instance(user))
```

**Limit:** No single introspection API reveals absolutely everything about every object. `__slots__`, dynamic attributes, descriptors, built-ins, and custom `__getattribute__` or `__dir__` can change what each tool sees.

---

## 8. Practical questions and the best tool

| Question | Best first choice |
| --- | --- |
| What class is `x`? | `type(x)` |
| What metaclass created `User`? | `type(User)` |
| Does `User` inherit from `BaseModel`? | `issubclass(User, BaseModel)` |
| What are the direct parents? | `User.__bases__` |
| What is the full lookup hierarchy? | `User.__mro__` / `inspect.getmro(User)` |
| What attributes are stored directly on `user`? | `vars(user)` |
| What attributes are stored on `User` itself? | `vars(User)` |
| What names might I access? | `dir(user)` |
| Which members exist, including inherited ones? | `inspect.getmembers(User)` |
| Which plain Python functions exist? | `inspect.getmembers(User, inspect.isfunction)` |
| Which bound methods exist on the class? | `inspect.getmembers(User, inspect.ismethod)` |
| What parameters does a callable accept? | `inspect.signature(callable)` |
| Which parent defined an attribute? | `inspect.classify_class_attrs(User)` |
| What is its implementation? | `inspect.getsource(obj)` (when available) |
| How to inspect without executing a property? | `inspect.getattr_static()` / `getmembers_static()` |

## 9. Dunder methods — Python's data model

**Dunder** means *double underscore*: names such as `__len__`, `__bool__`, and `__add__`. These **special methods** allow objects of your own classes to participate in Python's built-in syntax and operations. This section extends the earlier metaclass and introspection examples with ordinary instance behavior, descriptors, and class-creation hooks.

### 9.1 The mental model: syntax calls special methods

| Python operation | Special method(s) involved |
| --- | --- |
| `obj = MyClass(...)` | Metaclass `__call__`, then usually instance `__new__` and `__init__` |
| `bool(obj)` / `if obj:` | `__bool__`, falling back to `__len__` |
| `str(obj)` / `repr(obj)` | `__str__` / `__repr__` |
| `len(obj)` | `__len__` |
| `obj[key]` / `obj[key] = v` | `__getitem__` / `__setitem__` |
| `x in obj` | `__contains__` (or iteration/sequence fallback) |
| `iter(obj)` / `next(it)` | `__iter__` / `__next__` |
| `a + b` / `a += b` | `__add__`, `__radd__` / `__iadd__` |
| `a == b` / `hash(a)` | `__eq__` / `__hash__` |
| `obj.name` / `obj.missing` | `__getattribute__` / sometimes `__getattr__` |
| `obj(...)` | Instance's class `__call__` |
| `with obj as x:` | `__enter__` / `__exit__` |
| `class Child(Parent): ...` | Potentially `Parent.__init_subclass__` |

**Crucial lookup rule:** for implicit special operations, Python generally looks up special methods **on the object's type**, not in the object's instance dictionary. This differs from normal `obj.method()` attribute lookup. See Section 9.13 for an example.

### 9.2 Object creation: `__new__()` and `__init__()`

- `__new__(cls, ...)` **creates/returns the instance**; it is commonly customized for immutable types or advanced construction.
- `__init__(self, ...)` **initializes an existing instance** and must return `None`.
- Normally, calling `MyClass(...)` is orchestrated by the metaclass's `__call__` (usually `type.__call__`).

```python
class Tracked:
    def __new__(cls, value):
        print("__new__: allocate")
        return super().__new__(cls)

    def __init__(self, value):
        print("__init__: initialize")
        self.value = value

obj = Tracked(10)
# __new__: allocate
# __init__: initialize
print(obj.value)  # 10
```

If `__new__` returns an object that is **not an instance of the class being constructed**, Python does not run that class's `__init__` on it. Most ordinary classes only need `__init__`.

### 9.3 Truthiness: `__bool__()` and `__len__()`

When evaluating `if obj:` or `bool(obj)`, Python follows this priority:

```text
obj
 ├── type(obj).__bool__() exists? ──▶ use its bool result
 └── otherwise
       ├── type(obj).__len__() exists? ──▶ False if length == 0
       └── neither exists ────────────▶ True
```

```python
class Basket:
    def __init__(self, items):
        self.items = list(items)

    def __len__(self):
        return len(self.items)

bool(Basket([]))           # False
bool(Basket(["apple"]))    # True
```

`__bool__` takes priority if both are present:

```python
class Account:
    def __init__(self, balance):
        self.balance = balance

    def __len__(self):
        return 0

    def __bool__(self):
        return self.balance > 0

bool(Account(100))  # True, despite __len__ returning 0
bool(Account(0))    # False
```

**Rules:** `__bool__` must return a real `bool`; `__len__` must return a nonnegative integer. Empty built-in lists, strings, tuples, dictionaries, and sets are falsy because their lengths are zero. When you need to distinguish `0` or `[]` from `None`, test `is not None` explicitly.

### 9.4 Printing and debugging: `__repr__()`, `__str__()`, `__format__()`

- `__repr__`: useful, unambiguous developer/debug representation; used by `repr(obj)` and `f"{obj!r}"`.
- `__str__`: human-friendly text; used by `str(obj)`, `print(obj)`, and `f"{obj}"`.
- `__format__`: handles formatting specifications such as `f"{obj:.2f}"` when defined.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point(x={self.x!r}, y={self.y!r})"

    def __str__(self):
        return f"({self.x}, {self.y})"

p = Point(2, 3)
repr(p)          # 'Point(x=2, y=3)'
str(p)           # '(2, 3)'
print(p)         # (2, 3)
f"Debug: {p!r}"  # 'Debug: Point(x=2, y=3)'
```

If `__str__` isn't defined, `object.__str__` falls back to `__repr__`. A good `__repr__` often looks like a constructor call, when practical.

### 9.5 Container behavior: `__len__()`, `__getitem__()`, `__setitem__()`, `__contains__()`

```python
class Bag:
    def __init__(self, items=()):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]  # supports integers and slices

    def __setitem__(self, index, value):
        self._items[index] = value

    def __contains__(self, value):
        return value in self._items

bag = Bag(["a", "b", "c"])
len(bag)          # 3
bag[0]            # 'a'
bag[1:]           # ['b', 'c']
"b" in bag        # True
bag[0] = "z"
bag[0]            # 'z'
```

Related methods: `__delitem__` enables `del bag[index]`; `__reversed__` customizes `reversed(bag)`; `__missing__` may be used by dict subclasses for absent keys.

### 9.6 Iteration: `__iter__()` and `__next__()`

An **iterable** supplies an iterator via `__iter__`; an **iterator** supplies successive values via `__next__` and raises `StopIteration` when exhausted.

```python
class Countdown:
    def __init__(self, start):
        self.remaining = start

    def __iter__(self):
        return self  # this instance is its own iterator

    def __next__(self):
        if self.remaining <= 0:
            raise StopIteration
        value = self.remaining
        self.remaining -= 1
        return value

list(Countdown(3))  # [3, 2, 1]

it = iter(Countdown(2))
next(it)  # 2
next(it)  # 1
# next(it) now raises StopIteration
```

Because `Countdown` is its own iterator, it is **consumed** when traversed. For a reusable iterable, `__iter__` can return a fresh iterator, for example `return iter(self._items)`. For simple custom iteration, a generator with `yield` is often easier than implementing `__next__` yourself.

### 9.7 Operators: `__add__()`, reflected methods, and in-place methods

```python
class Vector2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        if not isinstance(other, Vector2):
            return NotImplemented
        return Vector2(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

Vector2(1, 2) + Vector2(3, 4)  # Vector2(4, 6)
```

| Operator | Left-side | Reflected | In-place |
| --- | --- | --- | --- |
| `+` | `__add__` | `__radd__` | `__iadd__` (`+=`) |
| `-` | `__sub__` | `__rsub__` | `__isub__` (`-=`) |
| `*` | `__mul__` | `__rmul__` | `__imul__` (`*=`) |
| `/` | `__truediv__` | `__rtruediv__` | `__itruediv__` (`/=`) |
| `//` | `__floordiv__` | `__rfloordiv__` | `__ifloordiv__` (`//=`) |
| `**` | `__pow__` | `__rpow__` | `__ipow__` (`**=`) |

Return **`NotImplemented`** (not `NotImplementedError`) when an operand type isn't supported. Python can then try the other operand's reflected operation. If `__iadd__` is absent, `a += b` normally falls back to non-in-place addition and reassigns the result.

### 9.8 Equality, ordering, and hashing

| Operation | Special method |
| --- | --- |
| `a == b` / `a != b` | `__eq__` / `__ne__` |
| `a < b` / `a <= b` | `__lt__` / `__le__` |
| `a > b` / `a >= b` | `__gt__` / `__ge__` |
| `hash(a)` | `__hash__` |

```python
class Key:
    def __init__(self, code):
        self.code = code

    def __eq__(self, other):
        if not isinstance(other, Key):
            return NotImplemented
        return self.code == other.code

    def __hash__(self):
        return hash(self.code)

first = Key("A")
second = Key("A")
first == second             # True
len({first, second})        # 1
```

**Important:** overriding `__eq__` without supplying a suitable `__hash__` generally makes instances **unhashable**. Equal values must have equal hashes; values used as dictionary/set keys should not change their hash-relevant state. A frozen dataclass can often generate useful equality/hash behavior for value objects.

### 9.9 Attribute access: `__getattribute__()`, `__getattr__()`, `__setattr__()`

- `__getattribute__(self, name)` runs on **every ordinary attribute read**.
- `__getattr__(self, name)` is a **fallback** if normal lookup fails (typically an `AttributeError`).
- `__setattr__` and `__delattr__` customize writes and deletes.

```python
class Settings:
    def __init__(self):
        self.theme = "dark"

    def __getattr__(self, name):
        if name == "language":
            return "en"
        raise AttributeError(name)

settings = Settings()
settings.theme      # 'dark' (normal lookup)
settings.language   # 'en' (provided by __getattr__)
vars(settings)      # {'theme': 'dark'}
```

`language` is dynamic; it does **not** automatically appear in `vars(settings)`. If overriding `__getattribute__`, use `object.__getattribute__(self, name)` to delegate when appropriate; writing `self.name` inside it can accidentally cause infinite recursion.

### 9.10 Descriptors: `__get__()`, `__set__()`, `__set_name__()`

A **descriptor** is an attribute-management object stored on a class. Descriptors underpin Python's `property`, bound methods, and many ORM attributes.

```python
class Positive:
    def __set_name__(self, owner, name):
        self.storage_name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self  # access via the class
        return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError("Must be positive")
        instance.__dict__[self.storage_name] = value

class Product:
    price = Positive()

    def __init__(self, price):
        self.price = price

product = Product(12)
product.price = 15   # invokes Positive.__set__
product.price        # 15; invokes Positive.__get__
# product.price = -1  # raises ValueError
```

`__set_name__` is called during creation of the owning class, and tells a descriptor the attribute name it was assigned to. This connects descriptors directly to **metaclasses, class creation, and introspection**.

### 9.11 Context managers: `__enter__()` and `__exit__()`

These power `with` statements and are commonly used for files, locks, database transactions, and cleanup.

```python
class ManagedResource:
    def __enter__(self):
        print("Open")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Close")
        return False  # do not suppress any exception

with ManagedResource() as resource:
    print("Work")
# Open
# Work
# Close
```

`__exit__` runs when leaving the block, including when an exception is raised inside it. Returning a truthy value suppresses a pending exception; normally, return `False` or `None` unless suppression is deliberate.

### 9.12 Callable instances: `__call__()`

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, value):
        return self.factor * value

double = Multiplier(2)
double(5)        # 10
callable(double) # True
```

This is **instance** `__call__`. It's distinct from the **metaclass** `__call__` responsible for what happens when you write `Multiplier(2)` to create an instance.

### 9.13 Subclass customization and special-method lookup

`__init_subclass__` lets a base class react when a **subclass is declared**, without requiring a custom metaclass:

```python
class Plugin:
    registry = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.registry.append(cls.__name__)

class CsvPlugin(Plugin):
    pass

Plugin.registry  # ['CsvPlugin']
```

Implicit special-method lookup typically bypasses instance attributes:

```python
class Example:
    def __len__(self):
        return 2

example = Example()
example.__len__ = lambda: 99

example.__len__()  # 99: ordinary attribute lookup
len(example)       # 2: special lookup on type(example)
```

Don't confuse **special methods** (callable hooks like `__len__`) with **special attributes** (metadata like `__class__`, `__dict__`, `__mro__`, `__name__`, and `__bases__`). Some of those attributes can be absent on certain kinds of objects.

### 9.14 Quick selection guide

| If you want your object to... | Implement or inspect... |
| --- | --- |
| Be falsy when empty | `__len__` or `__bool__` |
| Print clearly | `__repr__`, optionally `__str__` |
| Support `[]` and `in` | `__getitem__`, `__contains__` |
| Work in `for` loops | `__iter__`, and `__next__` for iterators |
| Support arithmetic | `__add__` and related numeric methods |
| Behave as a dictionary key | `__eq__` and a consistent `__hash__` |
| Provide virtual attributes | `__getattr__` |
| Validate attributes on assignment | `property` or descriptor `__set__` |
| Clean up after a `with` block | `__enter__`, `__exit__` |
| Behave like a function | `__call__` |
| Register new subclasses | `__init_subclass__` |
| Customize class object construction | Metaclass `__new__` (or other metaclass hooks) |

**Rule of thumb:** implement special methods only when the corresponding **built-in Python operation** has a clear meaning for your class. Prefer normal methods when a behavior is domain-specific rather than a natural operator or protocol.

---

## 10. Five ideas to remember

1. **A class is an object.** `User` is an instance of its metaclass, generally `type`.
2. **Inheritance and metaclass relationships are different.** `User` inherits from `BaseModel` but is an instance of `TableMeta`.
3. **A metaclass receives the class definition before the class object exists.** `name`, `bases`, and `namespace` describe what Python is building.
4. **`vars()` reveals direct stored attributes; `dir()` advertises available names; `inspect` performs richer inspection.** These tools are complementary, not interchangeable.
5. **Use a metaclass only when you need to change class creation.** For simpler subclass registration or validation, consider `__init_subclass__()` or a class decorator.

### Mini practice exercises

```python
# Predict each result before running it.
type(User)
User.__bases__
User.__mro__
vars(user)
inspect.isfunction(User.greet)
inspect.ismethod(user.greet)
inspect.ismethod(User.get_category)
inspect.signature(User)
inspect.signature(user.greet)
```

*End of notes.*
