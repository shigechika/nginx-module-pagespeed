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
BuildRequires: libmodsecurity-devel >= 3.0.7
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

%define bdir %{_builddir}/%{name}-%{base_version}

%define WITH_CC_OPT $(echo %{optflags} $(pcre-config --cflags))
%define WITH_LD_OPT -Wl,-z,relro -Wl,-z,now

%define BASE_CONFIGURE_ARGS $(echo "--prefix=%{_sysconfdir}/nginx --sbin-path=%{_sbindir}/nginx --modules-path=%{_libdir}/nginx/modules --conf-path=%{_sysconfdir}/nginx/nginx.conf --error-log-path=%{_localstatedir}/log/nginx/error.log --http-log-path=%{_localstatedir}/log/nginx/access.log --pid-path=%{_localstatedir}/run/nginx.pid --lock-path=%{_localstatedir}/run/nginx.lock --http-client-body-temp-path=%{_localstatedir}/cache/nginx/client_temp --http-proxy-temp-path=%{_localstatedir}/cache/nginx/proxy_temp --http-fastcgi-temp-path=%{_localstatedir}/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=%{_localstatedir}/cache/nginx/uwsgi_temp --http-scgi-temp-path=%{_localstatedir}/cache/nginx/scgi_temp --user=%{nginx_user} --group=%{nginx_group} --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module")
%define MODULE_NAME ModSecurity-nginx
%define MODULE_CONFIGURE_ARGS $(echo "--add-dynamic-module=%{bdir}/%{MODULE_NAME}")

Summary: nginx ModSecurity dynamic module
Name: nginx-module-ModSecurity
Version: %{base_version}
Release: %{base_release}
Vendor: Nginx, Inc.
URL: http://nginx.org/
Group: %{_group}

Source0: http://nginx.org/download/nginx-%{base_version}.tar.gz
Source1: nginx.copyright

License: 2-clause BSD-like license

BuildRoot: %{_tmppath}/%{name}-%{base_version}-%{base_release}-root
BuildRequires: zlib-devel
BuildRequires: pcre-devel
Requires: nginx == %{?epoch:%{epoch}:}%{base_version}-%{base_release}

%description
ngx_ModSecurity dynamic module for nginx-%{base_version}-%{base_release}

%if 0%{?suse_version} || 0%{?amzn} 
%debug_package
%endif

%prep
%setup -qcTn %{name}-%{base_version}
tar --strip-components=1 -xzf %{SOURCE0}
git clone https://github.com/SpiderLabs/ModSecurity-nginx.git

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

The ModSecurity dynamic module for nginx has been installed.
To enable this module, add the following to /etc/nginx/nginx.conf
and reload nginx:

    load_module modules/ngx_http_modsecurity_module.so;

Please refer to the module documentation for further details:
https://github.com/SpiderLabs/ModSecurity-nginx

----------------------------------------------------------------------
BANNER
fi

%changelog
* Thu Jul 21 2022 AIKAWA Shigechika
- sync w/ nginx-1.23.1

* Thu Jan 27 2022 AIKAWA Shigechika
- sync w/ nginx-1.21.6