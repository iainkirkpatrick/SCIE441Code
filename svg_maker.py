def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

verts = open('verticescartfra.txt')
f = open('FRAcartvertSVG.txt', 'w')
s = ''

lines = verts.readlines()

for line in lines:
    if is_number(line[0]) == True:
        s = s + line.strip('\n') + ' '
    else:
        s = s + 'M' + ' '

f.write(s)
f.close()    