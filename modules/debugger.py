import time, datetime

class Logger:

    _loggers = []

    def __init__(self, lid):
        self.id = lid
        self._messages = []
        self._start_time = int(round(time.time() * 1000))

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
        if len(Logger._loggers) > 5:
            Logger._loggers = Logger._loggers[1:]
        Logger._loggers.append(self)

    def recall(dist):
        return Logger._loggers[len(Logger._loggers)-int(dist)]._messages
