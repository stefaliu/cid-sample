#!/usr/bin/python

import sys
import os
import shutil


# init variables
script_path = sys.path[0]
# TODO check script path's availability

root_path = os.path.join(script_path, "..", "..", "")
print("Project root path: " + root_path)

dep_path = os.path.join(root_path, "dep")
lib_path = os.path.join(root_path, "lib")


# set platform/abi parameters
import argparse
parser = argparse.ArgumentParser(description='Build curl module')
parser.add_argument("-p", "--platform", dest="platform", help="build platform")
parser.add_argument("-a", "--abi", dest="abi", help="build abi")
args = vars(parser.parse_args())

build_platform = args["platform"]
build_abi = args["abi"]
if (build_platform is None) or (build_abi is None):
    from util_core import get_current_os_info
    build_platform, build_abi = get_current_os_info()
print("Platform: " + build_platform)
print("ABI: " + build_abi)


# unpack module
module_name = "curl"
module_version = "7.50.3"
module_full_name = module_name + "-" + module_version
module_file_name = module_full_name + ".tar.gz"

module_unpack_path = os.path.join(dep_path, module_full_name)
shutil.rmtree(module_unpack_path, ignore_errors=True)

os.chdir(dep_path)
os.system("tar xvf " + module_file_name)    # TODO cross-platform unpacking


# reset environment
build_path = os.path.join(module_unpack_path, "build", build_platform, build_abi)
shutil.rmtree(build_path, ignore_errors=True)
os.makedirs(build_path)

install_path = os.path.join(lib_path, module_name, build_platform)
shutil.rmtree(install_path, ignore_errors=True)
os.makedirs(install_path)


# build module
os.chdir(build_path)
if build_platform == "macOS":
    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.6"
cflags = os.getenv("CFLAGS", "")
build_cmd = '''%s/configure --host=%s-apple-darwin \
    CFLAGS="%s -O3 -Os -fPIE" CPPFLAGS="%s" LDFLAGS="%s -pie" \
    --with-darwinssl --without-ssl \
    --enable-optimize --enable-symbol-hiding --disable-verbose --disable-debug --disable-curldebug --disable-manual --disable-versioned-symbols --disable-thread --disable-threaded-resolver --disable-libcurl-option \
    --disable-ftp --disable-file --disable-rtsp --disable-proxy --disable-dict --disable-telnet --disable-tftp --disable-pop3 --disable-imap --disable-smb --disable-smtp --disable-gopher \
    --disable-ldap --disable-ldaps --disable-crypto-auth --disable-sspi --disable-ntlm-wb --disable-tls-srp --disable-unix-sockets --disable-cookies --disable-ares --disable-rt --disable-largefile --disable-soname-bump \
    --without-libpsl --without-libmetalink --without-libssh2 --without-librtmp --without-winidn --without-libidn --without-nghttp2 --without-zsh-functions-dir \
    --prefix="%s"''' % (module_unpack_path, build_abi, cflags, cflags, cflags, install_path)
# print("Build command: " + build_cmd)
# sys.exit()
os.system(build_cmd)
os.system("make")


# install
os.system("make install-strip prefix=%s libdir=%s/lib/%s" % (install_path, install_path, build_abi))

