from KMCLib import *
import numpy

# Define the unit cell. We're going for hcp here, with c/a set for sphere-packing ratio for now.
cell_vectors = [[1.0,0.0,0.0],
                [0.0,1.0,0.0],
                [0.0,0.0,1.0]]

# I've set these up so that the Titaniums sit on the 1st and 3rd basis points, and the Oxygens on the others,
# where the octahedral interstitials are supposed to be
basis_points = [[0.0, 0.0, 0.0]]

unit_cell = KMCUnitCell(cell_vectors=cell_vectors,
                        basis_points=basis_points)

# Define the lattice.
xRep = 1
yRep = 1
zRep = 20
numPoints = xRep*(zRep+4)*yRep
lattice = KMCLattice(unit_cell=unit_cell,
                     repetitions=(xRep,yRep,zRep+4),
                     periodic=(False, False, True))

# Generate the initial types. I'm aiming to put Ti/Nb on the 1st and 3rd sites, and O/V on the 2nd and 4th,
# i.e. the Tis on the main sites with some substituted for Nbs, and vacancies on the interstitials except for a few Os.
types = ["V"]*numPoints
types[0] = "Bo"
types[1] = "Bo"
types[-2] = "To"
types[-1] = "To"

# Setup the configuration.
configuration = KMCConfiguration(lattice=lattice,
                                 types=types,
                                 possible_types=["O","V","To","Bo"])

# Use the _script() function to get a script that can generate the configuration.
print "from KMCLib import *"
print configuration._script()
