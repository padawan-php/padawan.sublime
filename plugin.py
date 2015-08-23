import sublime
import sublime_plugin
from .padawan import client


def sel_end(sel):
    return max(sel.a, sel.b)


def is_php_file(view):
    return view.score_selector(sel_end(view.sel()[0]), "source.php") > 0


class PadawanGenerateIndexCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        fname = self.view.file_name()
        if fname is None:
            return None
        client.Generate(fname, self.view)


class PadawanStartServerCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        client.StartServer()


class PadawanStopServerCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        client.StopServer()


class PadawanRestartServerCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        client.RestartServer()


class PadawanCompleter(sublime_plugin.EventListener):

    def run_completion(self, view):
        view.run_command('auto_complete', {
            'api_completions_only': True,
            'disable_auto_insert': True
            })

    def on_modified_async(self, view):
        if not is_php_file(view):
            return
        cursor = view.sel()[0].b
        if cursor < 1:
            return

        while cursor > 0:
            curChar = view.substr(sublime.Region(cursor-1, cursor))
            if curChar == '\\':
                return self.run_completion(view)
            if curChar == '$':
                return self.run_completion(view)
            if curChar == '(':
                return self.run_completion(view)
            if cursor > 1:
                curChar = view.substr(sublime.Region(cursor-2, cursor))
                if curChar == '->':
                    return self.run_completion(view)
                if curChar == '::':
                    return self.run_completion(view)
            if cursor > 3:
                curChar = view.substr(sublime.Region(cursor-4, cursor))
                if curChar == 'use ':
                    return self.run_completion(view)
            cursor -= 1

    def on_query_completions(self, view, prefix, locations):
        if not is_php_file(view):
            return None
        fname = view.file_name()
        if fname is None:
            return None
        column = 16
        line = 35
        line, column = view.rowcol(locations[0])
        contents = view.substr(sublime.Region(0, view.size()))
        completions = client.GetCompletion(
            fname,
            line+1,
            column+1,
            contents
            )["completion"]
        return (
            [[c["name"], c["name"]] for c in completions],
            sublime.INHIBIT_WORD_COMPLETIONS
            )
