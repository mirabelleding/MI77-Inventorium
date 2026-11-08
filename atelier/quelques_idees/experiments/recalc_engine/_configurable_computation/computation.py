from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import fields, is_dataclass
from functools import reduce
from inspect import Parameter, signature
from typing import Any


class ComputationEngine:
    """
    Compute named outputs from Python expressions and callables.

    Computations can be configured through keyword arguments or a mapping,
    using expression strings, lambda functions, existing functions, or
    other callable objects.

    Callable parameters are matched by name against available input
    variables, namespace entries, and previously computed outputs.

    Computations execute in definition order, allowing subsequent
    operations to reference earlier results. The optional namespace
    provides additional functions, modules, and constants.

    Supports dictionaries of arbitrary Python objects, dataclasses,
    pandas Series, and pandas/Polars DataFrames.

    Returns the original DataFrame type for DataFrame inputs, or a
    dictionary otherwise. Input variables are excluded by default.

    Examples
    --------
    >>> def to_percentage(ratio):
    ...     return ratio * 100
    ...
    >>> calc = Calculator(
    ...     squared_norm="x**2 + y**2",
    ...     norm=lambda squared_norm: squared_norm**0.5,
    ...     ratio=lambda norm, z: norm / z,
    ...     percentage=to_percentage,
    ... )
    >>> calc.calculate({"x": 3, "y": 4, "z": 10})
    {'squared_norm': 25, 'norm': 5.0, 'ratio': 0.5, 'percentage': 50.0}

    Notes
    -----
    Input values are not automatically cast. Result types and dtypes
    depend on the underlying operations.

    Callable parameters must be compatible with name-based keyword binding.

    Warnings
    --------
    Expression strings must be trusted because eval() can execute
    arbitrary Python code.
    """
    def __init__(
        self,
        formulas: Mapping[str, str | Callable[..., Any]] | None = None,
        *,
        namespace: Mapping[str, Any] | None = None,
        **expressions: str | Callable[..., Any],
    ) -> None:
        if formulas is not None and expressions:
            raise TypeError(
                "Provide formulas as a mapping or keyword arguments."
            )

        self.formulas = dict(
            formulas if formulas is not None else expressions
        )
        self.namespace = dict(namespace) if namespace is not None else {}

    def _evaluate(
        self,
        operation: str | Callable[..., Any],
        scope: dict[str, Any],
    ) -> Any:
        context = {**self.namespace, **scope}

        if isinstance(operation, str):
            return eval(operation, context)

        return operation(
            **{
                name: context[name]
                for name, param in signature(operation).parameters.items()
                if name in context
                and param.kind in (
                    Parameter.POSITIONAL_OR_KEYWORD,
                    Parameter.KEYWORD_ONLY,
                )
            }
        )

    def compute(
        self,
        data: Any,
        include_input: bool = False,
    ) -> Any:
        variables = reduce(
            lambda scope, name: {
                **scope,
                name: self._evaluate(self.formulas[name], scope),
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
            output = (
                data.assign(**result)
                if hasattr(data, "assign")
                else data.with_columns(**result)
            )
            return (
                output
                if include_input
                else output[list(result)]
            )

        return variables if include_input else result
