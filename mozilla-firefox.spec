# TODO:
# - crashreporter does not seem to be built on ac nor th
# - handle locales differently (runtime, since it's possible to do)
# - see ftp://ftp.debian.org/debian/pool/main/m/mozilla-firefox/*diff*
#   for hints how to make locales
# - make it more pld-like (bookmarks, default page etc..)
# - system nss, xulrunner
#
# Conditional build:
%bcond_with	tests		# enable tests (whatever they check)
%bcond_without	crashreporter	# disable crash reporter
%bcond_without	gnomeui		# disable gnomeui support
%bcond_without	gnomevfs	# disable GNOME comp. (gconf+libgnome+gnomevfs) and gnomevfs ext.
%bcond_without	gnome		# disable all GNOME components (gnome+gnomeui+gnomevfs)
%bcond_without	kerberos	# disable krb5 support

%if %{without gnome}
%undefine	with_gnomeui
%undefine	with_gnomevfs
%endif

%define		ver		3.0

Summary:	Firefox Community Edition web browser
Summary(pl.UTF-8):	Firefox Community Edition - przeglądarka WWW
Name:		mozilla-firefox
Version:	%{ver}
Release:	1.1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Networking
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}-source.tar.bz2
# Source0-md5:	4210ae0801df2eb498408533010d97c1
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch0:		%{name}-install.patch
Patch1:		%{name}-agent.patch
Patch2:		%{name}-agent-ac.patch
Patch3:		%{name}-gcc3.patch
URL:		http://www.mozilla.org/projects/firefox/
%{?with_gnomevfs:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.6.0
%{?with_crashreporter:BuildRequires:	curl-devel}
BuildRequires:	glib2-devel
%{?with_gnomevfs:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	gtk+2-devel >= 2:2.10
%if "%{pld_release}" == "ac"
%{?with_kerberos:BuildRequires:	heimdal-devel >= 0.7.1}
%else
%{?with_kerberos:BuildRequires:	krb5-devel}
%endif
BuildRequires:	libIDL-devel >= 0.8.0
%{?with_gnomevfs:BuildRequires:	libgnome-devel >= 2.0}
%{?with_gnomeui:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng(APNG)-devel >= 0.10
BuildRequires:	libpng-devel >= 1.2.7
BuildRequires:	libstdc++-devel
BuildRequires:	myspell-devel
BuildRequires:	nspr-devel >= 1:4.7
BuildRequires:	nss-devel >= 1:3.11.3-3
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	startup-notification-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires(post):	mktemp >= 1.5-18
Requires:	browser-plugins >= 2.0
Requires:	cairo >= 1.6.0
Requires:	libpng(APNG) >= 0.10
Requires:	nspr >= 1:4.7
Requires:	nss >= 1:3.11.3-3
Provides:	wwwbrowser
Obsoletes:	mozilla-firebird
Obsoletes:	mozilla-firefox-lang-en < 2.0.0.8-3
Obsoletes:	mozilla-firefox-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# firefox/thunderbird/seamonkey provide their own versions
%define		_noautoreqdep		libgkgfx.so libgtkxtbin.so libjsj.so libxpcom_compat.so libxpcom_core.so
%define		_noautoprovfiles	%{_libdir}/%{name}/components
# we don't want these to satisfy xulrunner-devel
%define		_noautoprov		libgtkembedmoz.so libmozjs.so libxpcom.so libxul.so
# and as we don't provide them, don't require either
%define		_noautoreq		libgtkembedmoz.so libmozjs.so libxpcom.so libxul.so

%if "%{cc_version}" >= "3.4"
%define		specflags	-fno-strict-aliasing -fno-tree-vrp -fno-stack-protector
%else
%define		specflags	-fno-strict-aliasing
%endif

%description
Firefox Community Edition is an open-source web browser, designed for
standards compliance, performance and portability.

%description -l pl.UTF-8
Firefox Community Edition jest przeglądarką WWW rozpowszechnianą
zgodnie z ideami ruchu otwartego oprogramowania oraz tworzoną z myślą
o zgodności ze standardami, wydajnością i przenośnością.

%prep
%setup -qc -n %{name}-%{version}
cd mozilla
%patch0 -p1
%if "%{pld_release}" == "ac"
%patch2 -p1
%else
%patch1 -p1
%endif
%if "%{cc_version}" < "3.4"
%patch3 -p2
%endif

%build
cd mozilla
cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf

cat << 'EOF' > .mozconfig
. $topsrcdir/browser/config/mozconfig

mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-%{_target_cpu}

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
ac_add_options --disable-debug-modules
ac_add_options --disable-logging
ac_add_options --enable-optimize="%{rpmcflags} -Os"
%endif
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
%if %{with gnomeui}
ac_add_options --enable-gnomeui
%else
ac_add_options --disable-gnomeui
%endif
%if %{with gnomevfs}
ac_add_options --enable-gnomevfs
%else
ac_add_options --disable-gnomevfs
%endif
%{!?with_crashreporter:ac_add_options --disable-crashreporter}
ac_add_options --disable-freetype2
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
ac_add_options --disable-strip
ac_add_options --disable-xprint
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --enable-startup-notification
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-system-myspell
ac_add_options --enable-xft
ac_add_options --enable-libxul
ac_add_options --enable-xinerama
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-pthreads
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
EOF

%{__make} -j1 -f client.mk build \
	STRIP="/bin/true" \
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

%{__make} -C obj-%{_target_cpu}/browser/installer stage-package \
	DESTDIR=$RPM_BUILD_ROOT \
	MOZ_PKG_APPDIR=%{_libdir}/%{name} \
	PKG_SKIP_STRIP=1

# move arch independant ones to datadir
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome $RPM_BUILD_ROOT%{_datadir}/%{name}/chrome
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults $RPM_BUILD_ROOT%{_datadir}/%{name}/defaults
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions $RPM_BUILD_ROOT%{_datadir}/%{name}/extensions
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs $RPM_BUILD_ROOT%{_datadir}/%{name}/greprefs
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/icons $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/modules $RPM_BUILD_ROOT%{_datadir}/%{name}/modules
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/res $RPM_BUILD_ROOT%{_datadir}/%{name}/res
mv $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins $RPM_BUILD_ROOT%{_datadir}/%{name}/searchplugins
ln -s ../../share/%{name}/chrome $RPM_BUILD_ROOT%{_libdir}/%{name}/chrome
ln -s ../../share/%{name}/defaults $RPM_BUILD_ROOT%{_libdir}/%{name}/defaults
ln -s ../../share/%{name}/extensions $RPM_BUILD_ROOT%{_libdir}/%{name}/extensions
ln -s ../../share/%{name}/greprefs $RPM_BUILD_ROOT%{_libdir}/%{name}/greprefs
ln -s ../../share/%{name}/modules $RPM_BUILD_ROOT%{_libdir}/%{name}/modules
ln -s ../../share/%{name}/icons $RPM_BUILD_ROOT%{_libdir}/%{name}/icons
ln -s ../../share/%{name}/res $RPM_BUILD_ROOT%{_libdir}/%{name}/res
ln -s ../../share/%{name}/searchplugins $RPM_BUILD_ROOT%{_libdir}/%{name}/searchplugins

rm -rf $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries
ln -s %{_datadir}/myspell $RPM_BUILD_ROOT%{_libdir}/%{name}/dictionaries

sed 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox
ln -s mozilla-firefox $RPM_BUILD_ROOT%{_bindir}/firefox

install browser/base/branding/icon64.png $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-firefox.png

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

# files created by regxpcom and firefox -register
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/compreg.dat
touch $RPM_BUILD_ROOT%{_libdir}/%{name}/components/xpti.dat

# what's this? it's content is invalid anyway.
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/dependentlibs.list
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/old-homepage-default.properties

cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/%{name}-chrome+xpcom-generate
#!/bin/sh
umask 022
rm -f %{_libdir}/%{name}/components/{compreg,xpti}.dat

# it attempts to touch files in $HOME/.mozilla
# beware if you run this with sudo!!!
export HOME=$(mktemp -d)
# also TMPDIR could be pointing to sudo user's homedir
unset TMPDIR TMP || :

#LD_LIBRARY_PATH=%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH} %{_libdir}/%{name}/regxpcom
%{_libdir}/%{name}/firefox -register

rm -rf $HOME
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
if [ -d %{_libdir}/%{name}/dictionaries ] && [ ! -L %{_libdir}/%{name}/dictionaries ]; then
	mv -v %{_libdir}/%{name}/dictionaries{,.rpmsave}
fi
for d in chrome defaults extensions greprefs icons res searchplugins; do
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

%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so
%{_libdir}/%{name}/blocklist.xml

%if %{with crashreporter}
%{_libdir}/%{name}/crashreporter
%{_libdir}/%{name}/crashreporter-override.ini
%{_libdir}/%{name}/crashreporter.ini
%{_libdir}/%{name}/Throbber-small.gif
%endif

# config?
%{_libdir}/%{name}/.autoreg
%{_libdir}/%{name}/application.ini
%{_libdir}/%{name}/platform.ini
# XXX: nss
%{_libdir}/%{name}/libfreebl3.chk
%{_libdir}/%{name}/libsoftokn3.chk

%dir %{_libdir}/%{name}/components

%{_libdir}/%{name}/components/aboutRobots.js
%{_libdir}/%{name}/components/FeedConverter.js
%{_libdir}/%{name}/components/FeedProcessor.js
%{_libdir}/%{name}/components/FeedWriter.js
%{_libdir}/%{name}/components/WebContentConverter.js
%{_libdir}/%{name}/components/browser.xpt
%{_libdir}/%{name}/components/fuelApplication.js
%{_libdir}/%{name}/components/jsconsole-clhandler.js
%{_libdir}/%{name}/components/nsAddonRepository.js
%{_libdir}/%{name}/components/nsBlocklistService.js
%{_libdir}/%{name}/components/nsBrowserGlue.js
%{_libdir}/%{name}/components/nsContentDispatchChooser.js
%{_libdir}/%{name}/components/nsContentPrefService.js
%{_libdir}/%{name}/components/nsDefaultCLH.js
%{_libdir}/%{name}/components/nsDownloadManagerUI.js
%{_libdir}/%{name}/components/nsExtensionManager.js
%{_libdir}/%{name}/components/nsFilePicker.js
%{_libdir}/%{name}/components/nsHandlerService.js
%{_libdir}/%{name}/components/nsHelperAppDlg.js
%{_libdir}/%{name}/components/nsLivemarkService.js
%{_libdir}/%{name}/components/nsLoginInfo.js
%{_libdir}/%{name}/components/nsLoginManager.js
%{_libdir}/%{name}/components/nsLoginManagerPrompter.js
%{_libdir}/%{name}/components/nsMicrosummaryService.js
%{_libdir}/%{name}/components/nsPlacesTransactionsService.js
%{_libdir}/%{name}/components/nsProxyAutoConfig.js
%{_libdir}/%{name}/components/nsSafebrowsingApplication.js
%{_libdir}/%{name}/components/nsSearchService.js
%{_libdir}/%{name}/components/nsSearchSuggestions.js
%{_libdir}/%{name}/components/nsSessionStartup.js
%{_libdir}/%{name}/components/nsSessionStore.js
%{_libdir}/%{name}/components/nsSetDefaultBrowser.js
%{_libdir}/%{name}/components/nsSidebar.js
%{_libdir}/%{name}/components/nsTaggingService.js
%{_libdir}/%{name}/components/nsTryToClose.js
%{_libdir}/%{name}/components/nsURLFormatter.js
%{_libdir}/%{name}/components/nsUpdateService.js
%{_libdir}/%{name}/components/nsUrlClassifierLib.js
%{_libdir}/%{name}/components/nsUrlClassifierListManager.js
%{_libdir}/%{name}/components/nsWebHandlerApp.js
%{_libdir}/%{name}/components/pluginGlue.js
%{_libdir}/%{name}/components/storage-Legacy.js
%{_libdir}/%{name}/components/txEXSLTRegExFunctions.js
%{_libdir}/%{name}/components/nsBrowserContentHandler.js

%attr(755,root,root) %{_libdir}/%{name}/components/libbrowsercomps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libbrowserdirprovider.so
%attr(755,root,root) %{_libdir}/%{name}/components/libdbusservice.so
%attr(755,root,root) %{_libdir}/%{name}/components/libimgicon.so

%if %{with gnomevfs}
%attr(755,root,root) %{_libdir}/%{name}/components/libmozgnome.so
%attr(755,root,root) %{_libdir}/%{name}/components/libnkgnomevfs.so
%endif

%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/firefox
%attr(755,root,root) %{_libdir}/%{name}/firefox-bin
%{_pixmapsdir}/mozilla-firefox.png
%{_desktopdir}/mozilla-firefox.desktop

# symlinks
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/defaults
%{_libdir}/%{name}/dictionaries
%{_libdir}/%{name}/extensions
%{_libdir}/%{name}/greprefs
%{_libdir}/%{name}/icons
%{_libdir}/%{name}/modules
%{_libdir}/%{name}/res
%{_libdir}/%{name}/searchplugins

# browserconfig
%{_libdir}/%{name}/browserconfig.properties

%{_libdir}/%{name}/README.txt

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/chrome
%{_datadir}/%{name}/defaults
%{_datadir}/%{name}/greprefs
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/modules
%{_datadir}/%{name}/res
%{_datadir}/%{name}/searchplugins

%dir %{_datadir}/%{name}/extensions
# -dom-inspector subpackage?
#%{_datadir}/%{name}/extensions/inspector@mozilla.org
# the signature of the default theme
%{_datadir}/%{name}/extensions/{972ce4c6-7e08-4474-a285-3208198ce6fd}

# files created by regxpcom and firefox -register
%ghost %{_libdir}/%{name}/components/compreg.dat
%ghost %{_libdir}/%{name}/components/xpti.dat
