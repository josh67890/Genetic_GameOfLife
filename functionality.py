import secrets, parameters, copy

#six digit floating point precision random number in interval [0,1)
def get_random(precision = 1000000):
    rand = float(secrets.randbelow(precision))
    return rand/precision

def get_fitness(max_population, generations):
    weighted_population =  (max_population**parameters.max_population_weight)+1
    weighted_generations = (generations**parameters.generations_weight)+1
    fitness = ((weighted_generations**weighted_population))**parameters.fitness_pressure
    return fitness

def get_line_cut_for_cromosome_crossover():
    return secrets.choice(range(-1, parameters.configuration_size_bound+1,1)) # can result in crossover in any line - including the option for choosing any one of the parents alone

def get_parent_roulette(cromosomes, first_parent = -1):
    rand = get_random()
    reduce = 0
    # first_cromo = None
    if first_parent > -1:
        # first_cromo = cromosomes.pop(first_parent)
        rand -= cromosomes[first_parent].reproduction_prob
        reduce = 1

    for i in range(len(cromosomes)-reduce):
        if i == first_parent: continue
        if rand - cromosomes[i].reproduction_prob < 0:
            # if first_cromo:
            #     cromosomes.append(first_cromo)
            return i
        rand -= cromosomes[i].reproduction_prob
    # if first_cromo:
    #         cromosomes.append(first_cromo)
    #         return len(cromosomes)-2
    if i-1 == first_parent:
        return i-2
    else:
        #return len(cromosomes)-1
        return i-1

def get_parent_tournament(cromosomes, contestant_count=2):
    size = len(cromosomes)
    contestants = []

    for i in range(contestant_count):
         contestants.append(cromosomes.pop(secrets.choice(range(size-i))))
    parent = copy.deepcopy(max(contestants, key=lambda x:x.fitness))
    cromosomes.extend(contestants)

    return parent
