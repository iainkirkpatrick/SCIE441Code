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