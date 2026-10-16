# Python Metaclasses & Introspection

*A practical reference for `object`, `type`, metaclasses, inheritance, class metadata, and the `inspect` module.*

## 1. The big picture: instance → class → metaclass

In Python, **classes are themselves objects**.

```text
user = User(1, "Alice")  ── instance of ──► User  ── instance of ──► TableMeta
                                                   (class)          (metaclass)
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

## 9. Five ideas to remember

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
