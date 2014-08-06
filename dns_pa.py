'''
Created on Feb 22, 2013

@author: leal

Generate an IDF file for the old (PA) DNS detector bank 

Run as:

python dns_pa.py | tidy -utf8 -xml -w 255 -i -c -q -asxml > DNS_Definition.xml

'''
import numpy as np
from collections import Counter
from time import gmtime, strftime

# # Global variables
instrumentName='DNS'
numberOfPixelsPerTube=1
firstDetectorId = 1
radius = 0.8 # meters

# Tubes DNS: 0.15m / 1 positions 
tubeHeight = 0.15
tubePixelStep =  tubeHeight
totalTubeHeight = tubePixelStep * numberOfPixelsPerTube

# Don't touch!
azimuthalAngle = [i*5.0 for i in range(24)]

azimuthalAngle.reverse()
numberOfTubes=len(azimuthalAngle)     
numberOfDetectors = numberOfPixelsPerTube * numberOfTubes

    
def printHeader():
    print """<?xml version="1.0" encoding="UTF-8"?>
    <!-- For help on the notation used to specify an Instrument Definition File see http://www.mantidproject.org/IDF -->
    <instrument name="%s" valid-from="1900-01-31 23:59:59"
    valid-to="2100-01-31 23:59:59" last-modified="%s">""" % (instrumentName,strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print """<!-- Author: m.ganeva@fz-juelich.de -->"""
    print """<defaults>
      <length unit="meter" />
      <angle unit="degree" />
      <reference-frame>
        <!-- The z-axis is set parallel to and in the direction of the beam. the 
             y-axis points up and the coordinate system is right handed. -->
        <along-beam axis="z" />
        <pointing-up axis="y" />
        <handedness val="right" />
      </reference-frame>
    </defaults>

    <component type="moderator">
      <location z="-2" />
    </component>
    <type name="moderator" is="Source"></type>

    <!-- Sample position -->
    <component type="sample-position">
      <location y="0.0" x="0.0" z="0.0" />
    </component>
    <type name="sample-position" is="SamplePos" />"""

def printDetectors():
    print """<idlist idname="detectors">
        <id start="%d" end="%d" />
    </idlist>""" % (firstDetectorId, numberOfDetectors)
    
    print """<!-- Detector list def -->
    <component type="detectors" idlist="detectors">
        <location />
    </component>"""
    
    print "<!-- Detector Banks -->"
    print """<type name="detectors">"""
    print """  <component type="bank_uniq"><location/></component>"""
    print "</type>"
    
    print "<!-- Definition of the unique existent bank (made of tubes) -->"
    
    print """<type name="bank_uniq">"""
    print """  <component type="standard_tube">"""
    for idx,angle in enumerate(azimuthalAngle):
        print """<location r="%f" t="%f" name="tube_%d" />"""%(radius,angle,idx+1)
    print """  </component>"""
    print """</type>"""
    
    print """<!-- Definition of standard_tube -->"""
    print """<type name="standard_tube" outline="yes">
        <component type="standard_pixel">"""
    pixelPositions = np.linspace(-totalTubeHeight/2,totalTubeHeight/2,numberOfPixelsPerTube)
    for  pos in pixelPositions :
        print """<location y="%f" />"""%(pos)
    print """</component> </type>"""
    

 

def printPixels():  
#    print """ <type name="pack" is="detector">  
#    <cuboid id="pack-pixel-shape">
#      <left-front-bottom-point x="0.0" y="-0.020" z="-0.0015"  />
#      <left-front-top-point  x="0.0" y="0.020" z="-0.0015"  />
#      <left-back-bottom-point  x="0.005" y="-0.020" z="-0.0015"  />
#      <right-front-bottom-point  x="0.0" y="-0.020" z="0.0015"  />
#    </cuboid>
#    <algebra val="pack-pixel-shape" />     
#    </type>"""
    print """<type name="standard_pixel" is="detector">
        <cylinder id="shape">
            <centre-of-bottom-base x="0.0" y="-0.006144" z="0.0" />
            <axis x="0.0" y="1.0" z="0.0" />
            <radius val="0.0127" />
            <height val=".15" />
        </cylinder>
        <algebra val="shape" />
    </type>"""
        

def printEnd():
    print "</instrument>"

    

if __name__ == '__main__':
    printHeader();
    printDetectors();
    printPixels();
    printEnd();
    
    
     
