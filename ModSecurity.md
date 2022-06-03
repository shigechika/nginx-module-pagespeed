
- prepare

```
curl -L -O https://github.com/SpiderLabs/ModSecurity/releases/download/v3.0.7/modsecurity-v3.0.7.tar.gz
cp modsecurity-v3.0.7.tar.gz rpmbuild/SOURCES
rpmquery flex bison ssdeep-devel yajl-devel libcurl-devel geoip-devel lmdb-devel libxml2-devel || sudo yum install -y flex bison ssdeep-devel yajl-devel libcurl-devel geoip-devel lmdb-devel libxml2-devel
QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild -ba nginx-module-pagespeed/libmodsecurity.spec
sudo yum localinstall rpmbuild/RPMS/x86_64/libmodsecurity-devel-3.0.7-1.el7.x86_64.rpm  rpmbuild/RPMS/x86_64/libmodsecurity-3.0.7-1.el7.x86_64.rpm
```


