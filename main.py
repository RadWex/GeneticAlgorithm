import random
import math
import statistics
import matplotlib.pyplot as plt


class Chromosome():
    def __init__(self, num):
        self.phenotype = None
        self.genotype = []
        self.fitness = 2 * (num * num + 1)
        self.encoding(num)

    def encoding(self, num):
        self.genotype = list('{0:0b}'.format(num))
        how_many_to_7 = 7 - len(self.genotype)
        while how_many_to_7 > 0:
            self.genotype.insert(0, '0')
            how_many_to_7 -= 1
        self.fitness = 2 * (num * num + 1)
        self.phenotype = num

    def decoding(self, binary):
        self.phenotype = int("".join(str(x) for x in binary), 2)
        self.fitness = 2 * (self.phenotype * self.phenotype + 1)
        self.genotype = binary


def linearRoulette(generation, precision=100):
    fortuneWheel = []
    sum = 0
    for i in generation:
        sum += i.fitness
    for i in range(0, len(generation)):
        proportion = generation[i].fitness
        proportion = proportion / sum * precision
        for j in range(0, round(proportion)):
            fortuneWheel.append(generation[i])
    return fortuneWheel


def squaredRoulette(generation, precision=100):
    fortuneWheel = []
    fitnesses_of_generation = []
    for i in generation:
        fitnesses_of_generation.append(i.fitness)
    fitnesses_of_generation = [x**2 for x in fitnesses_of_generation]
    sum = 0
    for i in fitnesses_of_generation:
        sum += i
    for i, chromo in enumerate(generation):
        proportion = fitnesses_of_generation[i] / sum * precision
        for j in range(0, round(proportion)):
            fortuneWheel.append(chromo)
    return fortuneWheel


def logRoulette(generation, precision=100):
    fortuneWheel = []
    fitnesses_of_generation = []
    for i in generation:
        fitnesses_of_generation.append(math.log(i.fitness))
    sum = 0
    for i in fitnesses_of_generation:
        sum += i
    for i, chromo in enumerate(generation):
        proportion = fitnesses_of_generation[i] / sum * precision
        for j in range(0, round(proportion)):
            fortuneWheel.append(chromo)
    return fortuneWheel


def printGeneration(generation):
    for i in generation:
        print(i.phenotype, end=' ')
    print()


def getMeanOfGeneration(generation):
    tmp = []
    for i in generation:
        tmp.append(i.phenotype)
    return statistics.mean(tmp)


def getBestValueOfGeneration(generation):
    tmp = []
    for i in generation:
        tmp.append((i.phenotype, i.fitness))
    tmp = sorted(tmp, key=lambda x: (x[1]), reverse=True)
    return tmp[0][0]


def main():
    N = 10  # chromosomes in generation
    probab_crossover = 0.8
    probab_mutation = 0.4
    ammount_of_generations = 20
    generation = []
    unique_numbers = random.sample(range(1, 127), N)

    # first generation draw
    print("First generation:")
    for i in range(0, N):
        generation.append(Chromosome(unique_numbers[i]))

    # print first generation
    printGeneration(generation)

    # list for chart
    populationMean = []
    populationBestVal = []
    populationMean.append(getMeanOfGeneration(generation))
    populationBestVal.append(getBestValueOfGeneration(generation))

    for i in range(0, ammount_of_generations):

        # roulette
        fortuneWheel = linearRoulette(generation)
        #fortuneWheel = squaredRoulette(generation)
        #fortuneWheel = logRoulette(generation)

        # random selection from the roulette wheel
        new_generation = []
        for i in range(0, N):
            new_generation.append(
                fortuneWheel[random.randint(0, len(fortuneWheel)-1)])

        generation = []
        for i in range(0, N, 2):
            # crossover
            if random.uniform(0, 1.0) <= probab_crossover:
                crosscut = random.randint(0, 7)
                parent1_gen = new_generation[i].genotype
                parent2_gen = new_generation[i+1].genotype

                child1_gen = parent1_gen[:crosscut] + parent2_gen[crosscut:]
                child2_gen = parent2_gen[:crosscut] + parent1_gen[crosscut:]

                generation.append(
                    Chromosome(int("".join(str(x) for x in child1_gen), 2)))
                generation.append(
                    Chromosome(int("".join(str(x) for x in child2_gen), 2)))
            # no crossover
            else:
                generation.append(new_generation[i])
                generation.append(new_generation[i+1])

        # mutation
        for i in generation:
            if random.uniform(0, 1.0) <= probab_mutation:
                index_gen = random.randint(0, len(i.genotype)-1)

                if (int(i.genotype[index_gen])):
                    i.genotype[index_gen] = 0
                else:
                    i.genotype[index_gen] = 1
                i.decoding(i.genotype)

        populationMean.append(getMeanOfGeneration(generation))
        populationBestVal.append(getBestValueOfGeneration(generation))

    print("Last generation:")
    printGeneration(generation)

    print("Best value")
    print(getBestValueOfGeneration(generation))

    # charts
    number_of_generations = list(range(1, len(populationMean)+1))
    plt.plot(number_of_generations, populationMean, label="Mean of generation")
    plt.plot(number_of_generations, populationBestVal,
             label="Best Value of generation")
    plt.axis([1, len(populationMean), 1, 130])
    plt.xticks(number_of_generations)
    plt.xlabel('Generation')
    plt.ylabel('Phenotype')
    plt.legend(loc="lower right")
    plt.show()


if __name__ == "__main__":
    main()
