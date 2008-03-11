# TODO:
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
%define		subver	b4
%define		rel		0.1

Summary:	Firefox Community Edition web browser
Summary(pl.UTF-8):	Firefox Community Edition - przeglądarka WWW
Name:		mozilla-firefox
Version:	%{ver}
Release:	0.%{subver}.%{rel}
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Networking
#Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}%{subver}/source/firefox-%{version}%{subver}-source.tar.bz2
Source0:	firefox-%{version}%{subver}-20080310-source.tar.bz2
# Source0-md5:	016763e9b4f6a14c119d0be050d6198b
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch0:		%{name}-install.patch
#Patch1:	%{name}-lib_path.patch
#Patch2:	%{name}-fonts.patch
Patch3:		%{name}-agent.patch
#Patch4:	%{name}-myspell.patch
#Patch5:	%{name}-pango-cursor-position.patch
#Patch6:	%{name}-pango-ligatures.patch
#Patch7:	%{name}-pango-cursor-position-more.patch
#Patch8:	%{name}-pango-justified-range.patch
#Patch9:	%{name}-pango-printing.patch
#Patch10:	%{name}-pango-underline.patch
#Patch11:	%{name}-xft-randewidth.patch
# if ac rebuild is needed...
#PatchX: %{name}-ac.patch
URL:		http://www.mozilla.org/projects/firefox/
%{?with_gnomevfs:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.5.2
%{?with_crashreporter:BuildRequires:	curl-devel}
BuildRequires:	glib2-devel
%{?with_gnomevfs:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	gtk+2-devel >= 2:2.10
%{?with_kerberos:BuildRequires:	krb5-devel}
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
BuildRequires:	rpmbuild(macros) >= 1.356
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.1
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zip
BuildRequires:	zlib-devel >= 1.2.3
Requires(post):	mktemp >= 1.5-18
Requires:	browser-plugins >= 2.0
Requires:	cairo >= 1.5.2
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

%if "%(rpm -q --qf %{V} gcc)" >= "3.4"
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
%setup -qc -n %{name}-%{version}%{?subver}
cd mozilla
%patch0 -p1
#%patch1 -p1
#%patch2 -p1 # applied in sources
%patch3 -p1
#%patch4 -p1
#%patch5 -p1
#%patch6 -p1
#%patch7 -p1
#%patch8 -p1
#%patch9 -p0
#%patch10 -p1
#%patch11 -p1

#gmake[1]: Entering directory `/home/glen/rpm/pld/BUILD/mozilla-firefox-3.0/mozilla/obj-amd64/memory/jemalloc'
#rm -f libjemalloc.so
#ccache amd64-pld-linux-g++ -I/usr/X11R6/include -fno-rtti -fno-exceptions -Wall -Wconversion -Wpointer-arith -Woverloaded-virtual -Wsynth -Wno-ctor-dtor-privacy -Wno-non-virtual-dtor -Wcast-align -Wno-long-long -pedantic -fno-strict-aliasing -fshort-wchar -pthread -pipe  -DNDEBUG -DTRIMMED -O2 -fno-strict-aliasing -fPIC -shared -Wl,-z,defs -Wl,-h,libjemalloc.so -o libjemalloc.so  jemalloc.o     -lpthread   -Wl,-rpath-link,../../dist/bin   -ldl -lm
#jemalloc.o(.text+0x1b5c): In function `choose_arena_hard':
#jemalloc.c: undefined reference to `__tls_get_addr'
#jemalloc.o(.text+0x3cf1): In function `arena_ralloc':
#jemalloc.c: undefined reference to `__tls_get_addr'
#jemalloc.o(.text+0x4921): In function `malloc_init_hard':
#jemalloc.c: undefined reference to `__tls_get_addr'
#jemalloc.o(.text+0x4ce1): In function `malloc':
#jemalloc.c: undefined reference to `__tls_get_addr'
#jemalloc.o(.text+0x4eb7): In function `calloc':
#jemalloc.c: undefined reference to `__tls_get_addr'
#jemalloc.o(.text+0x5051):jemalloc.c: more undefined references to `__tls_get_addr' follow
#collect2: ld returned 1 exit status
#gmake[1]: *** [libjemalloc.so] Error 1
%{__sed} -i -e '/Wl,-z,defs/s,^,: #,' configure{,.in}

%build
cd mozilla
cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf

cat << 'EOF' > .mozconfig
. $topsrcdir/browser/config/mozconfig

mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/obj-%{_target_cpu}
ac_cv_visibility_pragma=no

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
ac_add_options --enable-optimize="%{rpmcflags}"
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
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-system-myspell
ac_add_options --enable-xft
ac_add_options --enable-libxul
ac_add_options --with-distribution-id=org.pld-linux
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-nss
ac_add_options --with-system-png
ac_add_options --with-system-zlib
ac_add_options --with-default-mozilla-five-home=%{_libdir}/%{name}
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

# config?
%{_libdir}/%{name}/.autoreg
%{_libdir}/%{name}/application.ini
%{_libdir}/%{name}/platform.ini
# XXX: nss
%{_libdir}/%{name}/libfreebl3.chk
%{_libdir}/%{name}/libsoftokn3.chk

%dir %{_libdir}/%{name}/components
%if 0
%{?with_gnomeui:%attr(755,root,root) %{_libdir}/%{name}/components/libimgicon.so}
%{?with_gnomevfs:%attr(755,root,root) %{_libdir}/%{name}/components/libmozgnome.so}
%{?with_gnomevfs:%attr(755,root,root) %{_libdir}/%{name}/components/libnkgnomevfs.so}
%endif
%{_libdir}/%{name}/components/FeedConverter.js
%{_libdir}/%{name}/components/FeedProcessor.js
%{_libdir}/%{name}/components/FeedWriter.js
%{_libdir}/%{name}/components/WebContentConverter.js
%{_libdir}/%{name}/components/browser.xpt
%{_libdir}/%{name}/components/fuelApplication.js
%{_libdir}/%{name}/components/jsconsole-clhandler.js
%{_libdir}/%{name}/components/libbrowsercomps.so
%{_libdir}/%{name}/components/libbrowserdirprovider.so
%{_libdir}/%{name}/components/libdbusservice.so
%{_libdir}/%{name}/components/libimgicon.so
%{_libdir}/%{name}/components/libmozgnome.so
%{_libdir}/%{name}/components/libnkgnomevfs.so
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
%if 0
%{?with_gnomeui:%{_libdir}/%{name}/components/imgicon.xpt}
%endif
%{_libdir}/%{name}/components/nsBrowserContentHandler.js
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%attr(755,root,root) %{_libdir}/%{name}/*.sh
%attr(755,root,root) %{_libdir}/%{name}/mozilla-xremote-client
%attr(755,root,root) %{_libdir}/%{name}/firefox
%attr(755,root,root) %{_libdir}/%{name}/firefox-bin
#%attr(755,root,root) %{_libdir}/%{name}/regxpcom
#%attr(755,root,root) %{_libdir}/%{name}/xpcshell
#%attr(755,root,root) %{_libdir}/%{name}/xpicleanup
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

#%{_libdir}/%{name}/LICENSE
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
