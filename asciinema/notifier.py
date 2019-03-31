import shutil
import subprocess


class Notifier():
    def is_available(self):
        return shutil.which(self.cmd) is not None

    def notify(self, text):
        subprocess.run(self.args(text), capture_output=True)
        # we don't want to print *ANYTHING* to the terminal
        # so we capture and ignore all output


class AppleScriptNotifier(Notifier):
    cmd = "osascript"

    def args(self, text):
        text = text.replace('"', '\\"')
        return ['osascript', '-e', 'display notification "{}" with title "asciinema"'.format(text)]


class LibNotifyNotifier(Notifier):
    cmd = "notify-send"

    def args(self, text):
        return ['notify-send', 'asciinema', text]


class NoopNotifier():
    def notify(self, text):
        pass


def get_notifier():
    for c in [AppleScriptNotifier, LibNotifyNotifier]:
        n = c()

        if n.is_available():
            return n

    return NoopNotifier()