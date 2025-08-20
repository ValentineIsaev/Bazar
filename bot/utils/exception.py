class LoadConfigError(Exception):
    def __init__(self, error: str):
        self._error = error

    def __str__(self):
        return self._error


class UnknownCallback(Exception):
    def __init__(self, callback: str):
        self._cb = callback

    def __str__(self):
        return f'Unknown callback: {self._cb}'


class SingleUseCache(Exception):
    def __str__(self):
        return 'You can save the cache only once.'

WrongTypeData = ValueError('Data is of the wrong type!')
