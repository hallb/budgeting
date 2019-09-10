import unittest
from datetime import date as d, timedelta as td
from budgeting import *


class TestSavingsAndBudget(unittest.TestCase):

    def test_budget_specified_transaction_on_day(self):
        a_date = d(2018, 1, 1)
        budget_spec = BudgetSpec("apple", Money('123.45'), reactive_dates.onL(a_date))
        self.assertTrue(budget_specified_transaction_on_day(budget_spec, a_date))
        self.assertFalse(budget_specified_transaction_on_day(budget_spec, a_date + td(1)))

    def test_generate_budget(self):
        from_to = (d(2017, 11, 23), d(2018, 11, 23))

        budget_specs = [
            BudgetSpec('Opening Balance', Money('123.45'), reactive_dates.onL(d(2017, 11, 23))),
            BudgetSpec('Hydro Offset', Money('67.89'), reactive_dates.onL(d(2017, 11, 24)))
        ]
        actual = project_budget(budget_specs, from_to)
        expected = [SummaryTransaction(Transaction("Opening Balance", Money('123.45'), d(2017, 11, 23)), Money('123.45')),
                    SummaryTransaction(Transaction("Hydro Offset", Money('67.89'), d(2017, 11, 24)), Money('191.34'))]
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
