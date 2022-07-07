# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import spack
import os
import shutil


class CmsCommon(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    git      = "https://github.com/cms-sw/cms-common.git"

    version('1.0', commit='9505d2624c75659a537bba9bc46b5c3c7f5d201f')

    revision = '1219'

    def patch(self):
        filter_file('srbase=${cms_basedir}/share/lcg/SCRAMV1/${sver}',
                    'srbase=${cms_basedir}/share/scram/${sver}',
                    'common/scram',
                    string=True)


    def install(self, spec, prefix):
        cmsplatf = os.environ.get('SCRAM_ARCH', 'slc7_amd64_gcc900')
        # shutil.rmtree('.git')
        for root, dirs, files in os.walk('.'):
            for fn in files:
                if os.path.isfile(join_path(root, fn)):
                    # filter_file('@CMS_PREFIX@', os.environ.get('RPM_INSTALL_PREFIX'))
                    # ^-- done in cmspost b/c RPM_INSTALL_PREFIX may be undefined at buildtime
                    filter_file('@SCRAM_ARCH@', cmsplatf, join_path(root, fn))

        install_tree('.', prefix.join(self.revision))
        install(join_path(os.path.dirname(__file__), 'cmspost.sh'), prefix)
        filter_file('cmsplatf=.*', 'cmsplatf='+cmsplatf, join_path(prefix, 'cmspost.sh'))
        filter_file('pkgrevision=.*', 'pkgrevision='+self.revision, join_path(prefix, 'cmspost.sh'))
        set_executable(join_path(prefix, 'cmspost.sh'))
