#
%define nginx_user nginx
%define nginx_group nginx

# distribution specific definitions
%define use_systemd (0%{?rhel} >= 7 || 0%{?fedora} >= 19 || 0%{?suse_version} >= 1315 || 0%{?amzn} >= 2)

%if %{use_systemd}
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%if 0%{?rhel}
%define _group System Environment/Daemons
%endif

%if 0%{?rhel} == 6
Requires(pre): shadow-utils
Requires: initscripts >= 8.36
Requires(post): chkconfig
Requires: openssl >= 1.0.1
BuildRequires: openssl-devel >= 1.0.1
%endif

%if 0%{?rhel} == 7
%define epoch 1
Epoch: %{epoch}
Requires(pre): shadow-utils
Requires: openssl >= 1.0.2
BuildRequires: openssl-devel >= 1.0.2
BuildRequires: libuuid-devel
%define dist .el7
%define debug_package %{nil}
%endif

%if 0%{?rhel} == 8
%define epoch 1
Epoch: %{epoch}
Requires(pre): shadow-utils
BuildRequires: openssl-devel >= 1.1.1
%define _debugsource_template %{nil}
%endif

%if 0%{?suse_version} >= 1315
%define _group Productivity/Networking/Web/Servers
%define nginx_loggroup trusted
Requires(pre): shadow
BuildRequires: libopenssl-devel
%define _debugsource_template %{nil}
%endif

# end of distribution specific definitions

BuildRequires: make curl gcc gcc-c++

%define base_version 1.23.1
%define base_release 1%{?dist}.ngx
%define pagespeed_version 1.13.35.2

%define bdir %{_builddir}/%{name}-%{base_version}

%define WITH_CC_OPT $(echo %{optflags} $(pcre-config --cflags))
%define WITH_LD_OPT -Wl,-z,relro -Wl,-z,now

%define BASE_CONFIGURE_ARGS $(echo "--prefix=%{_sysconfdir}/nginx --sbin-path=%{_sbindir}/nginx --modules-path=%{_libdir}/nginx/modules --conf-path=%{_sysconfdir}/nginx/nginx.conf --error-log-path=%{_localstatedir}/log/nginx/error.log --http-log-path=%{_localstatedir}/log/nginx/access.log --pid-path=%{_localstatedir}/run/nginx.pid --lock-path=%{_localstatedir}/run/nginx.lock --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp --user=%{nginx_user} --group=%{nginx_group} --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module")
%define MODULE_NAME ngx_pagespeed-latest-stable
%define MODULE_CONFIGURE_ARGS $(echo "--add-dynamic-module=%{bdir}/%{MODULE_NAME}")

Summary: nginx pagespeed dynamic module
Name: nginx-module-pagespeed
Version: %{base_version}
Release: %{base_release}
Vendor: Nginx, Inc.
URL: http://nginx.org/
Group: %{_group}

