from world import World
from robot import Robot

import time
import pybullet as p
import pyrosim.pyrosim as pyrosim
import pybullet_data
import numpy
import constants as c
import math
import random
import pathlib



class Simulation:
    """
    The Simulation class places the Robot in the simulated World and measures the Robot's fitness in this environment.
    ...

    Parameters
    ___________
    DirectOrGUI : str
        Used to guide the simulator. Direct implies no visual, GUI implies the Robot's motion will be shown on screen.

    SolutionID : str
        Assigned from AFPO class

    Attributes
    __________
    DirectOrGUI : str
        Passed in from instantiation of class

    World : World
        Establishes the World conditions for simulation

    Robot : Robot
        Establishes Robot conditions for simulation

    Methods
    ________
    run()
        Passes in all components of simulation, including the Robot and World components

    get_fitness(solutionID)
        Returns fitness value of a Robot after simulation
    """
    def __init__(self, DirectOrGUI, SolutionID):
        if DirectOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        elif DirectOrGUI == "GUI":
            self.physicsClient = p.connect(p.GUI)

        self.DirectOrGUI = DirectOrGUI
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.World = World()
        self.Robot = Robot(SolutionID)

    def run(self):
        BackLegSensorValues = numpy.zeros(c.NUM_STEPS)
        FrontLegSensorValues = numpy.zeros(c.NUM_STEPS)
        FrontLegTargetAngles = c.FRONT_LEG_AMPLITUDE * numpy.sin(c.FRONT_LEG_FREQUENCY * numpy.linspace(-numpy.pi, numpy.pi,
                                                                                                        c.NUM_STEPS) +
                                                                 c.FRONT_LEG_PHASE_OFFSET)

        BackLegTargetAngles = c.BACK_LEG_AMPLITUDE * numpy.sin(c.BACK_LEG_FREQUENCY * numpy.linspace(-numpy.pi, numpy.pi,
                                                                                                     c.NUM_STEPS) +
                                                               c.BACK_LEG_PHASE_OFFSET)

        for x in range (0, c.NUM_STEPS):
            p.stepSimulation()
            self.Robot.sense(x)
            self.Robot.think()
            self.Robot.act(x)
            if self.DirectOrGUI == "GUI":
                time.sleep(c.SLEEP_AMOUNT)

    def get_fitness(self, solutionID):
        self.Robot.get_fitness(solutionID)

    def __del__(self):
        p.disconnect()
