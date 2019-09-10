import reactive_dates
from reactive_dates import DateRange
from typing import NamedTuple, List, Iterator, TypeVar, Callable, Optional
from functools import partial
from decimal import Decimal
from datetime import date


# Domain definitions
Money = Decimal


class BudgetSpec(NamedTuple):
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


def budget_specified_transaction_on_day(spec: BudgetSpec, day: date) -> Optional[Transaction]:
    return Transaction(spec.name, spec.amount, day) if spec.date_predicate(day) else None


def transactions_for_budget_on_day(budget_specs: List[BudgetSpec], day: date) -> Iterator[Transaction]:
    for spec in budget_specs:
        transaction = budget_specified_transaction_on_day(spec, day)
        if transaction is not None:
            yield transaction


def increment_summary_transaction(previous: SummaryTransaction, current: Transaction) -> SummaryTransaction:
    previous_balance = Money('0.00') if previous is None else previous.balance
    return SummaryTransaction(current, previous_balance + current.amount)


def project_budget(budget_specs: List[BudgetSpec], date_range: DateRange) -> List[SummaryTransaction]:
    return list(project_budget_iterator(budget_specs, date_range))


def project_budget_iterator(budget_specs, date_range):
    # Curry the budget_specs into the Transactions generator
    transactions_for_day = partial(transactions_for_budget_on_day, budget_specs)
    # Step 1. What are the dates?
    dates = reactive_dates.daily(date_range)
    # Step 2. What are the transactions for those dates?
    transactions = flat_map_iterator(dates, transactions_for_day)
    # Step 3. What's the running balance?
    z: SummaryTransaction = None  # Needed a type hint.
    summary_transactions = scan_left_iterator(transactions, z, increment_summary_transaction)
    return summary_transactions


# TODO: move to a utility module
A = TypeVar('A')
B = TypeVar('B')


# TODO: move to a utility module
def flat_map_iterator(it: Iterator[A], f: Callable[[A], Iterator[B]]) -> Iterator[B]:
    for i in it:
        for j in f(i):
            yield j


# TODO: move to a utility module
def scan_left_iterator(it: Iterator[A], z: B, f: Callable[[B, A], B]) -> Iterator[B]:
    previous = z
    for i in it:
        previous = f(previous, i)
        yield previous
