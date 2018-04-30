%global pname FreeFileSync
%define dummy_package   0
Name:		freefilesync
Version:	10.0
Release:	1%{?dist}
Summary:	A file synchronization utility

Group:	Applications/File
License:	GPL 3.0 
URL:		http://bgstack15.wordpress.com/
Source0:	freefilesync.tgz
Source1:	https://www.freefilesync.org/download/%{pname}_%{version}_Source.zip
Source2:	https://albion320.no-ip.biz/smith122/repo/patch/%{name}/%{pname}_%{version}-1%{?dist}.patch
Source3: https://astuteinternet.dl.sourceforge.net/project/xbrz/xBRZ/xBRZ_1.6.zip

Packager:	Bgstack15 <bgstack15@gmail.com>
Buildarch:	x86_64
BuildRequires:  boost-devel
BuildRequires:  compat-wxGTK3-gtk2-devel
BuildRequires:  gcc-c++
BuildRequires:  gtk3-devel
BuildRequires:  gtk+-devel
BuildRequires:  wxGTK3-devel
BuildRequires:  wxGTK-devel
BuildRequires:  /usr/bin/7za
BuildRequires:  webkitgtk4-devel
#Requires:	

%description
FreeFileSync is a fantastic, cross-platform FOSS tool for managing synchronized directories.It is useful for GUI environments and for detailed file comparisons. Rsync is recommended for automated solutions and in headless environments.

# %global debug_package %{nil}

%prep
#%setup -q
%setup -c
mv %{name}-%{version}/* . ; cd .%{_datadir}/%{name}/source
#tar -zxf %{SOURCE1}
/usr/bin/7za x %{SOURCE1}
cp %{SOURCE2} .
patch -p1 < %{SOURCE2}

# Fetch the extra lib that was not included by upstream but is required to build
# assuming pwd is .%{_datadir}/%{name}/source
mkdir -p xBRZ/src ; pushd xBRZ/src
/usr/bin/7za x %{SOURCE3}
popd

# Make the installed location the custom directory for this package
sed -i -r -e 's@^(prefix\s*)=\s*%{_prefix}.*@\1= %{_datadir}/%{name}/app%{_prefix}@;' %{pname}/Source/Makefile %{pname}/Source/RealTimeSync/Makefile

# Do some misc cleanup
cp -p Changelog.txt FreeFileSync/Build/Changelog.txt
ls -l %{pname}/Source/Makefile
sed \
  -e '/CXXFLAGS/s|-O3|-D"warn_static(arg)= " -DZEN_LINUX %{optflags}|g' \
  -e '/LINKFLAGS/s|-s|%{__global_ldflags}|g' \
  -i %{pname}/Source/Makefile %{pname}/Source/RealTimeSync/Makefile

%build
%make_build -C .%{_datadir}/%{name}/source/%{pname}/Source
%make_build -C .%{_datadir}/%{name}/source/%{pname}/Source/RealTimeSync

%install
rm -rf %{buildroot}
rsync -av ./ %{buildroot}/ --exclude='**/.*.swp' --exclude='**/.git'
%make_install -C .%{_datadir}/%{name}/source/%{pname}/Source
%make_install -C .%{_datadir}/%{name}/source/%{pname}/Source/RealTimeSync

# this is basically like a make_clean I guess. If you want the source code provided in the package, comment this line.
find %{buildroot}%{_datadir}/%{name}/source -mindepth 1 ! -regex '.*.patch' -exec rm -rf {} \; 2>/dev/null || :

# Solve the readme problem
#  echo "all README.md files"
#  find %{buildroot} -name 'README.md' || :
#  echo "THE CORRECT SEARCH"
#  find %{buildroot} -maxdepth 1 -name 'README.md' -type l || :
find %{buildroot} -maxdepth 1 -name 'README.md' -type l -exec unlink {} \; 2>%{devtty} || :

exit 0

%clean
rm -rf %{buildroot}
exit 0

