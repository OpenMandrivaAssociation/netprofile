Name: netprofile
Summary: Manage network profiles
Version: 0.28
Release: %mkrel 6
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


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.28-4mdv2011.0
+ Revision: 666614
- mass rebuild

* Sat Dec 18 2010 Eugeni Dodonov <eugeni@mandriva.com> 0.28-3mdv2011.0
+ Revision: 622769
- Split netprofile modules into subpackages to simplify installation.

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.28-2mdv2011.0
+ Revision: 606822
- rebuild

* Tue Apr 27 2010 Eugeni Dodonov <eugeni@mandriva.com> 0.28-1mdv2010.1
+ Revision: 539657
- 0.28:
- support stopping and starting services when switching profiles
- fix issues when module does not specifies any FILES at all.

* Mon Nov 09 2009 Eugeni Dodonov <eugeni@mandriva.com> 0.27-1mdv2010.1
+ Revision: 463497
- 0.27:
- install missing read-netprofile (#55451)

* Thu Oct 15 2009 Eugeni Dodonov <eugeni@mandriva.com> 0.26-1mdv2010.0
+ Revision: 457782
- 0.26:
- integrate nicely with plymouth
- do not fail on boot if fbgrab is not available (#54471)

* Wed Oct 07 2009 Eugeni Dodonov <eugeni@mandriva.com> 0.25-1mdv2010.0
+ Revision: 455561
- 0.25:
- implemented 'save' and 'load' actions
- implemented 'reset' action
- removed suggests on s2u to reduce basesystem size

* Wed Aug 19 2009 Eugeni Dodonov <eugeni@mandriva.com> 0.24-1mdv2010.0
+ Revision: 418223
- 0.24:
- improve urpmi cache handling on profile switch
- do not show misleading error message on startup

* Tue Aug 18 2009 Eugeni Dodonov <eugeni@mandriva.com> 0.23-1mdv2010.0
+ Revision: 417811
- 0.23
- improved urpmi module to handle /var/lib/urpmi
- implemented user notifications when switching profiles
- correctly reloading net_applet when profiles are changed

* Tue Aug 18 2009 Eugeni Dodonov <eugeni@mandriva.com> 0.22-2mdv2010.0
+ Revision: 417722
- fixed typo in set-netprofile name

* Mon Aug 17 2009 Eugeni Dodonov <eugeni@mandriva.com> 0.22-1mdv2010.0
+ Revision: 417138
- 0.22:
- ensuring variables from different modules are handled properly
- updated documentation
- removed empty save/restore functions from modules where they are not needed

* Fri Aug 14 2009 Eugeni Dodonov <eugeni@mandriva.com> 0.21-1mdv2010.0
+ Revision: 416371
- 0.21:
 - only restart services if they are enabled
 - only remove files from system configuration if they were saved by new profile
 - added urpmi module
 - added git url

* Fri Aug 14 2009 Eugeni Dodonov <eugeni@mandriva.com> 0.20-1mdv2010.0
+ Revision: 416351
- New netprofile.

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.10-4mdv2009.1
+ Revision: 351633
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.10-3mdv2009.0
+ Revision: 223343
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 0.10-2mdv2008.1
+ Revision: 130595
- kill re-definition of %%buildroot on Pixel's request
- fix URL


* Sun Jan 28 2007 Olivier Thauvin <nanardon@mandriva.org> 0.10-2mdv2007.0
+ Revision: 114731
- rebuild

* Tue Dec 06 2005 Frederic Lepied <flepied@mandriva.com> 0.10-1mdk
- add an ifup.d script to be able to switch the profile automatically
if the NETPROFILE variable is set.

* Fri Apr 08 2005 Warly <warly@mandrakesoft.com> 0.9.2-1mdk
- fix background not correctly displayed in silent mode for fbmenu

* Wed Mar 30 2005 Frederic Lepied <flepied@mandrakesoft.com> 0.9.1-1mdk
- fix return code of set-netprofile

* Wed Mar 30 2005 Olivier Blin <oblin@mandrakesoft.com> 0.9-2mdk
- set-netprofile: make net_applet reload the configuration

* Wed Mar 23 2005 Warly <warly@mandrakesoft.com> 0.9-1mdk
- Check for silent bootsplash and use bootsplash image

* Thu Mar 03 2005 Frederic Lepied <flepied@mandrakesoft.com> 0.8-1mdk
- add-to-netprofile: copy a file anyway to all profiles even if the
  file is already under netprofile control with -f option.
- fix a bug when using profile name from kernel command line

* Fri Feb 04 2005 Warly <warly@mandrakesoft.com> 0.7.5-1mk
- new call to fbgrab to dump the background before calling fbmenu

* Fri Jan 21 2005 Warly <warly@mandrakesoft.com> 0.7.4-1mdk
- add call to fbmenu to choose a profile during boot

* Thu Sep 30 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.7.3-1mdk
- back to using previously set profile is none is requested at boot

* Thu Sep 30 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.7.2-1mdk
- set-netprofile:
 o fix bug when changing the hostname at boot (reported by Charles Davant).
 o assume we want the default one if no profile name is
  specified. This allows to avoid setting PROFILE=default in
  lilo.conf.
 o use set_hostname from network-functions to work cleanly with s2u

* Fri Jun 25 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.7.1-1mdk
- use more meaningful names: add-to-netprofile and remove-from-netprofile

* Fri Jun 25 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.7-1mdk
- added add-netprofile and del-netprofile to add/remove a file under
  netprofile management.

* Wed Mar 17 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.6.3-1mdk
- save time, ntp and yp files (bug #7808)

