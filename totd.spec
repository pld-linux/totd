Summary:	DNS proxy that supports IPv6 <==> IPv4 record translation
Summary(pl):	Proxy DNS obs³uguj±cy t³umaczenie rekordów IPv6 <==> IPv4
Name:		totd
Version:	1.4
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	ftp://ftp.pasta.cs.uit.no/pub/Vermicelli/%{name}-%{version}.tar.gz
# Source0-md5:	f732aaad9b9507cd9985224fc40f5bab
Source1:	%{name}.init
Source2:	%{name}.conf
Patch0:		%{name}-Makefile.in.patch
URL:		http://www.vermicelli.pasta.cs.uit.no/ipv6/software.html
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

%description -l pl
Totd to ma³y serwer proxy dla serwera nazw (DNS) obs³uguj±cy hosty i
sieci tylko IPv6 komunikuj±cy siê ze ¶wiatem IPv4 przy u¿yciu jakiego¶
mechanizmu t³umaczenia. Przyk³adami takich mechanizmów t³umaczenia
aktualnie bêd±cych w u¿yciu s±:
 - t³umaczenie adresów sieciowych i pakietów IPv6/IPv4 (NAT-PT -
   Network Address and Packet Translation), zaimplementowane m.in.
   przez Cisco
 - t³umaczenie na poziomie aplikacji, jak np. faithd zaimplementowany
   przez KAME (http://www.kame.net/) albo pTRTd
   (http://v6web.litech.org/ptrtd/)

%prep
%setup -q
%patch0 -p1

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

%postun
if [ "$1" -ge "1" ]; then
	/etc/rc.d/init.d/totd condrestart >/dev/null 2>&1
fi

%post
/sbin/chkconfig --add totd

%preun
if [ $1 = 0 ]; then
	/etc/rc.d/init.d/totd stop >/dev/null 2>&1
	/sbin/chkconfig --del totd
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %{_sysconfdir}/totd.conf
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/*/*
