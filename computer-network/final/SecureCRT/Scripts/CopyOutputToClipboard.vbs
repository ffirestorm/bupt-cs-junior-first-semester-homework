# $language = "VBScript"
# $interface = "1.0"
' CopyOutputToClipboard.vbs
'
' Description:
'   This script example is designed to run while connected to a Cisco Pix
'   firewall or other router device.
'   
'   When launched, the following commands are sent to the device:
'      enable
'      configure terminal
'      pager 0
'      show config
'      show serial
'      show sysopt
'      exit
'      exit
'  
'  The results of the 'show config', 'show serial', and 'show sysopt' commands
'  are captured and stored within the Windows clipboard.  A messagebox then
'  displays the contents of the Windows clipboard.
'   
' Demonstrates:
'   - Use of crt.Screen.ReadString to capture output from a command as echoed
'     from the remote system.
'   - How to copy data from a script variable into the Windows clipboard
'     using the crt.Clipboard object (available in SecureCRT 6.1.0 and later;
'     otherwise, the InternetExplorer automation object is used to manipulate
'     the clipboard).
'   - Use of the ReadString method to either look for a shell
'     prompt (so it can be determined when a remote command has
'     completed) or some other entire line of data.
'   - Use of the crt.Version() method to branch based on the version of
'     SecureCRT running the script.
'   - How to use the VBScript Replace() method to substitute text within
'     an existing string.

' Extract SecureCRT's version components to determine how to go about
' getting the current selection (version 6.1 has an ActiveX scripting object
' for accessing the selection, but earlier versions do not)
szVersionPart = Split(crt.Version, " ")(0)
vVersionElements = Split(szVersionPart, ".")
nMajor = vVersionElements(0)
nMinor = vVersionElements(1)
nMaintenance = vVersionElements(2)


' Using GetScriptTab() will make this script 'tab safe' in that all of the
' script's functionality will be carried out on the correct tab. From here
' on out we'll use the objTab object instead of the crt object.
Dim g_objTab
Set g_objTab = crt.GetScriptTab
g_objTab.Screen.Synchronous = True


'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sub Main()
    if crt.Session.Connected = False then
        MsgBox "This script currently requires a valid connection to a " & _
            "Cisco Pix firewall or other similar device." & vbcrlf & vbcrlf & _
            "Please connect and then run this script again."
        exit sub
    end if
    crt.Screen.Synchronous = True
    
    ' We'll use a "SendExpect" function we wrote (see below) to help us
    ' easily send commands and wait for the remote device to be ready for
    ' us to send the next command (by waiting for text we assume indicates
    ' the remote device is ready -- a prompt for example)
    If Not SendExpect("enable", "ssword:") then exit sub
    If Not SendExpect("", "# ") then exit sub
    If Not SendExpect("configure terminal", "(config)# ") then exit sub
    If Not SendExpect("pager 0", "(config)# ") then exit sub
    
    ' Now, we'll use another function we wrote called "CaptureOutputOfCommand",
    ' which takes as its first parameter the command to run, and as the 2nd
    ' parameter, the text that indicates the command has completed -- the prompt
    ' in most cases.
    szData = CaptureOutputOfCommand("show config", "(config)# ")
    szData = szData & CaptureOutputOfCommand("show serial", "(config)# ")
    szData = szData & CaptureOutputOfCommand("show sysopt", "(config)# ")  
    
    ' Some Cisco devices send EOL as LFCR rather than CRLF.  If we find the
    ' LFCR pattern, let's replace it with the Windows CRLF.
    szData = Replace(szData, vblf & vbcr, vbcrlf)
    
    ' Now that we have captured the output of each of the 'show' commands, let's
    ' send the data to the windows clipboard using another helper function we
    ' wrote: 'SetClipboardText' (see below).
    If Not SetClipboardText(szData) then
        MsgBox "Unable to set clipboard text."
        exit sub
    end if
    
    ' Now get back to a normalized state on the remote device
    If Not SendExpect("exit", "# ") then exit sub
    If Not SendExpect("exit", "> ") then exit sub
    
    MsgBox "Text is now in the clipboard: " & vbcrlf & vbcrlf & _
        GetClipboardText
    
