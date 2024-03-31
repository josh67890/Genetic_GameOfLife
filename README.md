Hi :)

first - this project contains an all new implementation of the game of life - making the runtime of the genetic algorithm much more effecient.

To run the algorithm, 
simply enter the terminal and cd into the directory location on your computer
then run the command 'python gen_algo.py'

The algorithm will run until the specified evolution_gen_count parameter or optimal fitness has been satisfied

Every generation of evolution will output the best/fittest configuration. as well as the min/max/avg fitnesses,
as well as the relative changes compared to the previous generation

I encourage you to play with the different values (pressure values, configuration/population size, etc)!!

p.s.
the gridsize parameter in size.py is to one direction - i.e. 1/4 of the actual size of the grid - 
the actual size of the grid is in the range (-size... x coordenates ...size)*(-size... y coordenates ...size)
