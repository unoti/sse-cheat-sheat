def sse_format(event_name: str, event_payload: any) -> str:
    json_str = json.dumps(event_payload)
    return sse_format_str(event_name, json_str)


def sse_format_str(event_name: str, msg_data: str) -> str:
    msg = f'event: {event_name}\ndata: {msg_data}\n\n' # Events are separated by two newlines.
    return msg


# if you change the stream generator while the stream is running, and reload the page, it'll lock up django dev server.
def sse_event_stream_generator(assistant_id):
    counter = 0
    while True:
        counter += 1
        time.sleep(1)
        payload = {'count': counter}
        #msg = sse_format('pulse', payload)
        msg = sse_format_str('pulse', render_to_string('chat-message.html', payload))
        print(msg)
        yield(msg)


async def sse_test(request, assistant_id: str):
    response = HttpResponse(sse_event_stream_generator(assistant_id), content_type='text/event-stream')
    response['X-Accel-Buffering'] = 'no'
    response['Cache-Control'] = 'no-cache'
    response['connection'] = 'keep-alive'
    return response