End Sub

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function SendExpect(szSend, szExpect)
  ' Returns true if the text in 'szSend' was successfully sent and
  ' the text in 'szExpect' was successfully found as a result.

    ' If we're not connected, we can't possibly return true, or even send/recv
    ' text
    if g_objTab.Session.Connected <> True then exit function
        
    g_objTab.Screen.Send szSend & vbcr
    g_objTab.Screen.WaitForString szExpect

    SendExpect = True
End Function

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function CaptureOutputOfCommand(szCommand, szPrompt)
    if crt.Session.Connected <> True then
        CaptureOutputOfCommand = "[ERROR: Not Connected.]"
        exit function
    end if
    
    ' First, send the command to the remote.
    g_objTab.Screen.Send szCommand & vbcr
    
    ' Second, wait for the carriage return to be echoed by the remote device.
    ' This allows us to capture only the output of the command, not the line
    ' on which the command was issued (which would include the prompt + cmd).
    ' If you want to capture the command that was issued, simply comment out
    ' the following line of code.
    g_objTab.Screen.WaitForString vbcr
    
    ' Now that the command has been sent, use Screen.ReadString to capture
    ' all the data that is received up to the point at which the shell
    ' prompt appears (the captured data does not include the shell prompt).
    CaptureOutputOfCommand = g_objTab.Screen.ReadString(szPrompt)
End Function

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function SetClipboardText(szText)
    SetClipboardText = FALSE
    if nMajor >= 6 and nMinor > 0 then
        'MsgBox "Using new SecureCRT 6.1 API to set the clipboard text"
        crt.Clipboard.Format = "CF_TEXT"
        crt.Clipboard.Text = szText
    else
        'MsgBox "Using IE and clipboard copy to set the selected text"
        If Not SetClipboardTextWithOldVersionOfSecureCRT(szText) then
            exit function
        end if
    end if

    SetClipboardText = True
End Function

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function SetClipboardTextWithOldVersionOfSecureCRT(szText)
    ' http://msdn.microsoft.com/library/default.asp?url=/workshop/author/dhtml/reference/objects/clipboarddata.asp
    ' Put the value of szText into the IE Clipboard object...
    On Error Resume Next
    Do
        Err.Clear
        Set objIE = CreateObject("InternetExplorer.Application")
        objIE.Navigate "about:blank"
        SetClipboardTextWithOldVersionOfSecureCRT = _
            objIE.document.parentwindow.clipboardData.SetData(_
                "Text", _
                szText)
        If Err.Number = 0 then exit do
        WScript.Sleep 25
    Loop
    On Error Goto 0
    objIE.Quit
    Set objIE = Nothing
End Function

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function GetClipboardText()
    GetClipboardText = FALSE
    if nMajor >= 6 and nMinor > 0 then
        'Using new API to set the clipboard text
        GetClipboardText = crt.Clipboard.Text
    else
        'Using IE and clipboard copy to get the selected text
        GetClipboardText = GetClipboardTextWithOldVersionOfSecureCRT
    end if
End Function

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function GetClipboardTextWithOldVersionOfSecureCRT()
    ' http://msdn.microsoft.com/library/default.asp?url=/workshop/author/dhtml/reference/objects/clipboarddata.asp
    ' Extract the data from the clipboard into a variable
    nCounter = 0
    nMaxTries = 100
    On Error Resume Next
    Do
        Err.Clear
        Set objIE = CreateObject("InternetExplorer.Application")
        objIE.Navigate "about:blank"
        GetClipboardTextWithOldVersionOfSecureCRT = _
            objIE.document.parentwindow.clipboardData.GetData("Text")
        if Err.Number = 0 then
            exit do
        end if
        nCounter = nCounter + 1
        if nCounter > nMaxTries then exit do
        
        WScript.Sleep 25
    Loop
    objIE.Quit
    Set objIE = Nothing
    On Error Goto 0
End Function
