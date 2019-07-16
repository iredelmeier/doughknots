from .kind import Kind


class InsufficientDoughknots(Exception):
    def __init__(self, kind: Kind):
        super().__init__(f"Insufficient doughknots of kind {kind}")
