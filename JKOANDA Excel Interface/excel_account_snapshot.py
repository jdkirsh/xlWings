import requests
import xlsxwriter
import json
import time
import sys
import os

def GetValue(values, key):
    if (values is not None and values.has_key(key)):
        return values[key]
    else:
        return ''
        
def GetDuration(transaction):
    if (transaction is not None):
        r = requests.get(target_host + '/v3/accounts/' + str(transaction['accountId']) + '/transactions/' + str(transaction['tradeId']), headers=headers)
        opening_transaction = r.json()
        closing = time.mktime(time.strptime(transaction['time'], "%Y-%m-%dT%H:%M:%S.000000Z"))
        opening = time.mktime(time.strptime(opening_transaction['time'], "%Y-%m-%dT%H:%M:%S.000000Z"))
        return closing - opening
    else:
        return 0

def SetUpWorkbook():
    worksheet1.hide_gridlines(3)
    worksheet1.set_row('1:1', 20)
    worksheet1.insert_image('A1', 'oanda_logo.png')

    small_bold.set_bold()
    small_bold.set_font_size(9)

    small.set_font_size(9)
    small.set_align('left')

    green.set_bold()
    green.set_pattern(1)
    green.set_bg_color('#00FF00')
    green.set_font_color('#333333')

    blue.set_bold()
    blue.set_pattern(1)
    blue.set_bg_color('#0080FF')
    blue.set_font_color('#333333')

    red.set_bold()
    red.set_pattern(1)
    red.set_bg_color('#FE2E2E')
    red.set_font_color('#333333')    

    orange.set_bold()
    orange.set_pattern(1)
    orange.set_bg_color('#F79F81')
    orange.set_font_color('#333333')

def PopulateAccountInfo( account_info ):
    # Check if valid
    # if ( not account_info.has_key('accountId') ):
    if (not account_info.has_key('account')):
        print "Invalid account ID!"
        workbook.close()
        exit(-1)
    
    worksheet1.write('A3', 'Account snapshot created at: ' +  time.strftime("%c"), small_bold)
    worksheet1.write('A5', 'Account Summary', green)
    worksheet1.write('B5', '', green)

    worksheet1.set_row(5, 2)
    for col in range(0,8):
        worksheet1.write(5, col, '', green)

    worksheet1.write('A7', 'Account ID: ', small_bold)
    # worksheet1.write('C7', account_info['accountId'], small)
    worksheet1.write('C7', str(account_info['account']['id']), small)

    worksheet1.write('E7', 'Account Name: ', small_bold)
    # worksheet1.write('G7', account_info['accountName'], small)
    worksheet1.write('G7', str(account_info['account']['alias']), small)

    worksheet1.write('A8', 'Balance: ', small_bold)
    # worksheet1.write('C8', account_info['balance'], small)
    worksheet1.write('C8', str(account_info['account']['balance']) , small)

    worksheet1.write('E8', 'Unrealized P/L: ', small_bold)
    # worksheet1.write('G8', account_info['unrealizedPl'], small)
    worksheet1.write('G8', str(account_info['account']['unrealizedPL']), small)

    worksheet1.write('A9', 'NAV: ', small_bold)
    # worksheet1.write('C9', account_info['balance'] + account_info['unrealizedPl'], small)
    worksheet1.write('C9', str(account_info['account']['NAV']) , small)

    worksheet1.write('E9', 'Realized P/L: ', small_bold)
    # worksheet1.write('G9', account_info['realizedPl'], small)
    worksheet1.write('G9', 'N/A', small)

    worksheet1.write('A10', 'Margin Used: ', small_bold)
    # worksheet1.write('C10', account_info['marginUsed'], small)
    worksheet1.write('C10', str(account_info['account']['marginUsed']), small)

    worksheet1.write('E10', 'Margin Available: ', small_bold)
    # worksheet1.write('G10', account_info['marginAvail'], small)
    worksheet1.write('G10', str(account_info['account']['marginAvailable']), small)

    worksheet1.write('A11', 'Home Currency: ', small_bold)
    # worksheet1.write('C11', account_info['accountCurrency'], small)
    worksheet1.write('C11', str(account_info['account']['currency']), small)

    worksheet1.write('E11', 'Margin Rate: ', small_bold)
    # margin_rate = int(1.0 / account_info['marginRate'])
    margin_rate = int(1.0 / float(account_info['account']['marginRate']) )
    worksheet1.write('G11', str(margin_rate) + ':1', small)

