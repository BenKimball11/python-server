class Location():
    """Location Class
    """
    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every METHOD on a CLASS
    # needs as the first parameter.
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address