class UnknownCallback(Exception):
    def __init__(self, callback: str):
        self._cb = callback

    def __str__(self):
        return f'Unknown callback: {self._cb}'


class EmptyConfig(Exception):
    def __init__(self, key: str):
        self._key = key

    def __str__(self):
        return f'The parameter {self._key} is not specified in the environment variables'


class SingleUseCache(Exception):
    def __str__(self):
        return 'You can save the cache only once.'

WrongTypeData = ValueError('Data is of the wrong type!')
