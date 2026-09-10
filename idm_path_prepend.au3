#include <File.au3>

Opt("WinTitleMatchMode", 1)
Main()
Exit

Func SubstitutePath($pathOrig, $newDir)
	If StringInStr(FileGetAttrib($newDir), "D") And StringRight($newDir, 1) <> "\" Then
		$newDir &= "\"
	EndIf

	ConsoleWrite("$pathOrig: " & $pathOrig & @CRLF)
	ConsoleWrite("$newDir: " & $newDir & @CRLF)
	Local $sDrive = "", $sDir = "", $sFileName = "", $sExtension = ""
	_PathSplit($pathOrig, $sDrive, $sDir, $sFileName, $sExtension)

	Local $newPath = $newDir & $sFileName & $sExtension
	Return $newPath
EndFunc   ;==>SubstitutePath

Func CopyAndReplace()
	Local $newDir = ClipGet()
	Local $hwnd = WinActivate("[TITLE:Download File Info;CLASS:#32770]")
	Local $oldPath = ControlGetText($hwnd, "", "Edit4")
	Local $newPath = SubstitutePath($oldPath, $newDir)
	ControlSetText($hwnd, "", "Edit4", $newPath)

	ControlFocus($hwnd, "", "Edit4")
	Send("{BACKSPACE}^z")
EndFunc   ;==>CopyAndReplace

Func Main()
	CopyAndReplace()
EndFunc   ;==>Main
