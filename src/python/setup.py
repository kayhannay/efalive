#!/usr/bin/env python

from distutils.core import setup

setup(name='efaLiveSetup',
      version='1.0',
      description='Setup utility for efaLive',
      author='Kay Hannay',
      author_email='klinux@hannay.de',
      url='http://www.hannay.de/',
      packages=['efalivesetup', 'efalivesetup.common', 'efalivesetup.backup', 'efalivesetup.devicemanager', 'efalivesetup.screen', 'efalivesetup.datetime'],
     )

'''
#      data_files=[('icons', ['icons/backup.png', 'icons/mount.png', 'icons/restore.png', 'icons/screen_setup.png', 'icons/terminal.png', 'icons/unmount.png']),
#	  	  ('locale/de/LC_MESSAGES/', ['i18n/de/efaLiveSetup.mo']),
#	  	  ('', ['install.sh'])],
'''
