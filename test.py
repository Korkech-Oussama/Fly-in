class Test:
    def __init__(self, name: str):
        self.name = name
        self.type_test = 'normal'

class Manager:
    def __init__(self):
        self.tests = []

    def add_tests(self):
        names = ['test1', 'test2', 'test3']
        for name in names:
            new_zone = Test(name)
            self.tests.append(new_zone)

        types = [{'type': 'easy'},{'type':'medium'}, {'type':'hard'}]
        # for type in types:
        #     for test in self.tests:
        #         if type.get('type'):
        #             test.type_test =  type.get('type')
        for type, test in zip(types, self.tests):
            if type.get('type'):
                    test.type_test =  type.get('type')
            


if __name__ == "__main__":
    manager  = Manager()
    manager.add_tests()
    for manager in manager.tests:
        print(manager.type_test)


