
Name: libmodsecurity
Version: 3.0.6
Release: 1%{?dist}
Summary: A library that loads/interprets rules written in the ModSecurity SecRules

License: ASL 2.0
URL: https://www.modsecurity.org/

Source0: https://github.com/SpiderLabs/ModSecurity/releases/download/v%{version}/modsecurity-v%{version}.tar.gz

# Back-port of the pkg-config file expected in the 3.0.3 release
Source1: modsecurity.pc

#Patch0: ModSecurity_cookie_parsing_fix_303.patch

BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: flex
BuildRequires: bison
BuildRequires: git-core
BuildRequires: ssdeep-devel
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(yajl)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(geoip)
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(lmdb)

# libinjection is supposed to be bundled (same as with mod_security 2.x)
# See: https://github.com/client9/libinjection#embedding
Provides: bundled(libinjection) = 3.9.2

%description
Libmodsecurity is one component of the ModSecurity v3 project.
The library codebase serves as an interface to ModSecurity Connectors
taking in web traffic and applying traditional ModSecurity processing.
In general, it provides the capability to load/interpret rules written
in the ModSecurity SecRules format and apply them to HTTP content provided
by your application via Connectors.


%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package static
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description static
The %{name}-static package contains static libraries for developing
applications that use %{name}.



%prep
%autosetup -n modsecurity-v%{version} -S git


%build
%configure --libdir=%{_libdir} --with-lmdb
%make_build


%install
%make_install

# see Source1 above
mkdir -p %{buildroot}%{_libdir}/pkgconfig
sed s:@libdir@:%{_libdir}: <%{S:1} >%{buildroot}%{_libdir}/pkgconfig/modsecurity.pc

%if 0%{?rhel} == 7
%post
/sbin/ldconfig
%postun
/sbin/ldconfig
%endif
%if 0%{?rhel} >= 8
%ldconfig_scriptlets
%endif

%files
%doc README.md AUTHORS
%{_libdir}/*.so.*
%{_bindir}/*
%license LICENSE

%files devel
%doc README.md AUTHORS
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig
%license LICENSE

%files static
%{_libdir}/*.a
%{_libdir}/*.la


%changelog
* Sat Mar 21 2020 Othman Madjoudj <athmane@fedoraproject.org> - 3.0.2-6
- Fix DoS vulnerability (CVE-2019-19886, RHBZ #1801720 / #1801719)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 19 2018 Dridi Boukelmoune <dridi@fedoraproject.org> - 3.0.2-4
- Back-port of modsecurity.pc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Apr 29 2018 Athmane Madjoudj <athmane@fedoraproject.org> - 3.0.2-2
- Rebuild after PR#1

* Sat Apr 14 2018 Athmane Madjoudj <athmane@fedoraproject.org> - 3.0.2-1
- Update to 3.0.2 (rhbz #1563219)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 21 2018 Athmane Madjoudj <athmane@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0 final release
- Drop upstreamed patch
- Add some new BRs

* Sun Oct 22 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 3.0.0-0.2.rc1
- Add a patch to fix the build on non-x86 arch

* Fri Sep 01 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 3.0.0-0.1.rc1
- Fix release tag

* Wed Aug 30 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 3.0.0-0.rc1
- Update to RC1
- Fix some spec issues

* Mon Feb 22 2016 Athmane Madjoudj <athmane@fedoraproject.org> 3.0-0.git
- Initial release

