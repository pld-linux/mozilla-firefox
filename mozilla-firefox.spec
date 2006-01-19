#
# TODO:
# - handle locales differently (runtime, since it's possible to do)
# - see ftp://ftp.debian.org/debian/pool/main/m/mozilla-firefox/*diff*
#   for hints how to make locales and other stuff like extensions working
# - rpm upgrade is broken. First you need uninstall Firefox 1.0.x. 
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	gnome	# disable all GNOME components (gnomevfs, gnome, gnomeui)
#
Summary:	Mozilla Firefox web browser
Summary(pl):	Mozilla Firefox - przegl±darka WWW
Name:		mozilla-firefox
Version:	1.5
Release:	4
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}-source.tar.bz2
# Source0-md5:	fa915ddcadecda30ed3e13694f26a779
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch0:		%{name}-nss.patch
Patch1:		%{name}-lib_path.patch
Patch2:		%{name}-nss-system-nspr.patch
Patch3:		%{name}-nopangoxft.patch
Patch4:		%{name}-name.patch
# official patches
# certain ui operations cause prolonged hang (cpu at 100%)
Patch100:	%{name}-bug305970.patch
# UPDATE or DROP?
#PatchX:		%{name}-searchplugins.patch
URL:		http://www.mozilla.org/projects/firefox/
%{?with_gnome:BuildRequires:	GConf2-devel >= 1.2.1}
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.0.0
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	heimdal-devel >= 0.7.1
%{?with_gnome:BuildRequires:	gnome-vfs2-devel >= 2.0}
BuildRequires:	libIDL-devel >= 0.8.0
%{?with_gnome:BuildRequires:	libgnome-devel >= 2.0}
%{?with_gnome:BuildRequires:	libgnomeui-devel >= 2.2.0}
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6-0.20041030.1
BuildRequires:	nss-devel >= 3.8
BuildRequires:	pango-devel >= 1:1.6.0
BuildRequires:	perl-modules >= 5.004
BuildRequires:	pkgconfig
BuildRequires:	zip
Requires:	%{name}-lang-resources = %{version}
Requires:	nspr >= 1:4.6-0.20041030.1
Requires:	nss >= 3.8
# for /etc/ld.so.conf.d
Requires:	glibc >= 6:2.3.5-7.6
Requires(post,postun):	/sbin/ldconfig
Obsoletes:	mozilla-firebird
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_firefoxdir	%{_libdir}/%{name}
# mozilla and firefox provide their own versions
%define		_noautoreqdep		libgkgfx.so libgtkembedmoz.so libgtkxtbin.so libjsj.so libmozjs.so libxpcom.so libxpcom_compat.so
%define		_noautoprovfiles	libplc4.so libplds4.so

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l pl
Mozilla Firefox jest open sourcow± przegl±dark± sieci WWW, stworzon± z
my¶l± o zgodno¶ci ze standardami, wydajno¶ci± i przeno¶no¶ci±.

%package devel
Summary:	Headers for developing programs that will use Mozilla Firefox
Summary(pl):	Mozilla Firefox - pliki nag³ówkowe i biblioteki
Group:		X11/Development/Libraries
Obsoletes:	mozilla-devel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	nspr-devel >= 1:4.6-0.20041030.1

%description devel
Mozilla development package.

%description devel -l pl
Biblioteki i pliki nag³ówkowe.

%package lang-en
Summary:	English resources for Mozilla-firefox
Summary(pl):	Anglojêzyczne zasoby dla Mozilla-FireFox
Group:		X11/Applications/Networking
Requires(post,postun):	%{name} = %{version}-%{release}
Requires(post,postun):	textutils
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-lang-resources = %{version}-%{release}

%description lang-en
English resources for Mozilla-firefox

%description lang-en -l pl
Anglojêzyczne zasoby dla Mozilla-FireFox

%prep
%setup -q -n mozilla
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# official patches
%patch100 -p1
sed -i 's/\(-lgss\)\(\W\)/\1disable\2/' configure

%build
rm -f .mozconfig
export CFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"
export CXXFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf

