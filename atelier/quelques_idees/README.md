# Quelques Idées

Architectural sketches and technical explorations drawn from software engineering projects.

While some implementations remain private, selected abstractions, structural designs, and concepts are shared here.

---

## ECL-Modelling-Benchmark

An object-oriented Python library for Expected Credit Loss (ECL) modelling, supporting parallel batch execution across multiple portfolios.

**Architecture & Implementation**
- Modular calculation pipeline comprising RRM (Roll-Rate Model), SIR (Significant Increase in Risk), FLA (Forward-Looking Adjustments), and ECL stages.
- Dedicated input loaders and structured modelling result objects.
- Multiprocessing-based batch execution with consolidated DataFrame outputs.
- Automated pytest benchmark pipeline for verifying calculation results across all modelling stages.

[Notes](./ecl_modelling_benchmark.md)

## AlchemyReflection — Internal Extension

An extension of AlchemyReflection, adapting its object-oriented SQLAlchemy interfaces to enterprise-specific database structures and transactional infrastructure requirements.

**Architecture & Implementation**
- Schema reflection and object-oriented abstractions for database tables and queries.
- Specialized table classes with domain-specific schema constraints.
- Composable SQLAlchemy queries, including CTEs and reusable data retrieval expressions.

## Recalculation-Engine

An object-oriented Python library built around a transaction-driven recalculation framework, supporting modular calculation pipelines and scope-specific execution.

**Architecture & Implementation**
- Transaction objects encapsulating execution context, transaction types, and calculation scopes.
- Pipeline compilation into execution plans based on transaction-specific requirements.
- Modular calculation components with reusable computation interfaces.
- Centralized result aggregation and structured DataFrame outputs.
- Automated testing pipeline for verifying recalculation outputs against production benchmarks.

[Notes](./recalculation_engine.md)