
Summary: The GNU Portable Library Tool
Name:    libtool
Version: 2.4
Release: 1
License: GPLv2+ and LGPLv2+ and GFDL
Group:   Development/Tools
Source:  http://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.gz
Patch0: no-host-name.patch
URL:     http://www.gnu.org/software/libtool/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info

BuildRequires: autoconf >= 2.59, automake >= 1.9.2, texinfo
Requires: autoconf >= 2.58, automake >= 1.4, sed
# make sure we can configure all supported langs
#BuildRequires: gcc, gcc-c++, libstdc++-devel, gcc-gfortran, gcc-java
# /usr/bin/libtool includes paths within gcc's versioned directories
# Libtool must be rebuilt whenever a new upstream gcc is built

%description
GNU Libtool is a set of shell scripts which automatically configure UNIX and
UNIX-like systems to generically build shared libraries. Libtool provides a
consistent, portable interface which simplifies the process of using shared
libraries.

If you are developing programs which will use shared libraries, but do not use
the rest of the GNU Autotools (such as GNU Autoconf and GNU Automake), you
should install the libtool package.

The libtool package also includes all files needed to integrate the GNU 
Portable Library Tool (libtool) and the GNU Libtool Dynamic Module Loader
(ltdl) into a package built using the GNU Autotools (including GNU Autoconf
and GNU Automake).

%package ltdl
Summary:  Runtime libraries for GNU Libtool Dynamic Module Loader
Group:    System/Libraries
Provides: %{name}-libs = %{version}-%{release}
License:  LGPLv2+
Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%description ltdl
The libtool-ltdl package contains the GNU Libtool Dynamic Module Loader, a
library that provides a consistent, portable interface which simplifies the
process of using dynamic modules.

These runtime libraries are needed by programs that link directly to the
system-installed ltdl libraries; they are not needed by software built using 
the rest of the GNU Autotools (including GNU Autoconf and GNU Automake).



%package ltdl-devel
Summary: Tools needed for development using the GNU Libtool Dynamic Module Loader
Group:    Development/Libraries
Requires: %{name}-ltdl = %{version}-%{release}
License:  LGPLv2+

%description ltdl-devel
Static libraries and header files for development with ltdl.



%prep
%setup -n libtool-%{version} -q
%patch0 -p1

%build

./bootstrap

export CC=gcc
export CXX=g++
export F77=gfortran
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
# don't conflict with libtool-1.5, use own directory:
sed -e 's/pkgdatadir="\\${datadir}\/\$PACKAGE"/pkgdatadir="\\${datadir}\/\${PACKAGE}"/' configure > configure.tmp; mv -f configure.tmp configure; chmod a+x configure
./configure --prefix=%{_prefix} --exec-prefix=%{_prefix} --bindir=%{_bindir} --sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} --includedir=%{_includedir} --libdir=%{_libdir} --libexecdir=%{_libexecdir} --localstatedir=%{_localstatedir} --mandir=%{_mandir} --infodir=%{_infodir}
# build not smp safe:
make #%{?_smp_mflags}

%check
#make check VERBOSE=yes > make_check.log 2>&1 || (cat make_check.log && false)


%install
rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/libltdl.la  %{buildroot}%{_libdir}/libltdl.a


%clean
rm -rf %{buildroot}



%post
/sbin/install-info %{_infodir}/libtool.info.gz %{_infodir}/dir || :

%post ltdl -p /sbin/ldconfig



%preun
if [ "$1" = 0 ]; then
   /sbin/install-info --delete %{_infodir}/libtool.info.gz %{_infodir}/dir || :
fi

%postun ltdl -p /sbin/ldconfig



%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README THANKS TODO ChangeLog*
%{_infodir}/libtool.info*.gz
%{_mandir}/man1/libtool*.gz
%{_bindir}/libtool
%{_bindir}/libtoolize
%{_datadir}/aclocal/*.m4
%exclude %{_datadir}/libtool/libltdl
%{_datadir}/libtool

%files ltdl
%defattr(-,root,root)
%doc libltdl/COPYING.LIB libltdl/README
%{_libdir}/libltdl.so.*

%files ltdl-devel
%defattr(-,root,root)
%{_datadir}/libtool/libltdl
%{_libdir}/libltdl.so
%{_includedir}/ltdl.h
%{_includedir}/libltdl



