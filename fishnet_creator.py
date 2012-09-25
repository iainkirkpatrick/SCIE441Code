import arcpy
from arcpy import env

# set the workspace for arcpy functions
env.workspace = "F:\SCIE 441\ROBINSON PROEJCTED TM EDITED\cart proof of concept"

# Define the original shapefile that the cartogram is based upon
input_shapefile = "sample_euro_countries.shp"

# access the appropriate field for cartogram manipulation (via SearchCursor?) ##Does this go here?

# "create fishnet" tool. settings: polygons, extent should be the template plus the 3x3 grid (how to do this in arcpy?) or perhaps something a bit smaller (1.5x1.5?), rows and columns should be suitable for the size of the shapefile (may have to test this a bit?), generate the label points (if this is possible in arcpy?)
## else "feature to point" on the fishnet polygons to generate centroids

fishnet_shp = "sample_euro_countries_fishnet.shp"

##spat_ref = arcpy.CreateSpatialReference_management("", input_shapefile)

input_shp_extent = arcpy.Describe(input_shapefile).extent

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

originCoordinate = str(newXmin) + ' ' + str(newYmin)
yAxisCoordinate = str(newXmin) + ' ' + str(newYmin + 10)
cellSizeWidth = '0'
cellSizeHeight = '0'
numRows =  '256'
numColumns = '256'

oppositeCornerCoordinate = str(newXmax) + ' ' + str(newYmax)

# Create a point label feature class 
labels = 'true'

# Extent is set by origin and opposite corner - no need to use a template fc
templateExtent = '#'

# Each output cell will be a polygon
geometryType = 'POLYGON'

arcpy.CreateFishnet_management(fishnet_shp, originCoordinate, yAxisCoordinate, cellSizeWidth, cellSizeHeight, numRows, numColumns, oppositeCornerCoordinate, labels, templateExtent, geometryType)
