Summary:	Darwin Streaming Server
Summary(pl):	Serwer strumieni z Darwina
Name:		dstreamsrv
Version:	4.0
Release:	2
License:	APSL
Group:		Networking/Daemons
# Source0:	http://<user>:<password>@www.publicsource.apple.com/projects/streaming/source/DarwinStreamingServerSrc.tar.gz
Source0:	DarwinStreamingServerSrc.tar.gz
URL:		http://www.publicsource.apple.com/projects/streaming/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Streaming Server is server technology which allows you to send
streaming QuickTime data to clients across the Internet using the
industry standard RTP and RTSP protocols.

%description -l pl
Serwer strumieni pozwala wysy³aæ strumienie danych QuickTime do
klientów w Internecie przy u¿yciu protoko³ów RTP i RTSP.

%prep
%setup -q -n StreamingServer

%build
./buildtarball
tar -xvzf DarwinStreamingSrvr4.0-Linux.tar.gz
cd DarwinStreamingSrvr4.0-Linux
%{_bindir}/perl perlpath.pl %{_bindir}/perl streamingadminserver.pl AdminHtml/parse_xml.cgi
echo "admin: dssadmin" > qtgroups
./qtpasswd -f ./qtusers -p 'dssadmin' 'dssadmin'
./qtpasswd -f ./qtusers -F -d 'aGFja21l'

%install
rm -rf $RPM_BUILD_ROOT
install -d \
$RPM_BUILD_ROOT%{_sysconfdir}/streaming \
    $RPM_BUILD_ROOT/var/streaming \
    $RPM_BUILD_ROOT/var/streaming/logs \
    $RPM_BUILD_ROOT/var/streaming/playlists \
    $RPM_BUILD_ROOT/var/streaming/AdminHtml \
    $RPM_BUILD_ROOT/var/streaming/AdminHtml/html_de \
    $RPM_BUILD_ROOT/var/streaming/AdminHtml/html_en \
    $RPM_BUILD_ROOT/var/streaming/AdminHtml/html_fr \
    $RPM_BUILD_ROOT/var/streaming/AdminHtml/html_ja \
    $RPM_BUILD_ROOT/var/streaming/AdminHtml/images \
    $RPM_BUILD_ROOT/var/streaming/AdminHtml/includes \
    $RPM_BUILD_ROOT%{_prefix}/local/bin \
    $RPM_BUILD_ROOT%{_prefix}/local/sbin \
    $RPM_BUILD_ROOT%{_prefix}/local/movies

cd DarwinStreamingSrvr4.0-Linux

install MP3Broadcaster $RPM_BUILD_ROOT%{_prefix}/local/bin
install PlaylistBroadcaster $RPM_BUILD_ROOT%{_prefix}/local/bin
install qtpasswd $RPM_BUILD_ROOT%{_prefix}/local/bin

install *.mov $RPM_BUILD_ROOT%{_prefix}/local/movies/
install *.mp3 $RPM_BUILD_ROOT%{_prefix}/local/movies/

install DarwinStreamingServer $RPM_BUILD_ROOT%{_prefix}/local/sbin
install streamingadminserver.pl $RPM_BUILD_ROOT%{_prefix}/local/sbin

install readme.pdf $RPM_BUILD_ROOT/var/streaming

install AdminHtml/*.html $RPM_BUILD_ROOT/var/streaming/AdminHtml/
install AdminHtml/*.pl $RPM_BUILD_ROOT/var/streaming/AdminHtml/
install AdminHtml/*.cgi $RPM_BUILD_ROOT/var/streaming/AdminHtml/
install AdminHtml/html_de/* $RPM_BUILD_ROOT/var/streaming/AdminHtml/html_de/
install AdminHtml/html_en/* $RPM_BUILD_ROOT/var/streaming/AdminHtml/html_en/
install AdminHtml/html_fr/* $RPM_BUILD_ROOT/var/streaming/AdminHtml/html_fr/
install AdminHtml/html_ja/* $RPM_BUILD_ROOT/var/streaming/AdminHtml/html_ja/
install AdminHtml/images/* $RPM_BUILD_ROOT/var/streaming/AdminHtml/images/
install AdminHtml/includes/* $RPM_BUILD_ROOT/var/streaming/AdminHtml/includes/

install qtgroups $RPM_BUILD_ROOT%{_sysconfdir}/streaming
install qtusers $RPM_BUILD_ROOT%{_sysconfdir}/streaming
install streamingserver.xml $RPM_BUILD_ROOT%{_sysconfdir}/streaming

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/local/bin/*
%attr(750,root,root) %{_prefix}/local/sbin/*
%attr(644,root,root) %{_prefix}/local/movies/*
%attr(644,root,root) /var/streaming/readme.pdf
%attr(777,root,root) /var/streaming/playlists
%attr(755,root,root) /var/streaming/logs
%attr(600,root,root) /var/streaming/AdminHtml/*.html
%attr(600,root,root) /var/streaming/AdminHtml/*.pl
%attr(600,root,root) /var/streaming/AdminHtml/*.cgi
%attr(600,root,root) /var/streaming/AdminHtml/images/*
%attr(600,root,root) /var/streaming/AdminHtml/includes/*
%attr(600,root,root) /var/streaming/AdminHtml/html_de
%attr(600,root,root) /var/streaming/AdminHtml/html_en
%attr(600,root,root) /var/streaming/AdminHtml/html_fr
%attr(600,root,root) /var/streaming/AdminHtml/html_ja
%attr(600,root,root) %{_sysconfdir}/streaming/*
%doc DarwinStreamingSrvr4.0-Linux/*-Sample
%doc DarwinStreamingSrvr4.0-Linux/*-sample
