from sensor import Sensor
from motor import Motor
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c
import os

class Robot:
    """
    Configures all components of a simulated Robot in PyBullet simulator. The Robot class establishes
    a joint, motor, and sensor functions prior to simulation.

    ...

    Parameters
    __________
    solutionID : int
        Assigned from AFPO class

    Attributes
    __________
    Sensors : arr
        Holds all Sensor links

    Motors : arr
        Holds all Motor links

    Robot : pybullet body plan
        Establishes body plan prior to simulation

    NN : NEURAL_NETWORK
        Creates the neural network for the Robot body by creating a file that establishes the weighted values
        between Sensors and Motors


    Methods
    ________
    prepare_to_sense():
        Establishes values for each sensor by call Sensor class

    sense(t):
        Returns the values of each Sensor according to the index value, t

    prepare_to_act():
        Establishes connections between each joint

    act(t):
        Set the value for each motor joint with a desired angle for the Robot. Each value is also printed

    think():
        The neural network is updated and printed

    get_fitness(solutionID):
        Creates a fitness.txt file on disk for a certain Robot. Note the Fitness value is negative since it is currently
        decided by the distance the Robot travels "away" from the camera, which is a negative coordinate value.
    """
    def __init__(self, solutionID):
        self.Sensors = {}
        self.Motors = {}
        self.Robot = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate("body.urdf")
        self.prepare_to_sense()
        self.prepare_to_act()
        self.NN = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")

        os.system("rm brain" + str(solutionID) + ".nndf")

    def prepare_to_sense(self):
        self.Sensors = {}
        for LinkName in pyrosim.linkNamesToIndices:
            self.Sensors[LinkName] = Sensor(LinkName)

    def sense(self, t):
       for i in self.Sensors:
            self.Sensors[i].get_value(t)

    def prepare_to_act(self):
        for JointName in pyrosim.jointNamesToIndices:
            self.Motors[JointName] = Motor(JointName)

    def act(self, t):
        for NeuronName in self.NN.Get_Neuron_Names():
            if self.NN.Is_Motor_Neuron(NeuronName):
                JointName = self.NN.Get_Motor_Neurons_Joint(NeuronName)
                DesiredAngle = self.NN.Get_Value_Of(NeuronName) * c.MOTOR_JOINT_RANGE
                for i in self.Motors:
                    self.Motors[i].set_value(self.Robot, DesiredAngle)
                print(NeuronName, JointName, DesiredAngle)

    def think(self):
        self.NN.Update()
        self.NN.Print()

    def get_fitness(self, solutionID):
        stateOfLinkZero = p.getLinkState(self.Robot, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = str(positionOfLinkZero[0])
        f = open("tmp" + str(solutionID) + ".txt", "w")
        f.write(xCoordinateOfLinkZero)
        f.close()

        os.rename("tmp" + str(solutionID) + ".txt", "fitness" + str(solutionID) + ".txt")
        exit()