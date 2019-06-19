#!/usr/bin/env python

from distutils.core import setup

setup(name='efaLiveTools',
      version='3.0',
      description='Tools for efaLive',
      author='Kay Hannay',
      author_email='klinux@hannay.de',
      url='http://www.hannay.de/',
      packages=['.',
                'efalive',
                'efalive.common',
                'efalive.setup',
                'efalive.setup.setupcommon',
                'efalive.setup.backup',
                'efalive.setup.devicemanager',
                'efalive.setup.screen',
                'efalive.setup.dttime',
                'efalive.daemon'],
     )

'''
#      data_files=[('icons', ['icons/backup.png', 'icons/mount.png', 'icons/restore.png', 'icons/screen_setup.png', 'icons/terminal.png', 'icons/unmount.png']),
#	  	  ('locale/de/LC_MESSAGES/', ['i18n/de/efaLiveSetup.mo']),
#	  	  ('', ['install.sh'])],
'''
