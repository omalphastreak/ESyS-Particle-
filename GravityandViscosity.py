#
#import the appropriate ESyS-Particle modules:
from esys.lsm import *
from esys.lsm.util import Vec3, BoundingBox
from POVsnaps import POVsnaps
#instantiate a simulation object
#and initialise the neighbour search algorithm:
sim = LsmMpi(numWorkerProcesses=1, mpiDimList=[1,1,1])
sim.initNeighbourSearch(
particleType="NRotSphere",
gridSpacing=2.5,
verletDist=0.5
)
#set the number of timesteps and timestep increment:
sim.setNumTimeSteps(20000)
sim.setTimeStepSize(0.001)
#specify the spatial domain for the simulation:
domain = BoundingBox(Vec3(-20,-20,-20), Vec3(20,20,20))
sim.setSpatialDomain(domain)
#add a particle to the domain:
particle=NRotSphere(id=0, posn=Vec3(0,5,0), radius=1.75, mass=1.8)
particle.setLinearVelocity(Vec3(1.0,10.0,1.0))
sim.createParticle(particle)
#initialise gravity in the domain:
sim.createInteractionGroup(
GravityPrms(name="earth-gravity", acceleration=Vec3(0,-9.81,0))
)
#add a horizontal wall to act as a floor on which to bounce particles:
sim.createWall(
name="floor",
posn=Vec3(0,-10,0),
normal=Vec3(0,1,0)
)
#specify the type of interactions between wall and particles:
sim.createInteractionGroup(
NRotElasticWallPrms(
name = "elasticWall",
wallName = "floor",
normalK = 10000.0
)
)
#add local viscosity to simulate air resistance:
sim.createInteractionGroup(
LinDampingPrms(
name="linDamping",
viscosity=0.1,
maxIterations=100
)
)
#add a POVsnaps Runnable:
povcam = POVsnaps(sim=sim, interval=100)
povcam.configure()
sim.addPostTimeStepRunnable(povcam)
#execute the simulation
sim.run()
