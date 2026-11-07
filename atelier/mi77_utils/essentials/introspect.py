
import inspect
from pprint import pprint as _pprint


def _signature(obj: object) -> str | None:
    try:
        return str(inspect.signature(obj))
    except (TypeError, ValueError):
        return None


def introspect(
    obj: object,
    pprint: bool = False,
) -> dict[str, object]:

    if inspect.isclass(obj):
        cls = obj

        inspection = {
            "name": cls.__name__,
            "qualname": cls.__qualname__,
            "module": cls.__module__,
            "metaclass": type(cls).__name__,
            "signature": _signature(cls),
            "bases": [base.__name__ for base in cls.__bases__],
            "mro": [base.__name__ for base in inspect.getmro(cls)],
            "own_attributes": list(vars(cls)),
            "slots": vars(cls).get("__slots__", ()),
            "abstract_methods": sorted(
                getattr(cls, "__abstractmethods__", ())
            ),
            "properties": [
                name
                for name, value in inspect.getmembers_static(cls)
                if isinstance(value, property)
            ],
            "functions": [
                name
                for name, _ in inspect.getmembers(cls, inspect.isfunction)
            ],
            "bound_methods": [
                name
                for name, _ in inspect.getmembers(cls, inspect.ismethod)
            ],
            "origins": {
                member.name: member.defining_class.__name__
                for member in inspect.classify_class_attrs(cls)
                if not member.name.startswith("__")
                and member.defining_class is not None
            },
        }

    else:
        cls = type(obj)

        inspection = {
            "class": cls.__name__,
            "qualname": cls.__qualname__,
            "module": cls.__module__,
            "metaclass": type(cls).__name__,
            "mro": [base.__name__ for base in inspect.getmro(cls)],
            "callable": callable(obj),
            "signature": _signature(obj) if callable(obj) else None,
            "instance_attrs": (
                vars(obj) if hasattr(obj, "__dict__") else None
            ),
            "available_names": [
                name
                for name in dir(obj)
                if not name.startswith("__")
            ],
            "methods": [
                name
                for name, value in inspect.getmembers_static(obj)
                if inspect.isroutine(value)
                and not name.startswith("__")
            ],
        }

    if inspect.ismethod(obj):
        bound = obj.__self__

        inspection["binding"] = {
            "type": "class" if inspect.isclass(bound) else "instance",
            "owner": (
                bound.__qualname__
                if inspect.isclass(bound)
                else type(bound).__qualname__
            ),
            "function": obj.__func__.__qualname__,
        }

    if pprint:
        _pprint(inspection, sort_dicts=False)

    return inspection