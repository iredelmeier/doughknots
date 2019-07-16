from . import Kind


class InsufficientDoughnuts(Exception):
    def __init__(self, kind: Kind):
        super().__init__(f"Insufficient doughnuts of kind {kind}")
