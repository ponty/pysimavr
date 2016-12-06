from setuptools import setup
from setuptools.extension import Extension
import fnmatch
import os.path
import sys

if os.environ.get('distutils_issue8876_workaround_enabled', False):
    # sdist_hack: Remove reference to os.link to disable using hardlinks when
    #             building setup.py's sdist target.  This is done because
    #             VirtualBox VMs shared filesystems don't support hardlinks.
    del os.link


NAME = 'pysimavr'
URL = 'https://github.com/ponty/pysimavr'
DESCRIPTION = 'python wrapper for simavr which is AVR and arduino simulator.'
PACKAGES = [NAME,
            NAME + '.swig',
            NAME + '.examples',
            ]

# get __version__
__version__ = None
exec(open(os.path.join(NAME, 'about.py')).read())
VERSION = __version__

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

classifiers = [
    # Get more strings from
    # http://www.python.org/pypi?%3Aaction=list_classifiers
    "License :: OSI Approved :: BSD License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    #    "Programming Language :: Python :: 2.3",
    #    "Programming Language :: Python :: 2.4",
    #"Programming Language :: Python :: 2.5",
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    #    "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 3",
#     'Programming Language :: Python :: 3.0',
    #     "Programming Language :: Python :: 3.1",
#     'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]

install_requires = open("requirements.txt").read().split('\n')

SWIG = 'pysimavr/swig'
SIMAVR = SWIG + '/simavr'  # simavr path

SIM = SIMAVR + '/simavr/sim'
CORES = SIMAVR + '/simavr/cores'
INCLUDE_SIMAVR = SIMAVR + '/simavr'
INCLUDE_AVR = SWIG + '/include'
PARTS = SWIG + '/parts'

EXCLUDE = ['sim_mega324.c', 'sim_mega128rfr2.c']

def listdir(directory, pattern):
    names = os.listdir(directory)
    names = fnmatch.filter(names, pattern)
    return [os.path.join(directory, child) for child in names]


def files(directory, pattern, exclude=[]):
    return [p for p in listdir(directory, pattern) if os.path.isfile(p) and os.path.basename(p) not in exclude]


def part(name):
    return Extension(name='pysimavr.swig._' + name,
                     sources=[
                     PARTS + '/' + name + '.c',
#                      SWIG + '/' + name + '.i',
                     SWIG + '/' + name + '_wrap.c',
                     #                     'pysimavr/swig/sim/sim_cycle_timers.c',
                     #                     'pysimavr/swig/sim/sim_irq.c',
                     #                     'pysimavr/swig/sim/sim_io.c',
                     ],
                     libraries=['elf'],
                     include_dirs=[
                     SIM,
                     INCLUDE_SIMAVR, INCLUDE_AVR,
                     PARTS,
                     ],
#                      swig_opts=[
#                      #                       '-modern',
#                      '-I' + PARTS,
#                      '-I' + SIM,
#                      ],
                     extra_compile_args=[
                    '--std=gnu99',
                     ],
                     )

ext_modules = [
    Extension(name='pysimavr.swig._simavr',
              sources=[
#               SWIG + '/simavr.i',
              SWIG + '/simavr_wrap.c',
              SWIG + '/simavr_logger.c',
              ]
              + files(SIM, '*.c')
              + files(CORES, 'sim_*.c', EXCLUDE),
              libraries=['elf'],
              include_dirs=[
              SIM,
              INCLUDE_SIMAVR, INCLUDE_AVR,
              ],
#               swig_opts=[
#               #                       '-modern',
#               '-I' + SIM,
#               ],
              extra_compile_args=[
            '--std=gnu99',
              '-DNO_COLOR',
              ],
              ),
    part('sgm7'),
    part('ledrow'),
    part('inverter'),
    part('hd44780'),
    part('ac_input'),
    part('button'),
    part('uart_udp'),
    part('spk'),
    part('uart_buff'),

]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.rst', 'r').read(),
    classifiers=classifiers,
    keywords='avr simavr',
    author='ponty',
    # author_email='',
    url=URL,
    license='GPL',
    packages=PACKAGES,
    include_package_data=True,
#     test_suite='nose.collector',
    zip_safe=False,
    install_requires=install_requires,
    ext_modules=ext_modules,
    **extra
)
