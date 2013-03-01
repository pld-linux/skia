#!/bin/sh
# Make snapshot of skia
# https://sites.google.com/site/skiadocs/user-documentation/quick-start-guides/linux
# Author: Elan Ruusamäe <glen@pld-linux.org>
set -e

package=skia
specfile=$package.spec
baseurl=http://$package.googlecode.com/svn
svnurl=$baseurl/trunk
release_dir=$package-$(date +%Y%m%d)
tarball=$release_dir.tar.xz

# get depot tools
# http://www.chromium.org/developers/how-tos/install-depot-tools
test -d depot_tools || {
	# could also checkout:
	# svn co http://src.chromium.org/svn/trunk/tools/depot_tools
	wget -c https://src.chromium.org/svn/trunk/tools/depot_tools.zip
	unzip -qq depot_tools.zip
	chmod a+x depot_tools/gclient depot_tools/update_depot_tools
}

topdir=${PWD:-($pwd)}
gclient=$topdir/gclient.conf
install -d $package
cd $package

if [ ! -f $gclient ]; then
	# create initial config that can be later modified
	../depot_tools/gclient config $svnurl --gclientfile=$gclient
fi

cp -p $gclient .gclient

# emulate gclient config, preserving our deps
sed -i -re '/"url"/ s,"http[^"]+","'$svnurl'",' .gclient

../depot_tools/gclient sync --nohooks -v

cd ..

cp -al $package $release_dir
XZ_OPT=-e9 tar -caf $tarball --exclude-vcs $release_dir
rm -rf $release_dir

../md5 $specfile
../dropin $tarball &
