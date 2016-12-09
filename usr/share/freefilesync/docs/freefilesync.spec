Name:		freefilesync
Version:	8.7
Release:	1
Summary:	FreeFileSync 8.7 for Fedora

Group:		Applications/File
License:	GPL 3.0 
URL:		http://bgstack15.wordpress.com
Source0:	freefilesync.tgz

Packager:	Bgstack15 <bgstack15@gmail.com>
Buildarch:	x86_64
#BuildRequires:	
#Requires:	

%description
FreeFileSync is a fantastic, cross-platform FOSS tool for managing synchronized directories.

#%global debug_package %{nil}

%prep
#%setup -q
%setup

%build

%install
#%make_install
rsync -a . %{buildroot}/
if test -x %{buildroot}%{_datarootdir}/%{name}/install-ffs.sh;
then
   %{buildroot}%{_datarootdir}/%{name}/install-ffs.sh || exit 1
fi

%clean
rm -rf %{buildroot}

%post
# Deploy desktop file
desktop-file-install --rebuild-mime-info-cache %{_datarootdir}/%{name}/%{name}.desktop 1>/dev/null 2>&1

%postun
rm -f /usr/share/applications/freefilesync.desktop >/dev/null 2>&1

%changelog

%files
/usr
/usr/share
/usr/share/freefilesync
/usr/share/freefilesync/inc
/usr/share/freefilesync/inc/freefilesync_ver.txt
/usr/share/freefilesync/inc/sha256sum.txt
/usr/share/freefilesync/inc/scrub.txt
%config %attr(666, -, -) /usr/share/freefilesync/inc/GlobalSettings.xml
/usr/share/freefilesync/inc/localize_git.sh
/usr/share/freefilesync/uninstall-ffs.sh
%attr(555, -, -) /usr/share/freefilesync/FreeFileSync
%attr(666, -, -) /usr/share/freefilesync/freefilesync.desktop
/usr/share/freefilesync/files-for-versioning.txt
/usr/share/freefilesync/install-ffs.sh
/usr/share/freefilesync/docs
%doc %attr(444, -, -) /usr/share/freefilesync/docs/packaging.txt
%doc %attr(444, -, -) /usr/share/freefilesync/docs/README.txt
/usr/share/freefilesync/docs/freefilesync.spec
