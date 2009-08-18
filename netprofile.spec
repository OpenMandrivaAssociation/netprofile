Name: netprofile
Summary: Manage network profiles
Version: 0.23
Release: %mkrel 1
Source: %{name}-%{version}.tar.bz2
License: GPLv2+
Group: System/Base
BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: initscripts >= 7.06-13mdk
Requires: diffutils
Suggests: s2u >= 0.9.1
URL: http://git.mandriva.com/?p=projects/netprofile.git

%description
Netprofile is a Mandriva solution to manage different network profile. It
allows to define specific network, firewall and proxy configuration to use in
different network environment (for example, at home, at work or while roaming),
and also provides a way for user to switch those profiles on the fly.

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
%attr(0755,root,root) /etc/netprofile/modules/*
/etc/bash_completion.d/netprofile
/etc/sysconfig/network-scripts/ifup.d/netprofile


