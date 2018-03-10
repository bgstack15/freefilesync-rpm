# Readme for FreeFileSync rpm
FreeFileSync is a cross-platform utility for synchronizing directories and files. It is open-source, but the developers do not provide an official rpm so here is my attempt at it.

Visit the FreeFileSync homepage at [https://www.freefilesync.org/](https://www.freefilesync.org/).

# Unique characteristics of this package
My packages tend to wrap the whole application inside the /usr/share/%{name}/app directory. I like to keep it all self-contained on my filesystem.

# Using FreeFileSync
Its main feature is the GUI application, but batch jobs are also possible. See the FreeFileSync homepage for details of how to use the program.

# Building this package
A build dependency is my [bgscripts](https://github.com/bgstack15/bgscripts) package.

Download this wrapper package source and run the pack utility.

    package=freefilesync
    thisver=9.9-1
    mkdir -p ~/rpmbuild/{SOURCES,RPMS,SPECS,BUILD,BUILDROOT}
    cd ~/rpmbuild/SOURCES
    git clone https://github.com/bgstack15/freefilesync-rpm "${package}-${thisver}"
    cd "${package}-${thisver}"
    usr/share/freefilesync/build/pack rpm

The build script will fetch the official source from its homepage and check it against its sha256sum in file [usr/share/freefilesync/inc/sha256sum.txt](usr/share/freefilesync/inc/sha256sum.txt).

The generated rpm will be in ~/rpmbuild/RPMS/x86_64 (for the x86_64 architecture, of course).

# Maintaining this package

## On the mirror server
For a new release from upstream, download the latest source using Firefox while inspecting the network traffic. Find the cdn site to use, so you can script it here.

    # Download the latest source from:
    cd /mnt/public/www/smith122/repo/patch/freefilesync
    thisver=9.9
    curl -O -J http://download1053.mediafireuserdownload.com/efawy8dj1uog/nzrklstofjb7xa6/FreeFileSync_${thisver}_Source.zip
    # Assemble patch file for each architecture (fc27, el7, etc.)
    # Collect the sha256sum for each source object (tarball, patch, etc.).
    sha256sum *.tar.gz *.tgz *.zip *.patch 1> sha256sum.txt 2>/dev/null

## On the rpmbuild server
For a new version release, download the latest sha256sum file from the maintainer server. Then pull up the list of files that need to be manually updated for version numbers.

    package=freefilesync
    thisver=9.9-0
    cd ~/rpmbuild/SOURCES/${package}-${thisver}/usr/share/${package}
    curl "http://albion320.no-ip.biz/smith122/repo/patch/${package}/sha256sum.txt" > ./inc/sha256sum.txt
    vi $( cat build/files-for-versioning.txt )

# Authors
**FreeFileSync:** Zenju [https://www.freefilesync.org/](https://www.freefilesync.org/)
**Rpm maintainer:** Bgstack15 [https://bgstack15.wordpress.com](https://bgstack15.wordpress.com)

# License
The rpm elements by bgstack15 are [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

# Credits
High contrast icon by [Freepik](http://www.flaticon.com/packs/extended-ui)

# Bugs

# References
See [References.txt](usr/share/doc/freefilesync/References.txt)

# Changelog
2016-12-15 freefilesync 8.7-2
Added a few icons, notably the hicolor and HighContrast themes.
Fixed the GlobalSettings.xml permissions so you can actually save your settings now.
Fixed the uninstall script so in the future upgrading freefilesync (rpm) will not remove your desktop file

2017-02-13 freefilesync 8.9-1
Updated the install-ffs.sh reference to framework.
Added inc/pack script and removed docs/packaging.txt.
Added get-files and redesigned how it scans the files and directories.
Rewrote spec icon deployment to match current design.

* 2017-10-21 Sat B Stack <bgstack15@gmail.com> 9.4-1
- Rearranged directory structure to match current standards
- Updated to latest version

* Wed Oct 25 2017 B Stack <bgstack15@gmail.com> 9.4-2
- Built from source now!

* Sat Jan  6 2018 B Stack <bgstack15@gmail.com> 9.4-3
- Fix listBoxHistory to reduce application crashes
- Update get-sources to work with alternate URLS with custom definitions

* Thu Jan 10 2018 B Stack <bgstack15@gmail.com> 9.6-1
- Version bump from upstream

* Sat Jan 13 2018 B Stack <bgstack15@gmail.com> 9.7-1
- Version bump from upstream

* Sat Mar 10 2018 B Stack <bgstack15@gmail.com> 9.9-1
- Version bump from upstream
- Rearrange package and documentation to current standards
