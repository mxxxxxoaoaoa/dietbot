from .message import start, generate
from .callback import gen

class HandlerLoader:
    def __init__(self, dp):

        # message
        start.register(dp)
        generate.register(dp)


        # callback
        gen.register(dp)