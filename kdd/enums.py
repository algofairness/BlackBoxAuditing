class Enumeration:
    def __init__(self, enums):
        for i, enum in enumerate(enums):
            setattr(self, enum, i)

repair_type = Enumeration(["COMBINATORIAL", "GEOMETRIC"])