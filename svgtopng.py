import os, sys, re, glob, time;
import subprocess;
import xml.etree.ElementTree as ET;
from alive_progress import alive_bar; 

os.add_dll_directory(r"C:\Program Files (x86)\GTK2-Runtime\bin")
os.environ['PATH'] = r"C:\Program Files (x86)\GTK2-Runtime\bin"

import cairosvg;

dir_path = os.path.dirname(os.path.realpath(__file__))
__SVGDIR = dir_path + '/svg/';
__SVGOUTPUT = dir_path + '/png/';

def SVGF():
    files = glob.glob(__SVGDIR + "/**/*.svg", recursive=True);

    with alive_bar(len(files)) as bar:
        last_msg_length = 0
        for entry in files:
            if os.path.isfile(entry):
                name = os.path.splitext(os.path.basename(entry))[0];

                tree = ET.parse(entry);
                root = tree.getroot();
                root.set('fill', 'rgb(255, 255, 255)');
                tree.write(entry);

                # image = pyvips.Image.thumbnail(entry, dpi=72)
                # image.write_to_file(__SVGOUTPUT + name + '.png');

                # svg2png(url=entry, write_to=__SVGOUTPUT + )

                bar();

if __name__ == '__main__':
    SVGF()