def PopulateAccountStatus(recent_transactions):
    global position_row
    num_winners = 0
    num_losers = 0
    profit = 0.0
    loss = 0.0
    max_stay = 0.0
    total_stay = 0.0
    num_long = 0
    num_short = 0
    num_long_winner = 0
    num_short_winner = 0
    profit_by_pair = {}
    max_profit = None
    min_profit = None
    best_trade = None
    worst_trade = None
    
    trans_row = 0
    worksheet2.write(trans_row, 0, 'ID', small_bold)
    worksheet2.write(trans_row, 1, 'Account ID', small_bold)
    worksheet2.write(trans_row, 2, 'Time', small_bold)
    worksheet2.write(trans_row, 3, 'Type', small_bold)
    worksheet2.write(trans_row, 4, 'Instrument', small_bold)
    worksheet2.write(trans_row, 5, 'Units', small_bold)
    worksheet2.write(trans_row, 6, 'Side', small_bold)
    worksheet2.write(trans_row, 7, 'Price', small_bold)
    worksheet2.write(trans_row, 8, 'Lower Bound', small_bold)
    worksheet2.write(trans_row, 9, 'Upper Bound', small_bold)
    worksheet2.write(trans_row, 10, 'Take Profit', small_bold)
    worksheet2.write(trans_row, 11, 'Stop Loss', small_bold)
    worksheet2.write(trans_row, 12, 'Trailing Stop Loss Distance', small_bold)
    worksheet2.write(trans_row, 13, 'Profit/Loss', small_bold)
    worksheet2.write(trans_row, 14, 'Interest', small_bold)
    worksheet2.write(trans_row, 15, 'Balance', small_bold)
    worksheet2.write(trans_row, 16, 'Trade ID', small_bold)
    worksheet2.write(trans_row, 17, 'Expiry', small_bold)
    worksheet2.write(trans_row, 18, 'Reason', small_bold)

    for transaction in recent_transactions:
        trans_row += 1
        worksheet2.write(trans_row, 0, GetValue(transaction, 'id'), small)
        worksheet2.write(trans_row, 1, GetValue(transaction, 'accountId'), small)
        worksheet2.write(trans_row, 2, GetValue(transaction, 'time'), small)
        worksheet2.write(trans_row, 3, GetValue(transaction, 'type'), small)
        worksheet2.write(trans_row, 4, GetValue(transaction, 'instrument'), small)
        worksheet2.write(trans_row, 5, GetValue(transaction, 'units'), small)
        worksheet2.write(trans_row, 6, GetValue(transaction, 'side'), small)
        worksheet2.write(trans_row, 7, GetValue(transaction, 'price'), small)
        worksheet2.write(trans_row, 8, GetValue(transaction, 'lowerBound'), small)
        worksheet2.write(trans_row, 9, GetValue(transaction, 'upperBound'), small)
        worksheet2.write(trans_row, 10, GetValue(transaction, 'takeProfitPrice'), small)
        worksheet2.write(trans_row, 11, GetValue(transaction, 'stopLossPrice'), small)
        worksheet2.write(trans_row, 12, GetValue(transaction, 'trailingStopLossDistance'), small)
        worksheet2.write(trans_row, 13, GetValue(transaction, 'pl'), small)
        worksheet2.write(trans_row, 14, GetValue(transaction, 'interest'), small)
        worksheet2.write(trans_row, 15, GetValue(transaction, 'accountBalance'), small)
        worksheet2.write(trans_row, 16, GetValue(transaction, 'tradeId'), small)
        worksheet2.write(trans_row, 17, GetValue(transaction, 'expiry'), small)
        worksheet2.write(trans_row, 18, GetValue(transaction, 'reason'), small)
        
        if (transaction['type'] == 'TRADE_CLOSE'):
            if (transaction['pl'] > 0):
                num_winners += 1
                profit += transaction['pl']
                if (profit_by_pair.has_key(transaction['instrument'])):
                    profit_by_pair[transaction['instrument']] += transaction['pl']
                else:
                    profit_by_pair[transaction['instrument']] = transaction['pl']
            elif (transaction['pl'] <= 0):
                num_losers += 1
                loss += transaction['pl']
                if (profit_by_pair.has_key(transaction['instrument'])):
                    profit_by_pair[transaction['instrument']] += transaction['pl']
                else:
                    profit_by_pair[transaction['instrument']] = transaction['pl']
            
            if (transaction['side'] == 'sell'):
                num_long += 1
                if (transaction['pl'] > 0):
                    num_long_winner += 1
            elif (transaction['side'] == 'buy'):
                num_short += 1
                if (transaction['pl'] > 0):
                    num_short_winner += 1

            if ( max_profit is None ):
                max_profit = transaction['pl']
            if ( min_profit is None ):
                min_profit = transaction['pl']
            
            if (transaction['pl'] >= max_profit):
                max_profit = transaction['pl']
                best_trade = transaction
            
            if (transaction['pl'] <= min_profit):
                min_profit = transaction['pl']
                worst_trade = transaction
                
            duration = GetDuration(transaction)
            
            total_stay += duration
            if (duration > max_stay):
                max_stay = duration

    position_row = 13
    worksheet1.write(position_row, 0, '30 Day Statistics', red)
    worksheet1.write(position_row, 1, '', red)        
    position_row += 1
    worksheet1.set_row(position_row, 2)
    for col in range(0,8):
        worksheet1.write(position_row, col, '', red)
    position_row += 1
    
    worksheet1.write(position_row, 0, '# Total Trades: ', small_bold)
    worksheet1.write(position_row, 2, num_winners + num_losers, small)
    worksheet1.write(position_row, 3, 'Winners:', small_bold)
    worksheet1.write(position_row, 4, num_winners, small)
    worksheet1.write(position_row, 5, 'Losers:', small_bold)
    worksheet1.write(position_row, 6, num_losers, small)
    position_row += 1
    worksheet1.write(position_row, 0, 'Long Trades (% Winners; #): ', small_bold)
    worksheet1.write(position_row, 3, str(num_long_winner * 100.0 / max(num_long,1)) + '%; ' + str(num_long) , small)
    position_row += 1
    worksheet1.write(position_row, 0, 'Short Trades (% Winners; #):', small_bold)
    worksheet1.write(position_row, 3, str(num_short_winner * 100.0 / max(num_short,1)) + '%; ' + str(num_short), small)
    position_row += 1
    worksheet1.write(position_row, 0, 'Avg P/L per Trade:', small_bold)
    worksheet1.write(position_row, 2, (profit + loss) / max(1,(num_winners + num_losers)), small)
    worksheet1.write(position_row, 3, 'Avg Profit:', small_bold)
    worksheet1.write(position_row, 4, profit / max(1,num_winners), small)
    worksheet1.write(position_row, 5, 'Avg Loss:', small_bold)
    worksheet1.write(position_row, 6, loss / max(1,num_losers), small)
    position_row += 1
    worksheet1.write(position_row, 0, 'Max Length Stay (Hours):', small_bold)
    worksheet1.write(position_row, 3, max_stay / 60.0 / 60.0, small)
    position_row += 1
    worksheet1.write(position_row, 0, 'Average Length Stay (Hours):', small_bold)
    worksheet1.write(position_row, 3, total_stay / max(1,(num_winners+num_losers)) / 60.0 / 60.0, small)
    position_row += 1
    worksheet1.write(position_row, 0, 'Profit by Instruments:', small_bold)
    position_row += 1
    chart_row = position_row - 1

    profit_by_pair_min = None
    profit_by_pair_max = None
    for key, value in profit_by_pair.iteritems():
        if ( profit_by_pair_min is None ):
            profit_by_pair_min = value
            profit_by_pair_max = value
        worksheet1.write(position_row, 0, key, small)
        worksheet1.write(position_row, 1, value, small)
        position_row += 1
        if ( value < profit_by_pair_min ):
            profit_by_pair_min = value
        if ( value > profit_by_pair_max ):
            profit_by_pair_max = value

    if (len(profit_by_pair.keys()) > 0 ):
        chart_profit_by_pair = workbook.add_chart({'type': 'bar'})

        # Configure the series. Note the use of the list syntax to define ranges:
        chart_profit_by_pair.add_series({
            'categories': ['Account_Snapshot', chart_row + 1, 0, chart_row + len(profit_by_pair.keys()), 0],
            'values':     ['Account_Snapshot', chart_row + 1, 1, chart_row + len(profit_by_pair.keys()), 1]
        })

        chart_profit_by_pair.set_x_axis({'num_font':  {'name': 'Arial', 'size': 5}})
        chart_profit_by_pair.set_y_axis({'num_font':  {'name': 'Arial', 'size': 5}})
        chart_profit_by_pair.set_style(11)
        chart_profit_by_pair.set_size({'width': 400, 'height': 25 + len(profit_by_pair.keys()) * 30})
        chart_profit_by_pair.set_legend({'none': True})

        worksheet1.insert_chart(chart_row, 2, chart_profit_by_pair)
    
    position_row += max(0, len(profit_by_pair.keys()) - 2)
    
    worksheet1.write(position_row, 0, 'Best Trade:', small_bold)
    worksheet1.write(position_row, 4, 'Worst Trade:', small_bold)
    position_row += 1
    worksheet1.write(position_row, 0, 'Trans ID:', small)
    worksheet1.write(position_row, 1, GetValue(best_trade, 'tradeId'), small)
    worksheet1.write(position_row, 4, 'Trans ID:', small)
    worksheet1.write(position_row, 5, GetValue(worst_trade, 'tradeId'), small)
    position_row += 1
    worksheet1.write(position_row, 0, 'Instrument:', small)
    worksheet1.write(position_row, 1, GetValue(best_trade, 'instrument'), small)
    worksheet1.write(position_row, 4, 'Instrument:', small)
    worksheet1.write(position_row, 5, GetValue(worst_trade, 'instrument'), small)
    position_row += 1
    worksheet1.write(position_row, 0, 'Units:', small)
    worksheet1.write(position_row, 1, GetValue(best_trade, 'units'), small)
    worksheet1.write(position_row, 4, 'Units:', small)
    worksheet1.write(position_row, 5, GetValue(worst_trade, 'units'), small)
    position_row += 1
    worksheet1.write(position_row, 0, 'Direction:', small)
    if (GetValue(best_trade, 'side') == 'sell'): 
        direction = 'Long'
    else:
        direction = 'Short'
    worksheet1.write(position_row, 1, direction, small)
    worksheet1.write(position_row, 4, 'Direction:', small)
    if (GetValue(worst_trade, 'side') == 'sell'): 
        direction = 'Long'
    else:
        direction = 'Short'        
    worksheet1.write(position_row, 5, direction, small)
    position_row += 1
    worksheet1.write(position_row, 0, 'P/L:', small)
    worksheet1.write(position_row, 1, GetValue(best_trade, 'pl'), small)
    worksheet1.write(position_row, 4, 'P/L:', small)
    worksheet1.write(position_row, 5, GetValue(worst_trade, 'pl'), small)
    position_row += 1
    worksheet1.write(position_row, 0, 'Duration:', small)
    worksheet1.write(position_row, 1, str(GetDuration(best_trade)/3600)+ ' hours', small)
    worksheet1.write(position_row, 4, 'Duration:', small)
    worksheet1.write(position_row, 5, str(GetDuration(worst_trade)/3600)+ ' hours', small)
    
