#import the appropriate ESyS-Particle modules:
from esys.lsm import *
from esys.lsm.util import *
from esys.lsm.geometry import *
#instantiate a simulation object
#and initialise the neighbour search algorithm:
sim = LsmMpi (numWorkerProcesses = 1, mpiDimList = [1,1,1])
sim.initNeighbourSearch (
particleType = "NRotSphere",
gridSpacing = 2.5000,
verletDist = 0.1000
)
#specify the number of timesteps and the timestep increment:
sim.setNumTimeSteps (100000)
sim.setTimeStepSize (1.0000e-04)
#specify the spatial domain for the simulation:
domain = BoundingBox(Vec3(-20,-20,-20), Vec3(20,20,20))
sim.setSpatialDomain(domain)
#construct a block of particles with radii in range [0.2,0.5]:
geoRandomBlock = RandomBoxPacker (
minRadius = 0.2000,
maxRadius = 0.5000,
cubicPackRadius = 2.2000,
maxInsertFails = 1000,
bBox = BoundingBox(
Vec3(-5.0000, 0.0000,-5.0000),
Vec3(5.0000, 10.0000, 5.0000)
),
circDimList = [False, False, False],
tolerance = 1.0000e-05
)
geoRandomBlock.generate()
geoRandomBlock_particles = geoRandomBlock.getSimpleSphereCollection()
#add particles to simulation one at a time,
#tagging those nearest the floor:
for pp in geoRandomBlock_particles:
centre = pp.getPosn()
radius = pp.getRadius()
Y = centre[1]
if (Y < 1.1*radius):
pp.setTag(12321) # tag particles nearest to the floor
sim.createParticle(pp) # add the particle to the simulation object
#add a wall as a floor for the model:
sim.createWall (
name = "floor",
posn = Vec3(0.0000, 0.0000, 0.0000),
normal = Vec3(0.0000, 1.0000, 0.0000)
)
#specify that particles undergo frictional interactions:
sim.createInteractionGroup (
NRotFrictionPrms (
name = "friction",
normalK = 1000.0,
dynamicMu = 0.6,
shearK = 100.0,
scaling = True
)
)
#specify that tagged particles undergo
#bonded elastic interactions with floor:
sim.createInteractionGroup (
NRotBondedWallPrms (
name = "floor_bonds",
wallName = "floor",
normalK = 10000.0,
particleTag = 12321
)
)
#specify the direction and magnitude of gravity:
sim.createInteractionGroup (
GravityPrms (
name = "gravity",
acceleration = Vec3(0.0000, -9.8100, 0.0000)
)
)
#add viscosity to damp particle oscillations:
sim.createInteractionGroup (
LinDampingPrms (
name = "viscosity",
viscosity = 0.1000,
maxIterations = 100
)
)
#add a CheckPointer to store simulation data:
sim.createCheckPointer (
CheckPointPrms (
fileNamePrefix = "slope_data",
beginTimeStep = 0,
endTimeStep = 100000,
timeStepIncr = 1000
)
)
#execute the simulation:
sim.run()
