# TODO:
# - handle locales differently (runtime, since it's possible to do)
# - see ftp://ftp.debian.org/debian/pool/main/m/mozilla-firefox/*diff*
#   for hints how to make locales
# - make it more pld-like (bookmarks, default page etc..)
#
# Conditional build:
%bcond_with	tests		# enable tests (whatever they check)
%bcond_without	gnomeui		# disable gnomeui support
%bcond_without	gnomevfs	# disable GNOME comp. (gconf+libgnome+gnomevfs) and gnomevfs ext.
%bcond_without	gnome		# disable all GNOME components (gnome+gnomeui+gnomevfs)
%bcond_without	kerberos	# disable krb5 support

%if %{without gnome}
%undefine	with_gnomeui
%undefine	with_gnomevfs
%endif

%define		ver		3.0
%define		subver	b3
%define		rel		0.1

Summary:	Firefox Community Edition web browser
Summary(pl.UTF-8):	Firefox Community Edition - przeglądarka WWW
Name:		mozilla-firefox
Version:	%{ver}
Release:	0.%{subver}.%{rel}
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		X11/Applications/Networking
Source0:	ftp://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}%{subver}/source/firefox-%{version}%{subver}-source.tar.bz2
# Source0-md5:	949cfbb596b786ba5a9f9ad6604e2849
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch0:		mozilla-install.patch
#Patch1:		%{name}-lib_path.patch
#Patch2:		%{name}-fonts.patch
Patch3:		%{name}-agent.patch
#Patch4:		%{name}-myspell.patch
#Patch5:		%{name}-pango-cursor-position.patch
#Patch6:		%{name}-pango-ligatures.patch
#Patch7:		%{name}-pango-cursor-position-more.patch
#Patch8:		%{name}-pango-justified-range.patch
#Patch9:		%{name}-pango-printing.patch
#Patch10:	%{name}-pango-underline.patch
#Patch11:	%{name}-xft-randewidth.patch
Patch12:	%{name}-414239.patch
# if ac rebuild is needed...
#PatchX:		%{name}-ac.patch
URL:		http://www.mozilla.org/projects/firefox/
%{?with_gnomevfs:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.5.2
%{?with_gnomevfs:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	gtk+2-devel >= 1:2.10
BuildRequires:	glib2-devel
%{?with_kerberos:BuildRequires:	krb5-devel}
BuildRequires:	libIDL-devel >= 0.8.0
%{?with_gnomevfs:BuildRequires:	libgnome-devel >= 2.0}
%{?with_gnomeui:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.7
BuildRequires:	libpng(APNG)-devel >= 0.10
BuildRequires:	libstdc++-devel
BuildRequires:	myspell-devel
BuildRequires:	nspr-devel >= 1:4.6.7
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
Requires:	nspr >= 1:4.6.7
Requires:	nss >= 1:3.11.3
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

%define		specflags	-fno-strict-aliasing -fno-tree-vrp -fno-stack-protector

%description
Firefox Community Edition is an open-source web browser, designed for
standards compliance, performance and portability.

%description -l pl.UTF-8
Firefox Community Edition jest przeglądarką WWW rozpowszechnianą
zgodnie z ideami ruchu otwartego oprogramowania oraz tworzoną z myślą
o zgodności ze standardami, wydajnością i przenośnością.

%prep
%setup -qc
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
%patch12 -p0

%build
cd mozilla

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
#cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf

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
ac_add_options --disable-freetype2
ac_add_options --disable-installer
ac_add_options --disable-javaxpcom
ac_add_options --disable-updater
ac_add_options --enable-default-toolkit=cairo-gtk2
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-system-myspell
ac_add_options --enable-xft
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

%{__make} -C obj-%{_target_cpu}/xpinstall/packager stage-package \
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

LD_LIBRARY_PATH=%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH} %{_libdir}/%{name}/regxpcom
%{_libdir}/%{name}/firefox -register

rm -rf $HOME
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
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

%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.so

%dir %{_libdir}/%{name}/components
%attr(755,root,root) %{_libdir}/%{name}/components/libaccessibility.so
%attr(755,root,root) %{_libdir}/%{name}/components/libappcomps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libauth.so
%attr(755,root,root) %{_libdir}/%{name}/components/libautoconfig.so
%attr(755,root,root) %{_libdir}/%{name}/components/libbrowsercomps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libbrowserdirprovider.so
%attr(755,root,root) %{_libdir}/%{name}/components/libcaps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libchrome.so
%attr(755,root,root) %{_libdir}/%{name}/components/libcommandlines.so
%attr(755,root,root) %{_libdir}/%{name}/components/libcomposer.so
%attr(755,root,root) %{_libdir}/%{name}/components/libcookie.so
%attr(755,root,root) %{_libdir}/%{name}/components/libdocshell.so
%attr(755,root,root) %{_libdir}/%{name}/components/libeditor.so
%attr(755,root,root) %{_libdir}/%{name}/components/libembedcomponents.so
%attr(755,root,root) %{_libdir}/%{name}/components/libfileview.so
%attr(755,root,root) %{_libdir}/%{name}/components/libgfx_gtk.so
%attr(755,root,root) %{_libdir}/%{name}/components/libgfxps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libgklayout.so
%attr(755,root,root) %{_libdir}/%{name}/components/libgkplugin.so
%attr(755,root,root) %{_libdir}/%{name}/components/libhtmlpars.so
%attr(755,root,root) %{_libdir}/%{name}/components/libi18n.so
%{?with_gnomeui:%attr(755,root,root) %{_libdir}/%{name}/components/libimgicon.so}
%attr(755,root,root) %{_libdir}/%{name}/components/libimglib2.so
%attr(755,root,root) %{_libdir}/%{name}/components/libjar50.so
%attr(755,root,root) %{_libdir}/%{name}/components/libjsd.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmork.so
%attr(755,root,root) %{_libdir}/%{name}/components/libmozfind.so
%{?with_gnomevfs:%attr(755,root,root) %{_libdir}/%{name}/components/libmozgnome.so}
%attr(755,root,root) %{_libdir}/%{name}/components/libmyspell.so
%attr(755,root,root) %{_libdir}/%{name}/components/libnecko2.so
%attr(755,root,root) %{_libdir}/%{name}/components/libnecko.so
%{?with_gnomevfs:%attr(755,root,root) %{_libdir}/%{name}/components/libnkgnomevfs.so}
%attr(755,root,root) %{_libdir}/%{name}/components/libnsappshell.so
%attr(755,root,root) %{_libdir}/%{name}/components/liboji.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpermissions.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpipboot.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpipnss.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpippki.so
%attr(755,root,root) %{_libdir}/%{name}/components/libpref.so
%attr(755,root,root) %{_libdir}/%{name}/components/librdf.so
%attr(755,root,root) %{_libdir}/%{name}/components/libremoteservice.so
%attr(755,root,root) %{_libdir}/%{name}/components/libsearchservice.so
%attr(755,root,root) %{_libdir}/%{name}/components/libspellchecker.so
%attr(755,root,root) %{_libdir}/%{name}/components/libstoragecomps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libsystem-pref.so
%attr(755,root,root) %{_libdir}/%{name}/components/libtoolkitcomps.so
%attr(755,root,root) %{_libdir}/%{name}/components/libtransformiix.so
%attr(755,root,root) %{_libdir}/%{name}/components/libtxmgr.so
%attr(755,root,root) %{_libdir}/%{name}/components/libuconv.so
%attr(755,root,root) %{_libdir}/%{name}/components/libucvmath.so
%attr(755,root,root) %{_libdir}/%{name}/components/libuniversalchardet.so
%attr(755,root,root) %{_libdir}/%{name}/components/libwebbrwsr.so
%attr(755,root,root) %{_libdir}/%{name}/components/libwebsrvcs.so
%attr(755,root,root) %{_libdir}/%{name}/components/libwidget_gtk2.so
%attr(755,root,root) %{_libdir}/%{name}/components/libxmlextras.so
%attr(755,root,root) %{_libdir}/%{name}/components/libxpcom_compat_c.so
%attr(755,root,root) %{_libdir}/%{name}/components/libxpconnect.so
%attr(755,root,root) %{_libdir}/%{name}/components/libxpinstall.so
%{_libdir}/%{name}/components/accessibility-atk.xpt
%{_libdir}/%{name}/components/accessibility.xpt
%{_libdir}/%{name}/components/alerts.xpt
%{_libdir}/%{name}/components/appshell.xpt
%{_libdir}/%{name}/components/appstartup.xpt
%{_libdir}/%{name}/components/autocomplete.xpt
%{_libdir}/%{name}/components/autoconfig.xpt
%{_libdir}/%{name}/components/bookmarks.xpt
%{_libdir}/%{name}/components/browsercompsbase.xpt
%{_libdir}/%{name}/components/browser-feeds.xpt
%{_libdir}/%{name}/components/browsersearch.xpt
%{_libdir}/%{name}/components/caps.xpt
%{_libdir}/%{name}/components/chardet.xpt
%{_libdir}/%{name}/components/chrome.xpt
%{_libdir}/%{name}/components/commandhandler.xpt
%{_libdir}/%{name}/components/commandlines.xpt
%{_libdir}/%{name}/components/composer.xpt
%{_libdir}/%{name}/components/content_base.xpt
%{_libdir}/%{name}/components/content_htmldoc.xpt
%{_libdir}/%{name}/components/content_html.xpt
%{_libdir}/%{name}/components/content_xmldoc.xpt
%{_libdir}/%{name}/components/content_xslt.xpt
%{_libdir}/%{name}/components/content_xtf.xpt
%{_libdir}/%{name}/components/cookie.xpt
%{_libdir}/%{name}/components/directory.xpt
%{_libdir}/%{name}/components/docshell.xpt
%{_libdir}/%{name}/components/dom_base.xpt
%{_libdir}/%{name}/components/dom_canvas.xpt
%{_libdir}/%{name}/components/dom_core.xpt
%{_libdir}/%{name}/components/dom_css.xpt
%{_libdir}/%{name}/components/dom_events.xpt
%{_libdir}/%{name}/components/dom_html.xpt
%{_libdir}/%{name}/components/dom_loadsave.xpt
%{_libdir}/%{name}/components/dom_range.xpt
%{_libdir}/%{name}/components/dom_sidebar.xpt
%{_libdir}/%{name}/components/dom_storage.xpt
%{_libdir}/%{name}/components/dom_stylesheets.xpt
%{_libdir}/%{name}/components/dom_svg.xpt
%{_libdir}/%{name}/components/dom_traversal.xpt
%{_libdir}/%{name}/components/dom_views.xpt
%{_libdir}/%{name}/components/dom_xbl.xpt
%{_libdir}/%{name}/components/dom_xpath.xpt
%{_libdir}/%{name}/components/dom.xpt
%{_libdir}/%{name}/components/dom_xul.xpt
%{_libdir}/%{name}/components/downloads.xpt
%{_libdir}/%{name}/components/editor.xpt
%{_libdir}/%{name}/components/embed_base.xpt
%{_libdir}/%{name}/components/extensions.xpt
%{_libdir}/%{name}/components/exthandler.xpt
%{_libdir}/%{name}/components/fastfind.xpt
%{_libdir}/%{name}/components/FeedConverter.js
%{_libdir}/%{name}/components/FeedProcessor.js
%{_libdir}/%{name}/components/feeds.xpt
%{_libdir}/%{name}/components/FeedWriter.js
%{_libdir}/%{name}/components/filepicker.xpt
%{_libdir}/%{name}/components/find.xpt
%{_libdir}/%{name}/components/gfx.xpt
%{_libdir}/%{name}/components/gksvgrenderer.xpt
%{_libdir}/%{name}/components/history.xpt
%{_libdir}/%{name}/components/htmlparser.xpt
%{?with_gnomeui:%{_libdir}/%{name}/components/imgicon.xpt}
%{_libdir}/%{name}/components/imglib2.xpt
%{_libdir}/%{name}/components/inspector.xpt
%{_libdir}/%{name}/components/intl.xpt
%{_libdir}/%{name}/components/jar.xpt
%{_libdir}/%{name}/components/jsconsole-clhandler.js
%{_libdir}/%{name}/components/jsconsole.xpt
%{_libdir}/%{name}/components/jsdservice.xpt
%{_libdir}/%{name}/components/layout_base.xpt
%{_libdir}/%{name}/components/layout_printing.xpt
%{_libdir}/%{name}/components/layout_xul_tree.xpt
%{_libdir}/%{name}/components/layout_xul.xpt
%{_libdir}/%{name}/components/locale.xpt
%{_libdir}/%{name}/components/lwbrk.xpt
%{_libdir}/%{name}/components/microsummaries.xpt
%{_libdir}/%{name}/components/migration.xpt
%{_libdir}/%{name}/components/mimetype.xpt
%{_libdir}/%{name}/components/mozbrwsr.xpt
%{_libdir}/%{name}/components/mozfind.xpt
%{_libdir}/%{name}/components/mozgnome.xpt
%{_libdir}/%{name}/components/necko_about.xpt
%{_libdir}/%{name}/components/necko_cache.xpt
%{_libdir}/%{name}/components/necko_cookie.xpt
%{_libdir}/%{name}/components/necko_data.xpt
%{_libdir}/%{name}/components/necko_dns.xpt
%{_libdir}/%{name}/components/necko_file.xpt
%{_libdir}/%{name}/components/necko_ftp.xpt
%{_libdir}/%{name}/components/necko_http.xpt
%{_libdir}/%{name}/components/necko_res.xpt
%{_libdir}/%{name}/components/necko_socket.xpt
%{_libdir}/%{name}/components/necko_strconv.xpt
%{_libdir}/%{name}/components/necko_viewsource.xpt
%{_libdir}/%{name}/components/necko.xpt
%{_libdir}/%{name}/components/nsBookmarkTransactionManager.js
%{_libdir}/%{name}/components/nsBrowserContentHandler.js
%{_libdir}/%{name}/components/nsBrowserGlue.js
%{_libdir}/%{name}/components/nsCloseAllWindows.js
%{_libdir}/%{name}/components/nsDefaultCLH.js
%{_libdir}/%{name}/components/nsDictionary.js
%{_libdir}/%{name}/components/nsExtensionManager.js
%{_libdir}/%{name}/components/nsFilePicker.js
%{_libdir}/%{name}/components/nsHelperAppDlg.js
%{_libdir}/%{name}/components/nsInterfaceInfoToIDL.js
%{_libdir}/%{name}/components/nsKillAll.js
%{_libdir}/%{name}/components/nsMicrosummaryService.js
%{_libdir}/%{name}/components/nsProgressDialog.js
%{_libdir}/%{name}/components/nsProxyAutoConfig.js
%{_libdir}/%{name}/components/nsResetPref.js
%{_libdir}/%{name}/components/nsSafebrowsingApplication.js
%{_libdir}/%{name}/components/nsSearchService.js
%{_libdir}/%{name}/components/nsSearchSuggestions.js
%{_libdir}/%{name}/components/nsSessionStartup.js
%{_libdir}/%{name}/components/nsSessionStore.js
%{_libdir}/%{name}/components/nsSetDefaultBrowser.js
%{_libdir}/%{name}/components/nsSidebar.js
%{_libdir}/%{name}/components/nsUpdateService.js
%{_libdir}/%{name}/components/nsUrlClassifierLib.js
%{_libdir}/%{name}/components/nsUrlClassifierListManager.js
%{_libdir}/%{name}/components/nsUrlClassifierTable.js
%{_libdir}/%{name}/components/nsURLFormatter.js
%{_libdir}/%{name}/components/nsXmlRpcClient.js
%{_libdir}/%{name}/components/oji.xpt
%{_libdir}/%{name}/components/passwordmgr.xpt
%{_libdir}/%{name}/components/pipboot.xpt
%{_libdir}/%{name}/components/pipnss.xpt
%{_libdir}/%{name}/components/pippki.xpt
%{_libdir}/%{name}/components/plugin.xpt
%{_libdir}/%{name}/components/prefetch.xpt
%{_libdir}/%{name}/components/pref.xpt
%{_libdir}/%{name}/components/profile.xpt
%{_libdir}/%{name}/components/progressDlg.xpt
%{_libdir}/%{name}/components/proxyObjInst.xpt
%{_libdir}/%{name}/components/rdf.xpt
%{_libdir}/%{name}/components/safebrowsing.xpt
%{_libdir}/%{name}/components/satchel.xpt
%{_libdir}/%{name}/components/saxparser.xpt
%{_libdir}/%{name}/components/search.xpt
%{_libdir}/%{name}/components/sessionstore.xpt
%{_libdir}/%{name}/components/shellservice.xpt
%{_libdir}/%{name}/components/shistory.xpt
%{_libdir}/%{name}/components/spellchecker.xpt
%{_libdir}/%{name}/components/storage.xpt
%{_libdir}/%{name}/components/toolkitprofile.xpt
%{_libdir}/%{name}/components/toolkitremote.xpt
%{_libdir}/%{name}/components/txmgr.xpt
%{_libdir}/%{name}/components/txtsvc.xpt
%{_libdir}/%{name}/components/uconv.xpt
%{_libdir}/%{name}/components/unicharutil.xpt
%{_libdir}/%{name}/components/update.xpt
%{_libdir}/%{name}/components/uriloader.xpt
%{_libdir}/%{name}/components/url-classifier.xpt
%{_libdir}/%{name}/components/urlformatter.xpt
%{_libdir}/%{name}/components/webBrowser_core.xpt
%{_libdir}/%{name}/components/webbrowserpersist.xpt
%{_libdir}/%{name}/components/WebContentConverter.js
%{_libdir}/%{name}/components/webshell_idls.xpt
%{_libdir}/%{name}/components/websrvcs.xpt
%{_libdir}/%{name}/components/widget.xpt
%{_libdir}/%{name}/components/windowds.xpt
%{_libdir}/%{name}/components/windowwatcher.xpt
%{_libdir}/%{name}/components/xml-rpc.xpt
%{_libdir}/%{name}/components/xpcom_base.xpt
%{_libdir}/%{name}/components/xpcom_components.xpt
%{_libdir}/%{name}/components/xpcom_ds.xpt
%{_libdir}/%{name}/components/xpcom_io.xpt
%{_libdir}/%{name}/components/xpcom_obsolete.xpt
%{_libdir}/%{name}/components/xpcom_threads.xpt
%{_libdir}/%{name}/components/xpcom_xpti.xpt
%{_libdir}/%{name}/components/xpconnect.xpt
%{_libdir}/%{name}/components/xpinstall.xpt
%{_libdir}/%{name}/components/xulapp.xpt
%{_libdir}/%{name}/components/xuldoc.xpt
%{_libdir}/%{name}/components/xultmpl.xpt
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
