from datetime import date, timedelta


def read_data(**kwargs):
    with open('data.csv') as f:
        lines = [line.strip().split(',') for line in f.readlines()[-1:0:-1]]
        if kwargs.get('select_all'):
            return lines

        for line in lines:
            timestamp = line[0]
            if timestamp[:5] == kwargs['date'].strftime('%m/%d'):
                # return [timestamp] + [int(float(i)) for i in line[1:]]
                return line


def htmlize_price():
    rows = []
    for line in read_data(select_all=True):
        timestamp = line[0]
        price_list = ['{0:,}'.format(int(float(price))) for price in line[1:]]
        td_list = ['<td>{}</td>'.format(item) for item in [timestamp] + price_list]
        row = '<tr>{}</tr>'.format(''.join(td_list))
        rows.append(row)
    return ''.join(rows)


def htmlize_rate():
    price_now = [int(float(i)) for i in read_data(date=date.today())[1:]]
    rows = []
    for i in range(7, 0, -1):
        dt = date.today() - timedelta(i)
        price_prev = [int(float(i)) for i in read_data(date=dt)[1:]]
        rate_list = ['{:.2f}%'.format((100 * (a - b) / b)) for a, b in zip(price_now, price_prev)]
        name = 'RSI(days={})'.format(i)
        td_list = ['<td>{}</td>'.format(item) for item in [name] + rate_list]
        row = '<tr class="table-active">{}</tr>'.format(''.join(td_list))
        rows.append(row)
    return ''.join(rows)


def render():
    template = '''
        <html>
        <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css">
        <script src="https://code.jquery.com/jquery-3.2.1.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js"></script>
        </head>
        <body>
            <table class="table table-hover table-sm">
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
                <tbody>{}</tbody>
                <tbody>{}</tbody>
            </table>
            </body>
        </html>
        '''
    return template.format(htmlize_rate(), htmlize_price())


if __name__ == '__main__':
    with open('index.html', 'w') as f:
        f.write(render())
