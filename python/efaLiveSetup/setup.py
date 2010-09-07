from distutils.core import setup

setup( 
     name = "efaLiveSetup", 
     version = "0.1", 
     author = "Kay Hannay", 
     author_email = "klinux@hannay.de", 
     url='http://www.hannay.de/',
     #py_modules = ["verwirbeln"],
     #package_dir = {"" : "src"}, 
     packages = ["efalivesetup"],
     #package_data = {"efalivesetup" : ["locale/de/LC_MESSAGES/efaLiveSetup.mo"]}
     data_files = [('locale/de/LC_MESSAGES', ['locale/de/LC_MESSAGES/efaLiveSetup.mo'])]
     )

