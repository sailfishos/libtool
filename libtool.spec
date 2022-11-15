Name:       libtool
Summary:    The GNU Portable Library Tool
Version:    2.4.7
Release:    1
License:    GPLv2+ and LGPLv2+ and GFDL
URL:        https://github.com/sailfishos/libtool
Source0:    %{name}-%{version}.tar.xz
# This patch is needed for reproducible builds on any host.
Patch0:     no-host-name.patch
Patch1:     libtool-nodocs.patch
Requires:   autoconf >= 2.58
Requires:   automake >= 1.4
Requires:   sed
BuildRequires:  autoconf >= 2.59
BuildRequires:  automake >= 1.9.2

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
Requires:   %{name}-ltdl = %{version}-%{release}

%description ltdl-devel
Static libraries and header files for development with ltdl.

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

%description doc
Man and info pages for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
autoreconf -v

%configure

%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/libltdl.la  %{buildroot}%{_libdir}/libltdl.a

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/libltdl
install -m0644 -t %{buildroot}%{_docdir}/%{name}-%{version} \
        AUTHORS ChangeLog* NEWS README THANKS TODO
install -m0644 libltdl/README \
        %{buildroot}%{_docdir}/%{name}-%{version}/libltdl

%preun doc
if [ "$1" = 0 ]; then
/sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%post doc
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%post ltdl -p /sbin/ldconfig

%postun ltdl -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/%{name}
%{_bindir}/%{name}ize
%{_datadir}/aclocal/*.m4
%exclude %{_datadir}/%{name}/libltdl
%exclude %{_datadir}/%{name}/COPYING.LIB
%exclude %{_datadir}/%{name}/README
%{_datadir}/%{name}

%files ltdl
%defattr(-,root,root,-)
%license libltdl/COPYING.LIB
%{_libdir}/libltdl.so.*

%files ltdl-devel
%defattr(-,root,root,-)
%{_datadir}/%{name}/libltdl
%{_libdir}/libltdl.so
%{_includedir}/ltdl.h
%{_includedir}/libltdl

%files doc
%defattr(-,root,root,-)
%{_infodir}/%{name}.*
%{_mandir}/man1/%{name}*
%{_docdir}/%{name}-%{version}
