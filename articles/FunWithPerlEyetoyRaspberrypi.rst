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

uWSGI subsystems
****************

The project makes use of the following uWSGI subsystems:

- :doc:`Websockets`

- :doc:`SharedArea`

- :doc:`Mules`

- :doc:`Symcall`

- :doc:`Async` (optional, we use Coro::Anyevent but you can rely on standard processes, albeit you will need way more memory)
