class Metadata:
    def __init__(self, uuid: str, fuzz_data: str, suspicious_reply: list):
        self.uuid = uuid
        self.fuzz_data = fuzz_data
        self.suspicious_reply = suspicious_reply
        self.enabled = True

    def reset(self):
        self.fuzz_data = None
        self.enabled = False

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"Metadata-{self.fuzz_data!r}-{self.uuid[:6]!r})"
        )

    def __hash__(self):
        return hash((self.uuid, self.fuzz_data))

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.uuid == other.uuid
