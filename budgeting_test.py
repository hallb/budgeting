import unittest
from datetime import date as d

from budgeting import BudgetItem, gen_budget
import reactive_dates


class TestSavingsAndBudget(unittest.TestCase):

    def test_gen_budget(self):
        budget_item_1 = BudgetItem("apple", 123.45, reactive_dates.onL(d(2018, 1, 1)))
        budget_item_2 = BudgetItem("banana", 234.45, reactive_dates.onL(d(2018, 1, 2)))
        budget_items = [budget_item_1, budget_item_2]
        actual = gen_budget(budget_items, (d(2017, 8, 15), d(2018, 8, 15)))

        self.assertEqual(2, len(actual))
        self.assert_equal_budget_item(budget_item_1, actual[0])
        self.assert_equal_budget_item(budget_item_2, actual[1])

    def assert_equal_budget_item(self, expected, actual):
        self.assertEqual(expected['name'], actual['name'])
        self.assertEqual(expected['amount'], actual['amount'])
        self.assertTrue(expected['datep'](actual['date']))


if __name__ == '__main__':
    unittest.main()
