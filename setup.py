#!/usr/bin/env python3

import os
import operator
import subprocess
import glob

from distutils.core import setup
from distutils.cmd import Command
from distutils.log import info, warn
from distutils.dep_util import newer
from distutils.command.sdist import sdist as _sdist

PACKAGENAME = "efaLiveTools"
PACKAGEVERSION = "3.0"
AUTHOR = "Kay Hannay"
AUTHOR_MAIL = "klinux@hannay.de"
URL = "https://www.hannay.de/efalive"
LICENSE = "GNU GPL 3"
DESCRIPTION = "Tools for efaLive"

PO_DIR = 'i18n/efaLiveTools/po_files'

class NoOptionCommand(Command):
    """Command that doesn't take any options"""
    user_options = []

    def initialize_options(self): pass
    def finalize_options(self): pass


class UpdatePot(NoOptionCommand):
    description = 'Update the .pot translation template'

    def run(self):
        all_py_files = sorted(reduce(operator.add, [[os.path.join(dn, f) for f in fs if f.endswith('.py')] for (dn,ds,fs) in os.walk('.')])) # sort to make diffs easier
        self.update_pot(all_py_files, PACKAGENAME, 'Python')
        self.update_pot(os.path.join('files', 'usr', 'lib', 'efalive', 'bin', 'autobackup.sh'), 'autobackup', 'shell')

    def update_pot(self, files, package, type):
        # not working around xgettext not substituting for PACKAGE everywhere in the header; it's just a template and usually worked on using tools that ignore much of it anyway
        if not self.dry_run:
            pot_file = os.path.join('i18n', package, 'messages.pot')
            info('Creating %s' % pot_file)
            subprocess.check_call(['xgettext', '-L' + type, '-o', pot_file, '--copyright-holder', AUTHOR, '--package-name', PACKAGENAME, '--package-version', PACKAGEVERSION, '--msgid-bugs-address', AUTHOR_MAIL, '--add-comments=#'] + files)


class UpdatePo(NoOptionCommand):
    description = 'Update the .po translations from .pot translation template'

    def run(self):
        self.update_po(PACKAGENAME)
        self.update_po('autobackup')

    def update_po(self, package):
        po_dir = os.path.join('i18n', package, 'po_files')
        pot_file = os.path.join('i18n', package, 'messages.pot')
        # msgmerge data/po/da.po data/po/messages.pot -U
        for po in glob.glob(os.path.join(po_dir, '*.po')):
            if not self.dry_run:
                info('Updating %s' % po)
                subprocess.check_call(['msgmerge', '-U', po, pot_file])


class CompileLanguages(NoOptionCommand):
    description = 'Compile .po files into .mo files'

    def run(self):
        self.compile_mo(PACKAGENAME)
        self.compile_mo('autobackup')

    def compile_mo(self, package):
        po_dir = os.path.join('i18n', package, 'po_files')
        base_path = os.path.join("build", "python", PACKAGENAME + "-" + PACKAGEVERSION, "locale")
        self.mkpath(base_path) # create directory even if there are no files, otherwise install would complain
        for po in glob.glob(os.path.join(po_dir,'*.po')):
            info("Current po file: {}".format(po))
            lang = os.path.basename(po[:-3])
            mo = os.path.join(base_path, lang, 'LC_MESSAGES', '{}.mo'.format(package))

            directory = os.path.dirname(mo)
            self.mkpath(directory)

            if newer(po, mo):
                cmd = ['msgfmt', '-o', mo, po]
                info('compiling %s -> %s' % (po, mo))
                if not self.dry_run:
                    subprocess.check_call(cmd)


class sdist(_sdist):
    sub_commands = _sdist.sub_commands + [('build_trans', None)]
    def run(self):
        _sdist.run(self)


setup(name=PACKAGENAME,
      version=PACKAGEVERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_MAIL,
      url=URL,
      license=LICENSE,
      packages=['.',
                'efalive',
                'efalive.common',
                'efalive.setuptool',
                'efalive.setuptool.setupcommon',
                'efalive.setuptool.backup',
                'efalive.setuptool.devicemanager',
                'efalive.setuptool.dttime',
                'efalive.daemon',
                'efalive.daemon.pythondaemon'],
      cmdclass={
        'sdist': sdist,
        'build_trans': CompileLanguages,
        'update_pot': UpdatePot,
        'update_po': UpdatePo,
      }
     )

'''
#      data_files=[('icons', ['icons/backup.png', 'icons/mount.png', 'icons/restore.png', 'icons/screen_setup.png', 'icons/terminal.png', 'icons/unmount.png']),
#	  	  ('locale/de/LC_MESSAGES/', ['i18n/de/efaLiveSetup.mo']),
#	  	  ('', ['install.sh'])],
'''
