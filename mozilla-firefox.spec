# TODO:
# - handle locales differently (runtime, since it's possible to do)
# - see ftp://ftp.debian.org/debian/pool/main/m/mozilla-firefox/*diff*
#   for hints how to make locales
# - make it more pld-like (bookmarks, default page etc..)
#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
Summary:	Firefox Community Edition web browser
Summary(pl.UTF-8):	Firefox Community Edition - przeglądarka WWW
Name:		mozilla-firefox
Version:	2.0.0.3
Release:	1
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}-source.tar.bz2
# Source0-md5:	24398e3d98673a2a92a01a8f771ca12a
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch0:		mozilla-install.patch
Patch1:		%{name}-lib_path.patch
Patch3:		%{name}-nopangoxft.patch
Patch5:		%{name}-fonts.patch
Patch69:	%{name}-agent.patch
# drop as soon as bug is fixed since it's so ugly hack
# fixing symptoms only
# https://bugzilla.mozilla.org/show_bug.cgi?id=362462
Patch6:		mozilla-hack-gcc_4_2.patch
Patch7:		%{name}-myspell.patch
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
BuildRequires:	myspell-devel
BuildRequires:	nspr-devel >= 1:4.6.3
BuildRequires:	nss-devel >= 1:3.11.3-3
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.356
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
Requires:	browser-plugins >= 2.0
Requires:	nspr >= 1:4.6.3
Requires:	nss >= 1:3.11.3
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# mozilla and firefox provide their own versions
%define		_noautoreqdep		libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so libxpcom_core.so
%define		_noautoprovfiles	%{_libdir}/%{name}/components
# we don't want these to satisfy xulrunner-devel
%define		_noautoprov			libmozjs.so libxpcom.so libxul.so
# and as we don't provide them, don't require either
%define		_noautoreq			libmozjs.so libxpcom.so libxul.so

%define		specflags	-fno-strict-aliasing -fno-tree-vrp -fno-stack-protector

%description
Firefox Community Edition is an open-source web browser, designed for
standards compliance, performance and portability.

%description -l pl.UTF-8
Firefox Community Edition jest przeglądarką sieci WWW rozpowszechnianą
zgodnie z ideami ruchu otwartego oprogramowania oraz tworzoną z myślą
o zgodności ze standardami, wydajnością i przenośnością.

%package libs
Summary:	Firefox Community Edition shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone przeglądarki Firefox Community Edition
Group:		Libraries
Conflicts:	mozilla-firefox < 2.0-1.4

%description libs
Firefox Community Edition shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone przeglądarki Firefox Community Edition.

%package lang-en
Summary:	English resources for Firefox Community Edition
Summary(pl.UTF-8):	Anglojęzyczne zasoby dla przeglądarki Firefox Community Edition
Group:		X11/Applications/Networking
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-lang-resources = %{version}-%{release}

%description lang-en
English resources for Firefox Community Edition.

%description lang-en -l pl.UTF-8
Anglojęzyczne zasoby dla przeglądarki Firefox Community Edition.

%prep
%setup -qc
cd mozilla
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch5 -p1
%patch6 -p2
%patch7 -p1
%patch69 -p1

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
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-system-myspell
ac_add_options --enable-xft
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-zlib
ac_add_options --with-system-jpeg
ac_add_options --with-system-png
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
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
	$RPM_BUILD_ROOT%{_datadir}/%{name}

%browser_plugins_add_browser %{name} -p %{_libdir}/%{name}/plugins

%{__make} -C xpinstall/packager stage-package \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_APPDIR=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs $RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/init.d $RPM_BUILD_ROOT%{_datadir}/%{name}/init.d
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins $RPM_BUILD_ROOT%{_datadir}/%{name}/searchplugins
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/extensions $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions
ln -s ../../share/%{name}/greprefs $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/init.d $RPM_BUILD_ROOT%{_libdir}/%{name}/init.d
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res
ln -s ../../share/%{name}/searchplugins $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins

rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

sed 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox
ln -s mozilla-firefox $RPM_BUILD_ROOT%{_bindir}/firefox

install browser/base/branding/icon64.png $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-firefox.png

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# header/development files
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/xpidl
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/xpt_dump
rm $RPM_BUILD_ROOT%{_libdir}/%{name}/xpt_link

# files created by regxpcom and firefox -register
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/xpti.dat

# what's this? it's content is invalid anyway.
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/dependentlibs.list

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate
#!/bin/sh
umask 022
rm -f %{_libdir}/%{name}/components/{compreg,xpti}.dat

# it attempts to touch files in $HOME/.mozilla
# beware if you run this with sudo!!!
export HOME=$(mktemp -d)
# also TMPDIR could be pointing to sudo user's homedir
unset TMPDIR TMP || :

LD_LIBRARY_PATH=%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH} %{_libdir}/%{name}/regxpcom
%{_libdir}/%{name}/firefox -register

rm -rf $HOME
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -d %{_libdir}/%{name}/dictionaries ] && [ ! -L %{_libdir}/%{name}/dictionaries ]; then
	mv -v %{_libdir}/%{name}/dictionaries{,.rpmsave}
fi
for d in chrome defaults extensions greprefs icons init.d res searchplugins; do
	if [ -d %{_libdir}/%{name}/$d ] && [ ! -L %{_libdir}/%{name}/$d ]; then
		install -d %{_datadir}/%{name}
		mv %{_libdir}/%{name}/$d %{_datadir}/%{name}/$d
	fi
done
exit 0

%post
%{_sbindir}/%{name}-chrome+xpcom-generate
%update_browser_plugins

%postun
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/firefox
%attr(755,root,root) %{_sbindir}/%{name}-chrome+xpcom-generate

# browser plugins v2
%{_browserpluginsconfdir}/browsers.d/%{name}.*
%config(noreplace) %verify(not md5 mtime size) %{_browserpluginsconfdir}/blacklist.d/%{name}.*.blacklist

%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/*.so
%{_libdir}/%{name}/components/*.js
%{_libdir}/%{name}/components/*.xpt
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/m*
%attr(755,root,root) %{_libdir}/%{name}/f*
%attr(755,root,root) %{_libdir}/%{name}/regxpcom
%attr(755,root,root) %{_libdir}/%{name}/xpcshell
%attr(755,root,root) %{_libdir}/%{name}/xpicleanup
%{_pixmapsdir}/mozilla-firefox.png
%{_desktopdir}/mozilla-firefox.desktop

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/extensions
%{_libdir}/%{name}/greprefs
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/init.d
%{_libdir}/%{name}/res
%{_libdir}/%{name}/searchplugins

# browserconfig
%{_libdir}/%{name}/browserconfig.properties

%{_libdir}/%{name}/LICENSE
%{_libdir}/%{name}/README.txt

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/greprefs
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/init.d
%{_datadir}/%{name}/res
%{_datadir}/%{name}/searchplugins

%dir %{_datadir}/%{name}/extensions
# -dom-inspector subpackage?
%{_datadir}/%{name}/extensions/inspector@mozilla.org
# the signature of the default theme
%{_datadir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

# files created by regxpcom and firefox -register
%ghost %{_libdir}/%{name}/components/compreg.dat
%ghost %{_libdir}/%{name}/components/xpti.dat

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so

%files lang-en
%defattr(644,root,root,755)
%{_datadir}/%{name}/chrome/en-US.jar
%{_datadir}/%{name}/chrome/en-US.manifest
