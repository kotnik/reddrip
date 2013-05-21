Reddit Ripper
=============

So, you are busy with the stuff, but don't want to miss a picture in
gonewild^Wmotivationalpics? Then, this is the project for you.

Installation
------------

You will need to have Redis instance ready. Then, the fastest way is to pip it:

    pip install reddrip

Pip will download and install the dependencies for you.

Running
-------

What you need is a configuration file. Take a look at ``example.cfg`` one to get
the idea.

After that, run it:

    reddrip run -c /path/to/configuration.cfg

Also, you may use ``-v`` to get more verbosity.

At any moment, you may query Redis database to get some stats:

    reddrip stat -c /path/to/configuration.cfg

History
-------

This code was born one evening after playing with ``praw``.

License
-------

This is GPLv3 or later code. See the LICENSE file if you must.
