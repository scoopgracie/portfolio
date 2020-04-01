import stockquotes
import json

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

longest_percent = 3
for stock in portfolio_data:
    length = len(str(round(((stock[1]*stock[2])/total)*100)))
    longest_percent = length if length > longest_percent else longest_percent

print('Stock        Qty    Last   Total  %Total')
print('-'*8*5)
for stock in portfolio_data:
    print('{}\t{}{}{}{}%'.format(
        stock[0],
        pad(stock[1], 8),
        pad(money(stock[2]), 8),
        pad(money(stock[1]*stock[2]), 8),
        pad(round((stock[1]*stock[2])/total * 100), 7)
    ))

print('Cash                    {}{}%'.format(pad(cash, 8), pad(round((cash/total)*100), 7)))
print('Total                   {}    100%'.format(pad(money(total), 8)))
