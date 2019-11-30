# Bug's Fake Mouse

This is the code for the proof of concept presented at DEFCON Porto Alegre 2019. The presentation is also attached here for reference, altough it's in Portuguese.

## Disclaimer

I do not endorse cheating and this is only a PoC. I do not recommend you to use this on a live/production environment (even though that's exactly what I did).

## Raspberry Pi code

`raspberrypi/` contains all the Raspberry Pi Zero W code. The scripts allow you to enable/disable the USB gadget mode, while the Python script allows you to receive USB-encapsulated data on an UDP port and transfer it to a device. The script must run as root and point to the device.

Setup example:

```
./add-gadget.sh
python3 hid-usb.py /dev/hidg1
```

From this moment, it should be listening on port 60123 over the network.

It must be noted that **this PoC uses an absolute-based mouse position report descriptor**. This essentially means that the position sent through the USB is absolute to the screen instead of the normal acceleration-based movement information. This allows for an easier prototyping, but could be more easily detected as well, as the operating system knows this. Keep that in mind.

This is the USB descriptor it uses:

```
0x05, 0x01,        // Usage Page (Generic Desktop Ctrls)
0x09, 0x02,        // Usage (Mouse)
0xA1, 0x01,        // Collection (Application)
0x09, 0x01,        //   Usage (Pointer)
0xA1, 0x00,        //   Collection (Physical)
0x05, 0x09,        //     Usage Page (Button)
0x19, 0x01,        //     Usage Minimum (0x01)
0x29, 0x03,        //     Usage Maximum (0x03)
0x15, 0x00,        //     Logical Minimum (0)
0x25, 0x01,        //     Logical Maximum (1)
0x95, 0x03,        //     Report Count (3)
0x75, 0x01,        //     Report Size (1)
0x81, 0x02,        //     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0x95, 0x01,        //     Report Count (1)
0x75, 0x05,        //     Report Size (5)
0x81, 0x03,        //     Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0x05, 0x01,        //     Usage Page (Generic Desktop Ctrls)
0x09, 0x30,        //     Usage (X)
0x09, 0x31,        //     Usage (Y)
0x16, 0x01, 0x80,  //     Logical Minimum (-32767)
0x26, 0xFF, 0x7F,  //     Logical Maximum (32767)
0x75, 0x10,        //     Report Size (16)
0x95, 0x02,        //     Report Count (2)
0x81, 0x02,        //     Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
0xC0,              //   End Collection
0xC0,              // End Collection

// 52 bytes
```

For comparison, the XY input for an acceleration-based mouse would be this:

```
0x81, 0x06,        //     	Input (Data,Var,Rel,No Wrap,Linear,Preferred State,No Null Position) == 16 bits
```

All information regarding the USB HID report descriptors can be found on the official documentation and some tutorials:

* [Official USB HID Usage tables documentation v1.12](https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf)
* [Tutorial about USB HID report descriptors](https://eleccelerator.com/tutorial-about-usb-hid-report-descriptors/)
* [USB Descriptor and Request Parser](https://eleccelerator.com/usbdescreqparser/)

Some setup documentation if you need help setting up the Raspberry Pi Zero into USB gadget mode can be found on these pages:

* [Composite USB gadgets on the Raspberry Pi Zero](http://www.isticktoit.net/?p=1383)
* [Turn Your Raspberry Pi Zero into a USB Keyboard (HID)](https://randomnerdtutorials.com/raspberry-pi-zero-usb-keyboard-hid/)

## PoC code

This code targets a Ragnarok Online game instance by default, although it can be easily changed into something else. Nevertheless, you'll need to provide your own images, as I prefer to not get a copyright strike on this ;)

To run it:

```
python3 poc.py
```

It will load images available in the folders specified in the source code into memory and start taking screenshots from 0,0 to 1024,768, as this was my test setup. Then it will look for the mobs and, once found, send the mouse position to the RPi network address. It will simulate an user moving the mouse instead of jumping to the position. That's it.