def PopulateOpenPositions( positions ):
    global position_row
    position_row += 1
    position_row += 1
    position_row += 1
    worksheet1.write(position_row, 0, 'Open Positions', blue)
    worksheet1.write(position_row, 1, '', blue)        
    position_row += 1
    worksheet1.set_row(position_row, 2)
    for col in range(0,8):
        worksheet1.write(position_row, col, '', blue)
    
    position_row += 1    
    worksheet1.write(position_row, 0, 'Symbol', small_bold)
    worksheet1.write(position_row, 2, 'Units', small_bold)
    worksheet1.write(position_row, 4, 'Avg. Price', small_bold)
    worksheet1.write(position_row, 6, 'Direction', small_bold)
    
    position_row += 1
    chart_cats = []
    chart_vals = []
    num_positions = 0
    # KeyError: 'units'
    for position in positions:
        position_info = str(position['units']) + ' ' + position['instrument'] + ' @ ' + str(position['avgPrice']) + ' '
        if ( position['side'] == 'buy' ):
            direction = 'LONG'
        else:
            direction = 'SHORT'
        position_info += direction
        worksheet1.write(position_row, 0, position['instrument'], small)
        worksheet1.write(position_row, 2, str(position['units']), small)
        worksheet1.write(position_row, 4, str(position['avgPrice']), small)
        worksheet1.write(position_row, 6, direction, small)
        
        position_row += 1
        chart_cats.append(position_info)
        chart_vals.append(position['units'])
        num_positions += 1
    

    worksheet3.write_column('A1', chart_cats)
    worksheet3.write_column('B1', chart_vals)

    if (len(positions) > 0):
        open_position_chart = workbook.add_chart({'type': 'pie'})

        # Configure the series. Note the use of the list syntax to define ranges:
        open_position_chart.add_series({
            'categories': ['Sheet3', 0, 0, num_positions-1, 0],
            'values':     ['Sheet3', 0, 1, num_positions-1, 1]
        })

        open_position_chart.set_style(10)
        open_position_chart.set_size({'width': 300, 'height': 190})
        worksheet1.insert_chart(position_row, 1, open_position_chart)

