import pandas as pd
import mar

from astropy.io import fits
from os.path import join

rd_folder = "/home/gustavo/MAR/reductionmedia"
outfolder = "/home/gustavo/testes"

df = pd.read_csv("source.csv")
zps = pd.read_csv("iDR4_zero-points.csv")
params = open("params.txt", "r").readlines()

fieldslist = []
for key, value in df.iterrows():
    print("started ", value['field'])
    im = fits.open(join(rd_folder, value['file_path']))

    sextr = mar.reduction.SExtractorCatalog(join(rd_folder, value["file_path"]), folder=outfolder, catname=value['field'] + ".cat")
    
    sextr.config['GAIN']['value'] = im[0].header['GAIN']
    sextr.config['SATUR_LEVEL']['value'] = im[0].header['SATURATE']
    sextr.config['SEEING_FWHM']['value'] = im[0].header['MAR PRO FWHMSEXT']
    sextr.config['PHOT_APERTURES']['value'] = "1.45454545455,1.81818181818,2.18181818182,2.72727272727,3.63636363636,5.45454545455,7.27272727273,10.9090909091"
    sextr.config['BACK_SIZE']['value'] = 512
    sextr.params = params 
    
    

    zp = zps[zps['Field'] == value['field']]
    print("zp: ", zp)
    if len(zp) >= 1:
        print("zp found! ")
        zp = float(zp['ZP_r'])
        print(zp)
    else:
        print("zp not found")
        zp = 23

    sextr.config['MAG_ZEROPOINT']['value'] = zp
    sextr.run()
    
    fieldslist.append(join(outfolder, value['field'] + ".cat"))

df["final_cat"] = fieldslist 

df.to_csv("source.csv", index=False)
