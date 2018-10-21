# A Simple Neural Evolution Simulator

This is a project that allowed me to combine evolutionary algorithms with neural networks. It works as follows: 

- There is a map (whose dimensions are labeled at the beginning of the python file)

- There are animals (which are displayed as the character 'o' in the map)

- There is food (which is displayed as the character 'star' in the map)

- Each animal has a neural network inside of it that governs which directiont they will move (left, right, up, or down). The input to this neural network is the distance to the closest food item.

- Initially the weights of the neural networks are randomized, and the fittest animals are the ones that can eat the most amount of food in a given time period. Animals that are unable to get food (or eat above a certain threshold of food) die.

- After the time period ends, the surviving animals randomly mate with each other in which the weights of the neural networks of the children are a combination of the weights of both the parents.

- The children are then released into the map where they try to find food as well.

- This entire process can go on for a varible number of generations.

## Getting Started

Install Python 3.5

### Prerequisites

You will need the following libraries that you can get through pip

```
pip install numpy
```

### Running

Run main.py on command prompt or terminal

