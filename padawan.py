import sublime
from os import path
import urllib
import json
import subprocess
import re

settings = sublime.load_settings("Padawan.sublime-settings")
server_addr = "http://127.0.0.1:15155"
composer = settings.get("padawan_composer")
timeout = 0.5
padawanPath = path.dirname(__file__)
server_path = path.join(padawanPath, 'padawan.php')


class IndexGenerator:

    def Generate(self, view, projectRoot):
        generatorCommand = server_path + '/bin/cli'
        stream = subprocess.Popen(
            'cd ' + projectRoot + ' && ' + generatorCommand + ' generate',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        self.Notify(view, stream)

    def Notify(self, view, stream):
        retcode = stream.poll()
        if retcode is not None:
            self.drawBars(view, 100)
            return
        line = stream.stdout.readline().decode('ascii')
        errorMatch = re.search('Error: (.*)', line)
        if errorMatch is not None:
            retcode = 1
            print(errorMatch.group(1).replace("'", "''"))
            return

        generator = self

        def Notifier():
            return generator.Notify(view, stream)

        match = re.search('Progress: ([0-9]+)', line)
        if not match or match is None:
            sublime.set_timeout(Notifier, 0.005)

        progress = int(match.group(1))
        self.drawBars(view, progress)

        sublime.set_timeout(Notifier, 0.005)

    def drawBars(self, view, progress):
        bars = int(progress / 5)
        barsStr = ''
        for i in range(20):
            if i < bars:
                barsStr += '='
            else:
                barsStr += ' '
        barsStr = '[' + barsStr + ']'

        view.set_status(
            "PadawanIndexGeneration",
            "Progress "+barsStr+' '+str(progress)+"%"
            )


class PadawanClient:

    def GetCompletion(self, filepath, line_num, column_num, contents):
        curPath = self.GetProjectRoot(filepath)

        params = {
            'filepath': filepath.replace(curPath, ""),
            'line': line_num,
            'column': column_num,
            'path': curPath
        }
        result = self.DoRequest('complete', params, contents)

        if not result:
            return {"completion": []}

        return result

    def SaveIndex(self, filepath):
        return self.DoRequest('save', {'filepath': filepath})

    def DoRequest(self, command, params, data=''):
        try:
            return self.SendRequest(command, params, data)
        except urllib.request.URLError:
            sublime.status_message("Padawan is not running")
        except Exception as e:
            print('Error occured {0}'.format(e))

        return False

    def SendRequest(self, command, params, data=''):
        addr = server_addr + "/"+command+"?" + urllib.parse.urlencode(params)
        response = urllib.request.urlopen(
            addr,
            data.encode("utf8"),
            timeout
        )
        completions = json.loads(response.read().decode("utf8"))
        if "error" in completions:
            raise ValueError(completions["error"])
        return completions

    def StartServer(self):
        command = '{0}/bin/server.php > {0}/../logs/server.log'.format(
            server_path
        )
        subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

    def StopServer(self):
        try:
            self.SendRequest('kill', {})
            return True
        except Exception:
            return False

    def RestartServer(self):
        if self.StopServer():
            self.StartServer()

    def AddPlugin(self, view, plugin):
        composerCommand = composer + ' require '
        generatorCommand = server_path + '/bin/cli'

        view.set_status("PadawanPlugin", "Started plugin installation")
        command = 'cd {0} && {1} {3} && {2} plugin add {3}'.format(
            self.PadawanPHPPath(),
            composerCommand,
            generatorCommand,
            plugin
        )

        stream = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        client = self

        def Notifier():
            retcode = stream.poll()
            if retcode is not None:
                return

            line = stream.stdout.readline()
            print(line)
            sublime.set_timeout(Notifier, 0.005)

            if not retcode:
                client.RestartServer()
                view.set_status("PadawanPlugin", "Plugin installed")
            else:
                view.set_status("PadawanPlugin", "Plugin installation failed")

        sublime.set_timeout(Notifier, 0.005)

    def RemovePlugin(self, view, plugin):
        composerCommand = composer + ' remove'
        generatorCommand = server_path + '/bin/cli'

        command = 'cd {0} && {1} {2}'.format(
            self.PadawanPHPPath(),
            composerCommand,
            plugin
        )

        subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        subprocess.Popen(
            'cd {0} && {1}'.format(
                self.PadawanPHPPath(),
                generatorCommand + ' plugin remove ' + plugin
            ),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ).wait()

        self.RestartServer()
        view.set_status("PadawanPlugin", "Plugin removed")

    def Generate(self, filepath, view):
        curPath = self.GetProjectRoot(filepath)
        generator = IndexGenerator()
        generator.Generate(view, curPath)
        self.RestartServer()

    def GetProjectRoot(self, filepath):
        curPath = path.dirname(filepath)
        while curPath != '/' and not path.exists(
            path.join(curPath, 'composer.json')
        ):
            curPath = path.dirname(curPath)

        if curPath == '/':
            curPath = path.dirname(filepath)

        return curPath

    def PadawanPHPPath(self):
        return padawanPath + '/padawan.php/'


client = PadawanClient()
