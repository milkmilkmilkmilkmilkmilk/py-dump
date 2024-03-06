import glob
import os
import sys
import VTFLibEnums

from alive_progress import alive_bar; import time
from pprint import pprint
from hurry.filesize import size
from ctypes import *
from VTFLib import VTFLib

vtf_files = "" # PATH TO VTF FILES FOR COMPRESS D:\dev\\vtf
output_files = "" # OUTPUT PATH FOR COMPRESSED VTF FILES D:\dev\\vtf_output 
clamp_to = 1024

def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

def compressor():
    vtf = VTFLib();
    find = glob.glob(vtf_files + '/**/*.vtf', recursive=True)
    files_total = 0
    old_total = 0.0
    new_total = 0.0
    with alive_bar(len(find)) as bar:
        for entry in find:
            if os.path.isfile(entry):
                file_info = os.stat(entry)
                kilobytes = file_info.st_size/1024 
                old_total += kilobytes

                if kilobytes > 1024:
                    files_total += 1
                    name = os.path.basename(entry).stem
                    file_path = entry[(len(vtf_files) + 1):(-len(name) - 1)]

                    if vtf.image_is_loaded():
                        vtf.ImageDestroy()
                    
                    vtf.image_load(entry, False)

                    print(vtf.image_buffer);

                    width = vtf.width()
                    height = vtf.height()

                    if (width > clamp_to) or (height > clamp_to):

                        newwidth = min(width, clamp_to)
                        newheight = min(height, clamp_to)

                        options = vtf.create_default_params_structure()
                        options.Resize = True
                        options.ResizeMethod = VTFLibEnums.ResizeMethod.ResizeMethodNearestPowerTwo
                        options.ResizeFilter = 2

                        options.ResizeWidth = newwidth
                        options.ResizeHeight = newheight

                        options.ResizeClamp = True
                        options.ResizeClampWidth = newwidth
                        options.ResizeClampHeight = newheight

                        options.ImageFormat = vtf.image_format().value

                        image_data = vtf.convert_to_rgba8888()
                    
                        try:
                            vtf.image_create_single(width, height, image_data, byref(options))
                        except OSError as e:
                            print(e)

                        new_size = vtf.compute_image_size(newwidth, newheight, vtf.depth(), vtf.mipmap_count(), vtf.image_format().value)
                        new_total += new_size/1024 

                        if not os.path.exists(output_files + file_path):
                            os.makedirs(output_files + file_path)
                        vtf.image_save(output_files + file_path + "\\" + name)        
                        print(name + ' has been compressed from ' + str(round(kilobytes/1024, 2)) + 'MB to ' + str(round((new_size/1024) / 1024, 2)) + 'MB')
                    else:
                        new_total += kilobytes
                else:
                    new_total += kilobytes
                bar()

    old_total = round((old_total / 1024), 2)
    new_total = round((new_total / 1024), 2)
    print('Compressed ' + str(files_total) + ' vtf files from ' + str(old_total) + 'MB. to ' + str(new_total) + 'MB.')

if __name__ == "__main__":
    compressor();