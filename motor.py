import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy
import constants as c
import pathlib

class Motor:
    """
    Motor class establishes the values for each joint and motion in a Robot.
    ...

    Attributes
    __________
    JointName : str
        Assigned value from Robot class

    Methods
    ________
    prepare_to_act()
        Sets parameters on each aspect of a joint prior to simulation

    set_value(robot, desiredAngle)
        Assigns the motor values to the robot

    save_values()
        Saves values to disk
    """
    def __init__(self, jointName):
        self.JointName = jointName
        self.prepare_to_act()

    def prepare_to_act(self):
        self.MotorValues = numpy.zeros(c.NUM_STEPS)
        self.Values = numpy.linspace(-numpy.pi, numpy.pi, c.NUM_STEPS)
        self.Frequency = c.BACK_LEG_FREQUENCY
        self.Amplitude = c.BACK_LEG_AMPLITUDE
        self.Offset = c.BACK_LEG_PHASE_OFFSET

        if self.JointName == "Torso_FrontLeg":
            self.Frequency *= 2

        for i in range(c.NUM_STEPS):
            self.MotorValues[i] = (self.Amplitude * numpy.sin(self.Frequency * self.Values[i] + self.Offset))

    def set_value(self, Robot, DesiredAngle):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = Robot,
            jointName = self.JointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = DesiredAngle,
            maxForce = c.FORCE_AMOUNT)

    def save_values(self):
        numpy.save(r'C:\Users\Administrator\Documents\LUDObots\data\motorValues.npy', self.MotorValues)