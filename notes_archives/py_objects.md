# Python Object Model, Metaclasses & Introspection

*An extensive reference to Python object identity, classes, metaclasses, inheritance, attribute lookup, introspection, special methods, object lifetime, and object-oriented interfaces.*

## Table of Contents

- [1. The big picture: instance → class → metaclass](#1-the-big-picture-instance--class--metaclass)
  - [`object` versus `type`](#object-versus-type)
  - [What about `int`, `str`, and `list`?](#what-about-int-str-and-list)
  - [Object identity, references, and mutability](#object-identity-references-and-mutability)
- [2. Creating classes with a metaclass](#2-creating-classes-with-a-metaclass)
  - [Meaning of the four arguments](#meaning-of-the-four-arguments)
  - [Which line creates `table_name`?](#which-line-creates-table_name)
  - [Creation sequence](#creation-sequence)
  - [Complete class creation lifecycle](#complete-class-creation-lifecycle)
- [3. One complete example: parent class + metaclass](#3-one-complete-example-parent-class--metaclass)
  - [An explicit override is possible](#an-explicit-override-is-possible)
  - [Metaclass conflicts](#metaclass-conflicts)
  - [Class attributes versus instance attributes](#class-attributes-versus-instance-attributes)
  - [`super()` and cooperative multiple inheritance](#super-and-cooperative-multiple-inheritance)
- [4. Inspecting a class versus inspecting an instance](#4-inspecting-a-class-versus-inspecting-an-instance)
  - [Quick reference](#quick-reference)
  - [`vars()` and `__dict__`: direct attributes](#vars-and-__dict__-direct-attributes)
  - [`dir()`: discover available names](#dir-discover-available-names)
  - [Useful special class attributes](#useful-special-class-attributes)
  - [Attribute lookup: the complete resolution order](#attribute-lookup-the-complete-resolution-order)
  - [Method binding: functions, methods, `self`, and `cls`](#method-binding-functions-methods-self-and-cls)
  - [`__slots__` and object storage](#__slots__-and-object-storage)
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
- [10. Object lifecycle, reference counting, and garbage collection](#10-object-lifecycle-reference-counting-and-garbage-collection)
  - [10.1 Reference ownership and reachability](#101-reference-ownership-and-reachability)
  - [10.2 CPython reference counting and cycles](#102-cpython-reference-counting-and-cycles)
  - [10.3 Weak references and weak containers](#103-weak-references-and-weak-containers)
  - [10.4 Finalizers, `__del__`, and deterministic cleanup](#104-finalizers-__del__-and-deterministic-cleanup)
- [11. Abstract Base Classes (ABCs)](#11-abstract-base-classes-abcs)
  - [11.1 `ABC`, `ABCMeta`, and `@abstractmethod`](#111-abc-abcmeta-and-abstractmethod)
  - [11.2 Abstract properties and class methods](#112-abstract-properties-and-class-methods)
  - [11.3 Abstract methods may still have implementations](#113-abstract-methods-may-still-have-implementations)
  - [11.4 Virtual subclasses and what they do not provide](#114-virtual-subclasses-and-what-they-do-not-provide)
  - [11.5 Inspecting an ABC and choosing the abstraction](#115-inspecting-an-abc-and-choosing-the-abstraction)
- [12. Protocols and structural typing](#12-protocols-and-structural-typing)
  - [12.1 Nominal versus structural contracts](#121-nominal-versus-structural-contracts)
  - [12.2 Protocols can include attributes and multiple methods](#122-protocols-can-include-attributes-and-multiple-methods)
  - [12.3 `@runtime_checkable`: limited runtime inspection](#123-runtime_checkable-limited-runtime-inspection)
  - [12.4 Protocols versus ABCs](#124-protocols-versus-abcs)
- [13. Class decorators versus metaclasses](#13-class-decorators-versus-metaclasses)
  - [13.1 Class decorator: transform an already-created class](#131-class-decorator-transform-an-already-created-class)
  - [13.2 `__init_subclass__`: automatically configure descendants](#132-__init_subclass__-automatically-configure-descendants)
  - [13.3 Metaclass: customize the actual construction mechanism](#133-metaclass-customize-the-actual-construction-mechanism)
  - [13.4 Comparison and selection guide](#134-comparison-and-selection-guide)
- [14. Dynamic class creation](#14-dynamic-class-creation)
  - [14.1 The three-argument form of `type()`](#141-the-three-argument-form-of-type)
  - [14.2 Use the metaclass explicitly when appropriate](#142-use-the-metaclass-explicitly-when-appropriate)
  - [14.3 `types.new_class()` and namespace initialization](#143-typesnew_class-and-namespace-initialization)
  - [14.4 Dynamic subclasses and factories](#144-dynamic-subclasses-and-factories)
- [15. Five ideas to remember](#15-five-ideas-to-remember)
  - [Additional concepts at a glance](#additional-concepts-at-a-glance)
  - [Python documentation references](#python-documentation-references)

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


### Object identity, references, and mutability

Every Python object has three fundamental characteristics:

| Characteristic | Meaning | Typical observation |
| --- | --- | --- |
| **Identity** | Which particular object this is | `id(obj)`, `a is b` |
| **Type** | Which operations the object supports | `type(obj)`, `isinstance(obj, cls)` |
| **Value/state** | Data represented or stored by the object | `obj == other`, object attributes |

Variables in Python are **names bound to objects**, not boxes into which objects are copied. Assignment generally creates or changes a binding; it does not clone the object.

```python
first = [1, 2]
second = first
third = [1, 2]

first is second
first is third
first == third

second.append(3)
first
third
```

Expected results, in order: `True`, `False`, `True`, then `[1, 2, 3]` and `[1, 2]`. `first` and `second` name the same list, whereas `third` names an equal but distinct list.

**Identity versus equality:** `is` and `is not` compare object identity; `==` delegates to equality behavior (usually `__eq__`). Prefer `x is None` rather than `x == None`. Avoid relying on whether separately constructed integers or strings happen to have the same identity: interning and implementation optimizations can affect the answer.

#### Mutability belongs to the object, not the variable

- Mutable objects, such as lists, dictionaries, and most ordinary class instances, can change their internal state while retaining their identity.
- Immutable objects, such as integers, strings, and tuples, cannot change their value *in place*. Rebinding a name is still possible.
- An immutable container may refer to mutable objects. A tuple containing a list cannot change its tuple entries, but the contained list can change.

```python
number = 10
before = number
number += 1

number == before
number is before

record = ([1, 2], "active")
record[0].append(3)
record
```

The comparisons are `False` and `False`; the tuple is now `([1, 2, 3], 'active')`. The tuple's reference to the list is unchanged, although the list contents changed.

#### Passing references to functions

Python uses **call by sharing** (also described as passing object references by assignment). A function receives a local name bound to the same object; mutation is visible outside, but rebinding the parameter does not rebind the caller's name.

```python
def mutate(items):
    items.append("added")


def rebind(items):
    items = ["replacement"]
    return items


values = ["original"]
mutate(values)
new_values = rebind(values)

values
new_values
```

`values` is `['original', 'added']`; `new_values` is `['replacement']`. This distinction matters for methods that modify a DataFrame, a configuration dictionary, or a mutable object passed through a processing pipeline.

#### `id()`, identity, and lifetime

`id(obj)` returns an integer unique among **simultaneously existing objects**. In CPython it is typically related to a memory address, but that is an implementation detail; an ID may be reused after an object is destroyed. `id()` is useful for debugging aliasing, not for permanent IDs, database keys, or serialization.

**Related sections:** equality and hashing in Section 9.8; object cleanup and weak references in Section 10.

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


### Complete class creation lifecycle

The simplified creation sequence above is useful, but Python exposes additional hooks. The full conceptual sequence for a normal `class` statement is:

1. Evaluate decorators and the class header; resolve non-type bases through `__mro_entries__` where applicable.
2. Determine the most-derived compatible metaclass from explicit and inherited metaclasses.
3. Ask the metaclass for the class namespace through `__prepare__` (if defined).
4. Execute the class body in that namespace: assignments create names, and `def` creates function objects.
5. Invoke the metaclass to construct the class object; typically its `__call__` runs metaclass `__new__` and `__init__`.
6. During `type.__new__`, call `__set_name__(owner, name)` on descriptors defined in the new class namespace, then the immediate parent's `__init_subclass__` hook.
7. Apply class decorators from the **bottom up**; bind the resulting object to the class name.
8. Later, when you invoke the completed class (`Class(...)`), the metaclass's `__call__` generally runs instance `__new__` followed by `__init__`.

The details of steps 5–6 assume a metaclass that delegates class construction to `type.__new__`. A metaclass that replaces the usual machinery may behave differently.

#### Trace the hooks in their actual order

```python
events = []


class TraceMeta(type):
    @classmethod
    def __prepare__(mcls, name, bases, **kwargs):
        events.append("prepare")
        return {}

    def __new__(mcls, name, bases, namespace, **kwargs):
        events.append("metaclass new: before")
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        events.append("metaclass new: after")
        return cls

    def __init__(cls, name, bases, namespace, **kwargs):
        events.append("metaclass init")
        super().__init__(name, bases, namespace)


class Root(metaclass=TraceMeta):
    def __init_subclass__(cls, **kwargs):
        events.append("init_subclass")
        super().__init_subclass__(**kwargs)


events.clear()


class Field:
    def __set_name__(self, owner, name):
        events.append("set_name")


def register(cls):
    events.append("decorator")
    return cls


@register
class Record(Root):
    events.append("class body")
    field = Field()


events
```

Expected sequence:

```text
['prepare', 'class body', 'metaclass new: before',
 'set_name', 'init_subclass', 'metaclass new: after',
 'metaclass init', 'decorator']
```

**What each hook can do:**

| Hook | Receives or observes | Typical use |
| --- | --- | --- |
| `Meta.__prepare__` | Class name, bases, class keywords | Supply the namespace mapping used by the class body |
| `Meta.__new__` | Name, bases, populated namespace | Validate or transform the class before returning it |
| Descriptor `__set_name__` | Constructed owner class and assigned field name | Set descriptor storage names |
| `Base.__init_subclass__` | Newly created subclass and class keywords | Lightweight subclass configuration or registration |
| `Meta.__init__` | Constructed class | Final class initialization |
| `@class_decorator` | Constructed class object | Register, mutate, or replace the class |
| `Meta.__call__` | Calls to the completed class | Control creation of *instances* of that class |

#### Important subtleties

- `__prepare__` must return a mapping, usually a dictionary. Ordered dictionaries are no longer necessary merely to preserve ordinary class-definition order because modern dictionaries preserve insertion order.
- `__init_subclass__` runs **as part of `type.__new__`**, before a custom metaclass's `__new__` has returned. It is not the same hook as metaclass `__init__`.
- `__set_name__` is automatically called for descriptors present during class creation. Assigning a descriptor to a class *later* does not automatically call that hook.
- Metaclass keywords can be forwarded through class creation and `__init_subclass__`; a custom metaclass must deliberately manage those keyword arguments.
- When implementing a custom metaclass `__new__`, preserve the compiler-generated `__classcell__` in the namespace passed to `type.__new__`. Zero-argument `super()` relies on this mechanism.
- Multiple inheritance and metaclass conflicts are discussed in Section 3; class decorators versus metaclasses are compared in Section 13.

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


### Class attributes versus instance attributes

The class namespace (`Class.__dict__`) and each normal instance namespace (`instance.__dict__`) are distinct. Attribute access can *find* class attributes through inheritance without copying those attributes into each instance.

```python
class Connection:
    timeout = 30

    def __init__(self, name):
        self.name = name


first = Connection("primary")
second = Connection("replica")

first.timeout
vars(first)
Connection.__dict__["timeout"]
```

Results: `30`, `{'name': 'primary'}`, and `30`. `timeout` is not initially stored on either instance.

#### Instance shadowing and class rebinding

```python
first.timeout = 60

first.timeout
second.timeout
Connection.timeout
vars(first)

Connection.timeout = 45
second.timeout
first.timeout
```

Results: `60`, `30`, `30`, `{'name': 'primary', 'timeout': 60}`, then `45` and `60`. For a normal class attribute, assigning `first.timeout` creates/shadows the name in `first` rather than changing `Connection.timeout`. The shadowed value is unaffected by a later class-level rebinding.

#### Shared mutable class attributes: a common bug

```python
class Registry:
    entries = []

    def add(self, value):
        self.entries.append(value)


left = Registry()
right = Registry()
left.add("A")
right.entries
```

The final result is `['A']`: both instances access the same mutable class list. If per-instance state is desired, create it in `__init__` instead:

```python
class Registry:
    def __init__(self):
        self.entries = []

    def add(self, value):
        self.entries.append(value)
```

#### Incrementing class-level counters deliberately

```python
class Task:
    created = 0

    def __init__(self):
        type(self).created += 1


Task()
Task()
Task.created
```

The result is `2`. Contrast this with `self.created += 1`, which typically reads the class attribute and then **writes a separate instance attribute**. Also note that `type(self).created += 1` can create a counter on a subclass rather than update the base class; choose `Task.created += 1` when the counter must be shared across the entire inheritance tree.

#### Methods and data are both class attributes

`def` inside a class body assigns a function object to the class namespace. An instance's access to this function triggers **method binding** (see below), while a simple integer or string class attribute is just returned. This is why ordinary instance methods need not be copied into every instance.

### `super()` and cooperative multiple inheritance

`super()` is a **dynamic lookup proxy**, not a synonym for “call my direct parent.” In an instance method, zero-argument `super()` effectively carries the class where the method was defined and the current instance. Lookup continues **after that class in the instance's MRO**.

#### The diamond hierarchy

```text
       Root
      /    \
    Left  Right
      \    /
       Child
```

```python
class Root:
    def trace(self):
        return ["Root"]


class Left(Root):
    def trace(self):
        return ["Left", *super().trace()]


class Right(Root):
    def trace(self):
        return ["Right", *super().trace()]


class Child(Left, Right):
    def trace(self):
        return ["Child", *super().trace()]


Child.__mro__
Child().trace()
```

Results:

```text
(Child, Left, Right, Root, object)
['Child', 'Left', 'Right', 'Root']
```

Even though `Left` directly inherits from `Root`, `super()` **inside `Left.trace`** proceeds to `Right.trace` when operating on a `Child` instance. This is the key to cooperative multiple inheritance and the C3 linearization algorithm.

#### `super()` in constructors

```python
class DatabaseMixin:
    def __init__(self, **kwargs):
        self.database_ready = True
        super().__init__(**kwargs)


class LoggingMixin:
    def __init__(self, **kwargs):
        self.logging_ready = True
        super().__init__(**kwargs)


class Service(DatabaseMixin, LoggingMixin):
    def __init__(self):
        super().__init__()


service = Service()
service.database_ready, service.logging_ready
Service.__mro__
```

Both flags are `True`, because each participant forwards construction to the **next method in the MRO**. The rightmost terminal `object.__init__()` must not receive unexpected arguments; cooperative hierarchies typically consume their own keyword arguments and forward the remainder.

#### Key rules for multiple inheritance

- **C3 linearization** preserves local base ordering and respects the ordering inherited from each parent. Inconsistent bases produce a `TypeError` when defining a class.
- Every participating override should normally call `super()` exactly once, and signatures should be designed to cooperate. A parent that omits `super()` can terminate the chain early.
- `super(CurrentClass, obj)` is the explicit proxy form; `super()` without arguments is intended for normal methods defined in the class body.
- An explicit `Parent.method(self)` bypasses cooperative lookup and can lead to duplicated or missing calls in a diamond hierarchy.
- `super()` also works in many class methods. Both it and ordinary method binding are implemented through descriptor-aware attribute lookup.

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


### Attribute lookup: the complete resolution order

For a **normal instance** whose class uses the usual `object.__getattribute__` implementation, reading `instance.name` roughly follows the precedence below. Python first searches the class's MRO for a candidate class attribute or descriptor; the outcome depends on the type of that candidate.

```text
instance.name
    │
    ├─ Data descriptor in class/MRO? ──────────────► call __get__
    │
    ├─ Instance's __dict__ has name? ─────────────► return stored value
    │
    ├─ Non-data descriptor in class/MRO? ─────────► call __get__
    │
    ├─ Ordinary class/MRO attribute? ─────────────► return class value
    │
    └─ No attribute resolved? ─────────────────────► __getattr__ fallback
```

This represents Python's **default** lookup behavior, not an unchangeable rule for classes overriding `__getattribute__` or for all extension types. A `__getattribute__` implementation that raises `AttributeError` can also cause `__getattr__` to run.

| Candidate | Defines | Relative precedence |
| --- | --- | --- |
| Data descriptor | `__get__` and `__set__` or `__delete__` | Above instance dictionary |
| Instance attribute | Entry in `instance.__dict__` | Above non-data descriptors and normal class attributes |
| Non-data descriptor | `__get__` but no `__set__`/`__delete__` | Below instance dictionary |
| Ordinary class attribute | Class or inherited namespace entry | Below instance dictionary |
| `__getattr__` | Fallback on failed regular lookup | Last resort |

#### Data descriptors beat instance attributes

Properties commonly act as data descriptors, even if they have no setter:

```python
class Profile:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name.upper()


profile = Profile("alice")
profile.__dict__["name"] = "shadow"

profile.name
vars(profile)
```

`profile.name` returns `'ALICE'` even though `vars(profile)` includes `'name': 'shadow'`: the class property takes precedence over the instance dictionary. Assigning `profile.name = ...` through ordinary attribute assignment would instead raise an `AttributeError` because no property setter exists.

#### Normal methods are non-data descriptors

```python
class Greeter:
    def greet(self):
        return "original"


greeter = Greeter()
greeter.greet()
greeter.__dict__["greet"] = lambda: "overridden"
greeter.greet()
Greeter.greet(greeter)
```

Results: `'original'`, `'overridden'`, `'original'`. A function stored on a class supports binding through `__get__` but is a non-data descriptor; an instance attribute of the same name can hide it.

#### Class lookup is not instance lookup

`Class.name` invokes class-object attribute lookup (normally `type.__getattribute__`), which is different from `instance.name` (normally `object.__getattribute__`). Class lookup consults both the class's own MRO and its metaclass's attributes/descriptors. For instance, a **metaclass property** can take precedence over an attribute in the class namespace.

```python
class Meta(type):
    @property
    def label(cls):
        return "from metaclass"


class Report(metaclass=Meta):
    label = "from class"


Report.label
vars(Report)["label"]
```

The first result is `'from metaclass'`; the second is `'from class'`. The distinction matters when debugging custom metaclasses.

#### Introspection without invoking the attribute

```python
import inspect

inspect.getattr_static(profile, "name")
getattr(profile, "name")
```

The first returns the **property descriptor itself**; the second returns `'ALICE'`. See Section 5.9 and Section 9.10 for further descriptor-related tools and methods.

### Method binding: functions, methods, `self`, and `cls`

An ordinary function defined in a class becomes a **bound method** when accessed through an instance. The binding process uses the function object's descriptor protocol; it is not a special transformation of the source code when the function is defined.

```python
class Account:
    def deposit(self, amount):
        return amount * 2


account = Account()
raw_function = Account.__dict__["deposit"]
bound_method = account.deposit

raw_function is Account.deposit
bound_method.__self__ is account
bound_method.__func__ is raw_function
bound_method(5)
Account.deposit(account, 5)
```

Results: `True`, `True`, `True`, `10`, `10`. Access through the instance supplies `self` automatically; retrieving `Account.deposit` from the class does **not** bind a particular account instance.

#### Explicit descriptor binding

```python
manual = Account.__dict__["deposit"].__get__(account, Account)
manual.__self__ is account
manual(5)
```

Results: `True` and `10`. This illustrates why `instance.method(x)` and `Class.method(instance, x)` commonly have the same effect.

| Definition | Accessed as | What is bound? | Typical inspection |
| --- | --- | --- | --- |
| Ordinary `def f(self, ...)` | `obj.f` | Instance (`self`) | `obj.f.__self__ is obj` |
| Ordinary `def f(self, ...)` | `Class.f` | Nothing | Function object |
| `@classmethod def f(cls, ...)` | `obj.f` or `Class.f` | Class (`cls`) | `Class.f.__self__ is Class` |
| `@staticmethod def f(...)` | `obj.f` or `Class.f` | Nothing | Function object |
| `@property def f(self)` | `obj.f` | No bound method returned; descriptor **evaluates** getter | Getter result |

#### Class methods versus static methods

```python
class Parser:
    kind = "base"

    @classmethod
    def describe(cls):
        return cls.kind

    @staticmethod
    def normalize(value):
        return value.strip().lower()


class JsonParser(Parser):
    kind = "json"


Parser.describe()
JsonParser.describe()
JsonParser.describe.__self__ is JsonParser
JsonParser.normalize("  DATA  ")
```

Results: `'base'`, `'json'`, `True`, and `'data'`. A class method naturally follows subclasses through `cls`, while a static method is merely a function namespaced on the class. Neither decorator is required just because code appears inside a class: choose based on whether the implementation needs instance state or the class object.

**Identity of bound methods:** repeated access to `account.deposit` may create different temporary bound-method objects, even though they bind the same instance and function. Inspect `__self__` and `__func__` instead of assuming `account.deposit is account.deposit`.

### `__slots__` and object storage

Ordinary Python instances typically store writable attributes in an instance dictionary. Declaring `__slots__` asks Python to create a fixed set of storage descriptors, often reducing the memory footprint when many instances have the same fields.

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


point = Point(2, 3)
point.x
hasattr(point, "__dict__")
```

Results: `2` and `False`. Assigning `point.z = 4` raises `AttributeError`, unless a parent class grants a `__dict__`.

#### Slots are descriptors, not a frozen-object feature

```python
Point.__dict__["x"]
point.x = 8
point.x
```

The first expression returns a slot descriptor; the later result is `8`. Slots restrict **which fields** may be stored, not whether an existing field is mutable. They do not create immutability, enforce types, or automatically validate values.

#### `__dict__` and weak-reference support

```python
class FlexiblePoint:
    __slots__ = ("x", "y", "__dict__", "__weakref__")

    def __init__(self, x, y):
        self.x = x
        self.y = y


flexible = FlexiblePoint(1, 2)
flexible.label = "origin"
vars(flexible)
```

`vars(flexible)` contains `{'label': 'origin'}`; the slotted `x` and `y` values are stored outside that instance dictionary. The `__weakref__` slot allows instances of this simple slotted class to be targets of `weakref.ref()`.

#### Inheritance rules and pitfalls

- A subclass of a slotted class that **omits** `__slots__` normally gains an instance dictionary again. Declare `__slots__ = ()` on the subclass when you want to preserve the slotted layout without adding new slots.
- If any base already provides `__dict__` or weak-reference support, declaring slots in a subclass does not remove those capabilities.
- Multiple inheritance among classes with nonempty slot layouts is restricted and can raise `TypeError` due to layout conflicts.
- Do not redeclare the same slot name already used by an ancestor; this can make the ancestor's slot inaccessible through ordinary lookup.
- Avoid using a class attribute to provide a default value under the **same name** as a slot: it conflicts with the descriptor generated for that name.
- `sys.getsizeof(obj)` measures only the object's shallow size. To compare memory use fairly, account for separate instance dictionaries and any referenced data.

**Selection:** use `__slots__` when instances are numerous and have predictable fields, after measuring benefit; prefer ordinary dictionaries when flexible attributes, framework integrations, or simpler debugging matter more.

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

## 10. Object lifecycle, reference counting, and garbage collection

The lifetime of an ordinary object runs from **allocation and initialization**, through a period of reachable use, to eventual finalization and memory reclamation. The `__new__`/`__init__` construction hooks are covered in Section 9.2; this section concerns what happens **after** an object is created.

### 10.1 Reference ownership and reachability

Names, containers, instance attributes, and some interpreter internals may all hold references to the same object. Deleting one name does **not** necessarily destroy that object if other references remain.

```python
class Item:
    pass


item = Item()
alias = item
original_id = id(item)
del item

id(alias) == original_id
```

The result is `True`: removing the binding `item` does not remove `alias`. Conversely, `del alias` removes a binding, not an object through a dedicated object-destruction operator.

### 10.2 CPython reference counting and cycles

CPython ordinarily reclaims many objects promptly when their reference count drops to zero. Cycles need an additional cyclic garbage collector because objects in a cycle can still reference one another after external references disappear.

```python
import gc
import weakref


class Node:
    pass


left = Node()
right = Node()
left.next = right
right.next = left
left_ref = weakref.ref(left)
right_ref = weakref.ref(right)

del left, right
gc.collect()

left_ref() is None, right_ref() is None
```

Normally both results are `True` on CPython after collection, provided nothing else retains the objects. The example illustrates a collectable reference cycle; collector behavior and timing can vary by Python implementation and object type.

| API | Purpose | Important qualification |
| --- | --- | --- |
| `sys.getrefcount(obj)` | Inspect an approximate CPython reference count | The call itself holds a temporary reference; CPython-specific |
| `gc.collect()` | Request garbage collection | Does not free objects that are still reachable |
| `gc.get_stats()` | Get collector statistics | Implementation and version details can vary |
| `gc.is_tracked(obj)` | Ask whether an object participates in cyclic GC | Some immutable/container objects are untracked |
| `weakref.ref(obj)` | Create a reference that does not keep the object alive | Target must support weak references |

**Important distinction:** Python's language semantics do not guarantee precisely when memory is reclaimed. Never rely on timely garbage collection as the primary way to close a file, release a lock, or commit/rollback a database transaction.

### 10.3 Weak references and weak containers

A **weak reference** lets you observe an object without prolonging its lifetime. Calling it returns the object if still alive, or `None` after it has been collected.

```python
import weakref


class CacheEntry:
    pass


entry = CacheEntry()
observer = weakref.ref(entry)
observer() is entry

del entry
observer() is None
```

On CPython, the final expression is ordinarily `True` because no strong references remain. Do not retain the result of `observer()` somewhere else if you intend the object to be collectable.

`weakref.WeakValueDictionary` is useful when you want cached values to disappear automatically after no other strong references remain. `weakref.WeakKeyDictionary` is useful for supplemental per-object metadata without keeping those keys alive. For slotted user classes, include `__weakref__` when necessary (Section 4).

### 10.4 Finalizers, `__del__`, and deterministic cleanup

`__del__` is a finalization hook, **not** the inverse of `__init__`. The interpreter may call it when an object is finalized, but its precise timing is not dependable; exceptions raised in it are ignored with a warning, and shutdown can complicate access to module globals.

```python
from contextlib import contextmanager


@contextmanager
def managed_resource():
    resource = open("sample.txt", "w")
    try:
        yield resource
    finally:
        resource.close()


with managed_resource() as handle:
    handle.write("ready")
```

The `with` statement guarantees normal block-exit cleanup (including exceptions within the block) independently of garbage-collection timing. Prefer built-in context managers, `try`/`finally`, or `contextlib` for resources. `weakref.finalize` can provide a fallback cleanup callback without writing `__del__`, but it is not a substitute for explicit resource management.

---

## 11. Abstract Base Classes (ABCs)

An **abstract base class** defines a nominal interface and can prevent instantiation until required abstract members have concrete implementations. It is appropriate when subclasses are intentionally part of the same inheritance family and must conform to a shared contract.

### 11.1 `ABC`, `ABCMeta`, and `@abstractmethod`

```python
from abc import ABC, abstractmethod


class Calculator(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float:
        raise NotImplementedError


class TaxCalculator(Calculator):
    def __init__(self, rate: float):
        self.rate = rate

    def calculate(self, amount: float) -> float:
        return amount * self.rate


calc = TaxCalculator(0.13)
calc.calculate(100)
```

The result is `13.0`. `Calculator()` raises `TypeError` because `calculate` is abstract; `TaxCalculator` is concrete because it supplies an implementation.

`ABC` is a helper class that uses `ABCMeta`. You can use `metaclass=ABCMeta` directly, but `ABC` is usually clearer. Decorating a method with `@abstractmethod` sets its abstract status; `ABCMeta` enforces that status at instantiation.

### 11.2 Abstract properties and class methods

```python
from abc import ABC, abstractmethod


class DataSource(ABC):
    @property
    @abstractmethod
    def source_name(self) -> str:
        ...

    @classmethod
    @abstractmethod
    def connect(cls):
        ...


class LocalSource(DataSource):
    @property
    def source_name(self) -> str:
        return "local"

    @classmethod
    def connect(cls):
        return cls()


LocalSource.connect().source_name
```

The result is `'local'`. When stacking decorators, `@abstractmethod` should normally be **innermost** for `@property`, `@classmethod`, and `@staticmethod` combinations.

### 11.3 Abstract methods may still have implementations

Unlike an empty interface declaration in some languages, an abstract method may contain useful code; subclasses may call it with `super()` while still being required to override it.

```python
class Processor(ABC):
    @abstractmethod
    def calculate(self, value):
        return value * 2


class FinalProcessor(Processor):
    def calculate(self, value):
        return super().calculate(value) + 1


FinalProcessor().calculate(3)
```

The result is `7`.

### 11.4 Virtual subclasses and what they do not provide

An ABC can register an unrelated class as a **virtual subclass** for `isinstance`/`issubclass` checks:

```python
from abc import ABC


class Repository(ABC):
    pass


class MemoryStore:
    pass


Repository.register(MemoryStore)
issubclass(MemoryStore, Repository)
isinstance(MemoryStore(), Repository)
```

Both checks are `True`, but **registration does not alter `MemoryStore.__mro__`, inject methods, or enforce abstract-method implementation**. It grants recognition in runtime subtype checks, not inherited implementation.

For standard collection interfaces, examine `collections.abc` (`Iterable`, `Mapping`, `Sequence`, etc.) before defining a custom ABC.

### 11.5 Inspecting an ABC and choosing the abstraction

```python
import inspect

inspect.isabstract(Calculator)
Calculator.__abstractmethods__
```

The first result is `True`; the second is a frozenset containing `'calculate'`.

| Choose | When |
| --- | --- |
| Plain base class | Sharing behavior without mandatory abstract members |
| `ABC` and `@abstractmethod` | Requiring implementations from a known subclass family |
| `Protocol` (Section 12) | Specifying the operations an object must support without requiring inheritance |
| `__init_subclass__` | Validating or configuring new subclasses at definition time |

**Metaclass caution:** `ABCMeta` is itself a metaclass. Combining an ABC with a second unrelated custom metaclass may require a compatible combined metaclass (see Section 3).

---

## 12. Protocols and structural typing

A **protocol** describes the structure or behavior an object must provide. Unlike nominal inheritance, **structural subtyping** does not require classes to inherit from the interface explicitly. This formalizes the practical Python idea of **duck typing**.

### 12.1 Nominal versus structural contracts

```python
from typing import Protocol


class Calculates(Protocol):
    def calculate(self, amount: float) -> float:
        ...


class RateModel:
    def __init__(self, rate: float):
        self.rate = rate

    def calculate(self, amount: float) -> float:
        return amount * self.rate


def evaluate(model: Calculates, amount: float) -> float:
    return model.calculate(amount)


evaluate(RateModel(0.2), 100)
```

The result is `20.0`. A static type checker can accept `RateModel` as a `Calculates` implementation even though `RateModel` does not inherit from `Calculates`. Type annotations are not, by themselves, runtime argument validation.

### 12.2 Protocols can include attributes and multiple methods

```python
from typing import Protocol


class NamedLoader(Protocol):
    source: str

    def load(self) -> list[int]:
        ...


class CsvLoader:
    source = "csv"

    def load(self) -> list[int]:
        return [1, 2, 3]


def describe(loader: NamedLoader) -> tuple[str, int]:
    return loader.source, len(loader.load())


describe(CsvLoader())
```

The result is `('csv', 3)`. The annotated protocol attribute `source` is part of the structural requirement, not an attribute automatically created on implementing classes.

### 12.3 `@runtime_checkable`: limited runtime inspection

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsSave(Protocol):
    def save(self) -> None:
        ...


class Record:
    def save(self) -> str:
        return "done"


isinstance(Record(), SupportsSave)
```

This returns `True`: runtime protocol checking only looks for required members; it **does not validate signatures, return annotations, or the semantics of those members**. A static type checker should reject `Record` as an implementation of `SupportsSave` because its `save` return type is incompatible.

Additional caveats:

- Protocols without `@runtime_checkable` generally cannot be used as runtime `isinstance`/`issubclass` targets.
- Runtime-checkable protocol checks can be slower than ordinary class checks; structural checks also have restrictions, particularly for protocols with data members and `issubclass`.
- In Python 3.12 and later, runtime protocol member lookup uses static attribute inspection; dynamically generated attributes may not be treated like ordinary accessed attributes.
- Do not use `@runtime_checkable` as a substitute for detailed validation or a static type checker.

### 12.4 Protocols versus ABCs

| Dimension | ABC | Protocol |
| --- | --- | --- |
| Primary relationship | Nominal inheritance | Structural compatibility |
| Explicit inheritance required for normal use | Yes | No |
| Prevents instantiating incomplete implementations | Yes (for concrete subclasses) | Not for independent classes that happen to match structurally |
| Supports shared implementations | Yes | May define implementations for explicit subclasses, but normally describes a contract |
| Type-checker support | Yes | Yes |
| Runtime membership checks | Built in | Opt-in with `@runtime_checkable`, limited |
| Best fit | Framework-owned class hierarchy | Pluggable libraries, dependency injection, loose coupling |

**Architecture example:** annotate a calculation pipeline's dependency as a protocol such as `DataLoader` or `Calculator` if it only needs `load()` or `calculate()`; use an ABC if you also need shared state, implementations, and enforced construction rules across your own hierarchy.

---

## 13. Class decorators versus metaclasses

Both class decorators and metaclasses can customize a class, but they operate at different points of class construction and expose different mechanisms.

### 13.1 Class decorator: transform an already-created class

```python
REGISTRY = {}


def register(cls):
    REGISTRY[cls.__name__] = cls
    return cls


@register
class CsvHandler:
    def process(self):
        return "csv"


REGISTRY["CsvHandler"] is CsvHandler
```

The result is `True`. `register` receives the completed class and stores it in a registry. A class decorator may also add attributes or return a **replacement object**, so it need not return the original class.

This is analogous to writing:

```python
class JsonHandler:
    pass


JsonHandler = register(JsonHandler)
```

Decorators on a class are applied bottom-to-top, just as multiple function decorators are:

```python
@outer
@inner
class Example:
    pass
```

This is conceptually `Example = outer(inner(Example))`, assuming the decorators are already defined.

### 13.2 `__init_subclass__`: automatically configure descendants

```python
class BaseHandler:
    handlers = {}

    def __init_subclass__(cls, *, kind, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseHandler.handlers[kind] = cls


class XmlHandler(BaseHandler, kind="xml"):
    pass


BaseHandler.handlers["xml"] is XmlHandler
```

The result is `True`. Unlike a decorator, the inherited `__init_subclass__` mechanism can respond automatically to each newly defined subclass, and it runs during class construction rather than afterward.

### 13.3 Metaclass: customize the actual construction mechanism

```python
class NamingMeta(type):
    def __new__(mcls, name, bases, namespace):
        if name != "Base" and not name.endswith("Service"):
            raise TypeError("Concrete service classes must end in Service")
        return super().__new__(mcls, name, bases, namespace)


class Base(metaclass=NamingMeta):
    pass


class EmailService(Base):
    pass
```

The metaclass checks and can reject the class before construction completes. This supports advanced behaviors that post-creation decorators cannot implement as naturally, such as supplying a custom namespace via `__prepare__` or integrating a family of classes under the same class-creation policy.

### 13.4 Comparison and selection guide

| Mechanism | Timing | Applies to subclasses automatically? | Best use |
| --- | --- | --- | --- |
| Class decorator | After class object creation | No, normally must decorate each class | Register or transform specific classes |
| `__init_subclass__` | During creation of a new subclass | Yes, via inheritance | Validate, configure, or register descendants |
| Custom metaclass | Before/during class object creation | Usually inherited through metaclass selection | Alter namespace preparation or class construction |

**Recommended escalation:** ordinary class or instance methods → class decorator → `__init_subclass__` → metaclass, as needed. A metaclass adds an extra compatibility constraint when different base classes use different metaclasses. See Section 2 for metaclass construction hooks and Section 3 for conflicts.

---

## 14. Dynamic class creation

Because classes are objects, Python can create them programmatically instead of using literal `class` statements. Dynamic classes are useful for framework-generated models, test fixtures, configuration-driven types, and adapter factories—but excessive use can make debugging and static analysis harder.

### 14.1 The three-argument form of `type()`

The single-argument form `type(obj)` returns an object's class. The **three-argument** form constructs a new class:

```python
def greet(self):
    return f"Hello, {self.name}"


User = type("User", (object,), {"greet": greet})
user = User()
user.name = "Alice"

user.greet()
User.__bases__
type(User)
```

Results: `'Hello, Alice'`, `(object,)`, and `type`. This is broadly equivalent to defining a `class User` with `greet` in its body.

| Argument | Meaning |
| --- | --- |
| Name (`"User"`) | Class's `__name__` |
| Bases (`(object,)`) | Direct base classes; an empty tuple is also possible |
| Namespace (`{"greet": greet}`) | Attributes/methods assigned directly to the new class |

For introspection and serialization, it can be important to set the class's `__module__` and ensure the resulting class is reachable by name from that module.

### 14.2 Use the metaclass explicitly when appropriate

```python
class TableMeta(type):
    def __new__(mcls, name, bases, namespace):
        namespace.setdefault("table_name", name.lower())
        return super().__new__(mcls, name, bases, namespace)


class BaseModel(metaclass=TableMeta):
    pass


Audit = TableMeta("Audit", (BaseModel,), {})
Audit.table_name
isinstance(Audit, TableMeta)
```

Results: `'audit'` and `True`. When classes have a custom metaclass, constructing with that metaclass explicitly makes the intention clear; do not assume direct calls to a particular class constructor reproduce every part of the `class` statement's header/decorator processing.

### 14.3 `types.new_class()` and namespace initialization

`types.new_class()` is a higher-level helper for dynamic class definitions, including metaclass selection, class keywords, and an optional callback to populate the namespace.

```python
import types


def populate(namespace):
    namespace["kind"] = "generated"
    namespace["describe"] = lambda self: self.kind


Generated = types.new_class("Generated", (), {}, populate)
Generated().describe()
Generated.__name__
```

Results: `'generated'` and `'Generated'`. Unlike the plain three-argument `type()` call, `types.new_class` is designed to follow more of the normal `class` statement's metaclass and class-keyword preparation process. It still does not apply arbitrary class decorators for you.

### 14.4 Dynamic subclasses and factories

```python
class BaseQuery:
    table_name = None

    def describe(self):
        return f"SELECT * FROM {self.table_name}"


def make_query_type(table_name):
    name = "".join(part.title() for part in table_name.split("_")) + "Query"
    return type(name, (BaseQuery,), {"table_name": table_name})


CustomerQuery = make_query_type("customers")
CustomerQuery().describe()
CustomerQuery.__mro__
```

Results: `'SELECT * FROM customers'` and an MRO beginning with `(CustomerQuery, BaseQuery, object)`.

This example creates SQL **text only** and does not execute or sanitize a query. In actual database APIs, prefer parameterized SQL for values and safe identifier handling through library constructs.

**When not to use dynamic classes:** prefer one ordinary class plus configuration values if behavior does not truly vary by type. Dynamic creation complicates stack traces, documentation, debugging, pickling, and static type checking. Use it when the **class itself** needs distinct identity, attributes, inheritance, or metaclass-level behavior.

---
## 15. Five ideas to remember

1. **A class is an object.** `User` is an instance of its metaclass, generally `type`.
2. **Inheritance and metaclass relationships are different.** `User` inherits from `BaseModel` but is an instance of `TableMeta`.
3. **A metaclass receives the class definition before the class object exists.** `name`, `bases`, and `namespace` describe what Python is building.
4. **`vars()` reveals direct stored attributes; `dir()` advertises available names; `inspect` performs richer inspection.** These tools are complementary, not interchangeable.
5. **Use a metaclass only when you need to change class creation.** For simpler subclass registration or validation, consider `__init_subclass__()` or a class decorator.

### Additional concepts at a glance

| Concept | Main insight | Section |
| --- | --- | --- |
| Identity and references | Assignment usually binds names rather than copying objects | 1 |
| Class creation | `__set_name__` and `__init_subclass__` run during class construction | 2 |
| Class state | Shadowing a class attribute is different from mutating its shared value | 3 |
| Cooperative inheritance | `super()` follows the current instance's MRO | 3 |
| Attribute precedence | Data descriptors generally outrank instance dictionaries | 4 |
| Binding | Instance methods are function descriptors bound to `self` | 4 |
| Storage | `__slots__` defines slot descriptors and may remove `__dict__` | 4 |
| Lifetime | Reachability and GC are different from deterministic resource cleanup | 10 |
| ABCs | Nominal interfaces can enforce abstract member implementation | 11 |
| Protocols | Structural compatibility can be checked without explicit inheritance | 12 |
| Class extension | Decorators, subclass hooks, and metaclasses act at different stages | 13 |
| Dynamic types | `type(...)` and `types.new_class(...)` construct class objects at runtime | 14 |


### Python documentation references

- [Data model — objects, attribute access, slots, class creation](https://docs.python.org/3/reference/datamodel.html)
- [Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)
- [`inspect` — Inspect live objects](https://docs.python.org/3/library/inspect.html)
- [`abc` — Abstract base classes](https://docs.python.org/3/library/abc.html)
- [`typing` — `Protocol` and `runtime_checkable`](https://docs.python.org/3/library/typing.html)
- [`types` — Dynamic type creation](https://docs.python.org/3/library/types.html)
- [`gc` — Garbage collector interface](https://docs.python.org/3/library/gc.html)
- [`weakref` — Weak references](https://docs.python.org/3/library/weakref.html)

*End of notes.*
