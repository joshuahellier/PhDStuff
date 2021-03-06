#This input file is supposed to perform computations in a purely periodic domain
#To look for phases and stuff, that sort of thing 
import sys
import os

resultDir = os.environ.get('RESULTS')
if resultDir == None :
    print "WARNING! $RESULTS not set! Attempt to write results will fail!\n"

# Expecting input avConc, rateConstFull, sysSize, numSteps, equilSteps, fileCode

from KMCLib import *
from KMCLib.Backend import Backend
import numpy

avConc = float(sys.argv[1])
rateConstFull = float(sys.argv[2])
sysSize = int(sys.argv[3])
numSteps = int(sys.argv[4])
equilSteps = int(sys.argv[5])
fileInfo = sys.argv[6]

resultsPlace = resultDir+"/"+fileInfo+"/"

if not os.path.exists(resultsPlace):
    os.makedirs(resultsPlace)

with open(resultsPlace+'/settings', 'w') as f:
    f.write('AverageConcentration = ' + str(avConc) +'\n')
    f.write('FullRate = ' + str(rateConstFull) +'\n')
    f.write('SysSize = ' + str(sysSize) +'\n')
    f.write('NumSteps = '+str(numSteps) +'\n')
    f.write('EquilSteps = '+str(equilSteps) +"\n")

"""I've put this in the file to make command line input easier"""
# Load the configuration and interactions.
# We're in 1d, so everything's a bit trivial
cell_vectors = [[1.0,0.0,0.0],
                [0.0,1.0,0.0],
                [0.0,0.0,1.0]]

# Only bothering with one set
basis_points = [[0.0, 0.0, 0.0]]

unit_cell = KMCUnitCell(cell_vectors=cell_vectors,
                        basis_points=basis_points)

# Define the lattice.
xRep = 1
yRep = 1
zRep = sysSize
numPoints = xRep*zRep*yRep
lattice = KMCLattice(unit_cell=unit_cell,
                     repetitions=(xRep,yRep,zRep),
                     periodic=(False, False, True))

# Generate the initial types; note that there's no top or bottom atoms in this simulation.
types = ["V"]*numPoints

#Stick
width = int(zRep*avConc)
start = sysSize/2 - width/2
end = start + width
for i in range(start, end):
    types[i] = "O"
    """
    # find a site which is not yet occupied by a "O" type.
    pos = int(numpy.random.rand()*zRep)
    while (types[pos] != "V"):
        pos = int(numpy.random.rand()*zRep)
    # Set the type.
    types[pos] = "O"
    """

# Setup the configuration.
configuration = KMCConfiguration(lattice=lattice,
                                 types=types,
                                 possible_types=["O","V"])





# Rates.
rateConstEmpty        	= 1.0

#
##
###
"""I've put the processes in here to make it easier to adjust them via command line arguments."""

# Fill the list of processes.
processes = []

# Only on the first set of basis_points for O/V
basis_sites     = [0]

# Bulk processes

# Up, empty.
#0
elements_before = ["O", "V"]
elements_after  = ["V", "O"]
coordinates = [[0.0, 0.0,  0.0], [0.0, 0.0, 1.0]]
processes.append( KMCProcess(coordinates=coordinates,
                             elements_before=elements_before,
                             elements_after=elements_after,
                             basis_sites=basis_sites,
                             rate_constant=1.0))
# Will customise

# Down, empty.
#1
elements_before = ["O", "V"]
elements_after  = ["V", "O"]
coordinates = [[0.0, 0.0, 0.0], [0.0, 0.0, -1.0]]
processes.append( KMCProcess(coordinates=coordinates,
                             elements_before=elements_before,
                             elements_after=elements_after,
                             basis_sites=basis_sites,
                             rate_constant=1.0))
# Will customise




# Create the interactions object.
interactions = KMCInteractions(processes, implicit_wildcards=True)

# Define the custom rates calculator, using the lol model as a template
class modelRates(KMCRateCalculatorPlugin):
    """ Class for defining the custom rates function for the KMCLib paper. """
    def rate(self, geometry, elements_before, elements_after, rate_constant, process_number, global_coordinate):
        if len([e for e in elements_before if e == "O"]) == 2:
            return rateConstFull
        else:
            return rateConstEmpty


    def cutoff(self):
        """ Overloaded base class API function """
        return 1.0

interactions.setRateCalculator(rate_calculator=modelRates)




"""End of processes"""
###
##
#

# Create the model.
model = KMCLatticeModel(configuration, interactions)


# Define the parameters; not entirely sure if these are sensible or not...
control_parameters = KMCControlParameters(number_of_steps=numSteps, dump_interval=numSteps)

# Run the simulation - save trajectory to resultsPlace, which should by now exist

model.run(control_parameters, trajectory_filename=(resultsPlace+"Inittraj1.tr"))

# Define the parameters; not entirely sure if these are sensible or not...
control_parameters = KMCControlParameters(number_of_steps=equilSteps, dump_interval=1)

# Run the simulation - save trajectory to resultsPlace, which should by now exist

model.run(control_parameters, trajectory_filename=(resultsPlace+"traj.tr"))

print("Process would appear to have succesfully terminated! How very suspicious...")
