import unittest
from datetime import date as d

from budgeting import BudgetSpec, gen_budget, generate_budget, SummaryTransaction, Transaction, Money
import reactive_dates


class TestSavingsAndBudget(unittest.TestCase):

    def test_gen_budget(self):
        budget_spec_1 = BudgetSpec("apple", Money('123.45'), reactive_dates.onL(d(2018, 1, 1)))
        budget_spec_2 = BudgetSpec("banana", Money('234.45'), reactive_dates.onL(d(2018, 1, 2)))
        budget_specs = [budget_spec_1, budget_spec_2]
        actual = gen_budget(budget_specs, (d(2017, 8, 15), d(2018, 8, 15)))

        self.assertEqual(2, len(actual))
        self.assert_equal_budget_specs(budget_spec_1, actual[0])
        self.assert_equal_budget_specs(budget_spec_2, actual[1])

    def test_generate_budget(self):
        from_to = (d(2017, 11, 23), d(2018, 11, 23))

        budget_specs = [
            BudgetSpec('Opening Balance', Money('123.45'), reactive_dates.onL(d(2017, 11, 23))),
            BudgetSpec('Hydro Offset', Money('67.89'), reactive_dates.onL(d(2017, 11, 24)))
        ]
        actual = generate_budget(budget_specs, from_to)
        expected = [SummaryTransaction(Transaction("Opening Balance", Money('123.45'), d(2017, 11, 23)), Money('123.45')),
                    SummaryTransaction(Transaction("Hydro Offset", Money('67.89'), d(2017, 11, 24)), Money('191.34'))]
        self.assertEqual(expected, actual)

    def assert_equal_budget_specs(self, expected, actual):
        self.assertEqual(expected.name, actual.name)
        self.assertEqual(expected.amount, actual.amount)
        self.assertTrue(expected.date_predicate(actual.date))


if __name__ == '__main__':
    unittest.main()
