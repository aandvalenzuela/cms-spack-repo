# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDxr(PythonPackage):
    """DXR is a code search and navigation tool aimed at making sense
       of large projects like Firefox."""

    homepage = "https://dxr.readthedocs.io"
    url      = "https://github.com/cms-externals/dxr"

    version('1.0.x', git='https://github.com/cms-externals/dxr.git')

    depends_on('m4@1.4.18', type=('build', 'run'))
    depends_on('llvm', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('sqlite', type=('build', 'run'))