LIBIDL_CONFIG="%{_bindir}/libIDL-config-2"; export LIBIDL_CONFIG

cat << EOF > .mozconfig
. \$topsrcdir/browser/config/mozconfig

export BUILD_OFFICIAL=1
export MOZILLA_OFFICIAL=1
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1

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
ac_add_options --enable-optimize="%{rpmcflags}"
%if %{?debug:1}0
ac_add_options --enable-debug
ac_add_options --enable-debug-modules
%else
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
%endif
%if %{with tests}
ac_add_options --enable-tests
%else
ac_add_options --disable-tests
%endif
ac_add_options --disable-composer
ac_add_options --disable-dtd-debug
ac_add_options --disable-freetype2
ac_add_options --disable-installer
ac_add_options --disable-jsd
ac_add_options --disable-ldap
ac_add_options --disable-mailnews
ac_add_options --disable-profilesharing
ac_add_options --disable-xprint
ac_add_options --enable-canvas
ac_add_options --enable-crypto
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-mathml
ac_add_options --enable-pango
ac_add_options --enable-reorder
ac_add_options --enable-single-profile
ac_add_options --enable-strip
ac_add_options --enable-strip-libs
ac_add_options --enable-svg
ac_add_options --enable-system-cairo
ac_add_options --enable-xft
ac_add_options --enable-xinerama
ac_add_options --enable-xpctools
ac_add_options --with-pthreads
ac_add_options --with-system-jpeg
ac_add_options --with-system-nspr
ac_add_options --with-system-png
ac_add_options --with-system-zlib
EOF

%{__make} -j1 -f client.mk build \
	CC="%{__cc}" \
	CXX="%{__cxx}"

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}{,extensions}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT{%{_includedir}/%{name}/idl,%{_pkgconfigdir}}
# extensions dir is needed (it can be empty)
	
%{__make} -C xpinstall/packager \
	MOZ_PKG_APPNAME="mozilla-firefox" \
	MOZILLA_BIN="\$(DIST)/bin/firefox-bin" \
	EXCLUDE_NSPR_LIBS=1

install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox

tar -xvz -C $RPM_BUILD_ROOT%{_libdir} -f dist/mozilla-firefox-*linux*.tar.gz

install other-licenses/branding/firefox/content/icon64.png $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-firefox.png
#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/
#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/US/

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

#grep locale $RPM_BUILD_ROOT%{_firefoxdir}/chrome/installed-chrome.txt > $RPM_BUILD_ROOT%{_firefoxdir}/chrome/%{name}-en-US-installed-chrome.txt
#grep -v locale $RPM_BUILD_ROOT%{_firefoxdir}/chrome/installed-chrome.txt > $RPM_BUILD_ROOT%{_firefoxdir}/chrome/%{name}-misc-installed-chrome.txt

rm -rf US classic comm embed-sample en-{US,mac,unix,win} modern pipnss pippki
rm -f en-win.jar en-mac.jar embed-sample.jar modern.jar

