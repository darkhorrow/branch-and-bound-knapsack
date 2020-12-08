#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from operator import itemgetter
from timeit import default_timer as timer

Item = namedtuple("Item", ['index', 'value', 'weight'])
max_estimate = 0
max_value = 0
max_node = None
items = []


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    class Node:

        def __init__(self, value, room, estimate, parent, item, items_taken):
            global max_value
            global max_node
            if max_value <= value:
                max_value = value
                max_node = self
            self.value = value
            self.room = room
            self.estimate = estimate
            self.treated = False
            self.parent = parent

            self.estimate_items_taken = items_taken
            self.next_items_taken = items_taken

            if item is not None:
                self.index_item = item.index
            else:
                self.index_item = -1

        def expand(self, item, lista):
            if max_value < self.estimate:
                if not self.treated:
                    #print("IZQ")
                    if self.room-item.weight >= 0:
                        lista.insert(0, Node(self.value + item.value, self.room - item.weight, self.estimate, self, items_org[self.index_item+1], self.estimate_items_taken))
                    self.treated = True
                else:
                   # print("DER")
                    self.next_items_taken = self.estimate_items_taken[:]
                    self.next_items_taken[item.index]= 0
                    #print("[")
                    #for d in self.next_items_taken:
                    #    print(str(d) + ", ")
                    global items
                    lista.pop(0)
                    estimate = self.calculate_estimate() #self.estimate - items[self.index_item][1]
                    #estimate = self.calculate_estimate_old(item) #self.estimate - items[self.index_item][1]

                    lista.insert(0, Node(self.value, self.room, estimate , self, items_org[self.index_item+1], self.next_items_taken))
            else:
                lista.pop(0);

        def calculate_estimate_old(self, item):
            return self.estimate - item.value

        def calculate_estimate(self):
            initial_estimated = 0
            weight_take = 0
            for i in items:
                if not self.next_items_taken[i[0].index] == 0:
                    weight_take += i[0].weight
                    if weight_take > capacity:
                        initial_estimated += (i[0].weight-(weight_take-capacity))*i[0].value/i[0].weight
                        break
                    initial_estimated += i[0].value
                #else:
                    #print("Index: " + str(i[0].index))
            #print("Estimado: " + str(initial_estimated))
            return initial_estimated

    # parse the input
    lines = input_data.split('\n')
    first_line = lines[0].split()
    item_count = int(first_line[0])
    capacity = int(first_line[1])
    items_org = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append((Item(i - 1, int(parts[0]), int(parts[1])), int(parts[0])/int(parts[1])))
        items_org.append(Item(i - 1, int(parts[0]), int(parts[1])))

    items.sort(key=itemgetter(1), reverse=True)
    initial_estimate = 0
    weight_taken = 0
    for i in items:
        weight_taken += i[0].weight
        if weight_taken > capacity:
            initial_estimate += (i[0].weight-(weight_taken-capacity))*i[0].value/i[0].weight
            break
        initial_estimate += i[0].value

    taken = [0] * len(items)
    items_taken = [1] * len(items)
    #a = 0
    #for i in items:
    #    a += i[0].value
    #initial_estimate = a
    node_list = [Node(0, capacity, initial_estimate, None, None, items_taken)]

    prev = timer()
    prev2 = timer()
    while len(node_list) > 0:
        #print("----")
        #print(node_list[0].value)
        #print(node_list[0].room)
        #print(node_list[0].estimate)
        if(timer()-prev2 > 5):
            print("Tiempo transcurrido: " + str(timer()-prev) + " ---- Valor: " + str(max_value))
            prev2 = timer()
        if node_list[0].index_item+1 < len(items_org):
            node_list[0].expand(items_org[node_list[0].index_item+1], node_list)
        else:
        #    print("fin hoja")
            node_list.pop(0)
        #print("----")
    print("Tiempo (s): " + str(timer()-prev))
    # prepare the solution in the specified output format
    output_data = str(max_value) + '\n'
    output_data += ' '.join(map(str, max_node.estimate_items_taken))
    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

