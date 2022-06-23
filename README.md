# nginx-module-pagespeed

- Compatible with nginx.org repository.
- Pagespeed Dynamic Module
- Currently supports CentOS7 only
- Automatic download PSOL(PageSpeed Optimization Libraries) stable version

## How to build

```
rpmquery rpmdevtools || sudo yum install -y rpmdevtools && rpmdev-setuptree
rpm -Uvh https://nginx.org/packages/mainline/centos/7/SRPMS/nginx-1.21.6-1.el7.ngx.src.rpm
git clone https://github.com/shigechika/nginx-module-pagespeed.git
rpmquery openssl-devel libuuid-devel gcc-c++ || sudo yum install -y openssl-devel libuuid-devel gcc-c++
rpmbuild -ba nginx-module-pagespeed/nginx-module-pagespeed.spec
sudo yum localupdate rpmbuild/RPMS/x86_64/nginx-module-pagespeed-1.21.6-1.el7.ngx.x86_64.rpm
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
	openssl-devel >= 1.0.2 is needed by nginx-module-pagespeed-1:1.21.X-1.el7.ngx.x86_64
	libuuid-devel is needed by nginx-module-pagespeed-1:1.21.X-1.el7.ngx.x86_64
	gcc is needed by nginx-module-pagespeed-1:1.21.X-1.el7.ngx.x86_64
	gcc-c++ is needed by nginx-module-pagespeed-1:1.21.X-1.el7.ngx.x86_64
	zlib-devel is needed by nginx-module-pagespeed-1:1.21.X-1.el7.ngx.x86_64
	pcre-devel is needed by nginx-module-pagespeed-1:1.21.X-1.el7.ngx.x86_64
```
please try
```
sudo yum install openssl-devel libuuid-devel gcc-c++
```

$ LANG=C rpmbuild -ba libmodsecurity.spec
error: Failed build dependencies:
	flex is needed by libmodsecurity-3.0.6-1.el7.x86_64
	bison is needed by libmodsecurity-3.0.6-1.el7.x86_64
	ssdeep-devel is needed by libmodsecurity-3.0.6-1.el7.x86_64
	pkgconfig(libxml-2.0) is needed by libmodsecurity-3.0.6-1.el7.x86_64
	pkgconfig(yajl) is needed by libmodsecurity-3.0.6-1.el7.x86_64
	pkgconfig(libcurl) is needed by libmodsecurity-3.0.6-1.el7.x86_64
	pkgconfig(geoip) is needed by libmodsecurity-3.0.6-1.el7.x86_64
	pkgconfig(lmdb) is needed by libmodsecurity-3.0.6-1.el7.x86_64

sudo yum install lmdb-devel geoip-devel libcurl-devel yajl-devel libxml2-devel ssdeep-devel bison flex gzip

curl -L -O https://github.com/SpiderLabs/ModSecurity/releases/download/v3.0.6/modsecurity-v3.0.6.tar.gz
curl -O https://src.fedoraproject.org/rpms/libmodsecurity/raw/rawhide/f/modsecurity.pc
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild -ba libmodsecurity.spec

sudo yum localinstall ../rpmbuild/RPMS/x86_64/libmodsecurity-devel-3.0.6-1.el7.x86_64.rpm  ../rpmbuild/RPMS/x86_64/libmodsecurity-3.0.6-1.el7.x86_64.rpm

2022/01/27 19:15:52 [notice] 12084#12084: ModSecurity-nginx v1.0.2 (rules loaded inline/local/remote: 0/0/0)
2022/01/27 19:16:06 [notice] 12117#12117: ModSecurity-nginx v1.0.2 (rules loaded inline/local/remote: 0/0/0)


## NO WARRANTY

Good LUCK :-)
