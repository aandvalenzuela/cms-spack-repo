#!/bin/bash
if [ `uname` == "Darwin" ]; then
	CORES=`sysctl -n hw.ncpu`
elif [ `uname` == "Linux" ]; then
	CORES=`awk '/^processor/ { N++} END { print N }' /proc/cpuinfo`
fi
export CORES
echo Setup Spack for CMS
cd $WORKSPACE/cms-spack-repo
bash -xe ./bootstrap.sh
cd spack
source share/spack/setup-env.sh
echo Add signing key
if [ ! -z ${SPACK_GPG_KEY+x} ]; then spack gpg trust $SPACK_GPG_KEY; fi
echo Add padding to install_tree
spack config add "config:install_tree:padded_length:128"
echo Start the installation
spack env activate ${SPACK_ENV_NAME}
spack -d install -j$CORES --fail-fast
echo Prepare mirror and buildcache
spack mirror create -d $WORKSPACE/mirror --all --dependencies
if [ ${UPLOAD_BUILDCACHE} = "true" ]; then
  spack buildcache create -r -f -a -d $WORKSPACE/mirror
  spack gpg publish -d $WORKSPACE/mirror --rebuild-index
  cd $WORKSPACE
  echo Upload mirror
  rsync -e "ssh -o StrictHostKeyChecking=no -o GSSAPIAuthentication=yes -o GSSAPIDelegateCredentials=yes" --recursive --links --ignore-existing mirror/ cmsbuild@lxplus:/eos/user/r/razumov/www/CMS/mirror
fi
echo Done
