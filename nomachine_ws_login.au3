#include <AutoItConstants.au3>
#include <MsgBoxConstants.au3>

Global Const $ENV_VAR_NAME = "VPN_PWD_FC"

Opt("WinTitleMatchMode", 1)
Opt("MouseCoordMode", 2)
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

	;~ Click somewhere in the window, tab to password field
	Send("{ESC}{ESC}{ESC}{ESC}{ESC}")
;~ 	MouseClick("left", 100, 100)
	Sleep(1000)

	;- Input password
	Send($pwd & "{ENTER}")
EndFunc