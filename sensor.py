import numpy
import constants as c
import pyrosim.pyrosim as pyrosim
import pathlib

class Sensor:
    """
    The Sensor class retrieves and saves the sensor values for each link in the Robot.

    ...
    Parameters
    __________
    LinkName : str
        Assigned from Robot class

    Attributes
    __________
    LinkName : str
        Assigned from Robot class

    Values : np array
        an array which holds the sensor value after the simulation occurs.


    Methods
    ________
    get_value(x)
        Returns the array from self.values

    save_value ()
        Saves the values to a file on disk
    """
    def __init__(self, LinkName):
        self.LinkName = LinkName
        self.Values = numpy.zeros(c.NUM_STEPS)


    def get_value(self, x):
        self.Values[x] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.LinkName)

    def save_value (self):
        numpy.save(r'C:\Users\Administrator\Documents\LUDObots\data\sensorValues.npy', self.Values)