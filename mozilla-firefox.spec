# TODO:
# - handle locales differently (runtime, since it's possible to do)
# - see ftp://ftp.debian.org/debian/pool/main/m/mozilla-firefox/*diff*
#   for hints how to make locales
# - make it more pld-like (bookmarks, default page etc..)
# - add dictionaries outside of mozilla
#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
Summary:	Mozilla Firefox web browser
Summary(pl):	Mozilla Firefox - przegl±darka WWW
Name:		mozilla-firefox
Version:	2.0
Release:	2
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}-source.tar.bz2
# Source0-md5:	03709c15cba0e0375ff5336d538f77e7
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch1:		%{name}-lib_path.patch
Patch3:		%{name}-nopangoxft.patch
Patch5:		%{name}-fonts.patch
# if ac rebuild is needed...
#PatchX:		%{name}-ac.patch
URL:		http://www.mozilla.org/projects/firefox/
%{?with_gnome:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0.0
%{?with_gnome:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	heimdal-devel >= 0.7.1
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
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	nspr >= 1:4.6.3
Requires:	nss >= 1:3.11.3
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/%{name}
# mozilla and firefox provide their own versions
%define		_noautoreqdep		libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so libxpcom_core.so
%define		_noautoprovfiles	%{_firefoxdir}/components

%define		specflags	-fno-strict-aliasing

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l pl
Mozilla Firefox jest open sourcow± przegl±dark± sieci WWW, stworzon± z
my¶l± o zgodno¶ci ze standardami, wydajno¶ci± i przeno¶no¶ci±.

%package libs
Summary:	Mozilla Firefox shared libraries
Summary(pl):	Biblioteki wspó³dzielone Mozilla Firefox
Group:		Libraries
Conflicts:	%{name} < 2.0-1.4

%description libs
Mozilla Firefox shared libraries.

%package devel
Summary:	Headers for developing programs that will use Mozilla Firefox
Summary(pl):	Mozilla Firefox - pliki nag³ówkowe
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
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
%patch1 -p1
%patch3 -p1
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

cat << 'EOF' > .mozconfig
. $topsrcdir/browser/config/mozconfig

# Options for 'configure' (same as command-line options).
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
ac_add_options --disable-optimize
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
ac_add_options --enable-debugger-info-modules
ac_add_options --enable-crash-on-assert
%else
ac_add_options --disable-debug
ac_add_options --disable-logging
ac_add_options --enable-optimize="%{rpmcflags}"
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
ac_add_options --disable-freetype2
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-system-cairo
ac_add_options --enable-xft
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-zlib
ac_add_options --with-system-jpeg
ac_add_options --with-system-png
ac_add_options --with-default-mozilla-five-home=%{_firefoxdir}
ac_cv_visibility_pragma=no
EOF

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

install browser/base/branding/icon64.png $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-firefox.png
#install -m644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/
#install -m644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/US/

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

# header/developement files
cp -rfL dist/include	$RPM_BUILD_ROOT%{_includedir}/%{name}
cp -rfL dist/idl	$RPM_BUILD_ROOT%{_includedir}/%{name}
ln -sf necko/nsIURI.h $RPM_BUILD_ROOT%{_includedir}/mozilla-firefox/nsIURI.h
install dist/bin/regxpcom $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT{%{_firefoxdir},%{_bindir}}/xpidl
mv $RPM_BUILD_ROOT{%{_firefoxdir},%{_bindir}}/xpt_dump
mv $RPM_BUILD_ROOT{%{_firefoxdir},%{_bindir}}/xpt_link

# pkgconfig files
for f in build/unix/*.pc; do
	sed -e 's/firefox-%{version}/mozilla-firefox/' $f > $RPM_BUILD_ROOT%{_pkgconfigdir}/${f##*/}
done

# already provided by standalone packages
rm $RPM_BUILD_ROOT%{_pkgconfigdir}/firefox-{nss,nspr}.pc

sed -i -e 's#firefox-nspr =.*#mozilla-nspr#g' -e 's#irefox-nss =.*#mozilla-nss#g' \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# includedir/dom CFLAGS
sed -i -e '/Cflags:/{/{includedir}\/dom/!s,$, -I${includedir}/dom,}' \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/firefox-plugin.pc

# files created by regxpcom and firefox -register
touch $RPM_BUILD_ROOT%{_firefoxdir}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_firefoxdir}/components/xpti.dat

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate
#!/bin/sh
umask 022
rm -f %{_firefoxdir}/components/{compreg,xpti}.dat

# it attempts to touch files in $HOME/.mozilla
# beware if you run this with sudo!!!
export HOME=$(mktemp -d)
# also TMPDIR could be pointing to sudo user's homedir
unset TMPDIR TMP || :

LD_LIBRARY_PATH=%{_firefoxdir}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH} %{_firefoxdir}/regxpcom
%{_firefoxdir}/firefox -register

rm -rf $HOME
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/%{name}-chrome+xpcom-generate

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/firefox
%attr(755,root,root) %{_sbindir}/%{name}-chrome+xpcom-generate

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
%dir %{_firefoxdir}/dictionaries
%dir %{_firefoxdir}/init.d
%{_firefoxdir}/init.d/README
%attr(755,root,root) %{_firefoxdir}/*.sh
%attr(755,root,root) %{_firefoxdir}/m*
%attr(755,root,root) %{_firefoxdir}/f*
%attr(755,root,root) %{_firefoxdir}/regxpcom
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

# the signature of the default theme
%dir %{_firefoxdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}
%{_firefoxdir}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}/install.rdf

# browserconfig
%{_firefoxdir}/browserconfig.properties

%{_firefoxdir}/LICENSE
%{_firefoxdir}/README.txt
%{_firefoxdir}/chrome/chromelist.txt
%{_firefoxdir}/dependentlibs.list

# files created by regxpcom and firefox -register
%ghost %{_firefoxdir}/components/compreg.dat
%ghost %{_firefoxdir}/components/xpti.dat

%files libs
%defattr(644,root,root,755)
%dir %{_firefoxdir}
%attr(755,root,root) %{_firefoxdir}/*.so

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
