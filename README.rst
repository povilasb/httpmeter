=====
About
=====

.. image:: https://travis-ci.org/povilasb/httpmeter.svg?branch=master
    :target: https://travis-ci.org/povilasb/httpmeter

This is a hackable python based HTTP/HTTPS benchmarking tool.
It supports traffic proxying for both HTTP and HTTPS, thus also can be used to
test performance of proxy servers.

It is implemented with asyncio and runs on Python >= 3.5.
You can optionally use `uvloop <https://github.com/MagicStack/uvloop>`_ for
better performance.

Usage
=====

::

    pip3 install httpmeter

Synopsis::

    httpmeter [options] URL

Options::

    -h  Display usage information.

    -c, --concurrency <N>
        How many requests should be executed in parallel.

    -n, requests <N>
        How many requests to make in total.

    -H, --header <custom-header>
        Additional headers to send with every request. Multiple entries
        allowed. E.g.
            --header "Connection: close" --header "User-Agent: benchmark"

    -X, --proxy <http://user:pass@proxy:port>
        Proxy address. E.g. http://user1:pass123@localhost:8080

    --uvloop
        Use uvloop to increase networking performance.

Other Tools
===========

* https://github.com/httperf/httperf
* https://github.com/wg/wrk
* http://httpd.apache.org/docs/current/programs/ab.html
* https://github.com/borgstrom/httpbenchmark

Development
===========

Get dependencies::

    $ virtualenv --python3 pyenv
    $ pyenv/bin/pip install -r requirements/prod.txt

Run the benchmark::

    $ pyenv/bin/python -m httpmeter -c 100 -n 500 -P username:password \
        -X http://1.2.3.4:8080 http://target.com
