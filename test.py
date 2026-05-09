# class Test:
#     def __init__(self, name: str):
#         self.name = name
#         self.type_test = 'normal'

# class Manager:
#     def __init__(self):
#         self.tests = []

#     def add_tests(self):
#         names = ['test1', 'test2', 'test3']
#         for name in names:
#             new_zone = Test(name)
#             self.tests.append(new_zone)

#         types = [{'type': 'easy'},{'type':'medium'}, {'type':'hard'}]
#         # for type in types:
#         #     for test in self.tests:
#         #         if type.get('type'):
#         #             test.type_test =  type.get('type')
#         for type, test in zip(types, self.tests):
#             if type.get('type'):
#                     test.type_test =  type.get('type')
import heapq

def test_heapify(vertexes) -> list:
    heapq.heapify(vertexes)
    return vertexes
def build_graph(vertexes):
    return

if __name__ == "__main__":

    vertexes = [(0,'A'), (4, 'B'), (2, 'C'), (float('inf'), 'D'),(float('inf'), 'E'),(float('inf'), 'F')]

    reorderded_list = test_heapify(vertexes)

    print(reorderded_list)
