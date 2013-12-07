Summary:	Manage network profiles
Name:		netprofile
Version:	0.28
Release:	11
License:	GPLv2+
Group:		System/Base
Url:		http://git.mandriva.com/?p=projects/netprofile.git
Source0:	%{name}-%{version}.tar.bz2
BuildArch:	noarch
Requires:	diffutils
Requires:	initscripts
Requires(post):	dbus
# s2u is used for desktop notifications. It will be pulled by xinit
# to reduce basesystem size
#Suggests:	s2u >= 0.9.1
Suggests:	%{name}-plugin-firewall
Suggests:	%{name}-plugin-network
Suggests:	%{name}-plugin-proxy
Suggests:	%{name}-plugin-services
Suggests:	%{name}-plugin-urpmi

%description
Netprofile is a Mandriva solution to manage different network profile. It
allows to define specific network, firewall and proxy configuration to use in
different network environment (for example, at home, at work or while roaming),
and also provides a way for user to switch those profiles on the fly.

%package plugin-services
Summary:	service management plugin for netprofile
Group:		System/Base
Requires:	netprofile >= 0.28-3

%description plugin-services
This plugin allows netprofile to save and restore the list of running services
when changing to a different profile.

%package plugin-network
Summary:	network configuration plugin for netprofile
Group:		System/Base
Requires:	netprofile >= 0.28-3

%description plugin-network
This plugin allows netprofile to save and restore network settings saved in
redhat and mandriva-compatible format.

%package plugin-firewall
Summary:	firewall configuration plugin for netprofile
Group:		System/Base
Requires:	netprofile >= 0.28-3

%description plugin-firewall
This plugin allows netprofile to save and restore firewall configuration based
on iptables shorewall applications.

%package plugin-proxy
Summary:	proxy configuration plugin for netprofile
Group:		System/Base
Requires:	netprofile >= 0.28-3

%description plugin-proxy
This plugin allows netprofile to save and restore local proxy settings.

%package plugin-urpmi
Summary:	urpmi configuration plugin for netprofile
Group:		System/Base
Requires:	netprofile >= 0.28-3

%description plugin-urpmi
This plugin allows netprofile to save and restore multiple configurations
for urpmi database.

%prep
%setup -q

%install
%makeinstall_std INITDIR=%{_initrddir}

%post
# checking for old netprofile files
if [ -f /etc/netprofile/list ]; then
        # upgrading from old netprofile
        echo "Upgrading from old netprofile. Your old profiles are saved in /etc/netprofile.rpmsave"
        # temporarily, save old files. This will be removed on newer versions.
        mkdir /etc/netprofile.rpmsave && cp -a /etc/netprofile/list /etc/netprofile/profiles /etc/netprofile.rpmsave
        rm -rf /etc/netprofile/profiles/*/
        # creating new default profile
        /sbin/netprofile switch default
fi

if [ ! -d /etc/netprofile/profiles/default ]; then
  /sbin/set-netprofile default
fi

%files
%doc ChangeLog TODO README NEWS
/sbin/*
%dir /etc/netprofile
%dir /etc/netprofile/profiles
%dir /etc/netprofile/modules
/etc/bash_completion.d/netprofile
/etc/sysconfig/network-scripts/ifup.d/netprofile

%files plugin-services
%attr(0755,root,root) /etc/netprofile/modules/*_services

%files plugin-network
%attr(0755,root,root) /etc/netprofile/modules/*_network

%files plugin-firewall
%attr(0755,root,root) /etc/netprofile/modules/*_firewall*

%files plugin-proxy
%attr(0755,root,root) /etc/netprofile/modules/*_proxy

%files plugin-urpmi
%attr(0755,root,root) /etc/netprofile/modules/*_urpmi

