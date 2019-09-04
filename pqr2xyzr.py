import sys

pqr_name = sys.argv[1]
xyzr = open('NanoShaper_input.xyzr','w') #generate modified file

pqr_file = open(pqr_name,'r')
for line in pqr_file:
    if line[:4] == "ATOM":
        x = line[30:38]
        y = line[38:46]
        z = line[46:54]
        r = line[63:70]
        linemod = x + ' ' + y + ' ' + z + ' ' + r + "\n"
        #print(linemod)

        xyzr.write(linemod)
    

#Save output
pqr_file.close()
xyzr.close()

print("Converted to xyzr")
