#
# Regular cron jobs for the efalive package
#
0 4	* * *	root	[ -x /usr/bin/efalive_maintenance ] && /usr/bin/efalive_maintenance
