Summary:	DNS proxy that supports IPv6 <==> IPv4 record translation
Summary(pl.UTF-8):	Proxy DNS obsługujący tłumaczenie rekordów IPv6 <==> IPv4
Name:		totd
Version:	1.5.1
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.pasta.cs.uit.no/pub/Vermicelli/%{name}-%{version}.tar.gz
# Source0-md5:	7edaedae9f6aca5912dd6c123582cf08
Source1:	%{name}.init
Source2:	%{name}.conf
Patch0:		%{name}-Makefile.in.patch
Patch1:		%{name}-buildfix.patch
URL:		http://www.vermicelli.pasta.cs.uit.no/ipv6/software.html
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Totd is a small DNS proxy nameserver that supports IPv6 only
hosts/networks that communicate with the IPv4 world using some
translation mechanism. Examples of such translation mechanisms
currently in use are:
- IPv6/IPv4 Network Address and Packet Translation (NAT-PT)
  implemented e.g. by Cisco.
- Application level translators as the faithd implemented by the KAME
  project (http://www.kame.net/) or pTRTd
  (http://v6web.litech.org/ptrtd/)

%description -l pl.UTF-8
Totd to mały serwer proxy dla serwera nazw (DNS) obsługujący hosty i
sieci tylko IPv6 komunikujący się ze światem IPv4 przy użyciu jakiegoś
mechanizmu tłumaczenia. Przykładami takich mechanizmów tłumaczenia
aktualnie będących w użyciu są:
- tłumaczenie adresów sieciowych i pakietów IPv6/IPv4 (NAT-PT -
  Network Address and Packet Translation), zaimplementowane m.in.
  przez Cisco
- tłumaczenie na poziomie aplikacji, jak np. faithd zaimplementowany
  przez KAME (http://www.kame.net/) albo pTRTd
  (http://v6web.litech.org/ptrtd/)

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/totd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/totd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add totd

%preun
if [ "$1" = "0 "]; then
	/etc/rc.d/init.d/totd stop >&2
	/sbin/chkconfig --del totd
fi

%postun
if [ "$1" -ge "1" ]; then
	/etc/rc.d/init.d/totd condrestart >&2
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/totd.conf
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/*/*
