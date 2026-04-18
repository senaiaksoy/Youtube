Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "E:\git_repo\youtube"
WshShell.Run "cmd /c yarn desktop:dev", 0, False
