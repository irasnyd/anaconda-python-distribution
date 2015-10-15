Anaconda Python Distribution RPM
================================

RPM spec file to install the Continuum Analytics Anaconda Python Distribution
without using the shell script installer. This is intended to make it easier to
install the Anaconda Python Distribution with configuration management tools
such as Puppet.

**This project is not affiliated with Continuum Analytics. Please visit them
at:**

<https://www.continuum.io/anaconda>

Technical Details
-----------------

Due to the lack of DESTDIR support in the Anaconda Python Distribution install
script, this RPM spec file creates a small chroot environment, and then runs the
install script inside the chroot.

The `chroot` system call requires root privileges, and so there is a single
point where you must enter your root password during the build. This is
admittedly a strange practice when building an RPM, but I could not find a way
around it.

This RPM spec file has been tested on CentOS 5/6/7 32/64 bit.

In order to build this package, you must have already installed the
[mkchroot](https://github.com/irasnyd/mkchroot) utility.

Building an RPM
---------------

Download the Anaconda Python Distribution installer from the Continuum
Analytics website. Make sure to download both the 32 and 64 bit versions. Place
the files into your `~/rpm/SOURCES/` directory.

<https://www.continuum.io/downloads#_unix>

Now you are ready to build the RPM itself:

    $ rpmbuild -ba ~/rpm/SPECS/anaconda-python-distribution.spec

Thanks
------

Thanks to the wonderful folks at Continuum Analytics for providing the Anaconda
Python Distribution!
