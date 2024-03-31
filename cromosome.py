from grid import grid
import game, parameters
from functionality import get_random, get_fitness
import secrets


class cromosome:
    def __init__(self, parentA = None, parentB = None):
        self.fitness = 0
        self.reproduction_prob = 0
        self.max_population = 0
        self.generations = 0
        

        if not parentA:
            self.grid = grid(parameters.gridsize)
            self.grid.set_cells(game.get_random_config(parameters.configuration_size_bound, parameters.fill_percentage, random_fill = parameters.fill_random, offset = parameters.offset))
        elif not parentB:
            self.grid = grid(parameters.gridsize)
            self.grid.set_cells(parentA.configuration)
        else:
            self.grid = grid(parameters.gridsize, parentA.configuration, parentB.configuration)
        if len(self.grid.field) == 0:
            self.grid.set_cells(((0,0),))                          
        self.configuration = self.grid.get_vals()


    def set_fitness(self, max_population, generations):
        self.fitness = get_fitness(max_population, generations) / ((len(self.configuration)**parameters.initial_population_pressure)+1)
        return self.fitness


    def set_reproduction_probability(self, global_fitness):
        self.reproduction_prob = self.fitness / global_fitness


    def set_max_values(self, max_population, generations):
        self.max_population = max(self.max_population, max_population)
        self.generations = max(self.generations, generations)


    def mutate(self,need_to_mutate=1, mutation_cell_count=3, random_cell_count = parameters.random_cell_mutation_count, generations_count = 1):
        if get_random() <= need_to_mutate:
            secrets.choice((self.random_mutation ,self.new_mutation, self.new_mutation,self.shorten_mutation,self.sequence_mutation,self.inversion_mutation, self.line_inversion_mutation))(mutation_cell_count, random_cell_count)
            if len(self.grid.field) <= 3:
                self.grid.reset()
                self.grid.set_cells(game.get_random_config(parameters.configuration_size_bound, parameters.fill_percentage, random_fill = parameters.fill_random, offset = parameters.offset))
            self.configuration = self.grid.get_vals()

    def flip_mutation(self, mutation_cell_count, random_cell_count = False):
        new_cells = [(parameters.configuration_size_bound-1-cl[0],cl[1]) for cl in self.configuration]
        self.grid.kill_cells(self.configuration)
        self.grid.set_cells(new_cells)

    def random_mutation(self, mutation_cell_count, random_cell_count=False):
         if random_cell_count:
             mutation_cell_count = secrets.choice(range(1,mutation_cell_count))
         for p in range(mutation_cell_count):
                i = int(get_random()*parameters.configuration_size_bound) + parameters.offset
                j = int(get_random()*parameters.configuration_size_bound) + parameters.offset
                index = (i,j)
                if index in self.grid.field:
                    self.grid.field.pop(index)
                else:
                    self.grid.field[index] = 0

    def line_inversion_mutation(self, mutation_cell_count=0, random_cell_count = False):
        line = secrets.randbelow(parameters.configuration_size_bound-1)
        prev_indices_lower = [ind for ind in self.grid.get_vals() if ind[0] == line]
        prev_indices_upper = [ind for ind in self.grid.get_vals() if ind[0] == line+1]
        self.grid.kill_cells(prev_indices_upper+prev_indices_lower)
        self.grid.set_cells([(ind[0+1], ind[1]) for ind in prev_indices_lower]+[(ind[0-1], ind[1]) for ind in prev_indices_upper]) 


    def inversion_mutation(self, mutation_cell_count, random_cell_count=False):
        row = secrets.choice(range(parameters.configuration_size_bound))
        for column in range(int(mutation_cell_count/2)):
            source_i, target_i = (row, column), (row, mutation_cell_count-column-1)
            source_val = self.grid.field.get(source_i, -1)
            target_val = self.grid.field.get(target_i, -1)
            if source_val==target_val==-1:
                pass
                
            elif source_val==target_val:
                pass
                
            elif source_val == -1:
                self.grid.set_cells((source_i,))
                self.grid.field.pop(target_i)
            else:
                self.grid.set_cells((target_i,))
                self.grid.field.pop(source_i)

                
    
    def sequence_mutation(self, mutation_cell_count, random_cell_count=False):
        line_number = secrets.randbelow(parameters.configuration_size_bound)
        for i in range(secrets.choice(range(2, mutation_cell_count))):
            cl = (line_number, i)
            if cl in self.grid.field:
                self.grid.kill_cells((cl,))
            else:
                self.grid.set_cells((cl,))


    def shorten_mutation(self, mutation_cell_count, random_cell_count = False):
        row = secrets.randbelow(parameters.configuration_size_bound)
        row_cells =  [cl for cl in self.grid.field if cl[0] == row]
        self.grid.kill_cells(row_cells)
        old_cells = [cl for cl in self.configuration if cl[0] > row]
        new_cells = [(cl[0]-1, cl[1]) for cl in old_cells]
        self.grid.kill_cells(old_cells)
        self.grid.set_cells(new_cells)



    def shift_mutation(self, mutation_cell_count, random_cell_count=False):
        row = secrets.randbelow(parameters.configuration_size_bound)
        upshift = secrets.choice(range(parameters.upshift_mutation_amount))
        sideshift = secrets.choice(range(parameters.sideshift_mutation_amount))
        old_cells = [cl for cl in self.configuration if cl[0] <= row]
        new_config = [(cl[0]+upshift,cl[1]+sideshift) for cl in old_cells]
        self.grid.kill_cells(old_cells)
        self.grid.set_cells(new_config)


    def new_mutation(self, mutation_cell_count, random_cell_count=False):
        self.grid.reset()
        self.grid.set_cells(game.get_random_config(parameters.configuration_size_bound, parameters.fill_percentage, random_fill = True,random_fill_percentage=True, offset = parameters.offset))


    def optimal_fitness(self):
        return get_fitness(max_population=parameters.optimal_population, generations=parameters.optimal_generations)