def PopulateCurrentRates( positions ):
    global position_row
    if (len(positions) > 0 ):
        position_row += 10
    position_row += 2
    worksheet1.write(position_row, 0, 'Current Rates', orange)
    worksheet1.write(position_row, 1, '', orange)        
    position_row += 1
    worksheet1.set_row(position_row, 2)
    for col in range(0,8):
        worksheet1.write(position_row, col, '', orange)
    position_row += 1
    worksheet1.write(position_row, 0, 'Symbol', small_bold)
    worksheet1.write(position_row, 3, 'Bid', small_bold)
    worksheet1.write(position_row, 6, 'Ask', small_bold)
    position_row += 1
    for position in positions:
        r = requests.get(target_host + '/v1/prices?instruments=' + position['instrument'], headers=headers)
        prices = (r.json())['prices']
        worksheet1.write(position_row, 0, prices[0]['instrument'], small)
        worksheet1.write(position_row, 3, prices[0]['bid'], small)
        worksheet1.write(position_row, 6, prices[0]['ask'], small)
        position_row += 1

    cur_column = 0
    first_col = True
    for position in positions:
        r = requests.get(target_host + '/v1/candles?instrument=' + position['instrument'] + '&granularity=H1&count=24&candleFormat=bidask', headers=headers)
        prices = r.json()
        cur_row = 0
        for price in prices['candles']:
            worksheet4.write(cur_row, 0 + cur_column, price['time'])
            worksheet4.write(cur_row, 1 + cur_column, price['closeBid'])
            worksheet4.write(cur_row, 2 + cur_column, price['closeAsk'])
            cur_row += 1
            
        rates_chart = workbook.add_chart({'type': 'line'})
        rates_chart.add_series({
            'name':       'Close Bid',
            'categories': ['Sheet4', 0, cur_column, 24, cur_column],
            'values':     ['Sheet4', 0, cur_column+1, 24, cur_column+1],
        })
        
        rates_chart.add_series({
            'name':       'Close Ask',
            'categories': ['Sheet4', 0, cur_column, 24, cur_column],
            'values':     ['Sheet4', 0, cur_column+2, 24, cur_column+2],
        })

        rates_chart.set_style(10)
        rates_chart.set_title({'name': position['instrument'], 'name_font':  {'name': 'Arial', 'size': 5}})
        rates_chart.set_legend({'none': True})
        rates_chart.set_x_axis({'num_font':  {'name': 'Arial', 'size': 5}})
        rates_chart.set_y_axis({'num_font':  {'name': 'Arial', 'size': 5}})
        rates_chart.set_size({'width': 260, 'height': 200})
        
        if (first_col):
            worksheet1.insert_chart(position_row, 0, rates_chart)
        else:
            worksheet1.insert_chart(position_row, 4, rates_chart)
            position_row += 10
        first_col = not first_col
        cur_column += 3

