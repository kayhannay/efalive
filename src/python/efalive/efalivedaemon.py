from daemon import runner
from efalive.daemon.efalivedaemon import EfaLiveDaemon

if __name__ == '__main__':
    daemon = EfaLiveDaemon()
    daemon_runner = runner.DaemonRunner(daemon)
    daemon_runner.do_action()

