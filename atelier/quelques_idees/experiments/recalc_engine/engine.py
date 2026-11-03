from __future__ import annotations

import multiprocessing as mp
from typing import Self

from .config.results import RecalcResults
from .core.queues import RecalcQueues
from .core.transaction import Transaction
from .execution.pipeline import Pipeline


class RecalcEngine:
    def __init__(self, *transaction_ids):
        self.transactions = tuple(Transaction(id) for id in transaction_ids)
        self.queues = RecalcQueues(self.transactions)

    @staticmethod
    def _execute_pipeline(transactions: tuple[Transaction, ...]) -> RecalcResults:
        results = RecalcResults()

        for transaction in transactions:
            Pipeline(transaction).compile().execute(results)

        return results

    def run(self) -> Self:
        with mp.Pool(processes=2) as pool:
            division_results = pool.map(
                RecalcEngine._execute_pipeline,
                (self.queues.ib, self.queues.cb),
            )

        self.results = RecalcResults.consolidate(*division_results)

        return self