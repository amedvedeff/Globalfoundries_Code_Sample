# Python_Code_Sample


This code sample displays an interpretation of the Age-Fitness Pareto Optimization algorithm as described [here](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.375.6168&rep=rep1&type=pdf)

**To Read the Code**

Begin with search.py, as this is the program that is called from command line. Notice, it refers to the AFPO class, this is your next destination, AFPO.py. This establishes the actual implementation of the AFPO algorithm. The rest of the code essentially builds a world (the "physical" conditions), the robot (the "organism" moving in the world), and a neural network (the "brain" of the organism describing how the parts should move).

From AFPO.py, look at solution.py to see how a robot is generated and how the simulation begins. This file calls the os to begin simulate.py which triggers methods in simulation.py. This is where the actual simulation takes place. The building block of the simulation (world.py, robot.py, motor.py, and sensor.py) do not need to be viewed in any particular order.

These files are intended to be read for style and documentation. If instructions for implementation are desired please contact me at medvedeffalexander@gmail.com
