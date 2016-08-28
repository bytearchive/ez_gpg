#!/bin/bash -e

if [ -z "$(which fpm)" ]; then
  echo "ERROR! You need to install Ruby and fpm Ruby package first! Exiting..."
  exit 1
fi

package_type="deb"
if [ $# -gt 0 ]; then
  package_type=$1
fi

echo "Package type: $package_type"

# TODO: Use dirname/readlink instead of assuming we build from this dir
echo "Checking setup.py validity..."
./setup.py check

echo "Removing old package (if needed)..."
rm -f ezgpg_*.$package_type

echo "Building package..."
fpm -s python \
    -t $package_type \
    -d python3 \
    -d gnupg \
    -d python3-gi \
    -d gobject-introspection \
    -d libgtk-3-0 \
    -d gir1.2-gtk-3.0 \
    -n ezgpg \
    -m "Srdjan Grubor <sgnn7@sgnn7.org>" \
    --deb-no-default-config-files \
    --python-package-name-prefix python3 \
    --python-pip pip3 \
    --python-easyinstall easy_install3 \
    --python-bin python3 \
    ./setup.py