Source0: http://nginx.org/download/nginx-%{base_version}.tar.gz
Source1: nginx.copyright
Patch0: PR1750.diff

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{base_version}-%{base_release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
Requires: nginx == %{?epoch:%{epoch}:}%{base_version}-%{base_release}

%description
ngx_pagespeed-%{pagespeed_version} dynamic module for nginx-%{base_version}-%{base_release}

%if 0%{?suse_version} || 0%{?amzn} 
%debug_package
%endif

%prep
%setup -qcTn %{name}-%{base_version}
tar --strip-components=1 -xzf %{SOURCE0}
mkdir %{bdir}/%{MODULE_NAME}
pagespeed_url=https://github.com/pagespeed/ngx_pagespeed/archive/v%{pagespeed_version}-stable.tar.gz
curl -L ${pagespeed_url} | tar --strip-components=1 -xz -C %{bdir}/%{MODULE_NAME}  # extracts to ngx_pagespeed
cd %{bdir}/%{MODULE_NAME}
[ -e scripts/format_binary_url.sh ] && psol_url=$(scripts/format_binary_url.sh PSOL_BINARY_URL)
curl -L ${psol_url} | tar -xz # extracts to psol/
%patch0 -p1

%build

cd %{bdir}

./configure %{BASE_CONFIGURE_ARGS} %{MODULE_CONFIGURE_ARGS} \
    --with-cc-opt="%{WITH_CC_OPT}" \
    --with-ld-opt="%{WITH_LD_OPT}"
make %{?_smp_mflags} modules

%install
cd %{bdir}
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{base_version}
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{base_version}/COPYRIGHT

%{__mkdir} -p $RPM_BUILD_ROOT%{_libdir}/nginx/modules
for so in `find %{bdir}/objs/ -maxdepth 1 -type f -name "*.so"`; do
%{__install} -m755 $so \
   $RPM_BUILD_ROOT%{_libdir}/nginx/modules/
done

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/nginx/modules/*
%dir %{_datadir}/doc/%{name}-%{base_version}
%{_datadir}/doc/%{name}-%{base_version}/*

%post
if [ $1 -eq 1 ]; then
cat <<BANNER
----------------------------------------------------------------------

The pagespeed dynamic module for nginx has been installed.
To enable this module, add the following to /etc/nginx/nginx.conf
and reload nginx:

    load_module modules/ngx_pagespeed.so;

Please refer to the module documentation for further details:
https://www.modpagespeed.com/doc/build_ngx_pagespeed_from_source

----------------------------------------------------------------------
BANNER
fi

%changelog
* Wed Jul 20 2022 AIKAWA Shigechika
- sync w/ nginx-1.23.1 and pagespeed-1.13.35.2-stable.

* Thu Jun 23 2022 AIKAWA Shigechika
- sync w/ nginx-1.22.0 and pagespeed-1.13.35.2-stable.

* Thu Jan 27 2022 AIKAWA Shigechika
- sync w/ nginx-1.21.6 and pagespeed-1.13.35.2-stable.

* Thu Jan 20 2022 AIKAWA Shigechika
- sync w/ nginx-1.21.5 and pagespeed-1.13.35.2-stable.

* Tue Dec 14 2021 AIAKWA Shigechika
- sync w/ nginx-1.21.4 and pagespeed-1.13.35.2-stable.

* Mon Oct 25 2021 AIAKWA Shigechika
- sync w/ nginx-1.21.3 and pagespeed-1.13.35.2-stable.

* Thu Oct 21 2021 AIAKWA Shigechika
- sync w/ nginx-1.20.1 and pagespeed-1.13.35.2-stable.

* Thu May 13 2021 AIAKWA Shigechika
- sync w/ nginx-1.20.0 and pagespeed-1.13.35.2-stable.

* Fri Nov 20 2020 AIAKWA Shigechika
- sync w/ nginx-1.18.0-2 and pagespeed-1.13.35.2-stable.

* Tue Apr 28 2020 AIAKWA Shigechika
- sync w/ nginx-1.18.0 and pagespeed-1.13.35.2-stable.

* Thu Aug 22 2019 AIAKWA Shigechika
- sync w/ nginx-1.16.1 and pagespeed-1.13.35.2-stable.

* Tue May 07 2019 AIAKWA Shigechika
- sync w/ nginx-1.16.0 and pagespeed-1.13.35.2-stable.

* Wed Dec 05 2018 AIAKWA Shigechika
- sync w/ nginx-1.14.2 and pagespeed-1.13.35.2-stable.

* Wed Nov 07 2018 AIAKWA Shigechika
- sync w/ nginx-1.14.1 and pagespeed-1.13.35.2-stable.

* Mon May 07 2018 AIAKWA Shigechika
- sync w/ nginx-1.14.0 and pagespeed-1.13.35.2-stable.

* Sat Feb 10 2018 AIAKWA Shigechika
- sync w/ nginx-1.12.2 and pagespeed-1.13.35.2-stable.
- automatic download ngx_pagespeed source and psol (binary) library.

* Sun Oct 22 2017 AIAKWA Shigechika
- base on nginx-1.12.2 and pagespeed-1.12.34.3-stable.

* Fri Oct 13 2017 AIAKWA Shigechika
- base on nginx-1.12.1 and pagespeed-1.12.34.2-stable.
- referenced nginx module spec files.
