Summary:	List based packet handler
Name:		iplist
Version:	0.29
Release:	3
Source0:	%{name}-%{version}.tar.bz2
Patch0:		iplist-0.28-fix-init.patch
Patch1:		iplist-0.29-unsigned_char.patch
Patch2:		iplist-0.29-linking.patch
patch3:		iplist-0.29-cstdlib.patch
License:	GPLv2+
Group:		System/Configuration/Networking
URL:		https://iplist.sourceforge.net/
BuildRequires:	gcc-c++
BuildRequires:	zlib-devel
BuildRequires:	netfilter_queue-devel
BuildRequires:	libpcre-devel
Requires(post):         rpm-helper
Requires(preun):        rpm-helper
Requires:       java >= 1.6
Requires:       usermode-consoleonly
Requires:	wget
Provides:	ipblock = %{version}-%{release}

%description
iplist is a list based packet handler which uses the netfilter netlink-queue
library (kernel 2.6.14 or later). It filters by IP-address and is optimized
for thousands of IP-address ranges.

%prep
%setup -q -n %{name}
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p1 -b .cstdlib

# fix compiler flags
sed -i -e 's|-O2|%{optflags}|' Makefile

%build
%make LDFLAGS="%{ldflags}"

%install

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily/
mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps/
mkdir -p %{buildroot}%{_initrddir}/
mkdir -p %{buildroot}%{_datadir}/java/
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/icons/
mkdir -p %{buildroot}%{_mandir}/man8/
mkdir -p %{buildroot}%{_var}/cache/iplist/

ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/ipblock

install -p -m 644 ipblock.conf \
	%{buildroot}%{_sysconfdir}/ipblock.conf
install -p -m 644 ipblock.lists \
	%{buildroot}%{_sysconfdir}/ipblock.lists
install -p -m 644 fedora/ipblock.pam \
	%{buildroot}%{_sysconfdir}/pam.d/ipblock
install -p -m 644 fedora/ipblock.security \
	%{buildroot}%{_sysconfdir}/security/console.apps/ipblock
install -p -m 755 fedora/ipblock.init \
	%{buildroot}%{_initrddir}/ipblock
install -p -m 755 debian/ipblock.cron.daily \
	%{buildroot}%{_sysconfdir}/cron.daily/ipblock
install -p -m 644 fedora/ipblock.desktop \
	%{buildroot}%{_datadir}/applications/ipblock.desktop
install -p -m 644 ipblock.png \
	%{buildroot}%{_datadir}/icons/ipblock.png

install -p -m 644 iplist.8 %{buildroot}%{_mandir}/man8/
install -p -m 644 ipblock.8 %{buildroot}%{_mandir}/man8/
install -p -m 644 allow.p2p %{buildroot}%{_var}/cache/iplist/

%makeinstall_std

%post
%_post_service ipblock

%preun
%_preun_service ipblock

%files
%defattr(-,root,root)
%doc debian/copyright changelog THANKS
%config(noreplace) %{_sysconfdir}/ipblock.conf
%config(noreplace) %{_sysconfdir}/ipblock.lists
%config(noreplace) %{_sysconfdir}/pam.d/ipblock
%config(noreplace) %{_sysconfdir}/security/console.apps/ipblock
%config(noreplace) %{_sysconfdir}/cron.daily/ipblock
%{_initrddir}/ipblock
%{_sbindir}/iplist
%{_sbindir}/ipblock
%{_bindir}/ipblock
%{_mandir}/man8/iplist.8*
%{_mandir}/man8/ipblock.8*
%{_var}/cache/iplist
%{_javadir}/ipblockUI.jar
%{_datadir}/applications/ipblock.desktop
%{_datadir}/icons/ipblock.png


%changelog
* Tue Apr 19 2011 Jani Välimaa <wally@mandriva.org> 0.29-2mdv2011.0
+ Revision: 655877
- require wget (mdv#63075)
- new version 0.29
- add patch to fix build
- add patch to fix linking, disable strip and use ldflags

* Sun Mar 21 2010 Jani Välimaa <wally@mandriva.org> 0.28-1mdv2010.1
+ Revision: 526170
- import iplist


