import http.server
import socketserver
import random
from urllib.parse import parse_qs

PORT = 8000

def split_teams(people, num_teams):
    random.shuffle(people)
    teams = [[] for _ in range(num_teams)]
    for i, person in enumerate(people):
        team_index = i % num_teams
        teams[team_index].append(person)
    return teams

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(body)

        num_people = int(params['numPeople'][0])
        num_teams = int(params['numTeams'][0])
        people = []
        for i in range(1, num_people + 1):
            person = params.get(f'person{i}')[0]
            if person:
                people.append(person)

        teams = split_teams(people, num_teams)
        result = self.render_result(teams)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))

    def render_result(self, teams):
        team_html = ""
        for index, team in enumerate(teams):
            team_text = f"Team {index+1}: {', '.join(team)}"
            team_html += f"<p>{team_text}</p>"

        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Team Splitter - Result</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                    }}
                    h1 {{
                        text-align: center;
                    }}
                    #result {{
                        max-width: 400px;
                        margin: 20px auto;
                        padding: 20px;
                        background-color: #f5f5f5;
                        border-radius: 5px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    #result p {{
                        margin-bottom: 5px;
                    }}
                </style>
            </head>
            <body>
                <h1>Team Splitter - Result</h1>
                <div id="result">
                    <h2>Teams:</h2>
                    {team_html}
                </div>
            </body>
            </html>
        """

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(open('index.html', 'rb').read())

with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Server running on port {PORT}")
    httpd.serve_forever()
