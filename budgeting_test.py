import unittest
from datetime import date as d

from budgeting import BudgetItem, gen_budget, generate_budget
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

    def test_generate_budget(self):
        from_to = (d(2017, 11, 23), d(2018, 11, 23))

        budget_items = [
            BudgetItem('Opening Balance', 123.45, reactive_dates.onL(d(2017, 11, 23))),
            BudgetItem('Hydro Offset', 67.89, reactive_dates.onL(d(2017, 11, 24)))
        ]
        actual = generate_budget(budget_items, from_to)
        expected = [{'balance': 0},
                    {'amount': 123.45,
                     'balance': 123.45,
                     'date': d(2017, 11, 23),
                     'name': 'Opening Balance'},
                    {'amount': 67.89,
                     'balance': 191.34,
                     'date': d(2017, 11, 24),
                     'name': 'Hydro Offset'}]
        self.assertEqual(expected, actual)

    def assert_equal_budget_item(self, expected, actual):
        self.assertEqual(expected['name'], actual['name'])
        self.assertEqual(expected['amount'], actual['amount'])
        self.assertTrue(expected['datep'](actual['date']))


if __name__ == '__main__':
    unittest.main()
