Summary:	Trick-or-Treat DNS translator daemon
Name:		totd
Version:	1.5
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:		ftp://ftp.pasta.cs.uit.no/pub/Vermicelli/totd-latest.tar.gz
# Source0-md5:	b7da63fc1ea1b2e2ce959732826bc146
URL:	http://www.vermicelli.pasta.cs.uit.no/ipv6/software.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Totd is a small DNS proxy nameserver that supports IPv6 only hosts/networks that communicate with the IPv4 world using some translation mechanism. Examples of such translation mechanisms currently in use are:

- IPv6/IPv4 Network Address and Packet Translation (NAT-PT) implemented e.g. by Cisco.
- Application level translators as the faithd implemented by the KAME project. See faithd(8) on BSD/Kame. 

These translators translate map IPv4 to IPv6 connections and back in some way. In order for an application to connect through such a translator to the world beyond it needs to use fake or fabricated addresses that are routed to this translator. These fake addresses don't exist in the DNS, and most likely you would not want them to appear there either. Totd fixes this problem for now (until more elegant solutions emerge?) by translating DNS queries/responses for the faked addresses. totd constructs these fake addresses based on a configured IPv6 translator prefix and records it *does* find in DNS. Totd is merely a stateless DNS-proxy, not a nameserver itself. Totd needs to be able to forward requests to a real nameserver. In addition, totd has experimental support for reverse lookup of 6to4 addresses and for translation scoped address queries. See also, the README file and man page that ships with totd. 

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
install -d $RPM_BUILD_ROOT/{%{_sbindir},%{_mandir}/man8,,%{_sysconfdir}}

cp -a totd $RPM_BUILD_ROOT/%{_sbindir}
cp -a totd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
cp -a totd.conf.sample $RPM_BUILD_ROOT/%{_sysconfdir}/totd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
