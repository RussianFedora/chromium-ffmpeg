%define rev 121229

Name:           chromium-ffmpeg
Summary:        The ffmpeg lib for Google's opens source browser Chromium
Version:        19.0.1037.0
Release:        1%{?dist}.R

License:        BSD
Url:            http://code.google.com/p/chromium/
Group:          Applications/Internet
Source0:        http://download.rfremix.ru/storage/chromium/19.0.1031.0/%{name}.%{version}.svn%{rev}.tar.bz2
# Script used to create the tar.lzma archive from a checked out source
Source3:        pack_chromium_source.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gsm-devel
BuildRequires:  imlib2-devel
BuildRequires:  lame-devel
BuildRequires:  libogg-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libtheora-devel >= 1.1
BuildRequires:  ncurses-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  freetype-devel
BuildRequires:  SDL-devel
BuildRequires:  slang-devel
BuildRequires:  libX11-devel
BuildRequires:  zlib-devel
#BuildRequires:  faac-devel >= 1.28
BuildRequires:  x264-devel
BuildRequires:  xvidcore-devel
BuildRequires:  texinfo
BuildRequires:  opencore-amr-devel
BuildRequires:  libdc1394-devel
BuildRequires:  speex-devel
BuildRequires:  schroedinger-devel
BuildRequires:  liboil-devel >= 0.3.15
BuildRequires:  dirac-devel >= 1.0.0
BuildRequires:  openjpeg-devel
BuildRequires:  libvdpau-devel
BuildRequires:  python-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libvpx-devel

%description
FFMPEG library built from the chromium sources. 

%prep
%setup -q -n chromium

%if 0%{?rhel} < 7
find . -type f -name '*.gyp*' -o -name '*.mk' | while read f; do
    %__sed -i 's/-Wno-unused-result//g' "$f"
done
%endif

%build

## create make files
pushd src

./build/gyp_chromium -f make third_party/ffmpeg/ffmpeg.gyp \
-Dffmpeg_branding=Chrome \
%ifnarch x86_64
-Ddisable_sse2=1 \
%endif
%ifarch x86_64
-Dtarget_arch=x64 \
-Dlinux_use_gold_flags=0 \
%endif
-Dlinux_fpic=1

cd third_party/ffmpeg

make -r %{?_smp_mflags} -f ffmpeg.Makefile BUILDTYPE=Release V=1

popd

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/chromium/
pushd src/third_party/ffmpeg/out/Release
cp -a lib*.so %{buildroot}%{_libdir}/chromium/
popd


%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README-archive
%dir %{_libdir}/chromium
%attr(0755,root,root) %{_libdir}/chromium/lib*.so

%changelog
* Mon Feb 20 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 19.0.1037.0-1.R
- update to 19.0.1037.0

* Sun Feb 19 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 18.0.972.0-1.R
- initial build for EL6
