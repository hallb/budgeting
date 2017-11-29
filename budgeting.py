import reactive_dates
from rx import Observable, Observer


def BudgetItem(name, amount, datep=None):
    return {
        'name': name,
        'amount': amount,
        'datep': datep
    }


def amount_sum(budget):
    return Observable.from_(budget) \
            .map(lambda b: b['amount']) \
            .sum() \
            .to_future() \
            .result()


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


def reduce_list(fn, a_list, start):
    result = [start]
    prev = start
    for item in a_list:
        prev = fn(prev, item)
        result.append(prev)
    return result


def generate_budget(items, date_range):
    gb = gen_budget(items, date_range)
    sgb = sorted(gb, key=lambda b: b['date'])
    reduced_list = reduce_list(bi_sum, sgb, {'balance': 0})
    return reduced_list