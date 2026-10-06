#include <AutoItConstants.au3>
#include <MsgBoxConstants.au3>
#include <WinAPISys.au3>

Global Const $PWD_FILE_NAME = "vpn_pwd.cfg"

Opt("WinTitleMatchMode", 3)
Opt("MouseCoordMode", 2)
Main()
Exit

Func Main()
	Local $hActWnd = 0
	Local $hWnd = 0
	Local $pwd = FileReadLine($PWD_FILE_NAME)
	Local $funcLoop = True

	If Not @error = 0 Then
		MsgBox($MB_ICONERROR, "Error", "File " & $PWD_FILE_NAME _
			& " is nonexistent or empty. Script will now exit.")
		Return
	EndIf

	Sleep(100)
	$hActWnd = _WinAPI_GetActiveWindow()

	Local $dlgVal = $IDRETRY
	While $funcLoop
		$hWnd = WinActivate("FortiClient")
		If $hWnd == 0 Then
			$dlgVal = MsgBox($MB_ICONERROR + $MB_RETRYCANCEL, _
				"Error", "FortiClient window not found. Run it then retry, or cancel:")
			If $dlgVal == $IDCANCEL Then
				Return
			Else
				ContinueLoop
			EndIf
		EndIf
		$funcLoop = False
	WEnd

	Local $mPos = MouseGetPos()
	;~ Click somewhere in the window, tab to password field
	MouseClick($MOUSE_CLICK_LEFT, 125, 125, 1, 1)
	MouseMove($mPos[0], $mPos[1], 1)
	Send("{TAB}{TAB}{TAB}")

	;- Input password
	Send($pwd & "{ENTER}")

	;- Activate previously active window, if any
	If $hActWnd <> 0 Then
		WinActivate($hActWnd)
	EndIf
EndFunc