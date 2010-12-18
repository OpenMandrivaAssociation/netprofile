Name: netprofile
Summary: Manage network profiles
Version: 0.28
Release: %mkrel 3
Source: %{name}-%{version}.tar.bz2
License: GPLv2+
Group: System/Base
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: initscripts >= 7.06-13mdk
Requires: diffutils
# s2u is used for desktop notifications. It will be pulled by xinit
# to reduce basesystem size
#Suggests: s2u >= 0.9.1
URL: http://git.mandriva.com/?p=projects/netprofile.git
Suggests: %{name}-plugin-services, %{name}-plugin-network, %{name}-plugin-firewall
Suggests: %{name}-plugin-proxy, %{name}-plugin-urpmi

%description
Netprofile is a Mandriva solution to manage different network profile. It
allows to define specific network, firewall and proxy configuration to use in
different network environment (for example, at home, at work or while roaming),
and also provides a way for user to switch those profiles on the fly.

%package plugin-services
Summary:	service management plugin for netprofile
Group: 		System/Base
Requires:	netprofile >= 0.28-3

%description plugin-services
This plugin allows netprofile to save and restore the list of running services
when changing to a different profile.

%package plugin-network
Summary:	network configuration plugin for netprofile
Group: 		System/Base
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
rm -rf $RPM_BUILD_ROOT
%makeinstall_std INITDIR=%_initrddir

%clean
rm -rf $RPM_BUILD_ROOT

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
%defattr(-,root,root) 
%doc ChangeLog TODO README NEWS
/sbin/*
%dir /etc/netprofile
%dir /etc/netprofile/profiles
%dir /etc/netprofile/modules
/etc/bash_completion.d/netprofile
/etc/sysconfig/network-scripts/ifup.d/netprofile

%files plugin-services
%defattr(-,root,root)
%attr(0755,root,root) /etc/netprofile/modules/*_services

%files plugin-network
%defattr(-,root,root)
%attr(0755,root,root) /etc/netprofile/modules/*_network

%files plugin-firewall
%defattr(-,root,root)
%attr(0755,root,root) /etc/netprofile/modules/*_firewall*

%files plugin-proxy
%defattr(-,root,root)
%attr(0755,root,root) /etc/netprofile/modules/*_proxy

%files plugin-urpmi
%defattr(-,root,root)
%attr(0755,root,root) /etc/netprofile/modules/*_urpmi
