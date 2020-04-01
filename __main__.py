import stockquotes
import json

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

portfolio_data = []
for stock in portfolio.keys():
    if portfolio[stock] == 0:
        continue
    elif stock == 'CASH':
        cash = portfolio[stock]
    else:
        stock_data = stockquotes.Stock(stock)
        portfolio_data.append([stock, portfolio[stock], stock_data.currentPrice])

total = sum([ i[1]*i[2] for i in portfolio_data ]) + cash

longest_qty = 3
for stock in portfolio_data:
    length = len(money(stock[1]))
    longest_qty = length if length > longest_qty else longest_qty

longest_stock = 5
for stock in portfolio_data:
    length = len(stock[0])
    longest_stock = length if length > longest_stock else longest_stock

header = '│{}│{}│    Last   Total  %Total│'.format(pada('Stock', longest_stock), pad('Qty', longest_qty))
print('┌{}┐'.format('─' * (len(header)-2)))
print(header)
print('├{}┤'.format('─' * (len(header)-2)))
for stock in portfolio_data:
    print('{}|{}|{}|{}|{}%'.format(
        pada(stock[0], longest_stock),
        pad(stock[1], longest_qty),
        pad(money(stock[2]), longest_qty + 1),
        pad(money(stock[1]*stock[2]), 8),
        pad(round((stock[1]*stock[2])/total * 100), 7)
    ))

print('Cash                    {}{}%'.format(pad(cash, 8), pad(round((cash/total)*100), 7)))
print('Total                   {}    100%'.format(pad(money(total), 8)))
