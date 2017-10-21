Name:		freefilesync
Version:	9.4
Release:	1
Summary:	FreeFileSync 8.9 for Fedora

Group:		Applications/File
License:	GPL 3.0 
URL:		http://bgstack15.wordpress.com/
Source0:	freefilesync.tgz

Packager:	Bgstack15 <bgstack15@gmail.com>
Buildarch:	x86_64
#BuildRequires:	
#Requires:	

%description
FreeFileSync is a fantastic, cross-platform FOSS tool for managing synchronized directories.It is useful for GUI environments and for detailed file comparisons. Rsync is recommended for automated solutions and in headless environments.

#%global debug_package %{nil}

%prep
#%setup -q
%setup

%build

%install
#%make_install
rm -rf %{buildroot}
rsync -a . %{buildroot}/ --exclude='**/.*.swp' --exclude='**/.git'

# Run install script
if test -x %{buildroot}%{_datarootdir}/%{name}/inc/install-ffs.sh;
then
   %{buildroot}%{_datarootdir}/%{name}/inc/install-ffs.sh || exit 1
fi

%clean
rm -rf %{buildroot}

%post
# rpm post 2017-02-13
# Deploy icons
which xdg-icon-resource 1>/dev/null 2>&1 && {

   # Deploy default application icons
   for theme in hicolor HighContrast;
   do

      # Deploy scalable application icons
      cp -p %{_datarootdir}/%{name}/inc/icons/%{name}-${theme}-scalable.svg %{_datarootdir}/icons/${theme}/scalable/apps/freefilesync.svg

      # Deploy size application icons
      for size in 64 128;
      do
         xdg-icon-resource install --context apps --size "${size}" --theme "${theme}" --novendor --noupdate %{_datarootdir}/%{name}/inc/icons/%{name}-${theme}-${size}.png freefilesync &
      done
   done

   # Deploy custom application icons
   # none

   # Update icon caches
   xdg-icon-resource forceupdate &
   for word in hicolor HighContrast;
   do
      touch --no-create %{_datarootdir}/icons/${word}
      gtk-update-icon-cache %{_datarootdir}/icons/${word} &
   done

} 1>/dev/null 2>&1

# Deploy desktop file
desktop-file-install --rebuild-mime-info-cache %{_datarootdir}/%{name}/%{name}.desktop 1>/dev/null 2>&1

exit 0

%postun
# rpm postun 2017-02-13
if test "$1" = "0";
then
{
   # total uninstall

   # Remove desktop file
   rm -f %{_datarootdir}/applications/%{name}.desktop
   which update-desktop-database && update-desktop-database -q %{_datarootdir}/applications &

   # Remove icons
   which xdg-icon-resource && {

      # Remove default application icons
      for theme in hicolor HighConstrast;
      do

         # Remove scalable application icons
         rm -f %{_datarootdir}/icons/${theme}/scalable/apps/freefilesync.svg

         # Remove size application icons
         for size in 64 128;
         do
            xdg-icon-resource uninstall --context apps --size "${size}" --theme "${theme}" --noupdate freefilesync &
         done

      done

      # Update icon caches
      xdg-icon-resource forceupdate &
      for word in hicolor HighContrast;
      do
         touch --no-create %{_datarootdir}/icons/${word}
         gtk-update-icon-cache %{_datarootdir}/icons/${word} &
      done

   }
} 1>/dev/null 2>&1
fi 
exit 0

%files
%dir /usr/share/freefilesync
%dir /usr/share/freefilesync/inc
%dir /usr/share/freefilesync/inc/icons
%dir /usr/share/freefilesync/build
/usr/share/freefilesync/inc/install-ffs.sh
/usr/share/freefilesync/inc/sha256sum.txt
/usr/share/freefilesync/inc/freefilesync_ver.txt
%config %attr(666, -, -) /usr/share/freefilesync/inc/GlobalSettings.xml
/usr/share/freefilesync/inc/icons/freefilesync-hicolor-scalable.svg
/usr/share/freefilesync/inc/icons/freefilesync-HighContrast-scalable.svg
/usr/share/freefilesync/inc/icons/freefilesync-hicolor-64.png
/usr/share/freefilesync/inc/icons/freefilesync-hicolor-128.png
/usr/share/freefilesync/inc/uninstall-ffs.sh
/usr/share/freefilesync/build/scrub.txt
/usr/share/freefilesync/build/freefilesync.spec
/usr/share/freefilesync/build/localize_git.sh
/usr/share/freefilesync/build/pack
/usr/share/freefilesync/build/get-files
/usr/share/freefilesync/build/files-for-versioning.txt
%attr(666, -, -) /usr/share/freefilesync/freefilesync.desktop
/usr/share/freefilesync/doc
%attr(777, -, -) /usr/share/freefilesync/FreeFileSync
/usr/share/doc/freefilesync/version.txt
%doc %attr(444, -, -) /usr/share/doc/freefilesync/README.txt

%changelog
* Sat Oct 21 2017 B Stack <bgstack15@gmail.com> 9.4-1
- Updated content. See doc/README.txt
- Rearranged directory structure to match current standards
