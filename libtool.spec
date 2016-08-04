Name:       libtool
Summary:    The GNU Portable Library Tool
Version:    2.4.6
Release:    1
Group:      Development/Tools
License:    GPLv2+ and LGPLv2+ and GFDL
URL:        http://www.gnu.org/software/libtool/
Source0:    http://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.xz
# This patch is needed for reproducible builds on any host.
Patch0:     no-host-name.patch
Requires:   autoconf >= 2.58
Requires:   automake >= 1.4
Requires:   sed
Requires(preun): /sbin/install-info
Requires(post): /sbin/install-info
BuildRequires:  autoconf >= 2.59
BuildRequires:  automake >= 1.9.2
BuildRequires:  help2man
BuildRequires:  texinfo

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
Summary:    Runtime libraries for GNU Libtool Dynamic Module Loader
License:    LGPLv2+
Group:      System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides:   %{name}-libs = %{version}-%{release}

%description ltdl
The libtool-ltdl package contains the GNU Libtool Dynamic Module Loader, a
library that provides a consistent, portable interface which simplifies the
process of using dynamic modules.

These runtime libraries are needed by programs that link directly to the
system-installed ltdl libraries; they are not needed by software built using
the rest of the GNU Autotools (including GNU Autoconf and GNU Automake).

%package ltdl-devel
Summary:    Tools needed for development using the GNU Libtool Dynamic Module Loader
License:    LGPLv2+
Group:      Development/Libraries
Requires:   %{name}-ltdl = %{version}-%{release}

%description ltdl-devel
Static libraries and header files for development with ltdl.

%prep
%setup -q -n %{name}-%{version}

# no-host-name.patch
%patch0 -p2

%build
export CC=gcc
export CXX=g++
export F77=gfortran
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
# don't conflict with libtool-1.5, use own directory:
sed -e 's/pkgdatadir="\\${datadir}\/\$PACKAGE"/pkgdatadir="\\${datadir}\/\${PACKAGE}"/' configure > configure.tmp; mv -f configure.tmp configure; chmod a+x configure
./configure --prefix=%{_prefix} --exec-prefix=%{_prefix} --bindir=%{_bindir} --sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} --datadir=%{_datadir} --includedir=%{_includedir} --libdir=%{_libdir} --libexecdir=%{_libexecdir} --localstatedir=%{_localstatedir} --mandir=%{_mandir} --infodir=%{_infodir}
# build not smp safe:
make #%{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=$RPM_BUILD_ROOT
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/libltdl.la  %{buildroot}%{_libdir}/libltdl.a

%check
#make check VERBOSE=yes > make_check.log 2>&1 || (cat make_check.log && false)

%preun
if [ "$1" = 0 ]; then
/sbin/install-info --delete %{_infodir}/libtool.info.gz %{_infodir}/dir || :
fi

%post
/sbin/install-info %{_infodir}/libtool.info.gz %{_infodir}/dir || :

%post ltdl -p /sbin/ldconfig

%postun ltdl -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README THANKS TODO ChangeLog*
%{_infodir}/libtool.info*.gz
%{_mandir}/man1/libtool*.gz
%{_bindir}/libtool
%{_bindir}/libtoolize
%{_datadir}/aclocal/*.m4
%exclude %{_datadir}/libtool/libltdl
%{_datadir}/libtool

%files ltdl
%defattr(-,root,root,-)
%doc libltdl/COPYING.LIB libltdl/README
%{_libdir}/libltdl.so.*

%files ltdl-devel
%defattr(-,root,root,-)
%{_datadir}/libtool/libltdl
%{_libdir}/libltdl.so
%{_includedir}/ltdl.h
%{_includedir}/libltdl
