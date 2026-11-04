
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, fields, is_dataclass
from functools import reduce
from typing import Any


@dataclass(frozen=True, init=False)
class Calculator:
    """
    Evaluate Python expressions over named variables, configured through
    keyword arguments or a mapping of output names to formulas.

    Formulas are evaluated in definition order, allowing subsequent
    expressions to reference previously calculated variables.

    Custom functions, modules, and constants can be supplied through
    the namespace parameter.

    Supports dictionaries, dataclasses, Pandas and Polars DataFrames,
    and Pandas Series as inputs.

    Returns DataFrames of the original backend for DataFrame inputs,
    or dictionaries for other supported input types.

    Examples
    --------
    >>> from math import sqrt
    >>> calc = Calculator(
    ...     namespace={"sqrt": sqrt},
    ...     squared_norm="x**2 + y**2",
    ...     norm="sqrt(squared_norm)",
    ...     normalized="norm / z",
    ... )
    >>> calc.calculate({"x": 3, "y": 4, "z": 10})
    {'x': 3, 'y': 4, 'z': 10, 'squared_norm': 25, 'norm': 5.0, 'normalized': 0.5}

    Notes
    -----
    Input values are not automatically cast; output dtypes depend on
    the underlying types and operations.

    Warnings
    --------
    Formulas must be trusted because eval() can execute arbitrary code.
    """

    formulas: dict[str, str]
    namespace: dict[str, Any]

    def __init__(
        self,
        formulas: Mapping[str, str] | None = None,
        *,
        namespace: Mapping[str, Any] | None = None,
        **expressions: str,
    ) -> None:
        if formulas is not None and expressions:
            raise TypeError(
                "Provide formulas as a mapping or keyword arguments."
            )

        object.__setattr__(
            self,
            "formulas",
            dict(
                formulas
                if formulas is not None
                else expressions),
        )
        object.__setattr__(
            self,
            "namespace",
            dict(namespace) if namespace is not None else {},
        )

    def calculate(
        self,
        data: Any,
        output_only: bool = False,
    ) -> Any:
        """
        Evaluate configured formulas against the supplied data.

        Parameters
        ----------
        data : Any
            Input data containing named variables.
        output_only : bool, default False
            Whether to return only calculated outputs.
        """
        variables = reduce(
            lambda scope, name: {
                **scope,
                name: eval(
                    self.formulas[name],
                    {**self.namespace, **scope},
                ),
            },
            self.formulas,
            {name: data[name] for name in data.columns}
            if hasattr(data, "columns")
            else {
                field.name: getattr(data, field.name)
                for field in fields(data)
            }
            if is_dataclass(data) and not isinstance(data, type)
            else dict(data),
        )

        result = {
            name: variables[name]
            for name in self.formulas
        }

        if hasattr(data, "columns"):
            if hasattr(data, "assign"):
                output = data.assign(**result)
                return (
                    output[list(result)]
                    if output_only else output
                )

            output = data.with_columns(**result)
            return (
                output.select(list(result))
                if output_only else output
            )

        return result if output_only else variables
