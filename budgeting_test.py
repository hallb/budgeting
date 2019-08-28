import unittest
from datetime import date as d

from budgeting import BudgetItem, gen_budget, generate_budget, SummaryTransaction, Transaction, Money
import reactive_dates


class TestSavingsAndBudget(unittest.TestCase):

    def test_gen_budget(self):
        budget_item_1 = BudgetItem("apple", Money('123.45'), reactive_dates.onL(d(2018, 1, 1)))
        budget_item_2 = BudgetItem("banana", Money('234.45'), reactive_dates.onL(d(2018, 1, 2)))
        budget_items = [budget_item_1, budget_item_2]
        actual = gen_budget(budget_items, (d(2017, 8, 15), d(2018, 8, 15)))

        self.assertEqual(2, len(actual))
        self.assert_equal_budget_item(budget_item_1, actual[0])
        self.assert_equal_budget_item(budget_item_2, actual[1])

    def test_generate_budget(self):
        from_to = (d(2017, 11, 23), d(2018, 11, 23))

        budget_items = [
            BudgetItem('Opening Balance', Money('123.45'), reactive_dates.onL(d(2017, 11, 23))),
            BudgetItem('Hydro Offset', Money('67.89'), reactive_dates.onL(d(2017, 11, 24)))
        ]
        actual = generate_budget(budget_items, from_to)
        expected = [SummaryTransaction(Transaction("Opening Balance", Money('123.45'), d(2017, 11, 23)), Money('123.45')),
                    SummaryTransaction(Transaction("Hydro Offset", Money('67.89'), d(2017, 11, 24)), Money('191.34'))]
        self.assertEqual(expected, actual)

    def assert_equal_budget_item(self, expected, actual):
        self.assertEqual(expected.name, actual.name)
        self.assertEqual(expected.amount, actual.amount)
        self.assertTrue(expected.date_predicate(actual.date))


if __name__ == '__main__':
    unittest.main()
