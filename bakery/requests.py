from .kind import Kind


class BakeRequest:
    def __init__(self, kind: Kind, amount: int) -> None:
        self.kind = kind
        self.amount = amount
