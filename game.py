from grid import grid
import random, copy, parameters
from queue import SimpleQueue




def get_random_config(size, fill_percentage, random_fill = False, offset=0, random_fill_percentage = False):
    if random_fill:
        if random_fill_percentage:
            fill_percentage = 1
        else:
            fill_percentage = parameters.max_fill_percentage
        fill_percentage = random.random()*fill_percentage
    nums = {int((random.random())*(size**2)) for i in range(1,int((size**2)*fill_percentage)+1)}
    indexes = tuple((int(num/size)+offset, (num%size)+offset) for num in nums)
    return indexes


def run_gens(grd, gen_count=1000, max_osc = 50):

    max = grd.get_population()
    state_queue = SimpleQueue()
    states = set()

    for gen in range(gen_count):
        population = grd.next_gen()
        if population > max:
            max = population
        if max_osc > 0:
            state = grd.get_vals(True)
            if state in states:
                break
            else:
                states.add(state)
                if state_queue.qsize() >= max_osc:
                    states.remove(state_queue.get())
                state_queue.put(state)

    return max, gen


# g = grid(17000)
# g.set_cells(((0,0),(0,1),(0,4),(1,0),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(3,4),(4,1),(4,2)))
# print(run_gens(g,17465,0))
# print(g.get_population())
