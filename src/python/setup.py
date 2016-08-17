#!/usr/bin/env python

from distutils.core import setup

setup(name='efaLiveTools',
      version='2.4',
      description='Tools for efaLive',
      author='Kay Hannay',
      author_email='klinux@hannay.de',
      url='http://www.hannay.de/',
      packages=['efalive',
                'efalive.efalive',
                'efalive.efalive.common',
                'efalive.efalive.setup',
                'efalive.efalive.setup.setupcommon',
                'efalive.efalive.setup.backup',
                'efalive.efalive.setup.devicemanager',
                'efalive.efalive.setup.screen',
                'efalive.efalive.setup.dttime',
                'efalive.efalive.daemon'],
     )

'''
#      data_files=[('icons', ['icons/backup.png', 'icons/mount.png', 'icons/restore.png', 'icons/screen_setup.png', 'icons/terminal.png', 'icons/unmount.png']),
#	  	  ('locale/de/LC_MESSAGES/', ['i18n/de/efaLiveSetup.mo']),
#	  	  ('', ['install.sh'])],
'''
