#!/bin/bash

DEVNAME=magic

SYSDIR=/sys/kernel/config/usb_gadget/
DEVDIR=$SYSDIR/$DEVNAME

# These are the default values that will be used if you have not provided
# an explicit value in the environment.
USB_IDVENDOR=0x1d6b
USB_IDPRODUCT=0x0104
USB_BCDDEVICE=0x0100
USB_BCDUSB=0x0200
USB_SERIALNUMBER=deadbeef0000
USB_PRODUCT="RPi Zero Magic Gadget"
USB_MANUFACTURER="Ricardo Hacking Ltda."
USB_MAXPOWER=250
USB_CONFIG=conf.1

echo "Creating USB gadget $DEVNAME"

mkdir -p $DEVDIR

echo $USB_IDVENDOR > $DEVDIR/idVendor
echo $USB_IDPRODUCT > $DEVDIR/idProduct
echo $USB_BCDDEVICE > $DEVDIR/bcdDevice
echo $USB_BCDUSB > $DEVDIR/bcdUSB

mkdir -p $DEVDIR/strings/0x409
echo "$USB_SERIALNUMBER" > $DEVDIR/strings/0x409/serialnumber
echo "$USB_MANUFACTURER"        > $DEVDIR/strings/0x409/manufacturer
echo "$USB_PRODUCT"   > $DEVDIR/strings/0x409/product

mkdir -p $DEVDIR/configs/$USB_CONFIG
echo $USB_MAXPOWER > $DEVDIR/configs/$USB_CONFIG/MaxPower

echo "Adding serial port"
mkdir -p $DEVDIR/functions/acm.usb0
ln -s $DEVDIR/functions/acm.usb0 $DEVDIR/configs/$USB_CONFIG

echo "Adding keyboard"
mkdir -p $DEVDIR/functions/hid.usb0
echo 1 > $DEVDIR/functions/hid.usb0/protocol
echo 1 > $DEVDIR/functions/hid.usb0/subclass
echo 8 > $DEVDIR/functions/hid.usb0/report_length
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 \
  > $DEVDIR/functions/hid.usb0/report_desc
ln -s $DEVDIR/functions/hid.usb0 $DEVDIR/configs/$USB_CONFIG

echo "Adding mouse"
mkdir -p $DEVDIR/functions/hid.usb1
echo 1 > $DEVDIR/functions/hid.usb1/protocol
echo 1 > $DEVDIR/functions/hid.usb1/subclass
echo 5 > $DEVDIR/functions/hid.usb1/report_length
echo -ne \\x05\\x01\\x09\\x02\\xA1\\x01\\x09\\x01\\xA1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x16\\x01\\x80\\x26\\xFF\\x7F\\x75\\x10\\x95\\x02\\x81\\x02\\xC0\\xC0 \
  > $DEVDIR/functions/hid.usb1/report_desc
ln -s $DEVDIR/functions/hid.usb1 $DEVDIR/configs/$USB_CONFIG

udevadm settle -t 5 || :
ls /sys/class/udc/ > $DEVDIR/UDC

