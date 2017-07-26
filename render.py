from datetime import date as Date, timedelta


def read_data(**kwargs):
    with open('data.csv') as f:
        lines = [line.strip().split(',') for line in f.readlines()[-1:0:-1]]
        lines_cleaned = [(line[0], [int(float(i)) for i in line[1:]]) for line in lines]
        if kwargs.get('select_all'):
            return lines_cleaned

        for line in lines_cleaned:
            timestamp = line[0]
            if timestamp[:5] == kwargs['date'].strftime('%m/%d'):
                return line


def make_tr(name, num_list, active=False):
    td_list = ['<td>{}</td>'.format(item) for item in [name] + num_list]
    if active:
        row = '<tr class="table-active">{}</tr>'.format(''.join(td_list))
    else:
        row = '<tr>{}</tr>'.format(''.join(td_list))
    return row


def htmlize_price():
    rows = []
    for line in read_data(select_all=True):
        name = line[0]
        price_list = ['{:,}'.format(i) for i in line[1]]
        row = make_tr(name, price_list)
        rows.append(row)
    return ''.join(rows)


def htmlize_rate():
    price_now = read_data(date=Date.today())[1]
    rows = []
    for i in range(7, 0, -1):
        name = 'RSI(days={})'.format(i)
        date = Date.today() - timedelta(i)
        price_prev = read_data(date=date)[1]
        rate_list = ['{:.2f}%'.format((100 * (a - b) / b)) for a, b in zip(price_now, price_prev)]
        row = make_tr(name, rate_list, active=True)
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
