Using OpenBSD httpd as proxy
============================

Starting from version 5.7 OpenBSD includes a minimal (truly minimal) web server with FastCGI support

The first step to enable it is writing its configuration file ```/etc/httpd.conf```

.. code-block:: c

   server "default" {
       listen on 0.0.0.0 port 80
   
       fastcgi socket ":3031"
   }


this minimal configuration will spawn a chrooted webserver on port 80, running as user 'www' and forwarding every request
to the address 127.0.0.1:3031 using the FastCGI protocol.


Now you only need to spawn uWSGI on such address:

```ini
[uwsgi]
fastcgi-socket = 127.0.0.1:3031
; a simple python app
wsgi-file = app.py
```

you can obviously use uWSGI as a full-featured (well effectively it has way more features than every cgi server out there :P) CGI server,
just remember to force the modifier1 to the '9' one:

```ini
[uwsgi]
fastcgi-socket = 127.0.0.1:3031
fastcgi-modifier1 = 9
; a simple cgi-bin directory
cgi = /var/www/cgi-bin
```

now you can place your cgi scripts in /var/www/cgi-bin (remember to give them the executable permission)
