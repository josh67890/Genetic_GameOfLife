from operator import attrgetter
from parameters import *
from cromosome import cromosome
import functionality, game, grid
import time, math, copy, secrets

fitness_measurements = [1,1,1]
cromosomes = [cromosome() for i in range(population_size)]
best_configurations = {}
best_cromosomes = []
elite_cromosomes = {}
new_gen = []

for evolution in range(evolution_gen_count):
    global_fitness = 0
    average_global_fitness = 0
    
    if evolution % 100 == 0:
        print(f"in generation {evolution}:")
        try:
            for cromo in sorted(list(elite_cromosomes.values()), key= lambda x: x.fitness, reverse=True):
                print(f'''\n{cromo.grid}\n\nmax_population: {cromo.max_population}\ngenerations: {cromo.generations}\n\n''')
            time.sleep(10)
        except Exception:
            print("error while printing the configurations")

    for cromo in cromosomes:
        key = cromo.grid.get_vals(True)
        test = best_configurations.get(key, None)

        if test:
            # if key in elite_cromosomes:
            #     print(test.generations, test.fitness)
            global_fitness += cromo.set_fitness(test.max_population, test.generations)
            cromo.set_max_values(test.max_population, test.generations)
            #print(f"elite: \ngens:{cromo.generations}\nfitness:{cromo.fitness} ")

        else:
            max_population, generations = game.run_gens(cromo.grid, gameoflife_gen_count, oscillator_count)
            global_fitness += cromo.set_fitness(max_population, generations)
            cromo.set_max_values(max_population=max_population, generations=generations)

        
    average_global_fitness = global_fitness/len(cromosomes)

    for cromo in cromosomes:
        cromo.set_reproduction_probability(global_fitness)

    del(best_cromosomes)
    best_cromosomes = []
    best_cromosomes = copy.deepcopy(sorted(cromosomes, key = lambda x: x.fitness, reverse=True))

    max_cromosome, min_cromosome = copy.deepcopy(max(cromosomes, key=attrgetter('fitness'))), copy.deepcopy(min(cromosomes, key=attrgetter('fitness')))#copy.deepcopy(max(cromosomes, key=key_lambda)), copy.deepcopy(min(cromosomes, key=key_lambda))
    max_fitness, min_fitness = max_cromosome.fitness, min_cromosome.fitness+0.00001
    avg_diff, max_diff, min_diff = average_global_fitness/fitness_measurements[0], max_fitness/fitness_measurements[1], min_fitness / fitness_measurements[2]
    fitness_measurements.clear()
    fitness_measurements = [average_global_fitness, max_fitness, min_fitness]

    print(f'''in generation {evolution}:\n
          average fitness is {average_global_fitness} - difference from last generation: {avg_diff}\n
          max fitness is: {max_fitness} - difference from last generation: {max_diff}\n
          min fitness is: {min_fitness} - difference from last generation: {min_diff}\n\n
          best configuration:\n{cromosome(max_cromosome,max_cromosome).grid}\n\n
    max_population: {max_cromosome.max_population}\ngenerations: {max_cromosome.generations}\nfinal population: {max_cromosome.grid.get_population()}\n\n''')
    
    if evolution >= min_generations_to_run or max_fitness >= max_cromosome.optimal_fitness():
        break

    max_avg_ratio = average_global_fitness/max_fitness
    
    new_gen.clear()
    tournament_population = min_tournament_count#int(population_size*max_avg_ratio*additional_tournament_percentage)+min_tournament_count
    for i in range(population_size-tournament_population-elite_configurations_count):
        first_parent_index = functionality.get_parent_roulette(cromosomes)
        first_parent = copy.deepcopy(cromosomes[first_parent_index])
        second_parent = copy.deepcopy(cromosomes[functionality.get_parent_roulette(cromosomes,first_parent_index)])
        new_cromo = cromosome(first_parent, second_parent)
        new_gen.append(new_cromo)

    for i in range(tournament_population):
        first_parent = functionality.get_parent_tournament(cromosomes, tournament_contestant_count)
        second_parent = functionality.get_parent_tournament(cromosomes, tournament_contestant_count)
        new_cromo = cromosome(first_parent, second_parent)
        new_gen.append(new_cromo)

    for cromo in new_gen:
        cromo.mutate(need_to_mutate = max_avg_ratio*mutation_probability, mutation_cell_count = mutation_cell_count, generations_count = evolution)


    for cromo in cromosomes:
        if cromo.generations > best_configurations_gen_count :
            new_crom = cromosome(cromo).grid.get_vals(True)
            if new_crom not in best_configurations:
                crom = copy.deepcopy(cromo)
                crom.grid.kill_cells(crom.grid.get_vals())
                crom.grid.set_cells(crom.configuration)
                best_configurations[copy.deepcopy(new_crom)] = copy.deepcopy(crom)
    
    elite_cromosomes.clear()
    elite_cromosomes = {}
    if elite_configurations_count > 0:
        elite_count = elite_configurations_count
        
        for i in range(len(best_cromosomes)):# in best_cromosomes:  
            if elite_count > 0:
                cromo = best_cromosomes[i]
                config = cromosome(cromo).grid.get_vals(True)
                # if len(elite_cromosomes)==0 or cromo.configuration != elite_cromosomes[-1].configuration:
                if config not in elite_cromosomes and cromo.generations > elite_gen_count:
                    print(cromo.generations," ; ", round(cromo.fitness, 3))
                    crom = copy.deepcopy(cromo)
                    crom.grid.kill_cells(crom.grid.get_vals())
                    crom.grid.set_cells(crom.configuration)
                    elite_cromosomes[config] = copy.deepcopy(crom)
                    elite_count -= 1
            else:
                
                break
        print("\n--\n")
        for configuration in elite_cromosomes:
            new_gen.append(copy.deepcopy(elite_cromosomes[configuration])) 
        #new_gen.extend(copy.deepcopy(list(elite_cromosomes.values())))

    cromosomes.clear()
    cromosomes.extend(copy.deepcopy(new_gen))
    

best1, best2 = cromosomes.pop(cromosomes.index(max(cromosomes,key=attrgetter('fitness')))), cromosomes.pop(cromosomes.index(min(cromosomes,key=attrgetter('fitness'))))
print(f'''final fitness is:\naverage: {fitness_measurements[0]}\nmax: {fitness_measurements[1]}\n\n
      best configurations:\n{grid.grid(best1.grid.size, best1.configuration, best1.configuration)}\n\n
    {'-'*80}\n\n{grid.grid(best2.grid.size, best2.configuration, best2.configuration)}''')
    

