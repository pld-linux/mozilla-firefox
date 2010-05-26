#!/bin/sh
# based on script by (c) vip at linux.pl, wolf at pld-linux.org

LIBDIR="@LIBDIR@/mozilla-firefox"

# compreg.dat and/or chrome.rdf will screw things up if it's from an
# older version.  http://bugs.gentoo.org/show_bug.cgi?id=63999
for f in ~/{.,.mozilla/}firefox/*/{compreg.dat,chrome.rdf,XUL.mfasl}; do
	if [[ -f ${f} && ${f} -ot /usr/bin/mozilla-firefox ]]; then
		echo "Removing ${f} leftover from older firefox"
		rm -f "${f}"
	fi
done

FIREFOX="$LIBDIR/firefox"
PWD=${PWD:-$(pwd)}

if [ "$1" = "-remote" ]; then
	exec $FIREFOX "$@"
else
	if ! $FIREFOX -remote 'ping()' 2>/dev/null; then
		if [ -f "$PWD/$1" ]; then
			exec $FIREFOX "file://$PWD/$1"
		else
			exec $FIREFOX "$@"
		fi
	else
		if [ -z "$1" ]; then
			exec $FIREFOX -remote 'xfeDoCommand(openBrowser)'
		elif [ "$1" = "-mail" ]; then
			exec $FIREFOX -remote 'xfeDoCommand(openInbox)'
		elif [ "$1" = "-compose" ]; then
			exec $FIREFOX -remote 'xfeDoCommand(composeMessage)'
		else
			if [ -f "$PWD/$1" ]; then
				URL="file://$PWD/$1"
			else
				URL="$1"
			fi
			if ! grep -q 'browser\.tabs\.opentabfor\.middleclick.*false' ~/.mozilla/firefox/*/prefs.js ; then
				exec $FIREFOX -new-tab "$URL"
			else
				exec $FIREFOX -new-window "$URL"
			fi
		fi
	fi
fi
