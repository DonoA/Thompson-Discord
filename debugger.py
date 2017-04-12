import time, datetime

class Logger:

    _loggers = {}

    _last = None

    def __init__(self, lid):
        self.id = lid
        self._messages = []
        self._start_time = int(round(time.time() * 1000))
        Logger._loggers[lid] = self

    def log(self, message):
        self._messages.append("{} | {}".format(datetime.datetime.fromtimestamp(time.time()),message))

    def close(self):
        self._end_time = int(round(time.time() * 1000))
        self._execution_time = self._end_time - self._start_time
        self._messages.append("Execution took {}(ms)".format(self._execution_time))
        self._messages.append("Started: {} Ended: {}".format(
            str(datetime.datetime.fromtimestamp(self._start_time/1000)),
            str(datetime.datetime.fromtimestamp(self._end_time/1000))
        ))
        Logger._last = self

    def recall(lid):
        return Logger._loggers[lid]._messages

    def recall_last():
        return Logger._last._messages
