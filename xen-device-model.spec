Summary: qemu-dm device model
Name: xen-device-model
Version: 0.10.2.xs
Release: 1
License: GPL
Source0: http://hg.uk.xensource.com/git/carbon/%{branch}/qemu-trad.git/snapshot/refs/heads/master#/%{name}.tar.gz
BuildRequires: zlib-devel, xen-libs-devel, xen-dom0-libs-devel, pciutils-devel, libpciaccess-devel, check-devel, libdrm-devel
BuildRequires: ncurses-devel
Requires(pre): shadow-utils
Requires: libdrm
Provides: qemu-xen(syslog) = 1

%description
This package contains qemu-dm, the Xen device model.

%prep
%autosetup -p1

%build
./xen-setup --disable-opengl --disable-vnc-tls --disable-blobs --disable-sdl --enable-werror
%{?cov_wrap} %{__make}
%{__make} unittests

%install
rm -rf %{buildroot}
%{?cov_wrap} %{__make} install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/var/xen/qemu

# CA-157601 - Leave Qemu where xenops expects to find it until qemu-dm-wrapper can be fixed
mkdir -p %{buildroot}%{_libdir}/xen/bin/
ln %{buildroot}%{_libexecdir}/xen/bin/qemu-dm %{buildroot}%{_libdir}/xen/bin/qemu-dm

%pre
/usr/bin/getent passwd qemu >/dev/null 2>&1 || /usr/sbin/useradd \
    -M -U -r \
    -s /sbin/nologin \
    -d / \
    qemu >/dev/null 2>&1 || :
/usr/bin/getent passwd qemu_base >/dev/null 2>&1 || /usr/sbin/useradd \
    -M -U -r \
    -s /sbin/nologin \
    -d / \
    -u 65535 \
    qemu_base >/dev/null 2>&1 || :

%files
%doc COPYING COPYING.LIB LICENSE MAINTAINERS README
%{_libexecdir}/xen/bin/qemu-dm
# CA-157601 - Leave Qemu where xenops expects to find it until qemu-dm-wrapper can be fixed
%{_libdir}/xen/bin/qemu-dm
%{_datadir}/xen/qemu/keymaps
%exclude /etc/xen/scripts/qemu-ifup
%dir /var/xen/qemu

%changelog
