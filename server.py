from http.server import BaseHTTPRequestHandler, HTTPServer


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
                        <th>Timestamp</th>
                        <th>BTC</th>
                        <th>ETH</th>
                        <th>DASH</th>
                        <th>LTC</th>
                        <th>ETC</th>
                        <th>XRP</th>
                    </tr>
                </thead>
                <tbody>{}</tbody>
            </table>
            </body>
        </html>
        '''
    coins = ['BTC', 'ETH', 'DASH', 'LTC', 'ETC', 'XRP']

    def get_response(self):
        data = []
        with open('data/COINS_KRW') as f:
            lines = f.readlines()[1:]
            for line in lines:
                item_list = line.strip().split(',')
                timestamp = item_list[0]
                price_list = ['{0:,}'.format(int(price)) for price in item_list[1:]]
                td_list = ['<td>{}</td>'.format(item) for item in [timestamp] + price_list]
                row = '<tr>{}</tr>'.format(''.join(td_list))
                data.append(row)
        return bytes(self.template.format(''.join(data)), "utf8")

    # GET
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        response = self.get_response()
        self.wfile.write(response)
        return


server_address = ('127.0.0.1', 8000)
httpd = HTTPServer(server_address, myHandler)
print('running server...')
httpd.serve_forever()
