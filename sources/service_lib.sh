#!/bin/bash


echo "$1"


if [ "$1" = "init" ]
then
  rmmod g_mass_storage
  echo 1 > /proc/sys/vm/dirty_background_ratio
  echo 1 > /proc/sys/vm/dirty_ratio
  modprobe dwc2
  modprobe libcomposite
  insmod /usr/local/bin/usb_f_mass_storage.ko
  mount -o rw /dev/mmcblk0p3 /mnt > /tmp/mountreport.txt 2>&1
  cp /tmp/mountreport.txt /mnt
  cp /usr/local/bin/Manual\ CD-berry.pdf /mnt
  umount /mnt
  sync
  exit
fi

if [ "$1" = "poweroff" ]
then
  sleep 2
  rmmod g_mass_storage
  umount /mnt
  sync
  poweroff
fi

if [ "$1" = "remount_part" ]
then
  umount /mnt
  mount -o ro /dev/mmcblk0p3 /mnt
  exit
fi

if [ "$1" = "cdrom" ]
then
  if [ -f /mnt/cdrom.iso ]
  then
    cdmode=1
    rmmod g_mass_storage
    modprobe g_mass_storage file=/mnt/cdrom.iso removable=y cdrom=y
    exit 0 
  else
    cdmode=0
    rmmod g_mass_storage
    modprobe g_mass_storage file=/dev/mmcblk0p3 removable=y
    exit 1
  fi
fi

if [ "$1" = "mass_storage" ]
then
  cdmode=0
  rmmod g_mass_storage
  modprobe g_mass_storage file=/dev/mmcblk0p3 removable=y
  exit 0
fi

if [ "$1" = "ethernet" ]
then
  modprobe dwc2
  modprobe g_ether
fi

if [ "$1" = "reformat" ]
then
  umount /mnt
  mkntfs -Q -L CD-berry /dev/mmcblk0p3
  sync
fi
