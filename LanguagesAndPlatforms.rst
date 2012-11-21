Supported languages and platforms
=================================

.. list-table:: 
    :header-rows: 1
    
    * - Technology
      - Available since
      - Notes
      - Status
    * - Python
      - 0.9.1
      - The first available plugin, supports WSGI (PEP333, PEP3333), Web3 (from version 0.9.7-dev) and Pump (from 0.9.8.4). Works with :doc:`Virtualenv`, multiple Python interpreters, :doc:`Python3` and has unique features like :doc:`PythonModuleAlias`, :doc:`DynamicVirtualenv` and :doc:`uGreen`. A module exporting handy :doc:`Decorators` for the uWSGI API is available in the source distribution. PyPy is supported since 1.3. The :doc:`Tracebacker` was added in 1.3.
      - Stable, 100% uWSGI API support
    * - Lua
      - 0.9.5
      - Supports :doc:`LuaWSAPI`, coroutines and threads
      - Stable, 60% uWSGI API support
    * - Perl
      - 0.9.5
      - :doc:`Perl` (PSGI) support. Multiple interpreters, threading and async modes supported
      - Stable, 60% uWSGI API support
    * - Ruby
      - 0.9.7-dev
      - :doc:`Rack` and :doc:`RubyOnRails` support. A loop engine for :doc:`Ruby 1.9 fibers<FiberLoop>` is available as well as a handy :doc:`DSL <RubyDSL>` module.
      - Stable, 80% uWSGI API support
    * - :doc:`Erlang`
      - 0.9.5
      - Allows message exchanging between uWSGI and Erlang nodes.
      - Stable, no uWSGI API support
    * - :doc:`CGI`
      - 1.0-dev
      - Run CGI scripts
      - Stable, no uWSGI API support
    * - :doc:`PHP`
      - 1.0-dev
      - Run PHP scripts
      - Stable from 1.1, 5% uWSGI API support   
    * - :doc:`JVM`
      - 0.9.7-dev
      - Allows integration between uWSGI and the Java Virtual Machine. An :doc:`example WSGI-like handler<JWSGI>` is available.
      - Alpha
    * - mono
      - 0.9.7-dev
      - Still at early stage of development. Allows integration between uWSGI and Mono.
      - Unusable
