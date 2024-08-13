import json
import math
import queue
from datetime import datetime
from io import StringIO
from json import JSONEncoder
from logging.handlers import HTTPHandler
from logging.handlers import QueueListener
from typing import override, List, Any

from django.http import HttpRequest, HttpHeaders


class AutoStartingQueueListener(QueueListener):
    def __init__(self, queue, *handlers, respect_handler_level=False, auto_start=True):
        super().__init__(queue, *handlers, respect_handler_level=respect_handler_level)
        if auto_start:
            super().start()




def queue_factory():
    return queue.Queue(maxsize=10000)

class FaultTolerantJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return math.floor(o.timestamp() * 1000)
        elif isinstance(o, HttpRequest):
            return {
                'method': o.method,
                'path': o.get_full_path(),
                'headers': o.headers,
                'host': o.get_host(),
                'port': o.get_port()
            }
        elif isinstance(o, HttpHeaders):
            return {
                key: value for (key, value) in o.items()
            }
        else:
            return None



class BufferingHTTPHandler(HTTPHandler):

    def __init__(self,
                 host,
                 index='filebeat-logs',
                 secure=False,
                 credentials=None,
                 max_size=1000,
                 max_interval=5.0,
                 context=None):
        super().__init__(host, '', 'POST', secure, credentials, context)
        self._index: str = index
        self._buffer: List[Any] = []
        self._max_size: int = max_size
        self._last_flush: datetime = datetime.now()
        self._max_interval: float = max_interval

    @override
    def mapLogRecord(self, record):
        toBeExcluded = {
            'args',
            'asctime',
            'created',
            'exc_info',
            'filename',
            'funcName',
            'levelname',
            'levelno',
            'lineno',
            'message',
            'module',
            'msecs',
            'msg',
            'name',
            'pathname',
            'process',
            'processName',
            'relativeCreated',
            'stack_info',
            'thread',
            'threadName',
            'taskName'
        }
        return {
            '@timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'message': record.getMessage(),
            'log.level': record.levelno,
            'log.logger': record.name,
            'log.file.path': record.pathname,
            'log.file.name': record.filename,
            'log.file.line': record.lineno,
            'extra': {
                key: value for (key, value) in record.__dict__.items() if key not in toBeExcluded
            }
        }

    @override
    def flush(self):
        super().flush()
        try:
            body = StringIO()
            for record in self._buffer:
                json.dump({'create': {"_index": self._index}}, body)
                body.write('\n')
                json.dump(self.mapLogRecord(record), body, cls=FaultTolerantJSONEncoder)
                body.write('\n')

            import urllib.parse
            host = self.host
            h = self.getConnection(host, self.secure)
            url = self.url
            h.putrequest(self.method, f'/_bulk')
            # support multiple hosts on one IP address...
            # need to strip optional :port from host, if present
            i = host.find(":")
            if i >= 0:
                host = host[:i]
            # See issue #30904: putrequest call above already adds this header
            # on Python 3.x.
            # h.putheader("Host", host)
            if self.method == "POST":
                h.putheader("Content-type",
                            "application/x-ndjson")
                h.putheader("Content-length", str(body.tell()))
            if self.credentials:
                import base64
                s = ('%s:%s' % self.credentials).encode('utf-8')
                s = 'Basic ' + base64.b64encode(s).strip().decode('ascii')
                h.putheader('Authorization', s)
            h.endheaders()
            if self.method == "POST":
                h.send(body.getvalue().encode('utf-8'))
            response = h.getresponse()
            if response.status != 200:
                raise RuntimeError(response.status)
        except Exception:
            for record in self._buffer:
                self.handleError(record)
        finally:
            self._buffer.clear()
            self._last_flush = datetime.now()

    @override
    def emit(self, record):
        self._buffer.append(record)
        if len(self._buffer) == self._max_size or (datetime.now() - self._last_flush).total_seconds() > self._max_interval:
            self.flush()


