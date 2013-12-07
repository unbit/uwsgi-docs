Fun with Perl, Eyetoy and RaspberryPi
=====================================

Author: Roberto De Ioris

Intro
*****

This article is the result of various experiments aimed at improving uWSGI performance and usability on various area before the 2.0 release.

To follow the article you need:

- a raspberrypi (any model) with a Linux distro installed (i have used the standard raspbian)

- an Eyetoy webcam (the PS3 one)

- a websockets enabled browser (basically any serious browser)

- a bit of perl knowledge (really a bit, the perl code is less than 10 lines ;)

- patience (building uWSGI+psgi+coroae and the rpi requires 13 minutes)

uWSGI subsystems and plugins
****************************

The project makes use of the following uWSGI subsystems:

- :doc:`Websockets`

- :doc:`SharedArea`

- :doc:`Mules`

- :doc:`Symcall`

- :doc:`PSGI`

- :doc:`Async` (optional, we use Coro::Anyevent but you can rely on standard processes, albeit you will need way more memory)

What we want to accomplish
**************************

We want our rpi to gather frames from the eyetoy and stream them to the various connected clients using websockets (and a canvas to show them)

The whole system must use few memory, few cpu cycles and should support a big number of clients (well, even 10 clients will be a success for the raspberrypi hardware ;)

Technical background
********************

The eyetoy capture frames in YUYV format (known as YUV 4:2:2). It means we need 4 bytes for 2 pixels.

By default the resolution is set to 640x480, so each frame will need 614400 bytes

Once we have a frame we need to decode it as RGBA to allows the HTML5 canvas to show it.

The translation between YUYV and RGBA is pretty heavy for the rpi (expecially if you need to do it for every connected client) so we will do it
in the browser using javascript (well there are other approaches we can follow, just check the end of the article for them)

The uWSGI stack is composed by a mule gathering frames from the eyetoy and writing them to a sharedarea.

Workers constantly read from that sharedarea and send frames as websockets binary messages.

Let's start: the uwsgi-capture plugin
*************************************

uWSGI 1.9.21 introduced a simplified (and safe) procedure to build uWSGI plugins. (so expect more third party plugins soon).

The project at: https://github.com/unbit/uwsgi-capture

shows a very simple plugin using the video4linux 2 api to gather frames.

Each frame is written in a sharedarea initialized by the plugin itself.

The first step is getting uWSGI and building it with the 'coroae' profile:

.. code-block:: sh

   sudo apt-get install git build-essential libperl-dev libcoro-perl
   git clone https://github.com/unbit/uwsgi
   cd uwsgi
   make coroae
   
the whole procedure requires 13 minutes, if all goes well you can clone the uwsgi-capture plugin and build it

.. code-block:: sh

   git clone https://github.com/unbit/uwsgi-capture
   ./uwsgi --build-plugin uwsgi-capture
   
you know have the capture_plugin.so file in your uwsgi directory.

Plug your eyetoy to a usb port on your rpi and check if it works:

.. code-block::

   ./uwsgi --plugin capture --v4l-capture /dev/video0
   
(the --v4l-capture option is exposed by the capture plugin)

If all goes well you should see the following lines in uWSGI startup logs:

.. code-block:: sh

   /dev/video0 detected width = 640
   /dev/video0 detected height = 480
   /dev/video0 detected format = YUYV
   sharedarea 0 created at 0xb6935000 (150 pages, area at 0xb6936000)
   /dev/video0 started streaming frames to sharedarea 0
   
(the sharedarea memory pointers could be obviously different)

the uWSGI process will exit soon after them as we did not tell it what to do :)

The uwsgi-capture plugin exposes 2 functions:

captureinit() -> mapped as the init() hook of the plugin, it will be called automatically by uWSGI. If --v4l-capture is specified, this function will initialized the specified device and will map it to a uWSGI sharedarea.

captureloop() -> this is the function gathering frames and writing them to the sharedarea. This function should constantly run (even if there are no clients reading frames)

We want a mule to run the captureloop() function:

.. code-block:: sh

   ./uwsgi --plugin capture --v4l-capture /dev/video0 --mule="captureloop()" --http-socket :9090
   
this time we have bound uWSGI to http port 9090 with a mule mapped to the "captureloop()" function. This nule syntax is
exposed by the symcall plugin that take control of every mule argument ending with "()" (the quoting is required to avoid the shell making mess with parenthesis)

If all goes well you should see your uWSGI server spawning a master, a mule and a worker.

Step 2: the PSGI app
********************

Step 3: HTML5
*************

Concurrency
***********

Alternative approaches
**********************
