#!/usr/bin/python3

import pifacedigitalio as p
import pifacedigitalio as o
import time
import subprocess
import sys
import os
import picamera
import signal
import time


# some setting
iso=400
contrast=10

# ports
# 1 
# 2 ready light
# 3 pose light
# 4 processing light
# 5 printing light
# 6 picture light
# 7 
# 8




def ready(type):
 if type == 1:
  o.digital_write(2,1) #turn on
 if type == 0:
  o.digital_write(2,0) #turn off

def pose(type):
 if type == 1: 
  o.digital_write(3,1) #turn on
 if type == 0:  
  o.digital_write(3,0) #turn off

def photolight(type):
 if type == 1: 
  o.digital_write(6,1) #turn on
 if type == 0:  
  o.digital_write(6,0) #turn off

def processing(type):
 if type == 1: 
  o.digital_write(4,1) #turn on
 if type == 0:  
  o.digital_write(4,0) #turn off

def printing(type):
 if type == 1: 
  o.digital_write(5,1) #turn on
 if type == 0:  
  o.digital_write(5,0) #turn off

def test_lights():
 printing(1)
 processing(1)
 photolight(1)
 pose(1)
 ready(1)
 time.sleep(1)
 printing(0)
 time.sleep(1)
 processing(0)
 time.sleep(1)
 photolight(0)
 time.sleep(1)
 pose(0)
 time.sleep(1)
 ready(0) 
 time.sleep(1)

def light(type):
 if type == 1:
  o.digital_write(0,1) #turn on
 if type == 0:  
  o.digital_write(0,0) #turn off
  
def add_job(id):
 print("Adding job "+id+" to workfile")
 f = open('/var/tmp/photobooth-jobfile', 'a')
 f.write(id+"\n")
 f.close()
 
def take_picture(cam, file_name):
 if cam == 0:
  pose(1)
  time.sleep(1)
  pose(0)
  print("will write to"+file_name)
  gpout = subprocess.check_output("gphoto2 --force-overwrite --capture-image-and-download --filename "+file_name, stderr=subprocess.STDOUT, shell=True)
  
 if cam == 1:
  #gpout = subprocess.check_output("raspistill -f -vf -o "+file_name+" -sa -100 -w 500 -h 375", stderr=subprocess.STDOUT, shell=True)
  #with picamera.PiCamera() as camera:
  # camera.start_preview()
  # try:
  #  os.chdir("/var/www/fotos")
  #  for i, filename in enumerate(camera.capture_continuous('image_{counter:02d}.jpg', format=None, use_video_port=False, resize=None, splitter_port=0)):
  #   print(filename)
  #   time.sleep(1)
  #   if i == 3:
  #    break
  # finally:
  #  camera.stop_preview()
  with picamera.PiCamera() as camera:
   camera.resolution = (1024, 768)
   camera.start_preview()
   #camera.awb_mode='off'
   camera.contrast=contrast
   #camera.ISO=iso
   #camera.awb_gains=(1,1.9)
   # Camera warm-up time
   pose(1)
   time.sleep(1)
   print("1")
   camera.capture(file_name)
   pose(0)
   photolight(0)

p.init()
print ("Ready")
test_lights()
ready(1)
while(True):
 try:
  button0 = p.digital_read(0)
  button1 = p.digital_read(1)
  button3 = p.digital_read(3)

  if button3 == 1:
   print ("Button 4 gedrueckt!")  
   print ("shutdown in 7 Sekunden...")
   test_lights()
   subprocess.check_output("/sbin/shutdown -h now", stderr=subprocess.STDOUT, shell=True)
   sys.exit(0)
   time.sleep(1) 
  if ( button0 == 1 ) or ( button1 == 1):
   ready(0)
   if (button0 == 1):
    cam=0 # USB
    cam_name="usb"
    sleep=0.5
   elif (button1 == 1):
    cam=1 # raspi
    cam_name="raspi"
    sleep=2   
   o.digital_write(3,0) #turn off
   
   lt=str(time.time())
   print ("ID: "+lt)
   print ("Bitte recht freundlich!")
   print ("Kamera: ",cam)
   print ("type:",cam_name)  
   photolight(1)
   time.sleep(2)
   photolight(0)
   time.sleep(1)
   photolight(1)
   time.sleep(1)
   photolight(0)
   time.sleep(0.5)
   photolight(1)
   time.sleep(0.5)
   photolight(0)
   file_path = '/var/www/fotos/' #where do you want to save the photos
   file_name = file_path + lt + '_pic_'
 
   light(1)
   take_picture(cam, file_name+"1.jpg")
   time.sleep(sleep) 
   take_picture(cam, file_name+"2.jpg")
   time.sleep(sleep) 
   take_picture(cam, file_name+"3.jpg")
   time.sleep(sleep) 
   take_picture(cam, file_name+"4.jpg")
   light(0)
   processing(1)
   
   # add job to jobqueue
   add_job(lt)
   print ("ready.")
   processing(0)
   ready(1) 
  
 except (KeyboardInterrupt, SystemExit):
  print("Bye")
  test_lights()
  sys.exit()
           