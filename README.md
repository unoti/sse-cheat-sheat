# Server Sent Events
These are notes and code snippets I've used for working with Server Sent Events (SSE).

We have implementations on the server side in Python for Django and Flask.

## NGINX and proxies
Note about running this example through NGINX:
By default fastcgi_buffering is ON, thus you have to add fastcgi_buffering off; to the appropriate location block for this example to work.

Similarly, if you use a reverse proxy, proxy_buffering is ON by default, thus you have to add proxy_buffering off.

The headings you see in the examples are because of this.

* [Server-sent events - Web APIs | MDN (mozilla.org)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
    * [PHP example](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)

## Client side
* Client knows a URL to get server sent events
* In Javascript on the client, create an EventSource object
    * If you're using HTMX, this step is a little different
* EventSource you give it functions to call when it receives an event

### Named vs unnamed events
If you're using unnamed events, then you can use
```javascript
eventSource.onpopen = function(msg) { …
```
But if you're using named events, you must use
```javascript
eventSource.addEventListener('my_event_name': e=> {
```

## Server side
Create a url to provide server sent events
* Add headers:
    * X-Accel-Buffering: no
    * Content-Type: text/event-stream
    * Cache-Control: no-cache
To produce an event, output like this
```
event: my_event_name\n
data: { json goes here }\n\n
```
You may need to flush the output stream depending on your platform.
For Flask and Django I didn't need to do this when using a generator.


## Infrastructure Considerations
Remember to configure out NGINX and reverse proxy appropriately.

Be sure to use HTTP/2 or we'll be limited to 6 streams per domain name
See "Warning" here [Using server-sent events - Web APIs | MDN (mozilla.org)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
