import pybullet as p

class World:
    """
    The Worled class establishes the physical conditions of the robot's environment.
       ...
    Attributes
    __________
    PlaneId : pybullet loadURDF
        The variable begins the loading of the world

    Methods
    ________
    None
    """

    def __init__(self):
        self.PlaneId = p.loadURDF("plane.urdf")
        p.loadSDF("world.sdf")
        pass
