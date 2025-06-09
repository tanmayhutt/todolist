# vercel_wsgi.py (MIT License)
# https://github.com/juancabrera/vercel-wsgi (archived)
import io
import sys
import base64

def handle_request(event, application):
    body = event.get("body", "")
    if event.get("isBase64Encoded", False):
        body = base64.b64decode(body)
    else:
        body = body.encode("utf-8")

    environ = {
        "REQUEST_METHOD": event["httpMethod"],
        "PATH_INFO": event["path"],
        "QUERY_STRING": event["queryStringParameters"] or "",
        "SERVER_NAME": "vercel",
        "SERVER_PORT": "80",
        "CONTENT_TYPE": event.get("headers", {}).get("content-type", ""),
        "CONTENT_LENGTH": str(len(body)),
        "wsgi.version": (1, 0),
        "wsgi.input": io.BytesIO(body),
        "wsgi.errors": sys.stderr,
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
        "wsgi.url_scheme": "http",
        "REMOTE_ADDR": event["headers"].get("x-forwarded-for", "127.0.0.1"),
    }

    headers_set = []
    headers_sent = []

    def write(data):
        if not headers_sent:
            status, response_headers = headers_set
            sys.stdout.write("Status: %s\n" % status)
            for header in response_headers:
                sys.stdout.write("%s: %s\n" % header)
            sys.stdout.write("\n")
            headers_sent.append(1)
        sys.stdout.write(data.decode("utf-8"))

    def start_response(status, response_headers, exc_info=None):
        headers_set[:] = [status, response_headers]
        return write

    result = application(environ, start_response)
    output = b"".join(result)
    return {
        "statusCode": int(headers_set[0].split(" ")[0]),
        "headers": dict(headers_set[1]),
        "body": output.decode("utf-8"),
    }
