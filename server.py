from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import date, timedelta


# HTTPRequestHandler class
class myHandler(BaseHTTPRequestHandler):
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
    coins = ['BTC', 'ETH', 'DASH', 'LTC', 'ETC', 'XRP']

    def read_lines(self):
        with open('data.csv') as f:
            lines = f.readlines()[-1:0:-1]
            return lines

    def make_list(self):
        data = []
        lines = self.read_lines()
        for line in lines:
            item_list = line.strip().split(',')
            timestamp = item_list[0]
            price_list = ['{0:,}'.format(int(float(price))) for price in item_list[1:]]
            td_list = ['<td>{}</td>'.format(item) for item in [timestamp] + price_list]
            row = '<tr>{}</tr>'.format(''.join(td_list))
            data.append(row)
        return ''.join(data)

    def make_rate(self):
        today = date.today()
        days_before = today + timedelta(-7)
        lines = self.read_lines()
        for line in lines:
            item_list = line.split(',')
            if today.strftime('%m/%d') == item_list[0][:5]:
                curr = [int(float(i)) for i in item_list[1:]]
            if days_before.strftime('%m/%d') == item_list[0][:5]:
                prev = [int(float(i)) for i in item_list[1:]]
        rate_list = [(a - b) / b for a, b in zip(curr, prev)]
        name = 'RSI(7)'
        td_list = ['<td>{}</td>'.format(item) for item in [name] + rate_list]
        row = '<tr>{}</tr>'.format(''.join(td_list))
        return row

    # GET
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = bytes(self.template.format(self.make_rate(), self.make_list()), "utf8")
        self.wfile.write(response)
        return


server_address = ('127.0.0.1', 8000)
httpd = HTTPServer(server_address, myHandler)
print('running server...')
httpd.serve_forever()
