# TODO:
# - with new gcc version (it is possible that)
#   - -fvisibility=hiddenn and ac_cv_visibility_pragma=no can be removed
# - with new firefox version (it is possible that)
#   - -fno-strict-aliasing can be removed (needs to be tested carefuly,
#      not to be fixed soon, imho)
# - handle locales differently (runtime, since it's possible to do)
# - see ftp://ftp.debian.org/debian/pool/main/m/mozilla-firefox/*diff*
#   for hints how to make locales
# - check all remaining configure options... done. test them now!
# - make it more pld-like (bookmarks, default page etc..)
# - add dictionaries outside of mozilla
# - previous postun cleanup should be handled by ghost files
# - stop providing mozdir/components/*.so
#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
Summary:	Mozilla Firefox web browser
Summary(pl):	Mozilla Firefox - przegl±darka WWW
Name:		mozilla-firefox
Version:	2.0
Release:	0.13
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}-source.tar.bz2
# Source0-md5:	03709c15cba0e0375ff5336d538f77e7
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch1:		%{name}-lib_path.patch
Patch3:		%{name}-nopangoxft.patch
Patch4:		%{name}-name.patch
Patch5:		%{name}-fonts.patch
# if ac rebuild is needed...
#PatchX:		%{name}-ac.patch
# UPDATE or DROP?
#PatchX:	%{name}-searchplugins.patch
URL:		http://www.mozilla.org/projects/firefox/
%{?with_gnome:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0.0
%{?with_gnome:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	heimdal-devel >= 0.7.1
BuildRequires:	jdk
BuildRequires:	libIDL-devel >= 0.8.0
%{?with_gnome:BuildRequires:	libgnome-devel >= 2.0}
%{?with_gnome:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.7
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6.3
BuildRequires:	nss-devel >= 1:3.11.3-3
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires(post):	mktemp >= 1.5-18
Requires:	%{name}-lang-resources = %{version}
Requires:	nspr >= 1:4.6.3
Requires:	nss >= 1:3.11.3
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/%{name}
# mozilla and firefox provide their own versions
%define		_noautoreqdep		libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so

%define		specflags	-fno-strict-aliasing

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l pl
Mozilla Firefox jest open sourcow± przegl±dark± sieci WWW, stworzon± z
my¶l± o zgodno¶ci ze standardami, wydajno¶ci± i przeno¶no¶ci±.

%package devel
Summary:	Headers for developing programs that will use Mozilla Firefox
Summary(pl):	Mozilla Firefox - pliki nag³ówkowe
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	nspr-devel >= 1:4.6.3
Requires:	nss-devel >= 1:3.11.3-3
Obsoletes:	mozilla-devel

%description devel
Mozilla Firefox development package.

%description devel -l pl
Pliki nag³ówkowe przegl±darki Mozilla Firefox.

%package lang-en
Summary:	English resources for Mozilla Firefox
Summary(pl):	Anglojêzyczne zasoby dla przegl±darki Mozilla Firefox
Group:		X11/Applications/Networking
Requires(post,postun):	%{name} = %{version}-%{release}
Requires(post,postun):	textutils
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-lang-resources = %{version}-%{release}

%description lang-en
English resources for Mozilla Firefox.

%description lang-en -l pl
Anglojêzyczne zasoby dla przegl±darki Mozilla Firefox.

%prep
%setup -qc
cd mozilla
#%patch0 -p1
%patch1 -p1
#%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

sed -i 's/\(-lgss\)\(\W\)/\1disable\2/' configure

# use system
#rm -rf mozilla/nsprpub mozilla/security/nss

%build
cd mozilla
export CFLAGS="%{rpmcflags} $(%{_bindir}/pkg-config mozilla-nspr --cflags-only-I)"
export CXXFLAGS="%{rpmcflags} $(%{_bindir}/pkg-config mozilla-nspr --cflags-only-I)"

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf

#export LIBIDL_CONFIG="%{_bindir}/libIDL-config-2"

cat << 'EOF' > .mozconfig
. $topsrcdir/browser/config/mozconfig

# We're not allowed to do that!
#export BUILD_OFFICIAL=1
#export MOZILLA_OFFICIAL=1
#mk_add_options BUILD_OFFICIAL=1
#mk_add_options MOZILLA_OFFICIAL=1

ac_add_options --prefix=%{_prefix}
ac_add_options --exec-prefix=%{_exec_prefix}
ac_add_options --bindir=%{_bindir}
ac_add_options --sbindir=%{_sbindir}
ac_add_options --sysconfdir=%{_sysconfdir}
ac_add_options --datadir=%{_datadir}
ac_add_options --includedir=%{_includedir}
ac_add_options --libdir=%{_libdir}
ac_add_options --libexecdir=%{_libexecdir}
ac_add_options --localstatedir=%{_localstatedir}
ac_add_options --sharedstatedir=%{_sharedstatedir}
ac_add_options --mandir=%{_mandir}
ac_add_options --infodir=%{_infodir}
%if %{?debug:1}0
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --enable-debugger-info-modules
ac_add_options --disable-optimize
ac_add_options --enable-crash-on-assert
%else
ac_add_options --disable-debug
ac_add_options --enable-optimize="%{rpmcflags}"
ac_add_options --disable-logging
ac_add_options --enable-elf-dynstr-gc
ac_add_options --enable-cpp-exceptions
ac_add_options --enable-cpp-rtti
%endif
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
%if %{with gnome}
ac_add_options --enable-gnomevfs
ac_add_options --enable-gnomeui
%else
ac_add_options --disable-gnomevfs
ac_add_options --disable-gnomeui
%endif
ac_add_options --disable-dtd-debug
ac_add_options --disable-freetype2
ac_add_options --disable-installer
ac_add_options --disable-ldap
ac_add_options --disable-mailnews
ac_add_options --disable-profilesharing
ac_add_options --disable-xprint
ac_add_options --enable-canvas
ac_add_options --enable-cookies
ac_add_options --enable-crypto
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-image-encoder=all
ac_add_options --enable-image-decoder=all
ac_add_options --enable-mathml
ac_add_options --enable-pango
# This breaks mozilla start - don't know why
#ac_add_options --enable-places
ac_add_options --enable-postscript
ac_add_options --enable-reorder
ac_add_options --enable-safe-browsing --enable-url-classifier
ac_add_options --enable-single-profile
ac_add_options --enable-storage
ac_add_options --enable-svg --enable-svg-renderer=cairo --enable-system-cairo
ac_add_options --enable-view-source
ac_add_options --enable-xft
ac_add_options --enable-xinerama
ac_add_options --enable-xpctools
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-pthreads
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-zlib
ac_add_options --with-system-jpeg
ac_add_options --with-system-png
ac_add_options --enable-native-uconv
ac_add_options --enable-jsd --enable-javaxpcom --with-java-include-path=/usr/lib/jvm/java/include
ac_add_options --enable-update-channel=default
ac_add_options --enable-reorder
ac_add_options --enable-libxul
ac_add_options --disable-v1-string-abi
ac_add_options --with-default-mozilla-five-home=%{_firefoxdir}
ac_cv_visibility_pragma=no
EOF

%if 0
# sanity checks
# TODO: should hook somewhere between configure and real make
if [ $(grep -c "MOZ_NATIVE_NSPR = 1" config/autoconf.mk) != 1 ]; then
	: internal nspr used!
	exit 1
fi
if [ $(grep -c "MOZ_NATIVE_NSS = 1" config/autoconf.mk) != 1 ]; then
	: internal nss used!
	exit 1
fi
if [ $(grep -c "MOZ_NATIVE_ZLIB = 1" config/autoconf.mk) != 1 ]; then
	: internal zlib used!
	exit 1
fi
if [ $(grep -c "MOZ_NATIVE_JPEG = 1" config/autoconf.mk) != 1 ]; then
	: internal libjpeg used!
	exit 1
fi
if [ $(grep -c "MOZ_NATIVE_PNG = 1" config/autoconf.mk) != 1 ]; then
	: internal libpng used!
	exit 1
fi
%endif

%{__make} -j1 -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
cd mozilla
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT{%{_includedir},%{_pkgconfigdir}}

%{__make} -C xpinstall/packager stage-package \
	MOZ_PKG_APPNAME=%{name} \
	SIGN_NSS= \
	PKG_SKIP_STRIP=1

cp -a dist/%{name} $RPM_BUILD_ROOT%{_libdir}
sed 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox
ln -s mozilla-firefox $RPM_BUILD_ROOT%{_bindir}/firefox

install other-licenses/branding/firefox/content/icon64.png $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-firefox.png
#install -m644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/
#install -m644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/US/

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

# header/developement files
cp -rfL dist/include	$RPM_BUILD_ROOT%{_includedir}/%{name}
cp -rfL dist/idl	$RPM_BUILD_ROOT%{_includedir}/%{name}

install dist/bin/regxpcom $RPM_BUILD_ROOT%{_bindir}
install dist/bin/xpidl $RPM_BUILD_ROOT%{_bindir}
install dist/bin/xpt_dump $RPM_BUILD_ROOT%{_bindir}
install dist/bin/xpt_link $RPM_BUILD_ROOT%{_bindir}

ln -sf necko/nsIURI.h $RPM_BUILD_ROOT%{_includedir}/mozilla-firefox/nsIURI.h

# pkgconfig files
for f in build/unix/*.pc; do
	sed -e 's/firefox-%{version}/mozilla-firefox/' $f > $RPM_BUILD_ROOT%{_pkgconfigdir}/${f##*/}
done

# already provided by standalone packages
rm -f $RPM_BUILD_ROOT%{_pkgconfigdir}/firefox-{nss,nspr}.pc

sed -i -e 's#firefox-nspr =.*#mozilla-nspr#g' -e 's#irefox-nss =.*#mozilla-nss#g' \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# includedir/dom CFLAGS
sed -i -e '/Cflags:/{/{includedir}\/dom/!s,$, -I${includedir}/dom,}' \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/firefox-plugin.pc

# files created by regxpcom and firefox -register
touch $RPM_BUILD_ROOT%{_firefoxdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_firefoxdir}/components/xpti.dat

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/firefox-chrome+xpcom-generate
#!/bin/sh
umask 022
rm -f %{_firefoxdir}/chrome/{chrome.rdf,overlayinfo/*/*/*.rdf}
rm -f %{_firefoxdir}/components/{compreg,xpti}.dat
export MOZILLA_FIVE_HOME=%{_firefoxdir} # perhaps uneccessary after --with-default-mozilla-five-home?

# PATH
export PATH="%{_firefoxdir}:$PATH"

# added /usr/lib: don't load your local library
export LD_LIBRARY_PATH=%{_firefoxdir}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}

unset TMPDIR TMP || :
# it attempts to touch files in $HOME/.mozilla
# beware if you run this with sudo!!!
export HOME=$(mktemp -d)
%{_firefoxdir}/regxpcom
%{_firefoxdir}/firefox -register
rm -rf $HOME
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/firefox-chrome+xpcom-generate

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla*
%attr(755,root,root) %{_bindir}/firefox
%attr(755,root,root) %{_sbindir}/*
%dir %{_firefoxdir}
%{_firefoxdir}/res
%dir %{_firefoxdir}/components
%attr(755,root,root) %{_firefoxdir}/components/*.so
%{_firefoxdir}/components/*.js
%{_firefoxdir}/components/*.xpt
%dir %{_firefoxdir}/plugins
%attr(755,root,root) %{_firefoxdir}/plugins/*.so
%{_firefoxdir}/searchplugins
%{_firefoxdir}/icons
%{_firefoxdir}/defaults
%{_firefoxdir}/greprefs
%dir %{_firefoxdir}/extensions
%dir %{_firefoxdir}/init.d
%{_firefoxdir}/init.d/README
%attr(755,root,root) %{_firefoxdir}/*.so
%attr(755,root,root) %{_firefoxdir}/*.sh
%attr(755,root,root) %{_firefoxdir}/m*
%attr(755,root,root) %{_firefoxdir}/f*
%attr(755,root,root) %{_firefoxdir}/reg*
%attr(755,root,root) %{_firefoxdir}/x*
%{_pixmapsdir}/*
%{_desktopdir}/*

%dir %{_firefoxdir}/chrome
%{_firefoxdir}/chrome/*.jar
%{_firefoxdir}/chrome/*.manifest
%dir %{_firefoxdir}/chrome/icons
%{_firefoxdir}/chrome/icons/default

# -dom-inspector subpackage?
%dir %{_firefoxdir}/extensions/inspector@mozilla.org
%{_firefoxdir}/extensions/inspector@mozilla.org/*

# javaxpcom
%{_firefoxdir}/javaxpcom-src.jar
%{_firefoxdir}/javaxpcom.jar

# updater
%{_firefoxdir}/updater
%{_firefoxdir}/updater.ini

# browserconfig
%{_firefoxdir}/browserconfig.properties

# check what these are
%{_firefoxdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%{_firefoxdir}/extensions/{cf2812dc-6a7c-4402-b639-4d277dac4c36}

%{_firefoxdir}/LICENSE
%{_firefoxdir}/README.txt
%{_firefoxdir}/chrome/chromelist.txt
%{_firefoxdir}/chrome/installed-chrome.txt
%{_firefoxdir}/dependentlibs.list

# files created by regxpcom and firefox -register
%ghost %{_firefoxdir}/components/compreg.dat
%ghost %{_firefoxdir}/components/xpti.dat

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/regxpcom
%attr(755,root,root) %{_bindir}/xpidl
%attr(755,root,root) %{_bindir}/xpt_dump
%attr(755,root,root) %{_bindir}/xpt_link
%{_includedir}/%{name}
%{_pkgconfigdir}/*

%files lang-en
%defattr(644,root,root,755)
%{_firefoxdir}/chrome/en-US.jar
%{_firefoxdir}/chrome/en-US.manifest
# probably should share these with all mozilla apps
%{_firefoxdir}/dictionaries/en-US.aff
%{_firefoxdir}/dictionaries/en-US.dic
