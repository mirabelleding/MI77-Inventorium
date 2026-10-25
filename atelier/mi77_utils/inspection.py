import inspect
from pprint import pprint


def inspect_object(
    obj: object,
    display: bool = False,
) -> dict[str, object]:

    if inspect.isclass(obj):
        cls = obj

        inspection = {
            "name": cls.__name__,
            "module": cls.__module__,
            "metaclass": type(cls).__name__,
            "bases": [base.__name__ for base in cls.__bases__],
            "mro": [base.__name__ for base in inspect.getmro(cls)],
            "own_attributes": list(vars(cls)),
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
            },
        }

    else:
        cls = type(obj)

        inspection = {
            "class": cls.__name__,
            "metaclass": type(cls).__name__,
            "instance_attrs": (
                vars(obj) if hasattr(obj, "__dict__") else None
            ),
            "available_names": [
                name for name in dir(obj)
                if not name.startswith("__")
            ],
        }

    if display:
        pprint(inspection, sort_dicts=False)

    return inspection
