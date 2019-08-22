# nginx-module-pagespeed

- This package use with nginx.org yum repository.
- Pagespeed Dynamic Module
- Currently supports CentOS7 only
- Automatic download PSOL(PageSpeed Optimization Libraries) stable version

# How to build

```
rpmdev-setuptree
rpm -Uvh https://nginx.org/packages/centos/7/SRPMS/nginx-1.16.1-1.el7.ngx.src.rpm
git clone https://github.com/shigechika/nginx-module-pagespeed.git
cd nginx-module-pagespeed
rpmbuild -ba nginx-module-pagespeed.spec
yum localupdate /path/to/nginx-module-pagespeed-1.16.1-1.el7.ngx.x86_64.rpm
```

# NO WARRANTY

Good luck.
