#include <AutoItConstants.au3>
#include <MsgBoxConstants.au3>
#include <WinAPISys.au3>

Global Const $PWD_FILE_NAME = "vpn_pwd.cfg"
Global Const $FORTICLIENT_PATH = "C:\Program Files\Fortinet\FortiClient\FortiClient.exe"

Opt("WinTitleMatchMode", 3)
Opt("MouseCoordMode", 2)
Main()
Exit

Func CheckWindow()
	Local $hWnd = 0
	Local $funcLoop = True
	While $funcLoop
		$hWnd = WinActivate("FortiClient")
		If $hWnd == 0 Then
			ShellExecute($FORTICLIENT_PATH)
			WinWaitActive("FortiClient")
		Else
			$funcLoop = False
		EndIf
	WEnd
	Return True
EndFunc

Func Main()
	Local $pwd = FileReadLine($PWD_FILE_NAME)
	If Not @error = 0 Then
		MsgBox($MB_ICONERROR, "Error", "File " & $PWD_FILE_NAME _
				 & " is nonexistent or empty. Script will now exit.")
		Return
	EndIf

	If Not CheckWindow() Then Return

	Local $mPos = MouseGetPos()
	; Click somewhere in the window, tab to password field
	MouseClick($MOUSE_CLICK_LEFT, 125, 125, 1, 1)
	MouseMove($mPos[0], $mPos[1], 1)
	Send("{TAB}{TAB}{TAB}")

	;- Input password
	Send($pwd & "{ENTER}")
EndFunc
