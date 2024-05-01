# nginx-module-pagespeed

- Compatible with nginx.org repository.
- Pagespeed Dynamic Module
- Currently supports CentOS7 only
- Automatic download PSOL(PageSpeed Optimization Libraries) stable version

## How to install

```
sudo yum-config-manager --enable nginx-mainline
sudo yum install https://github.com/shigechika/nginx-module-pagespeed/releases/download/1.25.5/nginx-module-pagespeed-1.25.5-1.el7.ngx.x86_64.rpm
```

## How to build

```
rpmquery rpmdevtools || sudo yum install -y rpmdevtools && rpmdev-setuptree
rpm -Uvh https://nginx.org/packages/mainline/centos/7/SRPMS/nginx-1.25.5-1.el7.ngx.src.rpm
git clone https://github.com/shigechika/nginx-module-pagespeed.git
cp nginx-module-pagespeed/PR1750.diff ~/rpmbuild/SOURCES/
rpmquery openssl-devel libuuid-devel gcc-c++ || sudo yum install -y openssl-devel libuuid-devel gcc-c++
rpmbuild -ba nginx-module-pagespeed/nginx-module-pagespeed.spec
sudo yum localinstall ~/rpmbuild/RPMS/x86_64/nginx-module-pagespeed-1.25.5-1.el7.ngx.x86_64.rpm
```

## Workaround

- If you stopped at yum install...

Please check to nginx.org repository.

https://nginx.org/en/linux_packages.html#RHEL-CentOS

- If you stopped at rpmbuild...

example
```
% rpmbuild -ba ...
error: Failed build dependencies:
	openssl-devel >= 1.0.2 is needed by nginx-module-pagespeed-1:1.2X.X-1.el7.ngx.x86_64
	libuuid-devel is needed by nginx-module-pagespeed-1:1.2X.X-1.el7.ngx.x86_64
	gcc is needed by nginx-module-pagespeed-1:1.2X.X-1.el7.ngx.x86_64
	gcc-c++ is needed by nginx-module-pagespeed-1:1.2X.X-1.el7.ngx.x86_64
	zlib-devel is needed by nginx-module-pagespeed-1:1.2X.X-1.el7.ngx.x86_64
	pcre-devel is needed by nginx-module-pagespeed-1:1.2X.X-1.el7.ngx.x86_64
```
please try
```
sudo yum install openssl-devel libuuid-devel gcc-c++
```

## NO WARRANTY

Good LUCK :-)
