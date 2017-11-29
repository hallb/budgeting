import reactive_dates


def BudgetItem(name, amount, datep=None):
    return {
        'name': name,
        'amount': amount,
        'datep': datep
    }


def amount_sum(budget):
    result = 0
    for budgetItem in budget:
        result += budgetItem['amount']
    return result


def gen_budget(budget_items, from_to):
    result = []
    for bi in budget_items:
        event_dates = filter(bi['datep'], reactive_dates.daily(from_to))
        result.extend([{
            'name': bi['name'],
            'amount': bi['amount'],
            'date': ed
        } for ed in event_dates])
    return result


def bi_sum(bi1, bi2):
    result = dict(bi2)
    result['balance'] = bi1['balance'] + bi2['amount']
    return result
