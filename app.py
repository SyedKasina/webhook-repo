from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)
events = []

@app.route('/')
def home():
    return render_template("index.html", events=events)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        event_type = request.headers.get('X-GitHub-Event')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        parsed_event = {
            'type': event_type,
            'repo': data.get('repository', {}).get('full_name', ''),
            'pusher': data.get('pusher', {}).get('name', 'N/A'),
            'message': data.get('head_commit', {}).get('message', 'No message'),
            'timestamp': timestamp
        }
        events.insert(0, parsed_event)
    return '', 200

if __name__ == "__main__":
    app.run(debug=True)