# header/developement files
cp -rfL dist/include/*	$RPM_BUILD_ROOT%{_includedir}/%{name}
cp -rfL dist/idl/*	$RPM_BUILD_ROOT%{_includedir}/%{name}/idl

install dist/bin/regxpcom $RPM_BUILD_ROOT%{_bindir}
install dist/bin/xpidl $RPM_BUILD_ROOT%{_bindir}
install dist/bin/xpt_dump $RPM_BUILD_ROOT%{_bindir}
install dist/bin/xpt_link $RPM_BUILD_ROOT%{_bindir}

ln -sf %{_includedir}/mozilla-firefox/necko/nsIURI.h \
	$RPM_BUILD_ROOT%{_includedir}/mozilla-firefox/nsIURI.h
	
# CA certificates
ln -s %{_libdir}/libnssckbi.so $RPM_BUILD_ROOT%{_firefoxdir}/libnssckbi.so

# pkgconfig files
for f in build/unix/*.pc ; do
        sed -e 's/firefox-%{version}/mozilla-firefox/' $f \
	    > $RPM_BUILD_ROOT%{_pkgconfigdir}/$(basename $f)
done

# already provided by standalone packages
rm -f $RPM_BUILD_ROOT%{_pkgconfigdir}/firefox-{nss,nspr}.pc

sed -i -e 's#firefox-nspr =.*#mozilla-nspr#g' -e 's#irefox-nss =.*#mozilla-nss#g' \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# includedir/dom CFLAGS		
sed -i -e '/Cflags:/{/{includedir}\/dom/!s,$, -I${includedir}/dom,}' \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/firefox-plugin.pc
	
cat << 'EOF' > $RPM_BUILD_ROOT%{_sbindir}/firefox-chrome+xpcom-generate
#!/bin/sh
umask 022
#There is no such files (*-installed-chrome.txt). IMO obsolete.
#cat %{_firefoxdir}/chrome/*-installed-chrome.txt > %{_firefoxdir}/chrome/installed-chrome.txt
rm -f %{_firefoxdir}/chrome/{chrome.rdf,overlayinfo/*/*/*.rdf}
rm -f %{_firefoxdir}/components/{compreg,xpti}.dat
MOZILLA_FIVE_HOME=%{_firefoxdir}
export MOZILLA_FIVE_HOME

# PATH
PATH=%{_firefoxdir}:$PATH
export PATH

# added /usr/lib : don't load your local library
LD_LIBRARY_PATH=%{_firefoxdir}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
export LD_LIBRARY_PATH

unset TMPDIR TMP || :
MOZILLA_FIVE_HOME=%{_firefoxdir} %{_firefoxdir}/regxpcom
MOZILLA_FIVE_HOME=%{_firefoxdir} %{_firefoxdir}/firefox -register
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%{_sbindir}/firefox-chrome+xpcom-generate
%banner %{name} -e <<EOF
###################################################################
#                                                                 #
# NOTICE:                                                         #
# If you have problem with upgrade old mozilla-firefox 1.0.x, you #
# should remove it first.                                         #
#                                                                 #
###################################################################
EOF

%postun
/sbin/ldconfig
if [ "$1" != "0" ]; then
	%{_sbindir}/firefox-chrome+xpcom-generate
fi

%preun
if [ "$1" == "0" ]; then
	rm -rf %{_firefoxdir}/chrome/overlayinfo
	rm -f  %{_firefoxdir}/chrome/*.rdf
	rm -rf %{_firefoxdir}/components
	rm -rf %{_firefoxdir}/extensions
fi

#%post lang-en
#umask 022
#cat %{_firefoxdir}/chrome/*-installed-chrome.txt >%{_firefoxdir}/chrome/installed-chrome.txt

#%postun lang-en
#umask 022
#cat %{_firefoxdir}/chrome/*-installed-chrome.txt >%{_firefoxdir}/chrome/installed-chrome.txt

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mozilla*
%attr(755,root,root) %{_sbindir}/*
%dir %{_firefoxdir}
%{_firefoxdir}/res
%dir %{_firefoxdir}/components
%attr(755,root,root) %{_firefoxdir}/components/*.so
%{_firefoxdir}/components/*.js
%{_firefoxdir}/components/*.xpt
%{_firefoxdir}/plugins
%{_firefoxdir}/searchplugins
%{_firefoxdir}/icons
%{_firefoxdir}/defaults
%{_firefoxdir}/greprefs
%dir %{_firefoxdir}/extensions
%dir %{_firefoxdir}/init.d
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
# -chat subpackage?
#%{_firefoxdir}/chrome/chatzilla.jar
#%{_firefoxdir}/chrome/content-packs.jar
# -dom-inspector subpackage?
#%{_firefoxdir}/chrome/inspector.jar
#%{_firefoxdir}/chrome/mozilla-firefox-misc-installed-chrome.txt
%dir %{_firefoxdir}/chrome/icons
%{_firefoxdir}/chrome/icons/default

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
#%{_firefoxdir}/chrome/mozilla-firefox-en-US-installed-chrome.txt
