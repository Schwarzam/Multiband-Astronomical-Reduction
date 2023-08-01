import os
import subprocess


"""
Test adapting to IRAF in MAC-OSX
"""

os.system('PATH=/bin:/Users/gustavo/.iraf/bin:${PATH}:/Users/gustavo/.iraf/bin:${PATH}')

params = {"input": "@lista.txt", "output": "test.fits", 
          "gain": 0.96, "reject": "ccdclip", 
          "combine": "median", "outtype": "real", "zero": "mode",
          "rdnoise": 6, "maskvalue": 0, "lthresh": "INDEF", 
          "hthresh":"INDEF", "pclip":(-0.5), "grow": 0, "sigscale": 0.01,
          "statsec":"[28:1179,1:4616]", "offsets": "none", "weight": "none",
          "project": "no"}
folder = "/Users/gustavo/Documents/t80testblock/BIASOV/"

files = os.listdir(folder)
listfile = ""

for file in files:
    if 'fits' in file:
        listfile = listfile + folder + file + "[1]\n"

f = open('lista.txt', 'w')
f.write(listfile)
f.close()

string = "imcombine"

for param in params:
    if isinstance(params[param], int) or isinstance(params[param], float):
        string = string + " " + param + "=" + str(params[param])
    else:
        string = string + " " + param + "=" + str(params[param])
    
string = string + '\n' + 'logout'

file = open('clfile.cl', 'w')
file.write(string)
file.close()

os.system('cl < clfile.cl')