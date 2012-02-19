#!/bin/bash
#
# forgive me for the state of this script

chromium_svn_dir="$1"
chromium_tgt_dir=/sources/chromium-ffmpeg

name=chromium-ffmpeg
version="`cat $chromium_svn_dir/src/chrome/VERSION | cut -f2 -d= |while read i; do echo -n $i\. ; done`"
revision="svn`cat $chromium_svn_dir/src/.svn/entries | grep -m1 -A1 'dir' | tr '\n\r' '-' | cut -f2 -d-`"

echo "Version: $version"
echo "Revision: $revision"

xz="`which xz 2>/dev/null`"
lzma="`which lzma 2>/dev/null`"


if [ -z $chromium_svn_dir ]
then
	echo "Usage:  `basename $0` [SVN_SOURCE_DIR]"
	exit 1
fi

if [ -f $xz ]
then
	compress=$xz
	compress_opts='-9 -F lzma' #xz compresses MUCH faster, so why not make it compress more?  We have the RAM...
	echo "using xz"
else
	compress=$lzma
	compress_opts="-7"
	echo "using lzma"
fi

echo
echo "Moving source in staging area"
cp -R $chromium_svn_dir $chromium_tgt_dir
cd $chromium_tgt_dir/src/
rm -rf app breakpad ceee chrome chrome_frame courgette gears gfx google_update googleurl ipc jingle
rm -rf media native_client net o3d ppapi printing remoting sandbox sdch seccompsandbox skia testing v8
rm -rf views webkit gpu 
cd third_party
rm -rf activscp adobe angle angleproject apple apple_apsl bsdiff bspatch bzip2 cacheinvalidation cld 
rm -rf codesighs expat fuzzymatch gles2_book gpsd harfbuzz hunspell hunspell_dictionaries hyphen
rm -rf iaccessible2 iccjpeg icu isimpledom jemalloc lcov libevent libjingle libjpeg libpng libsrtp 
rm -rf libwebp libxml libxslt lss lzma_sdk mesa modp_b64 molokocacao mongoose mozilla npapi ocmock
rm -rf openmax openssl ots protobuf protobuf2 pyftpdlib qcms safe_browsing simplejson skia speex sqlite
rm -rf swig talloc tcmalloc tlslite undoview webdriver WebKit wtl xdg-utils zlib
rm base/*.cc
rm -rf base/allocator base/android base/build base/data base/debug base/files base/i18n base/json base/mac base/memory
rm -rf base/metrics base/nix base/synchronization base/system_monitor base/test base/third_party base/threading base/win

echo 
echo "Recompressing and excluding svn data"
echo "  this takes a while, sorry"
echo "  Compressing with $compress"

cd $chromium_tgt_dir/
cd ..

tar --exclude=\.svn -cjf "$name"."$version""$revision".tar.bz2 $name

rm -rf $chromium_tgt_dir
