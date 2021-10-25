# nginx-module-pagespeed

- This package use with nginx.org yum repository.
- Pagespeed Dynamic Module
- Currently supports CentOS7 only
- Automatic download PSOL(PageSpeed Optimization Libraries) stable version

## How to build

```
rpmquery rpmdevtools || sudo yum install rpmdevtools && rpmdev-setuptree
rpm -Uvh https://nginx.org/packages/centos/7/SRPMS/nginx-1.20.1-1.el7.ngx.src.rpm
git clone https://github.com/shigechika/nginx-module-pagespeed.git
rpmbuild -ba nginx-module-pagespeed/nginx-module-pagespeed.spec
sudo yum localupdate rpmbuild/RPMS/x86_64/nginx-module-pagespeed-1.20.1-1.el7.ngx.x86_64.rpm
```

## Workaround

- If you stopped at rpmbuild...

example
```
% rpmbuild -ba ...
error: Failed build dependencies:
	openssl-devel >= 1.0.2 is needed by nginx-module-pagespeed-1:1.20.1-1.el7.ngx.x86_64
	libuuid-devel is needed by nginx-module-pagespeed-1:1.20.1-1.el7.ngx.x86_64
	gcc is needed by nginx-module-pagespeed-1:1.20.1-1.el7.ngx.x86_64
	gcc-c++ is needed by nginx-module-pagespeed-1:1.20.1-1.el7.ngx.x86_64
	zlib-devel is needed by nginx-module-pagespeed-1:1.20.1-1.el7.ngx.x86_64
	pcre-devel is needed by nginx-module-pagespeed-1:1.20.1-1.el7.ngx.x86_64
```
please try
```
sudo yum install openssl-devel libuuid-devel gcc-c++
```

## NO WARRANTY

Good LUCK :-)
