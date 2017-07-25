from datetime import date, timedelta


def read_lines():
    with open('data.csv') as f:
        lines = [line.strip().split(',') for line in f.readlines()[-1:0:-1]]
        return lines


def htmlize_price():
    data = []
    for line in read_lines():
        print(read_lines())
        timestamp = line[0]
        price_list = ['{0:,}'.format(int(float(price))) for price in line[1:]]
        td_list = ['<td>{}</td>'.format(item) for item in [timestamp] + price_list]
        row = '<tr>{}</tr>'.format(''.join(td_list))
        data.append(row)
    return ''.join(data)


def htmlize_rate():
    today = date.today().strftime('%m/%d')
    days_before = (date.today() + timedelta(-7)).strftime('%m/%d')
    curr, prev = (None, None)
    for line in read_lines():
        mmdd = line[0][:5]
        price_list = line[1:]
        if mmdd == today:
            curr = [int(float(i)) for i in price_list]
            continue
        if mmdd == days_before:
            prev = [int(float(i)) for i in price_list]
            break
    if curr is None or prev is None:
        return ''

    rate_list = ['{:.2f}%'.format((100 * (a - b) / b)) for a, b in zip(curr, prev)]
    name = 'RSI(7)'
    td_list = ['<td>{}</td>'.format(item) for item in [name] + rate_list]
    row = '<tr>{}</tr>'.format(''.join(td_list))
    return row


def render():
    template = '''
        <html>
        <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css">
        <script src="https://code.jquery.com/jquery-3.2.1.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js"></script>
        </head>
        <body>
            <table class="table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>BTC</th>
                        <th>ETH</th>
                        <th>DASH</th>
                        <th>LTC</th>
                        <th>ETC</th>
                        <th>XRP</th>
                    </tr>
                </thead>
                <tbody>{}{}</tbody>
            </table>
            </body>
        </html>
        '''
    return template.format(htmlize_rate(), htmlize_price())
