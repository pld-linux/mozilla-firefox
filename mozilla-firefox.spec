#
# TODO:
# - handle locales differently (runtime, since it's possible to do)
# - see ftp://ftp.debian.org/debian/pool/main/m/mozilla-firefox/*diff*
#   for hints how to make locales and other stuff like extensions working
#
# Conditional build:
%bcond_with	tests	# enable tests (whatever they check)
%bcond_without	ft218	# compile with freetype < 2.1.8
#
Summary:	Mozilla Firefox web browser
Summary(pl):	Mozilla Firefox - przegl±darka WWW
Name:		mozilla-firefox
Version:	1.0.5
Release:	1
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/source/firefox-%{version}-source.tar.bz2
# Source0-md5:	b50fe116305b7f56b2105d464110228d
Source1:	%{name}.desktop
Source2:	%{name}.sh
Patch0:		%{name}-alpha-gcc3.patch
Patch1:		%{name}-gfx.patch
Patch2:		%{name}-nss.patch
Patch3:		%{name}-lib_path.patch
Patch4:		%{name}-freetype.patch
Patch5:		%{name}-searchplugins.patch
Patch6:		%{name}-gcc-bugs.patch
URL:		http://www.mozilla.org/projects/firefox/
BuildRequires:	automake
%if %{with ft218}
BuildRequires:	freetype-devel >= 1:2.1.9
%else
BuildRequires:	freetype-devel >= 2.1.3
BuildRequires:	freetype-devel < 1:2.1.8
BuildConflicts:	freetype-devel = 2.1.8
%endif
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	libIDL-devel >= 0.8.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	nspr-devel >= 1:4.6-0.20041030.1
BuildRequires:	nss-devel >= 3.8
BuildRequires:	pango-devel >= 1:1.1.0
BuildRequires:	perl-modules
BuildRequires:	pkgconfig
BuildRequires:	zip
BuildRequires:  heimdal-devel >= 0.7
Requires:	%{name}-lang-resources = %{version}
%if %{with ft218}
Requires:	freetype >= 1:2.1.3
%else
Requires:	freetype >= 2.1.3
Conflicts:	freetype = 2.1.8
%endif
Requires:	nspr >= 1:4.6-0.20041030.1
Requires:	nss >= 3.8
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
%{?with_ft218:%patch4 -p1}
%patch5 -p0
%patch6 -p0
sed -i 's/\(-lgss\)\(\W\)/\1disable\2/' configure

%build
export CFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"
export CXXFLAGS="%{rpmcflags} `%{_bindir}/pkg-config mozilla-nspr --cflags-only-I`"
export MOZ_PHOENIX="1"
export BUILD_OFFICIAL="1"
export MOZILLA_OFFICIAL="1"

cp -f %{_datadir}/automake/config.* build/autoconf
cp -f %{_datadir}/automake/config.* nsprpub/build/autoconf
cp -f %{_datadir}/automake/config.* directory/c-sdk/config/autoconf
%configure2_13 \
%if %{?debug:1}0
	--enable-debug \
	--enable-debug-modules \
%else
	--disable-debug \
	--disable-debug-modules \
%endif
	--disable-composer \
	--disable-dtd-debug \
	--disable-installer \
	--disable-jsd \
	--disable-ldap \
	--disable-mailnews \
%if %{with tests}
	--enable-tests \
%else
	--disable-tests \
%endif
	--disable-xprint \
	--enable-crypto \
	--enable-freetype2 \
	--enable-mathml \
	--enable-optimize="%{rpmcflags}" \
	--enable-plaintext-editor-only \
	--enable-reorder \
	--enable-strip \
	--enable-strip-libs \
	--enable-xinerama \
	--enable-xft \
	--enable-default-toolkit="gtk2" \
	--with-pthreads \
	--with-system-nspr \
	--with-system-jpeg \
	--with-system-png \
	--with-system-zlib \
	--enable-single-profile \
	--disable-profilesharing \
	--enable-extensions=cookie,xml-rpc,xmlextras,pref,transformiix,universalchardet,webservices,inspector,gnomevfs,negotiateauth
	

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}} \
	$RPM_BUILD_ROOT{%{_includedir}/%{name}/idl,%{_pkgconfigdir}}
	
