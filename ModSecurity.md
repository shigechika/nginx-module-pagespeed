# Install

```
sudo yum localinstall \
 https://github.com/shigechika/nginx-module-pagespeed/releases/download/1.23.1/nginx-module-ModSecurity-1.23.1-1.el7.ngx.x86_64.rpm \
 https://github.com/shigechika/nginx-module-pagespeed/releases/download/1.23.1/libmodsecurity-3.0.7-1.el7.x86_64.rpm
```

# Develop

## prepare

```
curl -L -O https://github.com/SpiderLabs/ModSecurity/releases/download/v3.0.7/modsecurity-v3.0.7.tar.gz
cp modsecurity-v3.0.7.tar.gz rpmbuild/SOURCES
cp nginx-module-pagespeed/modsecurity.pc rpmbuild/SOURCES/
rpmquery flex bison ssdeep-devel yajl-devel libcurl-devel geoip-devel lmdb-devel libxml2-devel || sudo yum install -y flex bison ssdeep-devel yajl-devel libcurl-devel geoip-devel lmdb-devel libxml2-devel
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild -ba nginx-module-pagespeed/libmodsecurity.spec
sudo yum localinstall rpmbuild/RPMS/x86_64/libmodsecurity-devel-3.0.7-1.el7.x86_64.rpm rpmbuild/RPMS/x86_64/libmodsecurity-3.0.7-1.el7.x86_64.rpm
```

## build

```
rpmbuild -ba nginx-module-pagespeed/nginx-module-ModSecurity.spec
sudo yum localinstall rpmbuild/RPMS/x86_64/nginx-module-ModSecurity-1.23.1-1.el7.ngx.x86_64.rpm
```

