#!/bin/sh
# File: /usr/share/freefilesync/uninstall-ffs.sh
# Author: bgstack15
# Startdate: 2016-11-29 08:58
# Title: Script that uninstalls irfanview
# Purpose: Removes the software that was downloaded and installed
# Package: freefilesync
# History:
# Usage: Generally available. Not needed by the rpm specifically.
# Reference: 
#    uninstall-irfanview.sh
# Improve:

# Definitions
package="freefilesync"
infile=${RPM_BUILD_ROOT}/usr/share/${package}/inc/${package}_ver.txt
outdir=${RPM_BUILD_ROOT}/usr/share/${package}
pver="" # dynamically defined by /usr/share/${package}/inc/${package}_ver.txt
temp_sw=${RPM_BUILD_ROOT}/usr/share/${package}/source/ffs.tgz
ini_source=/usr/share/${package}/inc/GlobalSettings.xml
ini_dest=/usr/share/${package}/FreeFileSync/GlobalSettings.xml

# Bup config if different from reference ini
if ! cmp "${ini_dest}" "${ini_source}" 2>/dev/null;
then
   /bin/cp -p "${ini_source}" "${ini_dest}.$( date "+%Y-%m-%d" ).uninstalled" 2>/dev/null
fi

# Remove software directory
rm -rf "${outdir:-NOTHINGTODEL}/FreeFileSync" 2>/dev/null && mkdir "${outdir}" 2>/dev/null;

# Provide final status notification
echo "${package} successfully removed."
exit 0
