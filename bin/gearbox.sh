#!/usr/bin/env sh

[ "${SNAKEGIT_HOME}xxx" = "xxx" ] &&  SNAKEGIT_HOME=${HOME}/.snakegit
[ "${VIRTUALENV_DIR}xxx" = "xxx" ] &&  VIRTUALENV_DIR=vendor/python

package() {
  echo "Building package"
  ${SNAKEGIT_HOME}/bin/build.sh

  ${VIRTUALENV_DIR}/bin/python setup.py install

  ${SNAKEGIT_HOME}/bin/virtualenv --relocatable ${VIRTUALENV_DIR}

  mkdir -p gearbox

  rsync -ar _gb/gbtemplates/ gearbox/gbtemplates/
  [ -e _gb/gbtest ] && rsync -ar _gb/gbtest/ gearbox/gbtest/

  rsync -ar ${VIRTUALENV_DIR}/ gearbox

  mkdir -p gearbox_dist

  current_dir=`pwd`

  tarfile=`pwd`/gearbox_dist/`date +%s`.tar.gz

  cd gearbox

  tar -czvf $tarfile *

  cd $current_dir
}



