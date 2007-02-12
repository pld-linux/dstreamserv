Summary:	Darwin Streaming Server
Summary(pl.UTF-8):	Serwer strumieni z Darwina
Name:		dstreamserv
Version:	5.0.3.2
Release:	0.1
License:	APSL
Group:		Networking/Daemons
Source0:	DSS-v5_0_3_2.zip
# NoSource0-md5:	394e74199a01e5f54c743bb02f898edd
NoSource:	0
Source1:	%{name}.init
Source2:	%{name}-relayconfig.xml
Patch0:		%{name}-Buildit.patch
Patch1:		%{name}-buildtarball.patch
Patch2:		%{name}-defaultpath.patch
Patch3:		%{name}-qtpasswd.patch
URL:		http://developer.apple.com/darwin/projects/streaming/
BuildRequires:	libstdc++-devel
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.202
Requires:	rc-scripts
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(qtss)
Provides:	user(qtss)
Obsoletes:	DSS
Obsoletes:	dstreamsrv
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Streaming Server is server technology which allows you to send
streaming QuickTime data to clients across the Internet using the
industry standard RTP and RTSP protocols.

%description -l pl.UTF-8
Serwer strumieni pozwala wysyłać strumienie danych QuickTime do
klientów w Internecie przy użyciu protokołów RTP i RTSP.

%package samples
Summary:	Darwin Streaming Server - samples
Summary(pl.UTF-8):	Przykłady do Darwin Streaming Servera
Group:		Networking/Daemons

%description samples
Sample files for Streaming Server.

%description samples -l pl.UTF-8
Przykładowe pliki do Darwin Streaming Servera.

%prep
%setup -q -n DSS-v%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export CC="%{__cxx}"
export CXX="%{__cxx}"
./buildtarball dss
tar -xvzf DarwinStreamingSrvrdss-Linux.tar.gz
cd DarwinStreamingSrvrdss-Linux
%{_bindir}/perl perlpath.pl %{_bindir}/perl streamingadminserver.pl AdminHtml/parse_xml.cgi
echo "admin: dssadmin" > qtgroups
./qtpasswd -f ./qtusers -c -F -r "DSS Admin Server" -p 'aGFja21l' 'dssadmin'

%install
rm -rf $RPM_BUILD_ROOT
install -d \
$RPM_BUILD_ROOT%{_sysconfdir}/streaming \
	$RPM_BUILD_ROOT/var/lib/streaming \
	$RPM_BUILD_ROOT/var/log/streaming \
	$RPM_BUILD_ROOT/var/lib/streaming/playlists \
	$RPM_BUILD_ROOT%{_libdir}/StreamingServerModules \
	$RPM_BUILD_ROOT%{_datadir}/streaming/AdminHtml \
	$RPM_BUILD_ROOT%{_datadir}/streaming/AdminHtml/html_en \
	$RPM_BUILD_ROOT%{_datadir}/streaming/AdminHtml/images \
	$RPM_BUILD_ROOT%{_datadir}/streaming/AdminHtml/includes \
	$RPM_BUILD_ROOT/var/lib/streaming/movies \
	$RPM_BUILD_ROOT/var/lib/streaming/http \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/streaming

cd DarwinStreamingSrvrdss-Linux

install MP3Broadcaster $RPM_BUILD_ROOT%{_bindir}
install PlaylistBroadcaster $RPM_BUILD_ROOT%{_bindir}
install qtpasswd $RPM_BUILD_ROOT%{_sbindir}

install *.mov $RPM_BUILD_ROOT/var/lib/streaming/movies
install *.mp3 $RPM_BUILD_ROOT/var/lib/streaming/movies
install *.mp4 $RPM_BUILD_ROOT/var/lib/streaming/movies

install DarwinStreamingServer $RPM_BUILD_ROOT%{_sbindir}
install streamingadminserver.pl $RPM_BUILD_ROOT%{_sbindir}

install AdminHtml/*.html $RPM_BUILD_ROOT%{_datadir}/streaming/AdminHtml
install AdminHtml/*.pl $RPM_BUILD_ROOT%{_datadir}/streaming/AdminHtml
install AdminHtml/*.cgi $RPM_BUILD_ROOT%{_datadir}/streaming/AdminHtml
install AdminHtml/html_en/* $RPM_BUILD_ROOT%{_datadir}/streaming/AdminHtml/html_en
install AdminHtml/images/* $RPM_BUILD_ROOT%{_datadir}/streaming/AdminHtml/images
install AdminHtml/includes/* $RPM_BUILD_ROOT%{_datadir}/streaming/AdminHtml/includes

install qtgroups $RPM_BUILD_ROOT%{_sysconfdir}/streaming
install qtusers $RPM_BUILD_ROOT%{_sysconfdir}/streaming
install streamingserver.xml $RPM_BUILD_ROOT%{_sysconfdir}/streaming

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/DSS ]; then
	/etc/rc.d/init.d/%{name} restart >&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start Streaming Server daemon."
fi
%banner %{name} -e <<EOF
Default admin password is aGFja21l. Set a password for it or, better
delete it and create new admin username and password (using qtpasswd)

EOF


%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/DSS ]; then
		/etc/rc.d/init.d/%{name} stop >&2
	fi
	/sbin/chkconfig --del %{name}
fi

%pre
%groupadd -f -g 148 qtss
%useradd -g qtss -d /tmp -u 148 -s /bin/false qtss

%postun
if [ "$1" = "0" ]; then
	%userremove qtss
	%groupremove qtss
fi

%files
%defattr(644,root,root,755)
%doc DarwinStreamingSrvrdss-Linux/*-Sample
%doc DarwinStreamingSrvrdss-Linux/*-sample
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(750,root,root) %{_sbindir}/*
%dir %attr(770,root,qtss) /var/log/streaming
%dir %{_libdir}/StreamingServerModules
# /var/lib files 
%dir /var/lib/streaming
%dir %attr(750,qtss,qtss) /var/lib/streaming/playlists
%dir %attr(750,qtss,qtss) /var/lib/streaming/movies
%dir %attr(750,qtss,qtss) /var/lib/streaming/http
# admin server
%dir %{_datadir}/streaming
%dir %attr(700,qtss,qtss) %{_datadir}/streaming/AdminHtml
%dir %attr(700,qtss,qtss) %{_datadir}/streaming/AdminHtml/images
%dir %attr(700,qtss,qtss) %{_datadir}/streaming/AdminHtml/includes
%dir %attr(700,qtss,qtss) %{_datadir}/streaming/AdminHtml/html_en
%attr(400,qtss,qtss) %{_datadir}/streaming/AdminHtml/*.html
%attr(400,qtss,qtss) %{_datadir}/streaming/AdminHtml/*.pl
%attr(400,qtss,qtss) %{_datadir}/streaming/AdminHtml/*.cgi
%attr(400,qtss,qtss) %{_datadir}/streaming/AdminHtml/images/*
%attr(400,qtss,qtss) %{_datadir}/streaming/AdminHtml/includes/*
%attr(400,qtss,qtss) %{_datadir}/streaming/AdminHtml/html_en/*
# etc 
%dir %attr(750,qtss,qtss) %{_sysconfdir}/streaming
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/streaming/*

%files samples
%defattr(644,root,root,755)
%attr(644,qtss,qtss) /var/lib/streaming/movies/*
