import arcpy
from arcpy import env

# set the workspace for arcpy functions
env.workspace = "F:\SCIE 441\ROBINSON PROEJCTED TM EDITED\cart proof of concept"

countries = "sample_euro_countries.shp" # SET THIS TO AN APPROPRIATE OUTPUT SHAPEFILE NAME

country_dict = {}
vertices_dict = {} # Think a dictionary is good storage for this task. Key is essentially the country, and values are arrays of points that make up contiguous lines.

desc = arcpy.Describe(countries)
shapefieldname = desc.ShapeFieldName

rows = arcpy.SearchCursor(countries)

# Enter for loop for each feature/row
#
for row in rows:
    # Create the geometry object
    #
    feat = row.getValue(shapefieldname)

    # Print the current multipoint's ID
    #
    feat_num = "Feature %i:" % row.getValue(desc.OIDFieldName)
    partnum = 0
    
    country_dict[feat_num] = {}    
    
    # Step through each part of the feature
    #
    for part in feat:
        # Print the part number
        #
        part_num = "Part %i:" % partnum
        
        vertices_dict[part_num] = [] # Creating an empty list for the part_num (key) to append coordinate tuples to
        
        # Step through each vertex in the feature
        #
        for pnt in feat.getPart(partnum):
            if pnt:
                # Print x,y coordinates of current point
                #
                
                #print pnt.X, pnt.Y
                
                vertices_dict[part_num].append((pnt.X, pnt.Y)) # Appending to the list (value) a tuple of coordinate points
            else:
                # If pnt is None, this represents an interior ring
                #
                
                #print "Interior Ring:"
                
                part_num = part_num + ' IR:'
                vertices_dict[part_num] = []
        partnum += 1 
    
    country_dict[feat_num] = vertices_dict
    
del row
del rows
del feat