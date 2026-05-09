import heapq

class NaivePriorityQueue():

    def __init__(self):
        self.queue = []

    def insert(self, cost: int, item: str) -> list:
        self.queue.append((cost, item))

    def pop_cheapest(self) -> tuple:
        if not self.queue:
            return "error"
        min_value = self.queue[0][0]
        
        min_index = 0
        for i, item in enumerate(self.queue):
            if item[0] < min_value:
                min_value = item[0]
                min_index = i
        return self.queue.pop(min_index)

if __name__ == "__main__":

    naive = NaivePriorityQueue()
    naive.insert(4, "start")
    naive.insert(2, "middle")
    naive.insert(5, "zone3")
    naive.insert(3, "end")

    heapq.heapify(naive.queue)

    for i in naive.queue:
        print(i)

    print(naive.queue)

    test: list = [50,16,88,23,45,11]

    heapq.heapify(test)

    print(test)

    sorted = [heapq.heappop(test) for _ in range(len(test))]
    print(sorted)