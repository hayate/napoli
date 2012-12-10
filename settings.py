import sys

# possible values are: devel and prod
environment = 'devel'

class Settings(object):
    def __init__(self):
        self.config = __import__(''.join(['configs.', environment]), fromlist=['configs'])

    def __getattr__(self, name):
        return getattr(self.config, name)


sys.modules[__name__] = Settings()

