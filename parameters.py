gridsize = 200
cell_count = (gridsize*2)**2
configuration_size_bound = 6
offset = 0 #int((gridsize-configuration_size_bound)/2)

gameoflife_gen_count = 50000
oscillator_count = 35

max_fill_percentage = 0.5
fill_percentage = 0.3
fill_random = True

population_size = 200
evolution_gen_count = 3000
min_generations_to_run = evolution_gen_count
min_continue_diff = 1.01

lines_in_each_cut_for_multiple_cut_crossover = 2
random_line_cut_count_in_multiple_cut_crossover = True

mutation_probability = 0.4
mutation_cell_count = configuration_size_bound*1
random_cell_mutation_count = True
upshift_mutation_amount = 3
sideshift_mutation_amount = 3

elite_percentage = 0.2
elite_configurations_count = int(elite_percentage*population_size)
#best_cromosome_count = int(population_size*1)
best_configurations_gen_count = 100
elite_gen_count = 1500

min_tournament_count = int((population_size-elite_configurations_count)*0)
additional_tournament_percentage = 0
tournament_contestant_count = 3

generations_weight = 0.6
max_population_weight = 0.3
fitness_pressure = 0.13
initial_population_pressure = 1

optimal_population = 7000
optimal_generations = gameoflife_gen_count*0.8

