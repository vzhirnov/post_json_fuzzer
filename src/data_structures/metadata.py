class Metadata:
    def __init__(self, uuid, fuzz_data, suspicious_reply):
        self.uuid = uuid
        self.fuzz_data = fuzz_data
        self.suspicious_reply = suspicious_reply

    def __repr__(self):
        return f"Metadata({self.uuid[:6]})"

    def __hash__(self):
        return hash((self.uuid, self.fuzz_data))

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.uuid == other.uuid
