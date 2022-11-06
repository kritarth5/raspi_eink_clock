# Raspberry Pi E-Ink Clock for Daylight Savings (EST/IST/UK/PST)

### References:
This project is essentially a tiny fork of the [rpi-eink-clock](https://github.com/emanueleg/rpi-eink-clock) by [Emanuele](https://github.com/emanueleg). Instead of showing a bunch of different information though, this shows 4 different time zones that can be switch among each other using buttons on the waveshare e-ink display

### Why: 
Daylight Savings Sucks. But Distributed teams are great. However this means constantly having to think what time it is for someone else when scheduling calls. Here's an overengineered solution: have all the time zones on a physical clock next to you that you can switch between without leaving your terminal. Sure you could go to google and type 10 am EST to IST, or... press button two on your Raspberry Pi and have it displayed right there. 

1. IST
![WhatsApp Image 2022-11-06 at 05 09 34](https://user-images.githubusercontent.com/20535340/200147177-35026652-b415-41c9-8f0f-0e54dd629fe7.jpeg)

2. EST 
![WhatsApp Image 2022-11-06 at 05 09 34 (1)](https://user-images.githubusercontent.com/20535340/200147186-e9fc0ad7-a4e2-401b-97f4-45c09d55fb2c.jpeg)

3. UK
![WhatsApp Image 2022-11-06 at 05 09 34 (2)](https://user-images.githubusercontent.com/20535340/200147188-96cd6b90-aad9-4f27-b158-10c3f16300a9.jpeg)

4. PST
![WhatsApp Image 2022-11-06 at 05 09 33](https://user-images.githubusercontent.com/20535340/200147192-aedd1582-6d6e-4948-979b-0f4096b9f496.jpeg)


### Hardware Required: 
- RaspberryPi 4
- Waveshare e-ink display 2.7 inch (color or black and white)

### Code:

1. main.py: The meat of the code which does the following:
  - This uses datetime to get timezone information across regions
  - Then uses pillow to write these out into images with the above datetime info on them in monochrome black
  - Then uses the epd2in7.py library (from wave share) to write it out to the e-ink display.
  - And GPIO to infer inputs from the button presses
  - all of this functionality is wrapped within a class. 
  
2. epd2in7.py: Essentially the drivers for the waveshare eink display. 

3. The main.py is then run through a cronjob at startup using these instructions [here](https://www.makeuseof.com/how-to-run-a-raspberry-pi-program-script-at-startup/)

### Instructions to get this on your Rasperry Pi

1. Flash your microsd with a raspberry pi OS
2. Get the IP address and then ssh into it
3. git clone this repository onto it
4. python /home/pi/wherever you git cloned/main.py
5. Wrap 4. in a crobjob and the clock will run everytime you run the raspberry on. 

### License

1. Official Waveshare Electronic paper driver/libraries (epdconfig.py and epdconfig.py) are available under the MIT License.
2. The official Raspberry Pi Logo used in raspberry.bmp is a (TM) of Raspberry Pi Foundation (https://www.raspberrypi.org/) and available under the Raspberry Pi Trademark rules and brand guidelines
3. All respective copyrights on earlier versions of this code is reserved with their [originators](https://github.com/emanueleg) adding onto code that has come before.
4. All rights reserved under GNU something something. Copy Left mumble mumble. (Feel free to use this code liberally.)

