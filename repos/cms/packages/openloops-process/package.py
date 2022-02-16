# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class OpenloopsProcess(Package):
    """Download process sources for OpenLoops"""

    homepage = "https://github.com/cms-externals/openloops"
    git      = "https://github.com/cms-externals/openloops.git"

    version('2.1.2', branch='cms/v2.1.2')
    patch('openloops-urlopen2curl.patch')

    resource('cms.coll',
             url='file://' + os.path.dirname(__file__) + 'cms.coll',
             sha256='ad84441b47bc01ea74487d153943d6bf9c6f2a1c40e6c158f9d0ce886ef29e4b',
             when='~tiny')

    resource('tiny.coll',
             url='file://' + os.path.dirname(__file__) + 'tiny.coll',
             sha256='eb0f24cc30fb10d75f828d60abe686fc0485d274f9832d26414f40e9a78dcd78',
             when='+tiny')

    variant('tiny', default=False, description='Only download one process to speed things up')

    depends_on('python@2.7,3.2:', type='build')

    def install(self, spec, prefix):
        coll_file = 'cms.coll' if not self.spec.variants['tiny'].value else 'tiny.coll'
        if self.spec.satisfies('target=aarch64:'):
            filter_file('pplljj_ew', '', coll_file)

        # copy(join_path(os.path.dirname(__file__), coll_file), coll_file)
        downloader = Executable('./pyol/bin/download_process.py')
        downloader(coll_file)
        install_tree('process_src', self.prefix.process_src)
        install_tree('proclib', self.prefix.proclib)
        install(coll_file, self.prefix)
