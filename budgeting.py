import reactive_dates
from reactive_dates import DateRange
from typing import NamedTuple, List
from decimal import Decimal
from datetime import date

Money = Decimal  # TODO...really should be decimal


class BudgetItem(NamedTuple):
    name: str
    amount: Money
    date_predicate: reactive_dates.DatePredicate


class Transaction(NamedTuple):
    name: str
    amount: Money
    date: date


class SummaryTransaction(NamedTuple):
    transaction: Transaction
    balance: Money


def gen_budget(budget_items: List[BudgetItem], from_to: DateRange) -> List[Transaction]:
    result: List[Transaction] = []
    for bi in budget_items:
        event_dates = filter(bi.date_predicate, reactive_dates.daily(from_to))
        result.extend([Transaction(bi.name, bi.amount, ed) for ed in event_dates])
    return result


def summarize_transactions(transactions: List[Transaction]) -> List[SummaryTransaction]:
    result: List[SummaryTransaction] = []
    running_total = Money('0.00')
    for transaction in transactions:
        running_total = running_total + transaction.amount
        summary_transaction = SummaryTransaction(transaction, running_total)
        result.append(summary_transaction)
    return result


def generate_budget(items: List[BudgetItem], date_range: DateRange) -> List[SummaryTransaction]:
    transactions: List[Transaction] = gen_budget(items, date_range)
    sorted_transactions: List[Transaction] = sorted(transactions, key=lambda b: b.date)
    return summarize_transactions(sorted_transactions)
