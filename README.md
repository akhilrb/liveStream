# liveStream
---

An RBAC live streaming service made for [my love for Sleep](https://akhilrb.github.io)

## Requirements

### Hardware

The script requires a camera device to either feed the live stream or request availabilty.  
My setup builds up on a Raspberry Pi with a USB Camera connected to it, which will hopefully be upgraded to a less bulky and less power hungry PiCam.  

### Software

* openCV (>3.3 because the DNN module is required)
* Flask (for all the effortless streaming)
* CaffeModel files (included in the repo, originally found [here](https://github.com/chuanqi305/MobileNet-SSD))

---

Originally forked from [Miguel Grinberg's wonderful tutorial on streaming images through Flask](http://blog.miguelgrinberg.com/post/video-streaming-with-flask)
