Summary:	DNS proxy that supports IPv6 <==> IPv4 record translation
Name:		totd
Version:	1.4
Release:	1
License:	BSD
URL:		http://www.vermicelli.pasta.cs.uit.no/ipv6/software.html
Group:		Networking/Daemons
Source0:	ftp://ftp.pasta.cs.uit.no/pub/Vermicelli/%{name}-%{version}.tar.gz
# Source0-md5:	f732aaad9b9507cd9985224fc40f5bab
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Source1:	%{name}.init
Source2:	%{name}.conf
Patch0:		%{name}-Makefile.in.patch

%description
Totd is a small DNS proxy nameserver that supports IPv6 only
hosts/networks that communicate with the IPv4 world using some
translation mechanism. Examples of such translation mechanisms
currently in use are:

   - IPv6/IPv4 Network Address and Packet Translation (NAT-PT)
     implemented e.g. by Cisco.
   - Application level translators as the faithd implemented by the KAME
     project (http://www.kame.net) or pTRTd
     (http://v6web.litech.org/ptrtd/)

%prep
%setup -q
%patch0 -p1

%build

%configure
make

%install
rm -rf $RPM_BUILD_ROOT
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_sbindir}
install -d $RPM_BUILD_ROOT/%{_sysconfdir}
install -d $RPM_BUILD_ROOT/%{_mandir}/man8
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d

%{__make} DESTDIR=$RPM_BUILD_ROOT install
install %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/totd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/totd.conf

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%postun
if [ "$1" -ge "1" ]; then
    /sbin/service totd condrestart >/dev/null 2>&1
fi

%post
/sbin/chkconfig --add totd

%preun
if [ $1 = 0 ]; then
   /sbin/service totd stop >/dev/null 2>&1
   /sbin/chkconfig --del totd
fi

%files
%defattr(644,root,root,755)
%doc README
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/totd.conf
%config %{_sysconfdir}/rc.d/init.d/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/*/*
