%global pname FreeFileSync
Name:		freefilesync
Version:	9.4
Release:	2%{?dist}
Summary:	A file synchronization utility

Group:		Applications/File
License:	GPL 3.0 
URL:		http://bgstack15.wordpress.com/
Source0:	freefilesync.tgz
Source1:	https://albion320.no-ip.biz/smith122/repo/patch/%{name}/%{pname}_%{version}_Source.tar.gz
Source2:	https://albion320.no-ip.biz/smith122/repo/patch/%{name}/%{pname}_%{version}%{?dist}.patch

Packager:	Bgstack15 <bgstack15@gmail.com>
Buildarch:	x86_64
BuildRequires:  boost-devel
BuildRequires:  compat-wxGTK3-gtk2-devel
BuildRequires:  gcc-c++
BuildRequires:  gtk3-devel
BuildRequires:  gtk+-devel
BuildRequires:  wxGTK3-devel
BuildRequires:  wxGTK-devel
#Requires:	

%description
FreeFileSync is a fantastic, cross-platform FOSS tool for managing synchronized directories.It is useful for GUI environments and for detailed file comparisons. Rsync is recommended for automated solutions and in headless environments.

#%global debug_package %{nil}

%prep
#%setup -q
%setup -c -n %{name}-%{version}
cd %{name}-%{version}/%{_datadir}/%{name}/source
tar -zxf %{SOURCE1}
cp %{SOURCE2} .
patch -p0 < %{SOURCE2}
sed -i -r -e 's4^(prefix\s*)=\s*%{_prefix}.*4\1= %{_datadir}/%{name}/app%{_prefix}4;' %{pname}/Source/Makefile %{pname}/Source/RealTimeSync/Makefile
cp -p Changelog.txt FreeFileSync/Build/Changelog.txt

%build
%make_build -C %{name}-%{version}/%{_datadir}/%{name}/source/%{pname}/Source
%make_build -C %{name}-%{version}/%{_datadir}/%{name}/source/%{pname}/Source/RealTimeSync

%install
rm -rf %{buildroot}
rsync -av ./freefilesync-9.4/ %{buildroot}/ --exclude='**/.*.swp' --exclude='**/.git'
%make_install -C %{name}-%{version}/%{_datadir}/%{name}/source/%{pname}/Source
%make_install -C %{name}-%{version}/%{_datadir}/%{name}/source/%{pname}/Source/RealTimeSync

# Run install script
#if test -x %{buildroot}%{_datarootdir}/%{name}/inc/install-ffs.sh;
#then
#   %{buildroot}%{_datarootdir}/%{name}/inc/install-ffs.sh || exit 1
#fi

%clean
#rm -rf %{buildroot}
exit 0

%post
# rpm post 2017-02-13

# Initialize config file
ini_source=%{_datarootdir}/%{name}/inc/GlobalSettings.xml
ini_dest=%{_datarootdir}/%{name}/app%{_datarootdir}/FreeFileSync/GlobalSettings.xml
if test -f "${ini_source}";
then
   /bin/cp -p "${ini_source}" "${ini_dest}" 2>/dev/null && { echo "Initialized the config file."; }
fi
chmod 0666 "${ini_source}" "${ini_dest}" 2>/dev/null

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

%preun
# rpm preun 2017-10-24
# Bup config if different from reference ini
{
if test "$1" = "0";
then
   ini_source=%{_datarootdir}/%{name}/inc/GlobalSettings.xml
   ini_dest=%{_datarootdir}/%{name}/app%{_datarootdir}/FreeFileSync/GlobalSettings.xml
   if ! cmp "${ini_dest}" "${ini_source}";
   then
      /bin/cp -p "${ini_dest}" "${ini_dest}.$( date "+%Y-%m-%d" ).uninstalled"
   fi
fi
} 1>/dev/null 2>&1
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
/usr/share/freefilesync/build/get-sources
/usr/share/freefilesync/build/files-for-versioning.txt
%attr(666, -, -) /usr/share/freefilesync/freefilesync.desktop
/usr/share/freefilesync/doc
%attr(777, -, -) /usr/share/freefilesync/app
/usr/share/freefilesync/source
/usr/share/doc/freefilesync/version.txt
%doc %attr(444, -, -) /usr/share/doc/freefilesync/README.txt
/usr/share/doc/freefilesync/REFERENCES.txt

%changelog
* Wed Oct 25 2017 B Stack <bgstack15@gmail.com> 9.4-2
- Updated content. See doc/README.txt
- Now use source instead of precompiled binaries

* Sat Oct 21 2017 B Stack <bgstack15@gmail.com> 9.4-1
- Updated content. See doc/README.txt
- Rearranged directory structure to match current standards
