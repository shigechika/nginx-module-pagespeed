#
%define nginx_user nginx
%define nginx_group nginx

BuildRequires: curl

%if 0%{?rhel} || 0%{?amzn}
%define _group System Environment/Daemons
BuildRequires: openssl-devel
%endif

%if 0%{?suse_version} == 1315
%define _group Productivity/Networking/Web/Servers
BuildRequires: libopenssl-devel
%endif

%if 0%{?rhel} == 7
BuildRequires: redhat-lsb-core
BuildRequires: curl
BuildRequires: libuuid-devel
%define epoch 1
Epoch: %{epoch}
%define os_minor %(lsb_release -rs | cut -d '.' -f 2)
%if %{os_minor} >= 4
%define dist .el7_4
%else
%define dist .el7
%endif
%endif

%define main_version 1.12.2
%define main_release 1%{?dist}.ngx
%define pagespeed_version 1.13.35.2

%define bdir %{_builddir}/%{name}-%{main_version}

Summary: nginx pagespeed dynamic module
Name: nginx-module-pagespeed
Version: 1.12.2
Release: 2%{?dist}.ngx
Vendor: Nginx, Inc.
URL: http://nginx.org/
Group: %{_group}

Source0: http://nginx.org/download/nginx-%{main_version}.tar.gz
Source1: COPYRIGHT

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{main_version}-%{main_release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
Requires: nginx == %{?epoch:%{epoch}:}%{main_version}-1%{?dist}.ngx

%description
ngx_pagespeed-%{pagespeed_version} dynamic module for nginx-%{main_version}-%{main_release}

%if 0%{?suse_version} || 0%{?amzn}
%debug_package
%endif

%define WITH_CC_OPT $(echo %{optflags} $(pcre-config --cflags))
%define WITH_LD_OPT -Wl,-z,relro -Wl,-z,now

%define BASE_CONFIGURE_ARGS $(echo "--prefix=%{_sysconfdir}/nginx --sbin-path=%{_sbindir}/nginx --modules-path=%{_libdir}/nginx/modules --conf-path=%{_sysconfdir}/nginx/nginx.conf --error-log-path=%{_localstatedir}/log/nginx/error.log --http-log-path=%{_localstatedir}/log/nginx/access.log --pid-path=%{_localstatedir}/run/nginx.pid --lock-path=%{_localstatedir}/run/nginx.lock --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp --user=%{nginx_user} --group=%{nginx_group} --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module")
%define MODULE_CONFIGURE_ARGS $(echo "--add-dynamic-module=%{bdir}/ngx_pagespeed-latest-stable")

%prep
%setup -qcTn %{name}-%{main_version}
tar --strip-components=1 -xzf %{SOURCE0}
mkdir %{bdir}/ngx_pagespeed-latest-stable
pagespeed_url=https://github.com/pagespeed/ngx_pagespeed/archive/v%{pagespeed_version}-stable.tar.gz
curl -L ${pagespeed_url} | tar --strip-components=1 -xz -C %{bdir}/ngx_pagespeed-latest-stable  # extracts to ngx_pagespeed
cd %{bdir}/ngx_pagespeed-latest-stable
[ -e scripts/format_binary_url.sh ] && psol_url=$(scripts/format_binary_url.sh PSOL_BINARY_URL)
curl -L ${psol_url} | tar -xz # extracts to psol/

%build

cd %{bdir}
yes Y | ./configure %{BASE_CONFIGURE_ARGS} %{MODULE_CONFIGURE_ARGS} \
	--with-cc-opt="%{WITH_CC_OPT}" \
	--with-ld-opt="%{WITH_LD_OPT}" \
	--with-debug
make %{?_smp_mflags} modules
for so in `find %{bdir}/objs/ -type f -name "*.so"`; do
debugso=`echo $so | sed -e "s|.so|-debug.so|"`
mv $so $debugso
done
./configure %{BASE_CONFIGURE_ARGS} %{MODULE_CONFIGURE_ARGS} \
	--with-cc-opt="%{WITH_CC_OPT}" \
	--with-ld-opt="%{WITH_LD_OPT}"
make %{?_smp_mflags} modules

%install
cd %{bdir}
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT%{_datadir}/doc/nginx-module-pagespeed
%{__install} -m 644 -p %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/doc/nginx-module-pagespeed/

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
%dir %{_datadir}/doc/nginx-module-pagespeed
%{_datadir}/doc/nginx-module-pagespeed/*

%post
if [ $1 -eq 1 ]; then
cat <<BANNER
----------------------------------------------------------------------

The pagespeed dynamic module for nginx has been installed.
To enable this module, add the following to /etc/nginx/nginx.conf
and reload nginx:

    load_module modules/ngx_pagespeed.so

Please refer to the module documentation for further details:
https://www.modpagespeed.com/doc/build_ngx_pagespeed_from_source

----------------------------------------------------------------------
BANNER
fi

%changelog
* Sat Feb 10 2018 Shigechika AIKAWA
- sync w/ nginx-1.12.2 and pagespeed-1.13.35.2-stable.
- automatic download ngx_pagespeed source and psol (binary) library.

* Sun Oct 22 2017 Shigechika AIKAWA
- base on nginx-1.12.2 and pagespeed-1.12.34.3-stable.

* Fri Oct 13 2017 Shigechika AIKAWA
- base on nginx-1.12.1 and pagespeed-1.12.34.2-stable.
- referenced nginx module spec files.
