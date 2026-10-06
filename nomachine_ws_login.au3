#include <AutoItConstants.au3>
#include <MsgBoxConstants.au3>

Global Const $PWD_FILE_NAME = "vpn_pwd.cfg"

Opt("WinTitleMatchMode", 1)
Opt("MouseCoordMode", 2)
Opt("SendKeyDelay", 10)
Main()
Exit

Func Main()
	Local $hwnd = 0
	Local $pwd = FileReadLine($PWD_FILE_NAME)
	Local $funcLoop = True

	If Not @error = 0 Then
		MsgBox($MB_ICONERROR, "Error", "File " & $PWD_FILE_NAME _
			& " is nonexistent or empty. Script will now exit.")
		Return
	EndIf

	Local $dlgVal = $IDRETRY
	While $funcLoop
		$hwnd = WinActivate("NoMachine - ")
		If $hwnd == 0 Then
			$dlgVal = MsgBox($MB_ICONERROR + $MB_RETRYCANCEL, _
				"Error", "NoMachine window not found. Run it then retry, or cancel:")
			If $dlgVal == $IDCANCEL Then
				Return
			Else
				ContinueLoop
			EndIf
		EndIf
		$funcLoop = False
	WEnd

	;~ Trigger password input
	For $i = 1 To 2
		Send("{ESC}")
		Sleep(500)
	Next

	;- Switch out of and back into input widget, to check if it gets focus
	;- Input password
	Send("{TAB}+{TAB}" & $pwd & "{ENTER}")
EndFunc