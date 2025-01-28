class TargetValueMapping:

    def __init__(self):
        self.neg = 0
        self.pos = 1

    def to_dict(self) -> dict:
        """"
        Converts the object to a dictionary.
        """
        return self.__dict__

    def reverse_mapping(self) -> dict:
        """
        Returns a dictionary with the target values as keys and 
        the target names as values.
        """
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))
