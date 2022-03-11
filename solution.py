import numpy
import pyrosim.pyrosim as pyrosim
import random
import os
import time
import constants as c

class Solution:
    """
    Solution class set ups the basic components of the Robot and establishes the neural network associated with a
    particular Robot.

    ...

    Parameters
    __________
    NextAvailableID
        Passed in from AFPO class

    Attributes
    __________
    Weights : int
        Used to assign random weights in the neural network
    MyID : int
        Equal to NextAvailableID assigned from AFPO class
    MyAge : int
        Keeps track of age for a Robot

    Methods
    ________
    evaluate(self, DirectOrGUI)
        Places the Robot in the World and determines the fitness of this Robot

    start_simulation(DirectOrGUI)
        The simulation begins, DirectOrGui determines if the simulation will be calculated or shown on screen

    wait_for_simulation_to_end()
        This method halts the rest of the program until a ftiness file is found and recorded

    create_world()
        Establishes the particular conditions of the world

    create_body()
        Establishes the particular body plan for the robot

    create_brain()
        Establishes the particular neural network for the robot

    mutate()
        Randomly changes the weights for a random neuron in the neural network
    """
    def __init__(self, NextAvailableID):
        self.Weights = (numpy.random.rand(c.NUM_SENSOR_NEURONS, c.NUM_MOTOR_NEURONS) * 2) - 1
        self.MyID = NextAvailableID
        self.MyAge = 0

    def evaluate(self, DirectOrGUI):
        self.create_world()
        self.create_body()
        self.create_brain()
        FitnessFloatValue = 0
        os.system("start /B python simulate.py " + DirectOrGUI + " " + str(self.MyID))

        while not os.path.exists("fitness" + str(self.MyID) + ".txt"):
            time.sleep(0.01)

        f = open("fitness" + str(self.MyID) + ".txt")
        FitnessFloatValue = float(f.read())
        self.Fitness = FitnessFloatValue
        f.close()

    def start_simulation(self, DirectOrGUI):
        self.create_world()
        self.create_body()
        self.create_brain()
        fitnessFloatValue = 0
        os.system("start /B python simulate.py " + DirectOrGUI + " " + str(self.MyID))

    def wait_for_simulation_to_end(self):
        while not os.path.exists("fitness" + str(self.MyID) + ".txt"):
            time.sleep(0.01)

        f = open("fitness" + str(self.MyID) + ".txt")
        fitnessFloatValue = float(f.read())
        self.Fitness = fitnessFloatValue
        f.close()

        os.system("rm fitness" + str(self.MyID) + ".txt")

    def create_world(self):
        length = 1.0
        width = 1.0
        height = 1.0
        x = -2
        y = 2
        z = 0.5
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
        pyrosim.End()

    def create_body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position="0 -0.5 1.0", jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[.2, 1, .2])
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position="0 -1 0", jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5], size=[.2, .2, 1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position="0 0.5 1.0", jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[.2, 1, .2])
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position="0 1 0", jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5], size=[.2, .2, 1])
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position="-0.5 0 1.0", jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0], size=[1, .2, .2])
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute", position="-1 0 0", jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -0.5], size=[.2, .2, 1])
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position="0.5 0 1.0", jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0], size=[1, .2, .2])
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position="1 0 0", jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -0.5], size=[.2, .2, 1])
        pyrosim.End()

    def create_brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.MyID) + ".nndf")

        pyrosim.Send_Sensor_Neuron(name=0, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="RightLowerLeg")


        pyrosim.Send_Motor_Neuron(name=8, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=9, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightLeg_RightLowerLeg")


        for currentRow in range(0, c.NUM_SENSOR_NEURONS):
            for currentCol in range(0, c.NUM_MOTOR_NEURONS):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentCol+c.NUM_SENSOR_NEURONS, weight=self.Weights[currentRow][currentCol])

        pyrosim.End()

    def mutate(self):
        randomRow =random.randint(0, c.NUM_MOTOR_NEURONS)
        randomColumn = random.randint(0,1)
        self.Weights[randomRow][randomColumn] = random.random() * 2 - 1

