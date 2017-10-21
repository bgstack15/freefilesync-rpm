#!/bin/sh -x
# File: /usr/share/freefilesync/install-ffs.sh
# Author: bgstack15
# Startdate: 2016-11-28 10:46
# Title: Script that Installs freefilesync
# Purpose: Downloads and installs freefilesync from official source
# Package: freefilesync
# History: 
#    2017-02-13 updated bgscripts reference
#    2017-10-21 updated for albion320.no-ip.biz location
# Usage: Is used during the rpm build phase. It is also generally available.
# Reference: irfan-4.42-6 file /usr/share/irfan/install-irfanview.sh
# Improve:

# Definitions
package="freefilesync"
infile=${RPM_BUILD_ROOT}/usr/share/${package}/inc/${package}_ver.txt
outdir=${RPM_BUILD_ROOT}/usr/share/${package}
pver="" # dynamically defined by /usr/share/${package}/inc/${package}_ver.txt
temp_sw=${RPM_BUILD_ROOT}/usr/share/${package}/source/ffs.tgz
ini_source=${RPM_BUILD_ROOT}/usr/share/${package}/inc/GlobalSettings.xml
ini_dest=${RPM_BUILD_ROOT}/usr/share/${package}/FreeFileSync/GlobalSettings.xml
sha256sumfile=${RPM_BUILD_ROOT}/usr/share/${package}/inc/sha256sum.txt
sourcefile="" # Defined later. Look it up.

# Functions
getsource() {
   # call: getsource http://sourcefile /tmp/destfile
   # will be fatal failure
   # will check the sha256sum file to ensure good download
   _gssource="${1}"
   _gstemp="${2}"
   echo "Fetching ${_gssource}"
   # get published sha256sum of good file
   _tmp=$( echo "${_gssource}" | sed -e 's!^.*\/!!' )
   _goodsha=$( awk "\$2 == \"${_tmp}\" {print;}" ${sha256sumfile} 2>/dev/null | cut -d' ' -f1 )
   touch "${_gstemp}" 2>/dev/null || { echo "Cannot modify ${_gstemp}. Run as root, perhaps. Aborted."; exit 1; }
   _attempts=0
   _state="";
   while test ${_attempts} -le 5;
   do
      curl "${_gssource}" --progress-bar --refer "${_gssource}" > "${_gstemp}"
      # verify good download
      if ! test -f "${_gstemp}" || test "$( stat -c "%s" "${_gstemp}" 2>/dev/null)" -lt 1000 || ! test "$( sha256sum "${_gstemp}" | cut -d' ' -f1 )" = "${_goodsha}";
      then
         case "${_attempts}" in
            #1) . ~/.bashrc 1>/dev/null 2>&1;; # was breaking weirdly on some interal definition
            2) test "$( ps -p $$ | xargs | awk '{print $NF}')" = "bash" && test -x /usr/bin/bp && . /usr/bin/bp --noclear --noglobalprofile 1>/dev/null 2>&1;;
            3) unset http_proxy; unset https_proxy; _gssource=$( echo "${_gssource}" | sed -e 's!'"${source1search}"'!'"${source1replace}"'!;' 2>/dev/null );;
            5) echo "File failed to download: ${_gssource}. Aborted." && exit 1;;
         esac
      else
         break
      fi
      _attempts=$(( _attempts + 1 ))
   done
}

extract() {
   # determine if tgz/tar.gz or other (use 7zip)
   # call: extract "${outdir}" -y "${temp_sw}"
   # available vars: ${command_7z}
   _outdir="${1}"
   _y="${2}" # should be a dash y
   _temp_sw="${3}"
   case "${_temp_sw##*.}" in
      tar|gz|tgz) # use tar -zxf
         tar -zx -C "${_outdir}" -f "${_temp_sw}"
         ;;
      *) # use command_7z
         ${command_7z} x -o"${_outdir}" "${_y}" "${_temp_sw}"
         ;;
   esac
}

# Ensure target directories exists
if ! test -d "${outdir}/source";
then
   mkdir -p "${outdir}/source" || { echo "Unable to make directory ${outdir}. Aborted."; exit 1; }
fi

# Get software version to install.
if ! test -f "${infile}";
then
   echo "Is ${package} package installed? Check ${infile}. Aborted."
   exit 1
fi
while read line;
do
   line=$( echo "${line}" | sed -e 's/^\s*//;s/\s*$//;/^[#$]/d;s/\s*[^\]#.*$//;' )
   if test -n "${line}";
   then
      echo "Config file reports version number ${line}."
      pver="${line}"
   fi
done < "${infile}"
# tmp1=$( echo "${pver}" | tr -d '.' ) # in case the source file needs the dot removed
sourcefile="https://www.freefilesync.org/download/FreeFileSync_${pver}_openSUSE_Tumbleweed_64-bit.tar.gz"
source1search='\(www\.\)\?freefilesync\.org\/download'
source1replace='albion320\.no-ip\.biz\/smith122\/repo\/rpm\/freefilesync'

# Check dependencies
if ! test -x "$( which curl 2>/dev/null)";
then
      # try wget maybe?
   echo "Please install curl. Aborted."
   exit 1
fi
command_7z=""
if ! test -x "$( which 7z 2>/dev/null)";
then
   if ! test -x "$( which 7za 2>/dev/null)";
   then
      # try wget maybe?
      echo "Please install 7zip. Try package p7zip. Aborted."
      exit 1
   else
      command_7z="$( which 7za 2>/dev/null)";
   fi
else
   # 7z is valid
   command_7z="$( which 7z 2>/dev/null)";
fi

# Fetch software source itself
getsource "${sourcefile}" "${temp_sw}"

# Extract software
echo "Extracting ${package}."
extract "${outdir}" -y "${temp_sw}" 1>/dev/null 2>&1 && rm -rf "${temp_sw}" "${temp_sw%%.*z}.tar" 2>/dev/null || { echo "Unable to extract for some reason. Aborted."; exit 1; }

# Adjust permissions on the directories
#chmod -R 0755 "${outdir}/Plugins" "${outdir}/Languages" "${outdir}/Toolbars"

# Initialize config file
if test -f "${ini_source}";
then
   /bin/cp -p "${ini_source}" "${ini_dest}" 2>/dev/null && { echo "Initialized the config file."; }
fi
chmod 0666 "${ini_source}" "${ini_dest}" 2>/dev/null

# Provide final status notification
echo "${package} ${pver} successfully installed."
exit 0
