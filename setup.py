#!/usr/bin/env python3

import os
import operator
import subprocess
import glob

from distutils.core import setup
from distutils.cmd import Command
from distutils.log import info, warn
from distutils.dep_util import newer
from distutils.command.build import build as _build

PO_DIR = 'i18n/po_files'
POT_FILE = os.path.join('i18n', 'messages.pot')

PACKAGENAME = "efaLiveTools"
PACKAGEVERSION = "3.0"
AUTHOR = "Kay Hannay"
AUTHOR_MAIL = "klinux@hannay.de"
URL = "https://www.hannay.de/efalive"
LICENSE = "GNU GPL 3"
DESCRIPTION = "Tools for efaLive"

class NoOptionCommand(Command):
    """Command that doesn't take any options"""
    user_options = []

    def initialize_options(self): pass
    def finalize_options(self): pass


class UpdatePot(NoOptionCommand):
    description = 'Update the .pot translation template'

    def run(self):
        all_py_files = sorted(reduce(operator.add, [[os.path.join(dn, f) for f in fs if f.endswith('.py')] for (dn,ds,fs) in os.walk('.')])) # sort to make diffs easier
        # not working around xgettext not substituting for PACKAGE everywhere in the header; it's just a template and usually worked on using tools that ignore much of it anyway
        if not self.dry_run:
            info('Creating %s' % POT_FILE)
            subprocess.check_call(['xgettext', '-LPython', '-o', POT_FILE, '--copyright-holder', AUTHOR, '--package-name', PACKAGENAME, '--package-version', PACKAGEVERSION, '--msgid-bugs-address', AUTHOR_MAIL, '--add-comments=#'] + all_py_files)


class UpdatePo(NoOptionCommand):
    description = 'Update the .po translations from .pot translation template'

    def run(self):
        # msgmerge data/po/da.po data/po/messages.pot -U
        for po in glob.glob(os.path.join(PO_DIR, '*.po')):
            if not self.dry_run:
                info('Updating %s' % po)
                subprocess.check_call(['msgmerge', '-U', po, POT_FILE])


class CompileLanguages(NoOptionCommand):
    description = 'Compile .po files into .mo files'

    def run(self):
        self.mkpath(os.path.join("build", "locale")) # create directory even if there are no files, otherwise install would complain
        for po in glob.glob(os.path.join(PO_DIR,'*.po')):
            info("Current po file: {}".format(po))
            lang = os.path.basename(po[:-3])
            mo = os.path.join('build', 'locale', lang, 'LC_MESSAGES', '{}.mo'.format(PACKAGENAME))

            directory = os.path.dirname(mo)
            self.mkpath(directory)

            if newer(po, mo):
                cmd = ['msgfmt', '-o', mo, po]
                info('compiling %s -> %s' % (po, mo))
                if not self.dry_run:
                    subprocess.check_call(cmd)


class build(_build):
    sub_commands = _build.sub_commands + [('build_trans', None)]
    def run(self):
        _build.run(self)


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
                'efalive.setup',
                'efalive.setup.setupcommon',
                'efalive.setup.backup',
                'efalive.setup.devicemanager',
                'efalive.setup.screen',
                'efalive.setup.screenlayout',
                'efalive.setup.dttime',
                'efalive.daemon',
                'efalive.daemon.pythondaemon'],
      cmdclass={
        'build': build,
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
