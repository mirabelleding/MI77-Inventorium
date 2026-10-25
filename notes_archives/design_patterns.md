# Design Patterns Notes

## Contents

1. [The GoF mental model](#1-the-gof-mental-model)
2. [Foundational object-oriented concepts](#2-foundational-object-oriented-concepts)
3. [Creational patterns — five](#3-creational-patterns)
4. [Structural patterns — seven](#4-structural-patterns)
5. [Behavioral patterns — eleven](#5-behavioral-patterns)
6. [Critical comparisons](#6-critical-comparisons)
7. [Integrated transaction-processing design](#7-integrated-transaction-processing-design)
8. [Selection guide and exercises](#8-selection-guide-and-exercises)

---

# 1. The GoF mental model

A **design pattern** is a reusable description of collaborating roles that solve a recurring *design* problem. It is not a library, algorithm, mandatory class diagram, or reason to introduce abstractions prematurely.

Each pattern is best studied through its **intent**, **context/problem**, **participants/collaboration**, **trade-offs**, and **alternatives**. The book groups patterns into: **creational** (object construction), **structural** (composition and interfaces), and **behavioral** (interaction, algorithms, and responsibility).

Core design guidance:

- **Program to an interface rather than a concrete implementation**: callers depend on the behavior they require.
- **Favor composition over inheritance** when collaborators should be replaceable independently.
- **Encapsulate what varies**: isolate algorithms, construction, backends, and policies likely to change.
- **Design for likely changes, not imaginary universality**: extra classes and indirection have a cost.
- **Evaluate consequences**: a pattern shifts complexity; it does not eliminate it.

### Class-based vs object-based patterns

Class-based patterns primarily depend on inheritance (e.g., Template Method); object-based patterns usually depend on references, composition, delegation, and runtime selection (e.g., Strategy). Many patterns admit multiple Python implementations.

### Python context

Python makes function objects, dictionaries of callables, `Protocol`, `ABC`, decorators, generators, and dataclasses available. Use these when they express the same responsibility more simply than classical C++/Smalltalk-style hierarchies.

---

# 2. Foundational object-oriented concepts

## 2.1 Abstraction

**Concept.** Specify essential behavior while suppressing unnecessary implementation detail. A stable contract lets a pipeline request data without knowing SQL, file formats, or connection details. `Protocol` supports structural typing without requiring inheritance.

**Python example:**

```python
from typing import Protocol
import pandas as pd

class Loader(Protocol):
    def load(self, transaction_id: str) -> pd.DataFrame: ...

class MemoryLoader:
    def __init__(self, frame: pd.DataFrame):
        self.frame = frame
    def load(self, transaction_id: str) -> pd.DataFrame:
        return self.frame.loc[self.frame["transaction_id"] == transaction_id].copy()

def fetch(loader: Loader, transaction_id: str) -> pd.DataFrame:
    return loader.load(transaction_id)
```

**Important nuance.** An abstraction is not necessarily an abstract base class. An API, a callable contract, or a `Protocol` can serve as one. Type annotations do not enforce all contracts at runtime.

**Ask yourself:** What responsibility or change boundary does this concept clarify in the application?

## 2.2 Encapsulation

**Concept.** Keep state and behavior together and control access to preserve invariants. `_name` is a non-public convention; `__name` uses name-mangling, not real security. Properties permit controlled read/write access.

**Python example:**

```python
class ExecutionPlan:
    def __init__(self, steps):
        self._steps = tuple(steps)  # defensive container copy
    @property
    def steps(self):
        return self._steps
    def execute(self):
        return [step() for step in self._steps]

plan = ExecutionPlan([lambda: 42])
assert plan.execute() == [42]
```

**Important nuance.** The tuple protects the *collection* from mutation but not the internal state of individual step objects. Encapsulation differs from abstraction: the former protects implementation and invariants; the latter defines the public contract.

**Ask yourself:** What responsibility or change boundary does this concept clarify in the application?

## 2.3 Polymorphism

**Concept.** Different concrete implementations can be used through the same interface. The caller invokes an operation, not an explicit `if isinstance` ladder. Python also supports polymorphism through duck typing.

**Python example:**

```python
class ECL:
    def calculate(self, data): return f"ECL: {data}"
class Impairment:
    def calculate(self, data): return f"Impairment: {data}"

def run(calculator, data):
    return calculator.calculate(data)

assert run(ECL(), 10) == "ECL: 10"
assert run(Impairment(), 10) == "Impairment: 10"
```

**Important nuance.** Subtype/interface polymorphism differs from parametric polymorphism (e.g. `def first(items: list[T]) -> T`). Polymorphism describes interchangeability; dynamic dispatch describes how the selected method runs.

**Ask yourself:** What responsibility or change boundary does this concept clarify in the application?

## 2.4 Delegation

**Concept.** An object asks another object to perform an operation that belongs to the latter. Composition is the relationship (`self.loader`), delegation is the action (`self.loader.load(...)`).

**Python example:**

```python
class Pipeline:
    def __init__(self, loader, validator):
        self.loader, self.validator = loader, validator
    def execute(self, key):
        data = self.loader.load(key)  # delegation
        return self.validator.validate(data)
```

**Important nuance.** Avoid chains of wrappers that only forward calls and add no policy, interface translation, or responsibility.

**Ask yourself:** What responsibility or change boundary does this concept clarify in the application?

## 2.5 Coupling

**Concept.** Coupling measures dependency between components. Concrete classes, global mutable state, implicit ordering, and knowledge of internals can all produce change propagation. Aim for explicit, stable dependencies—not zero dependencies.

**Python example:**

```python
# Tight: constructs its own particular collaborator.
class TightPipeline:
    def execute(self, key):
        return DatabaseLoader().load(key)

# Looser: caller supplies a compatible collaborator.
class LoosePipeline:
    def __init__(self, loader): self.loader = loader
    def execute(self, key): return self.loader.load(key)
```

**Important nuance.** Temporal coupling is important: a `compile(); execute()` calling requirement may be encoded more safely as `plan = compile(...); plan.execute()`. Ordering dependencies do not disappear merely because interfaces exist.

**Ask yourself:** What responsibility or change boundary does this concept clarify in the application?

## 2.6 Cohesion

**Concept.** Cohesion asks whether a class or module has a unified purpose. Loading, validation, ECL calculation, Excel formatting and email sending have different reasons to change and generally should not all live in a giant “Manager” class.

**Python example:**

```python
class DimensionValidator:
    def validate_columns(self, frame): ...
    def validate_membership(self, frame): ...
    def collect_rejected_rows(self, frame): ...

# All three methods serve one cohesive validation concern.
```

**Important nuance.** High cohesion does not mean one method per class. A sophisticated `ExecutionPlan` may legitimately validate dependencies, report ready steps, and compute topological order.

**Ask yourself:** What responsibility or change boundary does this concept clarify in the application?

## 2.7 Separation of concerns

**Concept.** Separate retrieval, transformation, validation, calculation, orchestration, and persistence so each concern can be changed and tested independently. Boundaries can be functions, classes, modules, or packages.

**Python example:**

```python
def execute(transaction, loader, validator, calculator, writer):
    data = loader.load(transaction)
    data = validator.validate(data)
    result = calculator.calculate(data)
    writer.write(result)
    return result
```

**Important nuance.** The orchestration function itself is cohesive: coordinating these steps is its concern. Separation of concerns does not imply maximal fragmentation.

**Ask yourself:** What responsibility or change boundary does this concept clarify in the application?

## 2.8 Dependency injection

**Concept.** A dependency is supplied to its consumer from outside rather than created or looked up internally. This separates construction from behavior, improves testing, and exposes requirements. Common forms: constructor injection, method injection, and property injection.

**Python example:**

```python
class Pipeline:
    def __init__(self, loader, calculator):  # constructor injection
        self.loader = loader
        self.calculator = calculator
    def execute(self, tx):
        return self.calculator.calculate(self.loader.load(tx))

# The composition root wires real implementations:
# pipeline = Pipeline(DatabaseLoader(db), ECLCalculator())

# Method injection instead:
class OnDemandPipeline:
    def execute(self, tx, loader):
        return loader.load(tx)
```

**Important nuance.** Dependency *injection* is a technique; dependency *inversion* is a principle concerning dependency direction and abstractions. A service locator hides required dependencies in a shared registry; injection advertises them in the API. Do not inject trivial helpers automatically.

**Ask yourself:** What responsibility or change boundary does this concept clarify in the application?

## 2.9 Dynamic dispatch

**Concept.** Python selects a method implementation based on the runtime receiver and attribute lookup rules. Method overriding and the method resolution order (MRO) are mechanisms. Python uses C3 linearization for multiple inheritance.

**Python example:**

```python
class Base:
    def run(self): return "base"
class Child(Base):
    def run(self): return "child"

def execute(obj): return obj.run()
assert execute(Child()) == "child"
assert Child.__mro__ == (Child, Base, object)

class A:
    def run(self): return ["A"]
class B(A):
    def run(self): return ["B"] + super().run()
class C(A):
    def run(self): return ["C"] + super().run()
class D(B, C): pass
assert D().run() == ["B", "C", "A"]
```

**Important nuance.** `super()` follows the next class in the receiver’s MRO, not invariably the lexical parent. Calling a function selected via a dictionary is runtime registry-based dispatch, distinct from ordinary attribute/method dispatch.

**Ask yourself:** What responsibility or change boundary does this concept clarify in the application?

## 2.10 Open/closed principle

**Concept.** A stable component should support likely extensions without continual modification of its core. For frequently changing handler types, a registry can remove an expanding conditional from a processor.

**Python example:**

```python
class Processor:
    def __init__(self, handlers): self.handlers = dict(handlers)
    def process(self, tx):
        try:
            handler = self.handlers[tx.type]
        except KeyError as exc:
            raise ValueError(f"Unsupported type: {tx.type}") from exc
        return handler.process(tx)

# Extend by supplying a new handler mapping, not editing Processor.
```

**Important nuance.** No component can be closed to every imaginable change; choose extension points for changes you genuinely expect. OCP is a goal; Strategy, Factory Method and Decorator are possible tools.

**Ask yourself:** What responsibility or change boundary does this concept clarify in the application?

## 2.11 Object collaboration

**Concept.** Systems are networks of objects exchanging requests. Decide who owns each responsibility, and let collaborators communicate through narrow contracts. “Tell, don’t ask” suggests invoking an object’s meaningful operation instead of manipulating its internals.

**Python example:**

```python
class Transaction:
    def __init__(self): self._status = "pending"
    def start(self):
        if self._status != "pending":
            raise ValueError("Invalid state transition")
        self._status = "running"

# Prefer transaction.start() over client code setting
# transaction.status = "running" after inspecting status.
```

**Important nuance.** Read-only data objects and analytical pandas workflows are different: accessing their data is often legitimate. Design collaborations around invariants and responsibilities, not dogmatic rules.

**Ask yourself:** What responsibility or change boundary does this concept clarify in the application?

### Focused comparisons

| Concepts | Distinction |
|---|---|
| Abstraction / encapsulation | Contract / protection of implementation and invariants |
| Polymorphism / dynamic dispatch | Interchangeable behavior / runtime lookup mechanism |
| Composition / delegation | Holding collaborators / forwarding a task |
| Cohesion / coupling | Internal responsibility fit / external dependency strength |
| Dependency injection / dependency inversion | Supplying dependencies / designing dependency direction |
| Factory / dependency injection | Choosing or creating collaborators / supplying them to consumers |

### Dependency injection + dynamic dispatch together

```python
from typing import Protocol

class Calculation(Protocol):
    def calculate(self, value: float) -> float: ...

class Double:
    def calculate(self, value): return 2 * value

class Square:
    def calculate(self, value): return value ** 2

class Processor:
    def __init__(self, calculation: Calculation):
        self.calculation = calculation  # dependency injected
    def run(self, value):
        return self.calculation.calculate(value)  # dynamic method dispatch

assert Processor(Double()).run(3) == 6
assert Processor(Square()).run(3) == 9
```

For *stateless* alternatives, a function is often enough:

```python
from collections.abc import Callable

class FunctionProcessor:
    def __init__(self, calculate: Callable[[float], float]):
        self.calculate = calculate
    def run(self, value: float) -> float:
        return self.calculate(value)

assert FunctionProcessor(lambda x: x * x).run(3) == 9
```

---
# 3. Creational patterns

## 3.1 Factory Method

**Intent:** Let a subclass decide which product object to create through an overridable factory method.

**Problem / context:** A reusable processor controls the processing workflow but different subclasses need distinct handlers.

**Runnable Python example:**

```python
from abc import ABC, abstractmethod

class BaseProcessor(ABC):
    def process(self, tx):
        return self.create_handler().handle(tx)
    @abstractmethod
    def create_handler(self): ...

class ModelHandler:
    def handle(self, tx): return f"model: {tx}"

class ModelProcessor(BaseProcessor):
    def create_handler(self): return ModelHandler()

assert ModelProcessor().process("TX1") == "model: TX1"
```

**How to recognize and use it:** Use when the creator hierarchy itself is valuable. In Python, a registry such as `HANDLERS[type_name]()` may be simpler, but is not the classical subclass-overridden GoF Factory Method.

**Trade-offs:** More subclasses and indirection; subclasses depend on compatible handler interfaces.

## 3.2 Abstract Factory

**Intent:** Provide operations to construct a related family of compatible products.

**Problem / context:** A production environment needs database transaction and balance loaders; tests need matched in-memory versions.

**Runnable Python example:**

```python
class DbTransactions:
    def load(self): return "real transactions"
class DbBalances:
    def load(self): return "real balances"
class FakeTransactions:
    def load(self): return "fake transactions"
class FakeBalances:
    def load(self): return "fake balances"

class ProductionFactory:
    def transactions(self): return DbTransactions()
    def balances(self): return DbBalances()

class TestFactory:
    def transactions(self): return FakeTransactions()
    def balances(self): return FakeBalances()

def fetch_pair(factory):
    return factory.transactions().load(), factory.balances().load()

assert fetch_pair(TestFactory()) == ("fake transactions", "fake balances")
```

**How to recognize and use it:** Use when related object families should be switched together. Abstract Factory is about family compatibility; Factory Method is about an overridable creation operation.

**Trade-offs:** Adding a new *product category* often requires changing each family factory.

## 3.3 Builder

**Intent:** Assemble a complex object through well-defined construction steps, independently of its representation.

**Problem / context:** A compiler assembles an execution plan from validations, data retrieval, and calculations.

**Runnable Python example:**

```python
from dataclasses import dataclass
from collections.abc import Callable

@dataclass(frozen=True)
class ExecutionPlan:
    steps: tuple[Callable[[], object], ...]
    def execute(self): return [step() for step in self.steps]

class PlanBuilder:
    def __init__(self): self._steps = []
    def add(self, step):
        if not callable(step): raise TypeError("step must be callable")
        self._steps.append(step)
        return self  # fluent API
    def build(self): return ExecutionPlan(tuple(self._steps))

plan = PlanBuilder().add(lambda: "validate").add(lambda: "calculate").build()
assert plan.execute() == ["validate", "calculate"]
```

**How to recognize and use it:** A Director may specify a repeatable building sequence. A `compile()` method is not automatically GoF Builder unless construction is deliberately separated and structured.

**Trade-offs:** Avoid for tiny objects with clear constructors; guard invalid construction and step dependencies.

## 3.4 Prototype

**Intent:** Make objects by cloning existing configured instances.

**Problem / context:** Create similar processing configurations with a changed currency or date horizon.

**Runnable Python example:**

```python
import copy
from dataclasses import dataclass, field, replace

@dataclass
class Config:
    currency: str
    stages: list[int] = field(default_factory=list)

base = Config("CAD", [1, 2, 3])
shallow = copy.copy(base)
deep = copy.deepcopy(base)
shallow.stages.append(4)
assert base.stages == [1, 2, 3, 4]  # shared nested list
assert deep.stages == [1, 2, 3]
changed = replace(base, currency="USD")
assert changed.stages is base.stages  # replace is not a deep copy
```

**How to recognize and use it:** Clone templates when setup is cumbersome and ownership is well understood. `copy.copy`, `copy.deepcopy`, and `dataclasses.replace` have different semantics.

**Trade-offs:** Copying DB sessions, locks, huge DataFrames, and handles can be unsafe or expensive.

## 3.5 Singleton

**Intent:** Make a shared instance available within an explicitly defined scope.

**Problem / context:** A process-local application config should be reused rather than re-created for every component.

**Runnable Python example:**

```python
from functools import lru_cache

class Config:
    def __init__(self): self.batch_size = 1000

@lru_cache(maxsize=1)
def get_config():
    return Config()

assert get_config() is get_config()
# This is a cached factory, not a strict prohibition on Config().
```

**How to recognize and use it:** A strict Singleton may override `__new__` and guard repeated `__init__`; module globals or injected configuration are frequently preferable.

**Trade-offs:** Global state complicates tests; cached factory first calls may race; multiprocessing gives separate process-local instances.

---

# 4. Structural patterns

## 4.1 Adapter

**Intent:** Translate an incompatible existing interface to one expected by a client.

**Problem / context:** Legacy ORM provides `get(filters)` while new code expects `load(filters)`.

**Runnable Python example:**

```python
class LegacyTable:
    def get(self, filters): return [filters]

class LoaderAdapter:
    def __init__(self, table): self.table = table
    def load(self, filters): return self.table.get(filters)

assert LoaderAdapter(LegacyTable()).load({"stage": 1}) == [{"stage": 1}]
```

**How to recognize and use it:** Use for integrations and legacy APIs; the adapter preserves the target interface while translating calls.

**Trade-offs:** An extra wrapper can obscure errors if translation is incomplete.

## 4.2 Bridge

**Intent:** Separate two independently variable hierarchies through composition.

**Problem / context:** Report type and storage format should vary independently.

**Runnable Python example:**

```python
class CSVWriter:
    def write(self, rows): return "CSV:" + str(rows)
class JsonWriter:
    def write(self, rows): return "JSON:" + str(rows)

class Report:
    def __init__(self, writer): self.writer = writer
    def export(self, rows): return self.writer.write(rows)

class AuditReport(Report): pass
assert AuditReport(JsonWriter()).export([1]) == "JSON:[1]"
```

**How to recognize and use it:** Bridge is intentional separation of orthogonal dimensions; Adapter usually reconciles pre-existing incompatibility.

**Trade-offs:** Introduces interfaces and object references; not useful without meaningful independent variation.

## 4.3 Composite

**Intent:** Represent leaves and containers through a common interface.

**Problem / context:** A nested execution plan includes individual steps and groups of steps.

**Runnable Python example:**

```python
class Step:
    def __init__(self, fn): self.fn = fn
    def execute(self): return self.fn()

class Group:
    def __init__(self, children): self.children = children
    def execute(self): return [child.execute() for child in self.children]

plan = Group([Step(lambda: 1), Group([Step(lambda: 2)])])
assert plan.execute() == [1, [2]]
```

**How to recognize and use it:** Useful for trees, document elements, nested workflows. Leaves and composites share `execute()`.

**Trade-offs:** A universal interface may permit operations that do not make sense for every node.

## 4.4 Decorator

**Intent:** Wrap an object with the same interface to add a responsibility.

**Problem / context:** Add timing or logging to calculation steps without changing their code.

**Runnable Python example:**

```python
from time import perf_counter

class BaseStep:
    def execute(self): return 42

class TimedStep:
    def __init__(self, inner): self.inner = inner
    def execute(self):
        start = perf_counter()
        result = self.inner.execute()
        self.elapsed = perf_counter() - start
        return result

assert TimedStep(BaseStep()).execute() == 42
```

**How to recognize and use it:** Object-pattern Decorator is broader than Python’s `@function_decorator` syntax. Can layer logging, timing, retries, etc.

**Trade-offs:** Wrapper order matters; excessive layering complicates tracing and identity.

## 4.5 Facade

**Intent:** Offer a simple high-level entry point to a complex subsystem.

**Problem / context:** Users call one engine API instead of constructing and invoking many internals.

**Runnable Python example:**

```python
class Engine:
    def __init__(self, loader, calculator):
        self.loader, self.calculator = loader, calculator
    def run(self, tx):
        data = self.loader.load(tx)
        return self.calculator.calculate(data)

# Engine.run is the convenience entry point.
```

**How to recognize and use it:** Facade simplifies external access; Mediator coordinates internal colleagues. A Facade can coexist with publicly accessible lower-level APIs.

**Trade-offs:** Beware giant facade classes that absorb all business logic.

## 4.6 Flyweight

**Intent:** Share intrinsic, usually immutable state between many objects; keep context-specific state separate.

**Problem / context:** Hundreds of thousands of data points share a measure definition.

**Runnable Python example:**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Measure:
    code: str
    unit: str

@dataclass
class DataPoint:
    value: float
    measure: Measure

ECL = Measure("ECL", "CAD")
a, b = DataPoint(10, ECL), DataPoint(20, ECL)
assert a.measure is b.measure
```

**How to recognize and use it:** Intrinsic: common measure metadata. Extrinsic: data-point value. In pandas, categorical/columnar storage may be preferable to row objects.

**Trade-offs:** Shared mutable state is dangerous; no benefit if you never duplicated the shared data.

## 4.7 Proxy

**Intent:** Place a surrogate in front of an object to control access, delay creation, or cache calls.

**Problem / context:** Cache repeated loader requests.

**Runnable Python example:**

```python
class CacheProxy:
    def __init__(self, loader):
        self.loader, self.cache = loader, {}
    def load(self, key):
        if key not in self.cache:
            self.cache[key] = self.loader.load(key)
        return self.cache[key]

# Beware callers mutating cached DataFrames.
```

**How to recognize and use it:** Decorator adds responsibilities; Proxy controls access. Their wrapper structures can look very similar.

**Trade-offs:** Cache invalidation, shared mutable data, race conditions, and stale results.

---

# 5. Behavioral patterns

## 5.1 Chain of Responsibility

**Intent:** Pass a request along potential handlers; each decides to process or forward it.

**Problem / context:** Transaction type routing when multiple independent handlers can accept or decline a request.

**Runnable Python example:**

```python
class Handler:
    def __init__(self, next_handler=None): self.next = next_handler
    def handle(self, request):
        if self.accepts(request): return self.process(request)
        if self.next: return self.next.handle(request)
        raise ValueError("No handler")

class PositiveHandler(Handler):
    def accepts(self, req): return req > 0
    def process(self, req): return "positive"

class ZeroHandler(Handler):
    def accepts(self, req): return req == 0
    def process(self, req): return "zero"

assert PositiveHandler(ZeroHandler()).handle(0) == "zero"
```

**How to recognize and use it:** A chain is not the same as a pipeline where all steps execute. A mapping may be simpler for deterministic transaction-type routing.

**Trade-offs:** Handler order affects results; requests may go unhandled.

## 5.2 Command

**Intent:** Represent a request or operation as an object containing what is needed to execute it.

**Problem / context:** Queue or defer calculations, or store a structured execution plan.

**Runnable Python example:**

```python
from dataclasses import dataclass

@dataclass
class MultiplyCommand:
    factor: float
    value: float
    def execute(self): return self.factor * self.value

queue = [MultiplyCommand(2, 10), MultiplyCommand(3, 10)]
assert [command.execute() for command in queue] == [20, 30]
```

**How to recognize and use it:** Command provides operation identity and deferred execution. Retriability and idempotency are *additional* requirements; do not assume either.

**Trade-offs:** More command objects and lifecycle decisions; captured arguments may not serialize across processes.

## 5.3 Interpreter

**Intent:** Represent a small grammar with expression objects that evaluate structured expressions.

**Problem / context:** Transaction-scoping rules such as stage=1 AND currency=CAD.

**Runnable Python example:**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Equals:
    key: str
    value: object
    def evaluate(self, row): return row[self.key] == self.value

@dataclass(frozen=True)
class And:
    left: object
    right: object
    def evaluate(self, row):
        return self.left.evaluate(row) and self.right.evaluate(row)

rule = And(Equals("stage", 1), Equals("currency", "CAD"))
assert rule.evaluate({"stage": 1, "currency": "CAD"})
```

**How to recognize and use it:** This is an expression tree; a complete language also needs grammar parsing and error reporting. Avoid `eval` on untrusted input.

**Trade-offs:** Complex languages are usually better handled by real parsers or established expression libraries.

## 5.4 Iterator

**Intent:** Provide sequential traversal without exposing a collection’s internal representation.

**Problem / context:** Expose a plan’s steps through the iterator protocol.

**Runnable Python example:**

```python
class Plan:
    def __init__(self, steps): self._steps = tuple(steps)
    def __iter__(self):
        yield from self._steps

assert list(Plan(["validate", "load"])) == ["validate", "load"]
```

**How to recognize and use it:** Generators implement Python’s iteration protocol; prefer native iteration over unnecessary custom iterator classes.

**Trade-offs:** Be aware of one-shot iterators, lazy side effects, and mutation during iteration.

## 5.5 Mediator

**Intent:** Centralize collaboration between objects that otherwise refer directly to one another.

**Problem / context:** A coordinator directs loading, validating, and calculating.

**Runnable Python example:**

```python
class Coordinator:
    def __init__(self, loader, validator, calculator):
        self.loader, self.validator, self.calculator = loader, validator, calculator
    def process(self, tx):
        data = self.loader.load(tx)
        checked = self.validator.validate(data)
        return self.calculator.calculate(checked)
```

**How to recognize and use it:** Mediator reduces colleague-to-colleague links; Facade simplifies subsystem access from outside. A coordinator can fulfill both roles in small systems.

**Trade-offs:** An overgrown mediator becomes a god object.

## 5.6 Memento

**Intent:** Capture and restore an object’s state without exposing or arbitrarily manipulating its internals.

**Problem / context:** Support an undo operation in a plan editor.

**Runnable Python example:**

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Snapshot:
    steps: tuple

class PlanEditor:
    def __init__(self): self._steps = []
    def add(self, step): self._steps.append(step)
    def save(self): return Snapshot(tuple(self._steps))
    def restore(self, snap): self._steps = list(snap.steps)

editor = PlanEditor()
editor.add("load")
saved = editor.save()
editor.add("calculate")
editor.restore(saved)
assert editor._steps == ["load"]
```

**How to recognize and use it:** The snapshot is shallow for contained mutable elements. Undoing in-memory state does not reverse external database writes.

**Trade-offs:** Large snapshots consume memory; versioning and external side effects require explicit handling.

## 5.7 Observer

**Intent:** A publisher notifies subscribed observers when events occur.

**Problem / context:** Log and collect metrics when a transaction finishes without baking those actions into calculation code.

**Runnable Python example:**

```python
class Publisher:
    def __init__(self): self.subscribers = []
    def subscribe(self, callback): self.subscribers.append(callback)
    def publish(self, event):
        for subscriber in tuple(self.subscribers):
            subscriber(event)

seen = []
pub = Publisher()
pub.subscribe(seen.append)
pub.publish({"type": "completed", "tx": "TX1"})
assert seen[0]["tx"] == "TX1"
```

**How to recognize and use it:** Basic Observer is synchronous here. Distributed event delivery requires independent choices about persistence, retries, ordering, and delivery guarantees.

**Trade-offs:** Subscriber failure can interrupt notifications; avoid memory leaks and accidental duplicate registrations.

## 5.8 State

**Intent:** Move lifecycle-specific behavior and transitions into state-specific objects.

**Problem / context:** A transaction transitions among pending, running, completed or failed.

**Runnable Python example:**

```python
class Pending:
    def start(self, tx): tx.state = Running()

class Running:
    def complete(self, tx): tx.state = Completed()

class Completed: pass

class Transaction:
    def __init__(self): self.state = Pending()
    def start(self): self.state.start(self)
    def complete(self): self.state.complete(self)

tx = Transaction()
tx.start()
tx.complete()
assert isinstance(tx.state, Completed)
```

**How to recognize and use it:** Strategy selects interchangeable algorithms; State models behavior that changes as an object transitions through a lifecycle.

**Trade-offs:** Overkill for a small status enum; make illegal transitions explicit rather than relying on missing-method errors in production.

## 5.9 Strategy

**Intent:** Encapsulate interchangeable algorithms behind a shared interface.

**Problem / context:** Select ECL versus impairment calculations at runtime.

**Runnable Python example:**

```python
class ECL:
    def calculate(self, value): return value * 0.03
class Impairment:
    def calculate(self, value): return value * 0.10

class Processor:
    def __init__(self, strategy): self.strategy = strategy
    def run(self, value): return self.strategy.calculate(value)

assert Processor(ECL()).run(100) == 3.0
assert Processor(Impairment()).run(100) == 10.0
```

**How to recognize and use it:** A pure function can be a strategy in Python; choose a class when it carries configuration, lifecycle or multiple operations.

**Trade-offs:** Makes implementations substitutable, but can overcomplicate a single unchanging calculation.

## 5.10 Template Method

**Intent:** A base class owns an algorithm skeleton and subclasses implement selected hooks.

**Problem / context:** All calculations share validation and formatting, but use different calculation logic.

**Runnable Python example:**

```python
from abc import ABC, abstractmethod

class Calculation(ABC):
    def run(self, value):
        if value < 0: raise ValueError("negative")
        result = self.calculate(value)
        return round(result, 2)
    @abstractmethod
    def calculate(self, value): ...

class ECL(Calculation):
    def calculate(self, value): return value * 0.03

assert ECL().run(100) == 3.0
```

**How to recognize and use it:** Template Method uses inheritance for a stable workflow; Strategy uses composition for replaceable algorithms.

**Trade-offs:** Too many overridable hooks produce fragile subclasses and implicit dependencies.

## 5.11 Visitor

**Intent:** Move operations over a stable object hierarchy into visitor implementations using double dispatch.

**Problem / context:** Add reporting or validation across several kinds of plan nodes.

**Runnable Python example:**

```python
class UploadNode:
    def accept(self, visitor): return visitor.visit_upload(self)
class AdjustmentNode:
    def accept(self, visitor): return visitor.visit_adjustment(self)

class NameVisitor:
    def visit_upload(self, node): return "upload"
    def visit_adjustment(self, node): return "adjustment"

visitor = NameVisitor()
assert UploadNode().accept(visitor) == "upload"
assert AdjustmentNode().accept(visitor) == "adjustment"
```

**How to recognize and use it:** Adds new *operations* easily when node variants are stable. Adding new node types usually requires modifying all visitors. `singledispatch` and pattern matching are Python alternatives.

**Trade-offs:** Double dispatch and many visitor methods can obscure code flow.

---

# 6. Critical comparisons

| Common confusion | Main distinction | Quick diagnostic |
|---|---|---|
| Factory Method vs Abstract Factory | One overridable creation method vs related product family | Is a subclass choosing a product, or an environment furnishing several coordinated products? |
| Abstract Factory vs Builder | Choose related products vs assemble a complex result | Is variation in the family, or in construction steps? |
| Builder vs Prototype | Construct deliberately vs clone a configured instance | Are you assembling fresh structure or starting from a template? |
| Adapter vs Bridge | Translate incompatible interfaces vs separate independently varying dimensions | Did incompatibility already exist? |
| Adapter vs Facade | Convert interface vs simplify subsystem | One interface mismatch, or many subsystem services? |
| Decorator vs Proxy | Add behavior vs control access | Is this timing/logging, or lazy/cached/authorized access? |
| Facade vs Mediator | External simplicity vs internal coordination | Whose interactions become simpler? |
| Composite vs Decorator | Tree of leaves/groups vs wrapper adding responsibilities | Does an object represent a collection, or augment one component? |
| Strategy vs Template Method | Composition vs inheritance | Swap a collaborator or override a framework hook? |
| Strategy vs State | Selected algorithm vs lifecycle-dependent behavior | Does the client select a policy or does the object transition states? |
| Command vs Chain | Package executable request vs find an accepting handler | Is work being queued, or dispatched among candidates? |
| Observer vs Mediator | Event subscribers vs coordinated colleague interaction | Independent listeners or managed bidirectional workflow? |
| Iterator vs Visitor | Traverse elements vs apply type-specific operations | Who controls traversal and operation? |

## Designing around realistic change

1. Identify what is stable: business workflow, input/output contract, dependency graph, invariant.
2. Identify independently variable dimensions: source, algorithm, policy, environment, output format.
3. Prefer a function/dictionary/`Protocol`/simple composition before building an inheritance hierarchy.
4. Choose one pattern only when it solves a concrete pressure point.
5. Test extension and replacement: can you introduce an additional algorithm without rewriting orchestration?
6. Review lifecycle issues: thread/process safety, caching, transaction boundaries, and side effects.

---

# 7. Integrated transaction-processing design

This example combines **dependency injection**, **Strategy**, a **factory registry**, a simple **Facade**, and an immutable plan built from callable steps. It is intentionally in-memory, so the architecture can be understood independently of SQLAlchemy.

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Protocol

@dataclass(frozen=True)
class Transaction:
    uuid: str
    transaction_type: str
    scope_id: str

class Loader(Protocol):
    def load(self, tx: Transaction) -> list[float]: ...

class Calculator(Protocol):
    def calculate(self, values: list[float]) -> float: ...

class InMemoryLoader:
    def __init__(self, data: dict[str, list[float]]):
        self._data = data
    def load(self, tx: Transaction) -> list[float]:
        return list(self._data[tx.scope_id])

class ECLCalculator:
    def calculate(self, values: list[float]) -> float:
        return round(sum(values) * 0.03, 2)

class AdjustmentCalculator:
    def calculate(self, values: list[float]) -> float:
        return round(sum(values) * -0.01, 2)

CALCULATOR_TYPES = {
    "model_upload": ECLCalculator,
    "other_upload": AdjustmentCalculator,
}

@dataclass(frozen=True)
class ExecutionPlan:
    steps: tuple[Callable[[], object], ...]
    def execute(self) -> list[object]:
        return [step() for step in self.steps]

class Pipeline:
    def __init__(self, loader: Loader, registry: dict):
        self.loader = loader
        self.registry = dict(registry)

    def compile(self, tx: Transaction) -> ExecutionPlan:
        calculator_type = self.registry[tx.transaction_type]
        calculator: Calculator = calculator_type()
        # The callable is deferred. Load happens when execute() runs.
        def calculate():
            values = self.loader.load(tx)
            return calculator.calculate(values)
        return ExecutionPlan((calculate,))

class RecalcEngine:  # Facade for callers
    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline  # dependency injection
    def run(self, tx: Transaction) -> list[object]:
        plan = self.pipeline.compile(tx)
        return plan.execute()

engine = RecalcEngine(Pipeline(
    loader=InMemoryLoader({"H001": [100, 200]}),
    registry=CALCULATOR_TYPES,
))

assert engine.run(Transaction("TX1", "model_upload", "H001")) == [9.0]
assert engine.run(Transaction("TX2", "other_upload", "H001")) == [-3.0]
```

### What the example demonstrates

- **Abstraction:** The pipeline requires only the `Loader` and `Calculator` contracts.
- **Encapsulation:** The loader hides its data store.
- **Dependency injection:** The engine receives its pipeline; the pipeline receives the loader and registry.
- **Factory/registry:** `transaction_type` determines which calculator class is instantiated.
- **Dynamic dispatch:** `calculator.calculate(values)` uses the actual calculator implementation.
- **Strategy:** ECL vs Adjustment algorithms are interchangeable.
- **Command-like plan:** Deferred callables represent work; more explicit command objects could carry metadata.
- **Facade:** `engine.run(tx)` hides compilation/execution details.

### Production upgrades for a batch recalculation engine

- Load shared database inputs **once per batch** outside per-transaction workers. Filter or partition data in memory by hierarchy, stage, currency, and month as appropriate.
- Keep `ExecutionPlan` as a serializable *description* of work if it must cross multiprocessing boundaries; nested closures and live DB connections often cannot be safely serialized/shared.
- Distinguish **compilation** (select steps and dependencies) from **execution** (acquire resources, run ordered work).
- Explicitly model required upstream measures and previous-month dependencies; calculate a topological order or schedule per independent partition.
- Create SQLAlchemy sessions/connections in the correct worker/process scope; do not share an active session across processes.
- Make retry/idempotency and durable persistence separate explicit design concerns.
- Test the pipeline with fake loaders and simple calculator strategies, independently of database integration tests.

---

# 8. Selection guide and exercises

## All 23 at a glance

| Category | Pattern | Recognition cue |
|---|---|---|
| Creational | **Factory Method** | Let a subclass decide which product object to create through an overridable factory method. |
| Creational | **Abstract Factory** | Provide operations to construct a related family of compatible products. |
| Creational | **Builder** | Assemble a complex object through well-defined construction steps, independently of its representation. |
| Creational | **Prototype** | Make objects by cloning existing configured instances. |
| Creational | **Singleton** | Make a shared instance available within an explicitly defined scope. |
| Structural | **Adapter** | Translate an incompatible existing interface to one expected by a client. |
| Structural | **Bridge** | Separate two independently variable hierarchies through composition. |
| Structural | **Composite** | Represent leaves and containers through a common interface. |
| Structural | **Decorator** | Wrap an object with the same interface to add a responsibility. |
| Structural | **Facade** | Offer a simple high-level entry point to a complex subsystem. |
| Structural | **Flyweight** | Share intrinsic, usually immutable state between many objects; keep context-specific state separate. |
| Structural | **Proxy** | Place a surrogate in front of an object to control access, delay creation, or cache calls. |
| Behavioral | **Chain of Responsibility** | Pass a request along potential handlers; each decides to process or forward it. |
| Behavioral | **Command** | Represent a request or operation as an object containing what is needed to execute it. |
| Behavioral | **Interpreter** | Represent a small grammar with expression objects that evaluate structured expressions. |
| Behavioral | **Iterator** | Provide sequential traversal without exposing a collection’s internal representation. |
| Behavioral | **Mediator** | Centralize collaboration between objects that otherwise refer directly to one another. |
| Behavioral | **Memento** | Capture and restore an object’s state without exposing or arbitrarily manipulating its internals. |
| Behavioral | **Observer** | A publisher notifies subscribed observers when events occur. |
| Behavioral | **State** | Move lifecycle-specific behavior and transitions into state-specific objects. |
| Behavioral | **Strategy** | Encapsulate interchangeable algorithms behind a shared interface. |
| Behavioral | **Template Method** | A base class owns an algorithm skeleton and subclasses implement selected hooks. |
| Behavioral | **Visitor** | Move operations over a stable object hierarchy into visitor implementations using double dispatch. |

## Architecture review checklist

- [ ] One clear responsibility per component; strong cohesion.
- [ ] Dependency contracts are stable and explicit.
- [ ] Implementations can be replaced when there is a real need.
- [ ] Object construction happens at a well-defined composition root.
- [ ] Mutable state and lifecycle ownership are understood.
- [ ] Validation, calculation, I/O, and persistence concerns are appropriately separated.
- [ ] The design can be tested without requiring the production database.
- [ ] Plan compilation and execution have distinct roles where useful.
- [ ] Extension points reflect expected changes rather than speculative complexity.
- [ ] Multiprocessing, idempotency, ordering, and transaction semantics are addressed separately from pattern selection.

## Exercises

1. Take a processor with an `if/elif` branch for ECL vs impairment. Refactor it once with a `dict[str, Callable]` and once with Strategy classes. Compare complexity.
2. Write a `Loader` Protocol, plus database and in-memory implementations. Inject each into the same pipeline and write a unit test.
3. Implement a logging Decorator for a calculator and a caching Proxy for a loader. Explain why their structures look alike but intentions differ.
4. Create a nested execution plan using Composite. Add an Iterator over leaf steps; decide who owns traversal order.
5. Build a small `ExecutionPlanBuilder` that rejects duplicated steps or missing prerequisites before `build()`.
6. Model a pending/running/completed transaction with State and with a simple enum. State the point at which State classes become worthwhile.
7. Design separate production and testing source families with Abstract Factory. Add a third product and observe the change cost.
8. Explain why a process-local Singleton does not solve sharing read-only benchmark inputs among multiprocessing workers.
9. Draw a sequence diagram for `engine.run → pipeline.compile → plan.execute → loader → calculator → results` and identify every delegation boundary.
10. Given a stable hierarchy of upload and adjustment nodes, add a reporting operation with Visitor; then add a new node and document the impact on visitors.

## Study order

1. Foundations: abstraction, encapsulation, cohesion, coupling, delegation.
2. Dependency injection + polymorphism + dynamic dispatch + `Protocol` and `ABC`.
3. Strategy, Factory Method, Abstract Factory, Template Method.
4. Builder, Facade, Adapter, Composite, Command.
5. The remaining patterns; focus on applicability and costs rather than memorization.
6. Revisit your real package and articulate *why* each class and boundary exists.

## Further reading

- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley (1994).
- Python documentation: [`abc`](https://docs.python.org/3/library/abc.html), [`typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol), [`dataclasses`](https://docs.python.org/3/library/dataclasses.html), [`copy`](https://docs.python.org/3/library/copy.html), [`functools`](https://docs.python.org/3/library/functools.html).
- [Refactoring.Guru: Design Patterns in Python](https://refactoring.guru/design-patterns/python) for additional illustrations and code examples.

**Study takeaway:** Patterns are tools for assigning responsibilities and stabilizing change boundaries. Prefer the smallest design that keeps real variations independent, dependencies explicit, and the overall program easy to understand.
