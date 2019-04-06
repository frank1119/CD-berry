#!/usr/bin/env python3

import gpiozero
import time
import subprocess 
import os.path

bootconfig_path="/sys/firmware/devicetree/base/bootconfig/bootvalue"
mass_storage_file="/sys/devices/platform/soc/20980000.usb/gadget/lun0/file"
libpath="/usr/local/bin/service_lib.sh"

bootconfig=open(bootconfig_path, 'r')
bootvalue=bootconfig.read()[:-1]
bootconfig.close()

led_shutdown=gpiozero.LED(26)
led_em=gpiozero.LED(19)
button_em=None
button_shutdown=None
do_em=False

cdrom=False
shutdown_confirmed=False
shutdown_starttime=None

button_shutdown_pressed=False;

def on_button_em_held():
  global do_em
  led_em.blink(.2,.2)
  do_em=True
  button_em.when_held=None

def on_button_shutdown_pressed():
  global button_shutdown_pressed
  button_shutdown_pressed=True;

def on_button_shutdown_released():
  global button_shutdown_pressed
  button_shutdown_pressed=False

def handle_emergency():
  global button_em
  global bootvalue

  button_em=gpiozero.Button(5, bounce_time=.2, hold_time=3)
  button_em.when_held=on_button_em_held
  led_em.blink(.5,.5)

  start=time.time();
  while not do_em and time.time() - start < 10:
    time.sleep(.1)

  if do_em:
    result=subprocess.run([libpath, "reformat"])
    print(result);
    led_em.off()
    time.sleep(2)
  button_em.close()

  bootvalue="normal"

def exportedFile():
  if os.path.isfile(mass_storage_file): 
    exportFile=open(mass_storage_file, 'r')
    exportValue=exportFile.read()[:-1]
    exportFile.close()
    return exportValue
  else:
    return "unloaded"

def handle_ethernet():
  global bootvalue
  args=bootvalue.split(";")
  file=open("/etc/network/interfaces", "w")
  seq = [ "source-directory /etc/network/interfaces.d\n", "allow-hotplug usb0\n", "iface usb0 inet static\n", "  address " + args[1], "\n", "  netmask " + args[2], "\n" ]
  file.writelines(seq)
  file.close()
  res=subprocess.run([libpath, "ethernet"])

def handle_normal():
  global cdrom
  global button_shutdown
  global shutdown_starttime
  global shutdown_confirmed
  global button_shutdown_pressed
  cdrom=False

  button_shutdown=gpiozero.Button(5, pull_up=True)
  button_shutdown.when_pressed=on_button_shutdown_pressed
  button_shutdown.when_released=on_button_shutdown_released

  while True:
    if not cdrom:
      if shutdown_confirmed:
        res=subprocess.run([libpath, "poweroff"])
        return

      res=subprocess.run([libpath, "remount_part"])
      res=subprocess.run([libpath, "cdrom"])

      if res.returncode == 0:
        led_shutdown.blink(.95,.05)
        cdrom=True
      else:
        cdrom=False
        led_shutdown.blink(.05,.95)
    else:
      shutdown_confirmed=False
      res=subprocess.run([libpath, "remount_part"])
      res=subprocess.run([libpath, "mass_storage"])
      cdrom=False
      led_shutdown.blink(.05,.95)

    while not exportedFile()=="":
      time.sleep(.25) 
      if button_shutdown_pressed and not shutdown_confirmed and shutdown_starttime==None:
        print("Pressed")
        shutdown_starttime=time.time()
        led_shutdown.blink(.5,.5)

      if not button_shutdown_pressed and not shutdown_confirmed and not shutdown_starttime==None:
        print("released")
        shutdown_starttime=None
        if cdrom:
          led_shutdown.blink(.95,.05)
        else:
          led_shutdown.blink(.05,.95)

      if not cdrom:
        if not shutdown_starttime == None and time.time() - shutdown_starttime > 12:
          print("timeout")
          shutdown_starttime=None
          shutdown_confirmed=False
          led_shutdown.blink(.05,.95)

      if not shutdown_confirmed and not shutdown_starttime == None and time.time() - shutdown_starttime > 3:
        print("confirmed")
        shutdown_confirmed=True
        led_shutdown.blink(.2,.2)
        if cdrom:
          res=subprocess.run([libpath, "poweroff"])

def main():
  if bootvalue=="emergency":
    handle_emergency()

  if bootvalue.startswith("ethernet"):
    handle_ethernet()

  if bootvalue=="normal":
    res=subprocess.run([libpath, "init"])
    handle_normal()


if __name__ == "__main__":
  main()

led_em.close()
led_shutdown.close()

