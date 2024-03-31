
from operator import itemgetter
import parameters, functionality, secrets

class grid:

    def __init__(self, gridsize_to_each_direction = 100, first = None, second = None):
        
        self.size = gridsize_to_each_direction
        self.field = {}
        if first and second:
            secrets.choice((self.single_cut, self.multiple_cuts))(first, second, parameters.random_line_cut_count_in_multiple_cut_crossover)
            
            
    def multiple_cuts(self, first, second, random = False):
        configs = [first, second]
        if random:
            cut_count = secrets.choice(range(1,int(parameters.configuration_size_bound/2)))
            
        else:
            cut_count = int(parameters.configuration_size_bound/parameters.lines_in_each_cut_for_multiple_cut_crossover) 
        step = parameters.lines_in_each_cut_for_multiple_cut_crossover 
        past = -1 
        i = 0
        for i in range(step, parameters.configuration_size_bound, step):
            self.set_cells([cl for cl in configs[i%2] if past < cl[0] <= i]) 
            past = i
        if i < parameters.configuration_size_bound:
            self.set_cells([cl for cl in configs[(i+1)%2] if past < cl[0]]) 

    def single_cut(self, first, second, placeholder = False):
        line_cut = functionality.get_line_cut_for_cromosome_crossover()
        first_cromosome = [cl for cl in first if cl[0] <= line_cut] + [cl for cl in second if cl[0] > line_cut]
        second_cromosome = [cl for cl in second if cl[0] <= line_cut] + [cl for cl in first if cl[0] > line_cut]
        gene = secrets.choice((first_cromosome, second_cromosome))
        for cell_index in gene:
            self.field[cell_index] = 0

    def set_cells(self, iterable_of_x_y_points_in_grid):
        for point in iterable_of_x_y_points_in_grid:
            self.field[(point[0],point[1])] = 0


    def reset(self):
        self.field.clear()
    
    def kill_cells(self, cells_to_kill):
        for cl in cells_to_kill:
            self.field.pop(cl)

    def __str__(self):
        rep_string = ""
        max_x, min_x = max(self.field, key = itemgetter(0))[0], min(self.field, key = itemgetter(0))[0]
        max_y, min_y = max(self.field, key = itemgetter(1))[1], min(self.field, key = itemgetter(1))[1]
        for i in range(min_x, max_x+1):
            for j in range(min_y, max_y+1):
                if (i,j) in self.field:
                    rep_string+=str(j)
                else:
                    rep_string+=" "
            rep_string+='\n'

        return rep_string
    

    def neighbors(self, cl):
        for x in range(-1,2):
            i=cl[0]+x
            for y in range(-1, 2):
                j=cl[1]+y
                if -(self.size)<=i<self.size and -(self.size)<=j<self.size and not (cl[0]==i and cl[1]==j):
                    index = (i,j)
                    if index in self.field:
                        if self.field[index] < 0:
                            self.field[index] -= 1
                        else:
                            self.field[index] += 1
                    else:
                        self.field[index] = -1
    

    def get_population(self):
        return len(self.field)
        

    def determine(self):
        for cl in tuple(self.field.keys()):
            self.neighbors(cl)


    def next_gen(self):
        self.determine()
        for cl in tuple(self.field.keys()):  
            match(self.field[cl]):
                case 2|3|-3:
                    self.field[cl] = 0
                case _:
                    self.field.pop(cl)
        return self.get_population()
    
    def get_vals(self, sort = False):
        if sort:
            return tuple(sorted([cl for cl in self.field],key=itemgetter(0,1)))
        else:
            return set(self.field.keys())
    
    