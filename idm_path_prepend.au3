#include <File.au3>

Opt("WinTitleMatchMode", 1)
Main()
Exit

Func SubstitutePath($pathOrig, $newDir)
	ConsoleWrite("$pathOrig: " & $pathOrig & @CRLF)
	Local $sDrive = "", $sDir = "", $sFileName = "", $sExtension = ""
	_PathSplit($pathOrig, $sDrive, $sDir, $sFileName, $sExtension)

	Local $newPath = $newDir & $sFileName & $sExtension
	Return $newPath
EndFunc

Func Main()
	Local $newDir = ClipGet()
	Local $hwnd = WinActivate("[TITLE:Download File Info;CLASS:#32770]")
	Local $oldPath = ControlGetText($hwnd, "", "Edit4")
	Local $newPath = SubstitutePath($oldPath, $newDir)
	ControlSetText($hwnd, "", "Edit4", $newPath)

	ControlFocus($hwnd, "", "Edit4")
	Send("{BACKSPACE}^z")
EndFunc
