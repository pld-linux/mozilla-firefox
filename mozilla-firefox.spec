%bcond_with tests	# enable tests (whatever they check)
#
Summary:	Mozilla Firefox web browser
Summary(pl):	Mozilla Firefox - przegl±darka WWW
Name:		mozilla-firefox
Version:	0.8
Release:	1.3
License:	MPL/LGPL
Group:		X11/Applications/Networking
Source0:	http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/firefox-source-%{version}.tar.bz2
# Source0-md5:	cdc85152f4219bf3e3f1a8dc46e04654
Source1:	%{name}.desktop
Patch0:		%{name}-alpha-gcc3.patch
URL:		http://www.mozilla.org/projects/firefox/
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:  libIDL-devel >= 0.8.0
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libpng-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	pango-devel >= 1.1.0
BuildRequires:	zip
Obsoletes:	mozilla-firebird
Requires:	%{name}-lang-resources
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_firefoxdir	%{_libdir}/%{name}

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l pl
Mozilla Firefox jest open sourcow± przegl±dark± sieci www, stworzon± z
my¶l± o zgodno¶ci ze standartami, wydajno¶ci± i przeno¶no¶ci±.

%package lang-en
Summary:	English resources for Mozilla-firefox
Summary(pl):	Anglojêzyczne zasoby dla Mozilla-FireFox
Group:	X11/Applications/Networking
Requires(post,postun):	mozilla-firefox >= %{version}-1.1
Requires(post,postun):	textutils
Requires:	mozilla-firefox >= %{version}-1.1
Provides:	%{name}-lang-resources
Obsoletes:	%{name}-lang-resources

%description lang-en
English resources for Mozilla-firefox

%description lang-en -l pl
Anglojêzyczne zasoby dla Mozilla-FireFox

%prep
%setup -q -n mozilla
%patch0 -p1

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export MOZ_PHOENIX="1"

./configure \
	--with-system-jpeg \
	--with-system-zlib \
	--with-system-png \
	--with-system-mng \
	--with-pthreads \
%if %{with debug}
	--enable-debug \
	--enable-debug-modules \
%else
	--disable-debug \
	--disable-debug-modules \
%endif
	--disable-xprint \
	--disable-mailnews \
	--disable-composer \
	--disable-ldap \
	--disable-jsd \
	--disable-dtd-debug \
%if %{with tests}
	--enable-tests \
%else
	--disable-tests \
%endif
	--disable-installer \
	--enable-plaintext-editor-only \
	--enable-optimize="%{optflags}" \
	--enable-crypto \
	--enable-strip \
	--enable-strip-libs \
	--enable-reorder \
	--enable-mathml \
	--enable-xinerama \
	--enable-freetype2 \
	--enable-xft \
	--enable-default-toolkit="gtk2"

#{__make} %{?_smp_mflags}
%{__make} -f client.mk build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}}

%{__make} -C xpinstall/packager \
	MOZ_PKG_APPNAME="mozilla-firefox" \
	MOZILLA_BIN="\$(DIST)/bin/firefox-bin"

#install -m0755 %{name}.sh $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox
ln -sf %{_firefoxdir}/firefox $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox

tar -xvz -C $RPM_BUILD_ROOT%{_libdir} -f dist/mozilla-firefox-*-linux-gnu.tar.gz

install browser/base/skin/Throbber.png $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-firefox.png
#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/
#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_firefoxdir}/defaults/profile/US/

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

grep locale $RPM_BUILD_ROOT%{_firefoxdir}/chrome/installed-chrome.txt > $RPM_BUILD_ROOT%{_firefoxdir}/chrome/%{name}-en-US-installed-chrome.txt
grep -v locale $RPM_BUILD_ROOT%{_firefoxdir}/chrome/installed-chrome.txt > $RPM_BUILD_ROOT%{_firefoxdir}/chrome/%{name}-misc-installed-chrome.txt

rm -rf US classic comm embed-sample en-{US,mac,unix,win} modern pipnss pippki toolkit
rm -f en-win.jar en-mac.jar embed-sample.jar modern.jar

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
cat %{_firefoxdir}/chrome/*-installed-chrome.txt >%{_firefoxdir}/chrome/installed-chrome.txt

%post lang-en
umask 022
cat %{_firefoxdir}/chrome/*-installed-chrome.txt >%{_firefoxdir}/chrome/installed-chrome.txt

%postun lang-en
umask 022
cat %{_firefoxdir}/chrome/*-installed-chrome.txt >%{_firefoxdir}/chrome/installed-chrome.txt

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_firefoxdir}
%{_firefoxdir}/res
%{_firefoxdir}/components
%{_firefoxdir}/plugins
%{_firefoxdir}/searchplugins
%{_firefoxdir}/icons
%{_firefoxdir}/defaults
%{_firefoxdir}/ipc
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
%attr(755,root,root) %{_firefoxdir}/libsoftokn3.chk
%attr(755,root,root) %{_firefoxdir}/shlibsign
%{_firefoxdir}/bloaturls.txt
%{_pixmapsdir}/*
%{_desktopdir}/*

%dir %{_firefoxdir}/chrome
%{_firefoxdir}/chrome/browser.jar
%{_firefoxdir}/chrome/classic.jar
%{_firefoxdir}/chrome/comm.jar
%{_firefoxdir}/chrome/pip*.jar
%{_firefoxdir}/chrome/toolkit.jar
%{_firefoxdir}/chrome/mozilla-firefox-misc-installed-chrome.txt

%files lang-en
%defattr(644,root,root,755)
%{_firefoxdir}/chrome/en-US.jar
%{_firefoxdir}/chrome/en-unix.jar
%{_firefoxdir}/chrome/US.jar
%{_firefoxdir}/chrome/mozilla-firefox-en-US-installed-chrome.txt
