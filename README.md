# nginx-module-pagespeed

- Pagespeed Dynamic Module
- Currently supports CentOS7 only
- Automatic download PSOL(PageSpeed Optimization Libraries) stable version

# How to build

    rpmdev-setuptree
    rpm -Uvh https://nginx.org/packages/centos/7/SRPMS/nginx-1.14.0-1.el7_4.ngx.src.rpm
    git clone https://github.com/shigechika/nginx-module-pagespeed.git
    cd nginx-module-pagespeed
    rpmbuild -ba nginx-module-pagespeed.spec
    yum localupdate /path/to/nginx-module-pagespeed-1.14.0-1.el7_4.ngx.x86_64.rpm
