# Quelques Idées

Architectural sketches and technical explorations drawn from software engineering projects.

While some implementations remain private, selected abstractions, structural designs, and concepts are shared here.

---

## ECL-Modelling-Benchmark

An object-oriented Python library for Expected Credit Loss (ECL) modelling, supporting modular calculation pipelines and parallel batch execution across multiple portfolios.

**Architecture & Implementation**
- Modular calculation pipeline comprising RRM (Roll-Rate Model), SIR (Significant Increase in Credit Risk), FLA (Forward-Looking Adjustments), and ECL (Expected Credit Loss) stages.
- Dedicated input loaders and structured, stage-specific modelling result objects
- Multiprocessing-enabled batch execution with consolidated DataFrame outputs.
- Automated pytest-based validation for verifying calculation results across all modelling stages.

[Designs](./designs/ecl_modelling_benchmark.md)

## AlchemyReflection — Internal Extension

An extension of AlchemyReflection, adapting its object-oriented SQLAlchemy interfaces to enterprise-specific database structures and transactional infrastructure requirements.

**Architecture & Implementation**
- Schema reflection and object-oriented abstractions for database tables and queries.
- Specialized table classes with domain-specific schema constraints.
- Composable SQLAlchemy queries, including CTEs and reusable data retrieval expressions.

## Recalculation-Engine

An object-oriented Python library for transaction-driven recalculation, featuring modular calculation pipelines, dependency-aware execution planning, and scope-specific computation.

**Architecture & Implementation**
- Transaction objects encapsulating execution context, transaction types, and input data.
- Pipeline compilation into scoped execution plans based on transaction scope and calculation dependencies.
- Reusable calculator classes with declarative input specifications, formulas, and output definitions.
- Centralized result collection and consolidation of calculator outputs across calculation pipelines.
- Automated testing and validation of recalculation outputs against production reference results.

[Designs](./designs/recalculation_engine.md)&emsp;|&emsp;[Experiments](./experiments/recalc_engine/)