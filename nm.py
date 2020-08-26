import stockquotes
import json
import threading
simple_graphics = False 
if simple_graphics:
    _print = print
    def print(text):
        text = text\
            .replace('╭', '┌')\
            .replace('╮', '┐')\
            .replace('╰', '└')\
            .replace('╯', '┘')\
            .replace('┝', '├')\
            .replace('━', '─')\
            .replace('┥', '┤')\
            .replace('┿', '┼')\
            .replace('╞', '├')\
            .replace('═', '─')\
            .replace('╡', '┤')\
            .replace('╪', '┼')
        _print(text)

def pada(string, length):
    string = str(string)
    string = string + ' '*(length - len(string))
    return string

def pad(string, length):
    string = str(string)
    string = ' '*(length - len(string)) + string
    return string

def money(amount):
    amount = str(round(amount*100)/100)
    if len(amount.split('.')) == 1:
        return '{}.00'.format(amount)
    elif len(amount.split('.')[1]) == 1:
        return '{}0'.format(amount)
    else:
        return amount

with open('portfolio.json') as f:
    portfolio = json.load(f)

def get_stock(stock, portfolio_data):
    stock_data = stockquotes.Stock(stock)
    portfolio_data.append([stock, portfolio[stock], stock_data.currentPrice])

portfolio_data = []
threads = []
for stock in portfolio.keys():
    if portfolio[stock] == 0:
        continue
    elif stock == '_CASH_':
        cash = portfolio[stock]
    else:
        t = threading.Thread(target=get_stock, args=(stock, portfolio_data,))
        threads.append(t)
        t.start()

for t in threads:
    t.join()

portfolio_data.sort(key=lambda l:l[0])

total = sum([ i[1]*i[2] for i in portfolio_data ]) + cash

longest_qty = 3
longest_stock = 5
longest_last = 4
longest_total = len(money(total)) if len(money(total)) > 5 else 5
for stock in portfolio_data:
    length = len(money(stock[1]))
    longest_qty = length if length > longest_qty else longest_qty
    length = len(stock[0])
    longest_stock = length if length > longest_stock else longest_stock
    length = len(money(stock[2]))
    longest_last = length if length > longest_last else longest_last
    length = len(money(stock[2]*stock[1]))
    longest_total = length if length > longest_total else longest_total

headings = [ pada('Stock', longest_stock), pad('Qty', longest_qty), pad('Last', longest_last), pad('Total', longest_total), '%Total' ]
header = '│{}│{}│{}│{}│{}│'.format(*headings)
print('╭{}┬{}┬{}┬{}┬{}╮'.format( *[ ('─' * len(i)) for i in headings] ))
print(header)
print('┝{}┿{}┿{}┿{}┿{}┥'.format( *[ ('━' * len(i)) for i in headings] ))
for stock in portfolio_data:
    print('│{}│{}│{}│{}│{}│'.format(
        pada(stock[0], longest_stock),
        pad(stock[1], longest_qty),
        pad(money(stock[2]), longest_last),
        pad(money(stock[1]*stock[2]), longest_total),
        pad(round((stock[1]*stock[2])/total * 100), 5) + '%'
    ))

print('├{}┼{}┼{}┼{}┼{}┤'.format( *[ ('─' * len(i)) for i in headings] ))
print('│{}│{}│{}│{}│{}│'.format(
    pada('Cash', longest_stock),
    ' ' * longest_qty,
    ' ' * longest_last,
    pad(money(cash), longest_total),
    pad(round(cash/total * 100), 5) + '%'
))
print('╞{}╪{}╪{}╪{}╪{}╡'.format( *[ ('═' * len(i)) for i in headings] ))
print('│{}│{}│{}│{}│{}│'.format(
    pada('Total', longest_stock),
    ' ' * longest_qty,
    ' ' * longest_last,
    pad(money(total), longest_total),
    pad('100', 5) + '%'
))
print('╰{}┴{}┴{}┴{}┴{}╯'.format( *[ ('─' * len(i)) for i in headings] ))
