%define floppyinject_name vdsm-hook-floppyinject
%define vdsm_name vdsm

Summary: Creating and mounting floppy disk for Red-Hat VDSM
Name: vdsm-hook-floppyinject
Source: %{floppyinject_name}.tar.gz
Version: 1.0
Vendor: Red-Had
Release: 1%{?dist}
License: GPLv2+
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
ExclusiveArch: x86_64
Requires: vdsm

%description
Creating and mounting floppy disk for Red-Hat VDSM

%prep
%setup -c -q

%build

%install
rm -rf $RPM_BUILD_ROOT

make -C %{_builddir}/%{name}-%{version} PREFIX="%{buildroot}" \
    LIBEXECDIR=%{_libexecdir}/%{vdsm_name} \
    install


%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr (755,vdsm,kvm) %{_libexecdir}/vdsm/hooks/before_vm_start/50_floppyinject
%attr (755,vdsm,kvm) %{_libexecdir}/vdsm/hooks/before_vm_migrate_destination/50_floppyinject
%attr (440,root,root) %{_sysconfdir}/sudoers.d/50_vdsm_hook_floppyinject

%post
# update sudoers
tmp_sudoers=$(mktemp)
cp -a /etc/sudoers $tmp_sudoers
/bin/sed -i -e "/# vdsm-hook-floppyinject/,/# end vdsm-hook-floppyinject/d" $tmp_sudoers

cat >> $tmp_sudoers <<EOF
# vdsm-hook-floppyinject customizations
#include /etc/sudoers.d/50_vdsm_hook_floppyinject
# end vdsm-hook-floppyinject customizations
EOF

cp -a $tmp_sudoers /etc/sudoers
rm -f $tmp_sudoers

%postun
if [ "$1" -eq 0 ]; then
    # remove updated qemu.conf
    sed -i '/# by vdsm-hook-floppyinject$/d' /etc/libvirt/qemu.conf

    # remove updated sudoers
    tmp_sudoers=$(mktemp)
    cp -a /etc/sudoers $tmp_sudoers
    /bin/sed -i -e "/# vdsm-hook-floppyinject/,/# end vdsm-hook-floppyinject/d" $tmp_sudoers
    cp -a $tmp_sudoers /etc/sudoers
    rm -f $tmp_sudoers
fi
exit 0

%doc

%changelog
