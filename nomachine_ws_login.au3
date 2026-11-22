#include <AutoItConstants.au3>
#include <MsgBoxConstants.au3>

Global Const $PWD_FILE_NAME = "vpn_pwd.cfg"

Opt("WinTitleMatchMode", 1)
Opt("MouseCoordMode", 2)
Opt("SendKeyDelay", 10)
Main()
Exit

Func CheckWindow()
	Local $hwnd = 0
	Local $funcLoop = True
	Local $dlgVal = $IDRETRY
	While $funcLoop
		$hwnd = WinActivate("NoMachine - ")
		If $hwnd == 0 Then
			Return False
		EndIf
		$funcLoop = False
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

	; Click the top left button of the screen
	Local $mPos = MouseGetPos()
	MouseMove(40, 20, 1)
	MouseClick($MOUSE_CLICK_LEFT)
	MouseMove($mPos[0], $mPos[1], 1)

	; Trigger password input
	For $i = 1 To 2
		Send("{ESC}")
		Sleep(500)
	Next

	;- Switch out of and back into input widget, to check if it gets focus
	;- Input password
	Send("{TAB}+{TAB}" & $pwd & "{ENTER}")
EndFunc
