Name:		freefilesync
Version:	8.9
Release:	1
Summary:	FreeFileSync 8.9 for Fedora

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
rm -rf %{buildroot}
rsync -a . %{buildroot}/ --exclude='**/.*.swp'

# Run install script
if test -x %{buildroot}%{_datarootdir}/%{name}/install-ffs.sh;
then
   %{buildroot}%{_datarootdir}/%{name}/install-ffs.sh || exit 1
fi

%clean
rm -rf %{buildroot}

%post
# Deploy icons
which xdg-icon-resource 1>/dev/null 2>&1 && {
   for num in 16 24 32 48 64 128;
   do
      for thistheme in hicolor;
      do
         xdg-icon-resource install --context apps --size "${num}" --theme "${thistheme}" --novendor --noupdate %{_datarootdir}/%{name}/inc/icons/%{name}-${num}.png %{name} &
      done
   done
   for word in HighContrast hicolor;
   do
      test -d %{_datarootdir}/icons/${word} 1>/dev/null 2>&1 && cp -p %{_datarootdir}/%{name}/inc/icons/%{name}-${word}-scalable.svg %{_datarootdir}/icons/${word}/scalable/apps/%{name}.svg
      gtk-update-icon-cache %{_datarootdir}/icons/${word} -q &
   done
   xdg-icon-resource forceupdate &
} 1>/dev/null 2>&1

# Deploy desktop file
desktop-file-install --rebuild-mime-info-cache %{_datarootdir}/%{name}/%{name}.desktop 1>/dev/null 2>&1

%postun
if test "$1" = "0";
then
   # total uninstall

   # Remove desktop file
   rm -f /usr/share/applications/%{name}.desktop >/dev/null 2>&1

   # Remove icons
   which xdg-icon-resource 1>/dev/null 2>&1 && {
      for num in 16 24 32 48 64 128;
      do
         for thistheme in hicolor;
         do
            xdg-icon-resource uninstall --context apps --size "${num}" --theme "${thistheme}" --noupdate %{name}
         done
      done
      for word in HighContrast hicolor;
      do
         rm -f %{_datarootdir}/icons/${word}/scalable/apps/%{name}.svg 
      done
      xdg-icon-resource forceupdate 
   } 1>/dev/null 2>&1
fi 
exit 0

%files
%dir /usr/share/freefilesync
%dir /usr/share/freefilesync/inc
%dir /usr/share/freefilesync/inc/icons
%dir /usr/share/freefilesync/docs
%attr(777, -, -) /usr/share/freefilesync/FreeFileSync
%config %attr(666, -, -) /usr/share/freefilesync/inc/GlobalSettings.xml
/usr/share/freefilesync/inc/scrub.txt
/usr/share/freefilesync/inc/sha256sum.txt
/usr/share/freefilesync/inc/freefilesync_ver.txt
/usr/share/freefilesync/inc/pack
/usr/share/freefilesync/inc/icons/freefilesync-hicolor-scalable.svg
/usr/share/freefilesync/inc/icons/freefilesync-hicolor-128.png
/usr/share/freefilesync/inc/icons/freefilesync-HighContrast-scalable.svg
/usr/share/freefilesync/inc/icons/freefilesync-hicolor-64.png
/usr/share/freefilesync/inc/localize_git.sh
/usr/share/freefilesync/inc/get-files
%attr(666, -, -) /usr/share/freefilesync/freefilesync.desktop
/usr/share/freefilesync/uninstall-ffs.sh
/usr/share/freefilesync/install-ffs.sh
/usr/share/freefilesync/files-for-versioning.txt
%doc %attr(444, -, -) /usr/share/freefilesync/docs/README.txt
/usr/share/freefilesync/docs/freefilesync.spec
/usr/share/freefilesync/docs/files-for-versioning.txt
