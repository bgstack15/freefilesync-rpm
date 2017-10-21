FreeFileSync README
###Readme
Package source is the official FreefileSync offering from the openSUSE Tumbleweed.
See its changelog.txt for updates to the actual software.
Package maintainer: bgstack15@gmail.com

###Credits
High contrast icon by Freepik http://www.flaticon.com/packs/extended-ui

###How to maintain this package
####On the mirror server
Download the latest freefilesync using firefox, while inspecting the network traffic. Find the cdn site.

    # Download the latest application version from:
    cd /mnt/public/www/smith122/repo/rpm/freefilesync
    thisver=9.4
    curl -O -J http://download1053.mediafireuserdownload.com/efawy8dj1uog/nzrklstofjb7xa6/FreeFileSync_9.4_openSUSE_Tumbleweed_64-bit.tar.gz
    # You need to collect the sha256sum for each tarball and put them in the usr/share/freefilesync/inc/sha256sum.txt file.
    sha256sum *.tar.gz > sha256sum.txt

####On the rpmbuild server
curl http://albion320.no-ip.biz/smith122/repo/rpm/freefilesync/sha256sum.txt > ~/rpmbuild/SOURCES/freefilesync-9.4-1/usr/share/freefilesync/inc/sha256sum.txt

###Changelog
2016-12-15 freefilesync 8.7-2
Added a few icons, notably the hicolor and HighContrast themes.
Fixed the GlobalSettings.xml permissions so you can actually save your settings now.
Fixed the uninstall script so in the future upgrading freefilesync (rpm) will not remove your desktop file

2017-02-13 freefilesync 8.9-1
Updated the install-ffs.sh reference to framework.
Added inc/pack script and removed docs/packaging.txt.
Added get-files and redesigned how it scans the files and directories.
Rewrote spec icon deployment to match current design.

* 2017-10-21 Wed B Stack <bgstack15@gmail.com> 9.4-1
- Rearranged directory structure to match current standards
- Updated to latest version
