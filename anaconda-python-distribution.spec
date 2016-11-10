# disable automatic requires and provides
%define _use_internal_dependency_generator 0

%define __find_requires %{nil}
%global __requires_exclude_from ^.*$

%define __find_provides %{nil}
%global __provides_exclude_from ^.*$

# disable building debug package
%global _enable_debug_packages 0
%global __debug_install_post %{nil}
%global debug_package %{nil}

# don't want to postprocess the stuff from upstream: it already has the
# bytecompiled Python, etc.
%define __os_install_post %{nil}

Name: anaconda-python-distribution
Version: 4.2.0
Release: 1%{?dist}
Summary: Anaconda Python Distribution
Group: System Environment/Base
License: http://docs.continuum.io/anaconda/eula
URL: https://www.continuum.io/anaconda
Source0: Anaconda2-%{version}-Linux-x86.sh
Source1: Anaconda2-%{version}-Linux-x86_64.sh
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# https://github.com/irasnyd/mkchroot
BuildRequires: mkchroot

# utilities required as part of the chroot
BuildRequires: bash
BuildRequires: bzip2
BuildRequires: coreutils
BuildRequires: file
BuildRequires: gawk
BuildRequires: grep
BuildRequires: tar
BuildRequires: util-linux
BuildRequires: which

%ifarch %{ix86}
%define anaconda_src %{SOURCE0}
%define anaconda_srcname Anaconda-%{version}-Linux-x86.sh
%else
%define anaconda_src %{SOURCE1}
%define anaconda_srcname Anaconda-%{version}-Linux-x86_64.sh
%endif

%description
Enterprise-ready Python distribution containing 330+ packages for large-scale
data processing, predictive analytics, and scientific computing.

%prep
# build an empty directory for our install
%setup -T -c -n %{name}-%{version}

# copy Anaconda install script
%{__install} -m 0644 %{anaconda_src} %{anaconda_srcname}

# build the chroot environment into the current directory
mkchroot \
    "$PWD" \
    awk basename bash bzip2 cat chown cp dirname echo file grep ln ls md5sum \
    mkdir mknod mount mv rm script seq tail tar umount uname wc tr

# build the chroot run script
cat > build.sh << EOF
#!/bin/bash -x

cleanup() {
        echo 'cleanup: umount /proc'
        umount /proc
        echo 'cleanup: rm /dev/null'
        rm -f /dev/null
        echo 'cleanup: chown to RPM build user'
        chown -R `id -u`:`id -g` /
}

trap cleanup SIGINT SIGKILL ERR EXIT

mkdir /dev
mknod -m 0666 /dev/null c 1 3

mkdir /proc
mount -n -t proc none /proc

mkdir /etc
ln -s /proc/self/mounts /etc/mtab

rm -rf /opt/anaconda
/bin/bash %{anaconda_srcname} -b -p /opt/anaconda

echo 'finished!'
exit 0
EOF

%build
echo 'Entering chroot and installing Anaconda Python Distribution'
echo
echo 'Please enter your root password now, so that we can run the "chroot" command'
su -l -c "chroot $PWD /bin/bash -x /build.sh"

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}/opt
%{__mv} "$PWD"/opt/anaconda %{buildroot}/opt/
%{__rm} -rf "$PWD"/*

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/anaconda

%changelog
* Thu Oct 15 2015 Ira W. Snyder <isnyder@lcogt.net> - 2.3.0-1
- Initial build. Tested on CentOS 5/6/7 32/64 bit.
- Using chroot environment to work around lack of DESTDIR support.
