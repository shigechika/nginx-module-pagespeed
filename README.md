# nginx-module-pagespeed

- Pagespeed Dynamic Module
- Currently supports CentOS7 only

# How to build

    rpm -Uvh https://nginx.org/packages/centos/7/SRPMS/nginx-1.14.0-1.el7_4.ngx.src.rpm
    git clone https://github.com/shigechika/nginx-module-pagespeed.git
    cd nginx-module-pagespeed
    rpmbuild nginx-module-pagespeed.spec
    yum localupdate /path/to/nginx-module-pagespeed-1.14.0-1.el7_4.ngx.x86_64.rpm
