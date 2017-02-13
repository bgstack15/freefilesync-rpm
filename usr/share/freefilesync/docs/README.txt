Package source is the official FreefileSync 8.9 offering FreeFileSync_8.9_openSUSE_Tumbleweed.tar.gz
See its changelog.txt for updates to the actual software.
Package maintainer: bgstack15@gmail.com

###Credits
High contrast icon by Freepik http://www.flaticon.com/packs/extended-ui

###How to maintain this package
For the highest chances of downloading the file, save the source tarball to the mirror server.
You need to collect the sha256sum for each tarball and put them in the usr/share/freefilesync/inc/sha256sum.txt file.
####On the mirror server
cd /mnt/mirror/bgscripts/freefilesync
sha256sum *.tar.gz > sha256sum.txt
####On the rpmbuild server
curl http://mirror/bgscripts/freefilesync/sha256sum.txt > ~/rpmbuild/SOURCES/freefilesync-8.9-1/usr/share/freefilesync/inc/sha256sum.txt

###Changelog
2016-12-15 freefilesync 8.7-2
Added a few icons, notably the hicolor and HighContrast themes.
Fixed the GlobalSettings.xml permissions so you can actually save your settings now.
Fixed the uninstall script so in the future upgrading freefilesync (rpm) will not remove your desktop file

2017-02-13 freefilesync 8.9-1
Updated the install-ffs.sh reference to framework.
Added inc/pack script and removed docs/packaging.txt.
