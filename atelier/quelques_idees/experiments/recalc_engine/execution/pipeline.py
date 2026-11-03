from typing import Self

from recalc_engine.calcs.demo_calcs import CalcA, CalcB, CalcC, CalcD, CalcE
from recalc_engine.config.inputs import ExecutionInputs
from recalc_engine.config.results import RecalcResults
from recalc_engine.core.plans import ExecutionPlan
from recalc_engine.core.transaction import Transaction

from .compiler import PipeCompiler


class Pipeline:

    PIPE = (
        CalcA,
        CalcB,
        CalcC,
        CalcD,
        CalcE,
        )

    def __init__(self, transaction: Transaction):
        self.transaction = transaction
        self.execution_plan: ExecutionPlan | None = None

    def compile(self) -> Self:
        self.execution_plan = PipeCompiler(
            self.transaction, self.PIPE
        ).compile()

        return self

    def execute(
        self,
        results: RecalcResults
    ) -> None:
        inputs = ExecutionInputs.from_plan(
            self.transaction, self.execution_plan, results
        )

        for calc_plan in self.execution_plan:
            calc = calc_plan.calculator(calc_plan.scope, inputs, results)

            results.collect(
                calc_plan.calculator,
                calc.calculate().assign(transaction_id=self.transaction.uuid),
            )