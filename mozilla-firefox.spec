Summary:	Mozilla Firefox web browser
Summary(pl):	Mozilla Firefox - przegl±darka WWW
Name:		mozilla-firefox
Version:	0.8
Release:	0.1
License:	MPL/LGPL
Group:		Applications/Networking
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%description -l pl
Mozilla Firefox jest open sourcow± przegl±dark± sieci www, stworzon± z
my¶l± o zgodno¶ci ze standartami, wydajno¶ci± i przeno¶no¶ci±.

%prep
%setup -q -n mozilla
%patch0 -p1

### FIXME: Shouldn't the default firefox config be part of original source ?
cat <<EOF >.mozconfig
export MOZ_PHOENIX="1"
mk_add_options MOZ_PHOENIX="1"
ac_add_options --with-system-jpeg
ac_add_options --with-system-zlib
ac_add_options --with-system-png
ac_add_options --with-system-mng
ac_add_options --with-pthreads
ac_add_options --disable-tests
ac_add_options --disable-debug
ac_add_options --disable-debug-modules
ac_add_options --disable-xprint
ac_add_options --disable-mailnews
ac_add_options --disable-composer
ac_add_options --disable-ldap
ac_add_options --disable-jsd
ac_add_options --disable-dtd-debug
ac_add_options --disable-gtktest
ac_add_options --disable-freetypetest
ac_add_options --disable-installer
ac_add_options --enable-plaintext-editor-only
ac_add_options --enable-optimize="%{optflags}"
ac_add_options --enable-crypto
ac_add_options --enable-strip
ac_add_options --enable-strip-libs
ac_add_options --enable-reorder
ac_add_options --enable-mathml
ac_add_options --enable-xinerama
ac_add_options --enable-extensions="pref,cookie,wallet"
ac_add_options --enable-freetype2
ac_add_options --enable-xft
ac_add_options --enable-default-toolkit="gtk2"
EOF

%build
#export MOZ_PHOENIX="1"
#configure
#{__make} %{?_smp_mflags}

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export MOZ_PHOENIX="1"

%{__make} -f client.mk build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_pixmapsdir},%{_desktopdir}}

%{__make} -C xpinstall/packager \
	MOZ_PKG_APPNAME="mozilla-firefox" \
	MOZILLA_BIN="\$(DIST)/bin/firefox-bin"

#install -m0755 %{name}.sh $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox
ln -sf %{_libdir}/mozilla-firefox/firefox-bin $RPM_BUILD_ROOT%{_bindir}/mozilla-firefox

tar -xvz -C $RPM_BUILD_ROOT%{_libdir} -f dist/mozilla-firefox-*-linux-gnu.tar.gz

install browser/base/skin/Throbber.png $RPM_BUILD_ROOT%{_pixmapsdir}/mozilla-firefox.png
#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_libdir}/mozilla-firefox/defaults/profile/
#install -m0644 bookmarks.html $RPM_BUILD_ROOT%{_libdir}/mozilla-firefox/defaults/profile/US/

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
## TODO:  %{_libdir}/mozilla-firefox/MozillaFirefox* powinny miec +x 
##         ale niewiem jak to prosto zorbic.
%dir %{_libdir}/mozilla-firefox
%{_libdir}/mozilla-firefox/res
%{_libdir}/mozilla-firefox/chrome
%{_libdir}/mozilla-firefox/components
%{_libdir}/mozilla-firefox/plugins
%{_libdir}/mozilla-firefox/searchplugins
%{_libdir}/mozilla-firefox/icons
%{_libdir}/mozilla-firefox/defaults
%{_libdir}/mozilla-firefox/ipc
%attr(755,root,root) %{_libdir}/mozilla-firefox/*.so
%attr(755,root,root) %{_libdir}/mozilla-firefox/*.sh
%attr(755,root,root) %{_libdir}/mozilla-firefox/m*
%attr(755,root,root) %{_libdir}/mozilla-firefox/M*
%attr(755,root,root) %{_libdir}/mozilla-firefox/reg*
%attr(755,root,root) %{_libdir}/mozilla-firefox/x*
%attr(755,root,root) %{_libdir}/mozilla-firefox/t*
%attr(755,root,root) %{_libdir}/mozilla-firefox/T*
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/mozilla-firefox/elf-dynstr-gc
%endif
%attr(755,root,root) %{_libdir}/mozilla-firefox/libsoftokn3.chk
%attr(755,root,root) %{_libdir}/mozilla-firefox/shlibsign
%{_libdir}/mozilla-firefox/bloaturls.txt
%{_pixmapsdir}/*
%{_desktopdir}/*
