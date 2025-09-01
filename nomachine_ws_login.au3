#include <AutoItConstants.au3>
#include <MsgBoxConstants.au3>

Global Const $ENV_VAR_NAME = "VPN_PWD_FC"

Opt("WinTitleMatchMode", 1)
Opt("MouseCoordMode", 2)
Opt("SendKeyDelay", 10)
Main()
Exit

Func Main()
	Local $hwnd = 0
	Local $pwd = EnvGet($ENV_VAR_NAME)
	Local $funcLoop = True

	If Not $pwd Then
		MsgBox($MB_ICONERROR, "Error", "Environment variable " & $ENV_VAR_NAME _
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