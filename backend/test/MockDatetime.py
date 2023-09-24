from datetime import timezone

class MockDatetime:

    def __init__(self):
        self.reset()

    def reset(self):
        self.__timeStamps = []
        self.__index = 0

    def add(self, timeStamp):
        self.__timeStamps.append(timeStamp)

    def assertThatAllTimeStampsWereUsed(self):
        assert self.__index == len(self.__timeStamps), \
            'The test did not use all time stamps.'

    def now(self, tz):
        assert tz == timezone.utc
        assert self.__index < len(self.__timeStamps), \
            'You did not define enough time stamps for the mock.'
        result = self.__timeStamps[self.__index]
        self.__index += 1
        return result