%{__make} -C xpinstall/packager \
	MOZ_PKG_APPNAME="mozilla-firefox" \
	MOZILLA_BIN="\$(DIST)/bin/firefox-bin" \
	EXCLUDE_NSPR_LIBS=1

install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox

tar -xvz -C $RPM_BUILD_ROOT%{_libdir} -f dist/mozilla-firefox-*-linux-gnu.tar.gz

install other-licenses/branding/firefox/content/icon32.png $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-firefox.png
#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/
#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/US/

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

grep locale $RPM_BUILD_ROOT%{_firefoxdir}/chrome/installed-chrome.txt > $RPM_BUILD_ROOT%{_firefoxdir}/chrome/%{name}-en-US-installed-chrome.txt
grep -v locale $RPM_BUILD_ROOT%{_firefoxdir}/chrome/installed-chrome.txt > $RPM_BUILD_ROOT%{_firefoxdir}/chrome/%{name}-misc-installed-chrome.txt

rm -rf US classic comm embed-sample en-{US,mac,unix,win} modern pipnss pippki
rm -f en-win.jar en-mac.jar embed-sample.jar modern.jar

# header/developement files
cp -rfL dist/include/*	$RPM_BUILD_ROOT%{_includedir}/%{name}
cp -rfL dist/idl/*	$RPM_BUILD_ROOT%{_includedir}/%{name}/idl

install dist/bin/regchrome $RPM_BUILD_ROOT%{_bindir}
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
cat %{_firefoxdir}/chrome/*-installed-chrome.txt > %{_firefoxdir}/chrome/installed-chrome.txt
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
%{_firefoxdir}/regxpcom
%{_firefoxdir}/regchrome
%{_firefoxdir}/firefox -register
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/firefox-chrome+xpcom-generate

%postun
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

%post lang-en
umask 022
cat %{_firefoxdir}/chrome/*-installed-chrome.txt >%{_firefoxdir}/chrome/installed-chrome.txt

%postun lang-en
umask 022
cat %{_firefoxdir}/chrome/*-installed-chrome.txt >%{_firefoxdir}/chrome/installed-chrome.txt

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
%dir %{_firefoxdir}/init.d
%attr(755,root,root) %{_firefoxdir}/*.so
%attr(755,root,root) %{_firefoxdir}/*.sh
%attr(755,root,root) %{_firefoxdir}/m*
%attr(755,root,root) %{_firefoxdir}/f*
%attr(755,root,root) %{_firefoxdir}/reg*
%attr(755,root,root) %{_firefoxdir}/x*
%attr(755,root,root) %{_firefoxdir}/T*
%ifarch %{ix86}
%attr(755,root,root) %{_firefoxdir}/elf-dynstr-gc
%endif
%{_firefoxdir}/bloaturls.txt
%{_pixmapsdir}/*
%{_desktopdir}/*

%dir %{_firefoxdir}/chrome
%{_firefoxdir}/chrome/browser.jar
# -chat subpackage?
#%{_firefoxdir}/chrome/chatzilla.jar
%{_firefoxdir}/chrome/classic.jar
%{_firefoxdir}/chrome/comm.jar
#%{_firefoxdir}/chrome/content-packs.jar
%{_firefoxdir}/chrome/help.jar
# -dom-inspector subpackage?
%{_firefoxdir}/chrome/inspector.jar
%{_firefoxdir}/chrome/modern.jar
%{_firefoxdir}/chrome/pip*.jar
%{_firefoxdir}/chrome/toolkit.jar
%{_firefoxdir}/chrome/mozilla-firefox-misc-installed-chrome.txt
%dir %{_firefoxdir}/chrome/icons
%{_firefoxdir}/chrome/icons/default

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/regchrome
%attr(755,root,root) %{_bindir}/regxpcom
%attr(755,root,root) %{_bindir}/xpidl
%attr(755,root,root) %{_bindir}/xpt_dump
%attr(755,root,root) %{_bindir}/xpt_link
%{_includedir}/%{name}
%{_pkgconfigdir}/*

%files lang-en
%defattr(644,root,root,755)
%{_firefoxdir}/chrome/en-US.jar
%{_firefoxdir}/chrome/mozilla-firefox-en-US-installed-chrome.txt
