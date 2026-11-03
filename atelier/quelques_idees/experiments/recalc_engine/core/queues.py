from .transaction import Transaction


class RecalcQueues:

    def __init__(self, transactions: tuple[Transaction, ...]):
        queues = {"IB": [], "CB": []}

        for transaction in transactions:
            queues[transaction.division].append(transaction)

        self.ib, self.cb = map(tuple, queues.values())