from osgeo import gdal
    
options_list = [
    '-ot Byte',
    '-of GTiff',
    '-b 1',
    '-scale'
]           


"""
options_list = [
    '-ot Byte',
    '-of JPEG',
    '-b 1',
    '-scale'
]           
"""
options_string = " ".join(options_list)

#GEOTIFF to JPG
gdal.Translate(
    '/mnt/hdd/mtgdata/output/MTG_true_color_r_20200405_120000_SINGLE_BAND.geotiff', #out
    '/mnt/hdd/mtgdata/output/MTG_true_color_r_20200405_120000.geotiff', #in
    options=options_string
)
