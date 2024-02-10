import flask
import json
import time

app = flask.Flask(__name__)
CORS_ALLOW_HOST = 'http://localhost:8000'

@app.route('/sse_lab/agents/<agent_id>')
def user_backlog(agent_id):
    print(f'agent backend for {agent_id}')
    resp = {
        'agent_id': agent_id,
    }
    return resp

def sse_format(event_name: str, event_payload: any) -> str:
    json_str = json.dumps(event_payload)
    msg = f'event: {event_name}\ndata: {json_str}\n\n' # Events are separated by two newlines.
    return msg

@app.route('/agents/<agent_id>/event_stream')
def agent_event_stream(agent_id):
    print(f'agent backend for {agent_id}')
    resp = {
        'agent_id': agent_id,
    }
    
    # This function is an interator.
    # When you put an iterator into a flask Response, it streams.
    def event_stream():
        count = 0
        while True:
            msg = sse_format('pulse', {'count': count})
            count += 1
            time.sleep(1)
            yield msg

    headers = {'X-Accel-Buffering': 'no',
               'Cache-Control': 'no-cache',
               'connection': 'keep-alive',
               'Access-Control-Allow-Origin': CORS_ALLOW_HOST}
    return flask.Response(event_stream(), mimetype='text/event-stream', headers=headers)


if __name__ == '__main__':
    app.run(port=8082)