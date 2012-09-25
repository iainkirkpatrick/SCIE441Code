'''MEGASCRIPT for SVG cartogram creation from original shapefile and attribute field. Created by Iain Kirkpatrick - email kirkpatrick.iain@gmail.com for queries about functionality

25/09 UPDATE: What the megascript does at this point is create the density grid for the chose .shp and field input. 
'''

import arcpy
from arcpy import env

# set the workspace for arcpy functions
env.workspace = "F:\SCIE 441\ROBINSON PROEJCTED TM EDITED\cart proof of concept"

# Define the original shapefile that the cartogram is based upon
input_shapefile = "sample_euro_countries.shp"

# access the appropriate field for cartogram manipulation (via SearchCursor?) ##Does this go here?

# "create fishnet" tool. settings: polygons, extent should be the template plus the 3x3 grid (how to do this in arcpy?) or perhaps something a bit smaller (1.5x1.5?), rows and columns should be suitable for the size of the shapefile (may have to test this a bit?), generate the label points (if this is possible in arcpy?)
## else "feature to point" on the fishnet polygons to generate centroids

fishnet_shp = "sample_euro_countries_fishnet.shp" # SET THIS TO AN APPROPRIATE OUTPUT SHAPEFILE NAME

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
## the output label file of points is just the fishnet_shp with '_label' on the end
fishnet_pts = fishnet_shp.split('.')[0]+"_label.shp"

# "spatial join" on the label points as the target, with the original shapefile as the feeder - the fields to join are the appropriate field for cartogram manipulation and the ISO3 field.
# for those points that now still have a appropriate field value of 0, assign the mean of those that do not have 0 (so for all values > 0, add them together and divide by the number (will this work?))
## else may have to code in the more cumbersome method I utilised manually

fishnet_pts_spatjoin = fishnet_shp.split('.')[0]+"_label_spatjoin.shp"

arcpy.SpatialJoin_analysis(fishnet_pts, input_shapefile, fishnet_pts_spatjoin) #NB. this takes forever at this stage - approx 30 mins. Speed could potentially be increased by limiting the fields joined, but looks like to do this programatically it requires use of a 'field mappings' object, which I would have to learn about etc.

rows = arcpy.SearchCursor(fishnet_pts_spatjoin, "POP2005 > 0", "", "POP2005") # SET THIS TO THE APPROPRIATE FIELD FOR BASIS OF CARTOGRAM (and also the options following in the next few lines should be similarly set)
i = 0
total_pop = 0
for row in rows:
    i+=1
    total_pop = total_pop + row.POP2005
mean_pop = (total_pop / i)
del row
del rows

update_rows = arcpy.UpdateCursor(fishnet_pts_spatjoin, "POP2005 = 0", "", "POP2005")
for row in update_rows:
    row.POP2005 = mean_pop
    update_rows.updateRow(row)
del row
del update_rows

# "export feature attribute to ASCII". settings: value fields should be just the appropriate field for cartogram manipulation field.









##arcpy.ExportXYv_stats(fishnet_pts_spatjoin, "POP2005", "SPACE", "europop", "NO_FIELD_NAMES") ##This is crashing the python.exe for the moment, or else throwing up an IOError - may have to ask Andy as to what is going on here. 










'''From here, run the mini-script below with the input dgrid as the output ASCII file from above'''

'''Utility program to convert from a prepared ASCII density grid, exported from Arc, to a density grid suitable for CART'''

# Opening target ASCII grid, and creating output file x.dat with write permissions
dgrid = open('europop')
f = open('europop.dat', 'w')

s = ''
final = ''
previousValue = ''
for line in dgrid.readlines():
    line = line.split(' ')
    pop_value = line[2].rstrip('\n')
    
    if previousValue == '': #for the first pass through the lines
        s = pop_value
        previousValue = line[1]
    elif line[1] == previousValue:
        s = s + ' ' + pop_value        
    else:
        s = s + '\n' + pop_value
        previousValue = line[1]

# The grid is currently in reverse order - need to reverse the order of the rows       
holder = s.split('\n')
holder.reverse()
for i in holder:
    final = final + i + '\n'

# Finally, strip the extra \n off of the end of the string    
final = final.strip('\n')

f.write(final)
f.close()

'''At this point, a .dat file for the original shapefile and appropriate field for cartogram manipulation has been generated. From here, the steps are generating the cartogram - involves running CART and INTERP with a wrapper of command line code, inputting the vertex geometry read from the original shapefile into CART and INTERP in a single file (and converting these coordinates to those of the density grid, possibly by also reading the DENSITY GRID geometry to get the corner coordinates), matching the output vertices with their respective ISO3 codes, and finally writing SVG files with extents based upon the extent of the density grid, and 'd' data based upon the vertices of each (original shapefile and cartogram).'''

'''NOTE: it is clear that this mega-script should really only focus on cartogram generation - i.e. assuming the original shapefile has already been made into an SVG. Of course, I will need a script to do precisely that for a single use - which should only be a matter of bastardising some of this mega-script for the purpose.'''


## Actually - this may have to be the end of the line for this part at least of the MEGASCRIPT - given the server doesn't have Arc, and installing CART/INTERP on the local machine is counter-intuitive to the longevity of this script, might be best to stop this script after the generation of the file to pipe through INTERP and then have a script that runs on the server that handles all the CART, INTERP input and output, and then another script on the server simply for converting the INTERP output to an SQL file, and inserting that file into a PostGreSQL database.

# Generate the list (or lists!) of vertices from the original shapefile of the countries, in a document format suitable for piping through INTERP. NB. Will have an issue with writing the new vertices back in if I do not know what country, AND what order the vertices go in! So need to figure out a way of organisation (the reading geometries example helps a bit?). FURTHER NB. Apparently good practice to make the start point of the lineArray the same as the end point, if possible.