%define name	iplist
%define version	0.28
%define release	1

Summary:	List based packet handler
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
Source0:	%{name}-%{version}.tar.gz
Patch0:		iplist-0.28-fix-init.patch
License:	GPLv2+
Group:		System/Configuration/Networking
URL:		http://iplist.sourceforge.net/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:	gcc-c++
BuildRequires:	zlib-devel
BuildRequires:	netfilter_queue-devel
BuildRequires:	libpcre-devel
Requires(post):         rpm-helper
Requires(preun):        rpm-helper
Requires:       java >= 1.6
Requires:       usermode-consoleonly
Provides:	ipblock = %{version}-%{release}

%description
iplist is a list based packet handler which uses the netfilter netlink-queue
library (kernel 2.6.14 or later). It filters by IP-address and is optimized
for thousands of IP-address ranges.

%prep
%setup -q
%patch0 -p0

# fix compiler flags
sed -i -e 's|-O2|%{optflags}|' Makefile

%build
%make

%install
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

%post
%_post_service ipblock

%preun
%_preun_service ipblock

%files
%defattr(-,root,root)
%doc debian/copyright changelog ipblock.lists allow.p2p ipblock.conf
%config(noreplace) %{_sysconfdir}/ipblock.conf
%config(noreplace) %{_sysconfdir}/ipblock.lists
%{_sysconfdir}/pam.d/ipblock
%{_sysconfdir}/security/console.apps/ipblock
%{_sysconfdir}/cron.daily/ipblock
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