%post
# rpm post 2018-03-18

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
   for theme in hicolor HighContrast ;
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
   for word in hicolor HighContrast ;
   do
      touch --no-create %{_datarootdir}/icons/${word}
      gtk-update-icon-cache %{_datarootdir}/icons/${word} &
   done

} 1>/dev/null 2>&1

# Deploy desktop file
desktop-file-install --rebuild-mime-info-cache %{_datarootdir}/%{name}/%{name}.desktop 1>/dev/null 2>&1

# Add mimetype and set default application
# NONE see bgscripts or palemoon-rpm for examples

exit 0

%preun
# rpm preun 2018-03-18
if test "$1" = "0" ;
then
{
   # total uninstall

   # Bup config if different from reference ini
   ini_source=%{_datarootdir}/%{name}/inc/GlobalSettings.xml
   ini_dest=%{_datarootdir}/%{name}/app%{_datarootdir}/FreeFileSync/GlobalSettings.xml
   if ! cmp "${ini_dest}" "${ini_source}";
   then
      /bin/cp -p "${ini_dest}" "${ini_dest}.$( date "+%Y-%m-%d" ).uninstalled"
   fi

   # Remove mimetype definitions
   # NONE

   # Remove systemd files
   # NONE

   # Remove desktop file
   rm -f %{_datarootdir}/applications/%{name}.desktop
   which update-desktop-database && update-desktop-database -q %{_datarootdir}/applications &

   # Remove icons
   which xdg-icon-resource && {

      # Remove default application icons
      for theme in hicolor HighContrast ;
      do

         # Remove scalable application icons
         rm -f %{_datarootdir}/icons/${theme}/scalable/apps/freefilesync.svg

         # Remove size application icons
         for size in 64 128;
         do
            xdg-icon-resource uninstall --context apps --size "${size}" --theme "${theme}" --noupdate freefilesync &
         done

      done

      # Remove custom application icons
      # NONE

      # Remove default mimetype icons
      # NONE

      # Remove custom mimetype icons
      # NONE

      # Update icon caches
      xdg-icon-resource forceupdate &
      for word in hicolor HighContrast ;
      do
         touch --no-create %{_datarootdir}/icons/${word}
         gtk-update-icon-cache %{_datarootdir}/icons/${word} &
      done

   }

} 1>/dev/null 2>&1
fi
exit 0

%postun
# rpm postun 2018-03-18
exit 0

%files
%dir /usr/share/freefilesync
%dir /usr/share/freefilesync/build
%dir /usr/share/freefilesync/inc
%dir /usr/share/freefilesync/inc/icons
%doc %attr(444, -, -) /usr/share/doc/freefilesync/README.md
/usr/share/doc/freefilesync/REFERENCES.txt
/usr/share/doc/freefilesync/version.txt
/usr/share/freefilesync/app
/usr/share/freefilesync/app/.keep
/usr/share/freefilesync/build/files-for-versioning.txt
/usr/share/freefilesync/build/freefilesync.spec
/usr/share/freefilesync/build/get-files
/usr/share/freefilesync/build/get-sources
/usr/share/freefilesync/build/pack
/usr/share/freefilesync/doc
%attr(666, -, -) /usr/share/freefilesync/freefilesync.desktop
/usr/share/freefilesync/inc/freefilesync_ver.txt
%config %attr(666, -, -) /usr/share/freefilesync/inc/GlobalSettings.xml
/usr/share/freefilesync/inc/icons/freefilesync-hicolor-128.png
/usr/share/freefilesync/inc/icons/freefilesync-hicolor-64.png
/usr/share/freefilesync/inc/icons/freefilesync-hicolor-scalable.svg
/usr/share/freefilesync/inc/icons/freefilesync-HighContrast-scalable.svg
/usr/share/freefilesync/inc/install-ffs.sh
/usr/share/freefilesync/inc/sha256sum.txt
/usr/share/freefilesync/inc/uninstall-ffs.sh
/usr/share/freefilesync/source

%changelog
* Mon Apr 30 2018 B Stack <bgstack15@gmail.com> 10.0-1
- Rpm built. See doc/README.md.
