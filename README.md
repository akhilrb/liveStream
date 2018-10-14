# statusCheck
---

A minimalist web-enquiry service made for [my love for Sleep](https://akhilrb.github.io)

## Requirements

### Hardware

The script requires a camera device to either feed the live stream or request availabilty.  
No image(s) are streamed while processing a request for availability.  
Watching the stream, however, requires authentication and blocks all availabilty requests.  
My setup builds up on a Raspberry Pi with a USB Camera connected to it, which will hopefully be upgraded to a less bulky and less power hungry PiCam.  

### Software

* openCV (>3.3 because the DNN module is required and status determination)
* Flask (for all the effortless streaming)
* CaffeModel files (included in the repo, originally found [here](https://github.com/chuanqi305/MobileNet-SSD))

---

Originally forked from [Miguel Grinberg's wonderful tutorial on streaming images through Flask](http://blog.miguelgrinberg.com/post/video-streaming-with-flask)