if __name__ == '__main__':
    # if ( len(sys.argv) != 4 ):
    #     print "Usage: " + os.path.basename(__file__) + " SANDBOX|PRACTICE|TRADE account_id personal_access_token"
    #     exit(-1)
    #
    # account_id = sys.argv[2]
    # target_host = None
    #
    # if ( str(sys.argv[1]).upper() == 'SANDBOX' ):
    #     target_host = 'http://api-sandbox.oanda.com'
    # elif ( str(sys.argv[1]).upper() == 'PRACTICE' ):
    #     target_host = 'https://api-fxpractice.oanda.com'
    # elif ( str(sys.argv[1]).upper() == 'TRADE' ):
    #     target_host = 'https://api-fxtrade.oanda.com'
    # else:
    #     print "Invalid target. Please specify either SANDBOX, PRACTICE, or TRADE."
    #     exit(-1)
    #
    # personal_access_token = sys.argv[3]
    target_host = 'https://api-fxtrade.oanda.com'
    # target_host = 'https://api-fxpractice.oanda.com'

    account_id = '001-001-2033767-001'     # prod
    # account_id = '101-001-6636926-001'    # practice
    # personal_access_token = 'bc05fa130d462a39c9d181f053eb4002-5d129c81a25f312a7528a423e57ce83f'
    personal_access_token = 'd306f3de3e785713223c1334bba71090-7c2fa5664d3665c336bcad6199dad4a4'
    # practice_access_token = 'd306f3de3e785713223c1334bba71090-7c2fa5664d3665c336bcad6199dad4a4'
    headers = {'Authorization': 'Bearer ' + personal_access_token}
    # headers = {'Authorization': 'Bearer ' + practice_access_token}

    # headers = {'Authorization' : 'Bearer ' + personal_access_token}
    
    # Create and set up workbook
    workbook = xlsxwriter.Workbook('account_snapshot.xlsx')
    worksheet1 = workbook.add_worksheet('Account_Snapshot')
    worksheet2 = workbook.add_worksheet('Recent_Transactions')
    worksheet3 = workbook.add_worksheet()
    worksheet4 = workbook.add_worksheet()
    small_bold = workbook.add_format()
    small = workbook.add_format()
    green = workbook.add_format()
    blue = workbook.add_format()
    red = workbook.add_format()
    orange = workbook.add_format()
    position_row = 0
    SetUpWorkbook()
    
    # Get account info
    r = requests.get(target_host + '/v3/accounts/' + str(account_id), headers=headers)
    PopulateAccountInfo( r.json() )
    
    # Populate recent transactions and stats
    r = requests.get(target_host + '/v3/accounts/' + str(account_id) + '/transactions?count=500', headers=headers)
    if ( r.status_code != requests.codes.ok ):
        print "Error while retrieving transactions: " + (r.json())['message']
        workbook.close()
        exit(-1)        
    # PopulateAccountStatus( (r.json())['transactions'] )
    recent_transactions = []

    for page in r.json()['pages']:
        r = requests.get(page, headers=headers)
        recent_transactions.extend(r.json()['transactions'])


    # PopulateAccountStatus((r.json())['pages'])
    PopulateAccountStatus(recent_transactions)
    
    # Populate open positions
    # r = requests.get(target_host + '/v3/accounts/' + str(account_id) + '/positions', headers=headers)
    # PopulateOpenPositions( (r.json())['positions'] )

    # curl \
    # - H
    # "Content-Type: application/json" \
    # - H
    # "Authorization: Bearer <AUTHENTICATION TOKEN>" \
    # "https://api-fxtrade.oanda.com/v3/accounts/<ACCOUNT>/openPositions"

    r = requests.get(target_host + '/v3/accounts/' + str(account_id) + '/openPositions', headers=headers)
    PopulateOpenPositions((r.json())['positions'])
    # PopulateOpenPositions = r.json()['positions']
    
    # Populate current rates
    PopulateCurrentRates( (r.json())['positions'] )
    
    # Close workbook
    workbook.close()
