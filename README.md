# nginx-module-pagespeed

- This package use with nginx.org yum repository.
- Pagespeed Dynamic Module
- Currently supports CentOS7 only
- Automatic download PSOL(PageSpeed Optimization Libraries) stable version

# How to build

```
rpmdev-setuptree
rpm -Uvh https://nginx.org/packages/centos/7/SRPMS/nginx-1.18.0-1.el7.ngx.src.rpm
git clone https://github.com/shigechika/nginx-module-pagespeed.git
cd nginx-module-pagespeed
rpmbuild -ba nginx-module-pagespeed.spec
yum localupdate /path/to/nginx-module-pagespeed-1.18.1-0.el7.ngx.x86_64.rpm
```

# Requiers

- If you stopped at rpmdev-setuptree...

```
yum install -y rpmdevtools...
```

- If you stopped at rpmbuild

```
yum install -y openssl-devel libuuid-devel gcc gcc-c++ zlib-devel pcre-devel
```

# NO WARRANTY

Good LUCK :-)
