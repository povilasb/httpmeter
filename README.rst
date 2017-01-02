=====
About
=====

This is a hackable python based HTTP/HTTPS benchmarking tool.
It supports traffic proxying for both HTTP and HTTPS, thus also can be used to
test performance of proxy servers.

It is implemented with asyncio and runs on Python >= 3.5.

Usage
=====

Get dependencies::

    $ virtualenv --python3 pyenv
    $ pyenv/bin/pip install -r requirements/prod.txt

Run the benchmark::

    $ pyenv/bin/python -m httpmeter -c 100 -n 500 -P username:password \
        -X 1.2.3.4:8080 http://target.com

Other Tools
===========

* https://github.com/httperf/httperf
* https://github.com/wg/wrk
* http://httpd.apache.org/docs/current/programs/ab.html
* https://github.com/borgstrom/httpbenchmark
