import arcpy
from arcpy import env

# set the workspace for arcpy functions
env.workspace = "F:\SCIE 441\ROBINSON PROEJCTED TM EDITED\cart proof of concept"

input_shapefile = "sample_euro_countries.shp"
 # SET THIS TO AN APPROPRIATE OUTPUT SHAPEFILE NAME
 
input_shp_extent = arcpy.Describe(input_shapefile).extent

# Mathematically (conceptually) move (by adding/subtracting) all the density grid and vertex coordinates so that the bottom-left corner of the grid is at 0,0. Then, work out what to divide both x and y of the top-right corner of the grid by in order that they are both 256. Then, apply this same number to each of the vertex coordinates in order to find it's 256x256 position.

# Calculating the 3x3 grid coordinates, and making sure the grid is square (increasing it in one dimension if necessary)
xRange = (input_shp_extent.Xmax - input_shp_extent.Xmin)
yRange = (input_shp_extent.Ymax - input_shp_extent.Ymin)
newXmin = (input_shp_extent.Xmin - xRange)
newYmin = (input_shp_extent.Ymin - yRange)
newXmax = (input_shp_extent.Xmax + xRange)
newYmax = (input_shp_extent.Ymax + yRange)
newXRange = (newXmax - newXmin)
newYRange = (newYmax - newYmin)

if newXRange > newYRange:
    newYmax = newYmin + newXRange
else:
    newXmax = newXmin + newYRange

Xchange = (0 - newXmin)
Ychange = (0 - newYmin)
Xconverter = ((newXmax + Xchange)/256)
Yconverter = ((newYmax + Ychange)/256)


vertices_output = open('vertices.txt', 'w')
st = ''

desc = arcpy.Describe(input_shapefile)
shapefieldname = desc.ShapeFieldName

rows = arcpy.SearchCursor(input_shapefile)

# Enter for loop for each feature/row
#
for row in rows:
        
    # Create the geometry object
    #
    feat = row.getValue(shapefieldname)

    # Print the current multipoint's ID
    #
    st = st + "%s:\n" % row.ISO3
    partnum = 0

    # Step through each part of the feature
    #
    for part in feat:
        # Print the part number
        #
        st = st + "Part %i:\n" % partnum

        # Step through each vertex in the feature
        #
        for pnt in feat.getPart(partnum):
            if pnt:
                # Print x,y coordinates of current point
                #
                st = st + str((pnt.X + Xchange) / Xconverter) + ' ' +  str((pnt.Y + Ychange) / Yconverter) + "\n"
            else:
                # If pnt is None, this represents an interior ring
                #
                st = st + "Interior Ring:\n"
        partnum += 1
        
del row
del rows
del feat        

vertices_output.write(st)
vertices_output.close()