class MockUuid:

    def __init__(self):
        self.reset()

    def reset(self):
        self.__uuids = []
        self.__index = 0

    def add(self, uuid):
        self.__uuids.append(uuid)

    def assertThatAllUuidsWereUsed(self):
        assert self.__index == len(self.__uuids), \
            'The test did not use all uuids.'

    def uuid4(self):
        assert self.__index < len(self.__uuids), \
            'You did not define enough uuids for the mock.'
        result = self.__uuids[self.__index]
        self.__index += 1
        return result
