# $language = "VBScript"
# $interface = "1.0"
' GoogleSelectedText.vbs
' 
' Description:
'   When this script is launched, the text selected within the terminal
'   window is used as the search term for a web search using google.com.
'   This script demonstrates capabilities only available in SecureCRT 6.1
'   and later (Screen.Selection property), but also provides a backwards
'   compatibility hack for earlier versions of SecureCRT.
' 
' Demonstrates:
'   - How to use the Screen.Selection property in SecureCRT 6.1 and later
'     to get access to the text selected in the terminal window.
'   - How to use the WScript.Shell object to launch an external application
'   - How to branch code based on version of SecureCRT in which this script
'     is being run.
'   - How to access selected text in versions prior to SecureCRT 6.1 by
'     using SendSpecial("MENU_COPY") to copy the selected text to the Windows
'     clipboard, then use the ActiveX InternetExplorer application to gain
'     access to the data stored in the Windows clipboard.

Sub Main()
    ' Extract SecureCRT's version components to determine how to go about
    ' getting the current selection (version 6.1 provides a scripting API
    ' for accessing the screen's selection, but earlier versions do not)
    szVersionPart = Split(crt.Version, " ")(0)
    vVersionElements = Split(szVersionPart, ".")
    nMajor = vVersionElements(0)
    nMinor = vVersionElements(1)
    nMaintenance = vVersionElements(2)
    
    if nMajor >= 6 and nMinor > 0 then
        ' Use new API to get the selected text:
        szSelection = Trim(crt.Screen.Selection)
    else
        If not crt.Session.Connected then
            crt.Dialog.MessageBox _
                   "In versions prior to 6.1, SecureCRT must have " & _
                   "an active connection when this script is run. " & _
                   vbcrlf & _
                   "Versions of SecureCRT 6.1 and later provide a " & _
                   "Screen.Selection property that can be used without " & _
                   "a valid connection being established." & vbcrlf & vbcrlf & _
                   "Connect to a remote system and run this script again."
            exit sub
        end if
    
        ' Use older method (IE clipboard copy) to get the selected text:
        szSelection = Trim(GetSelectedTextWithOldVersionOfSecureCRT)
    end if
    
    ' Now search on google for the information.
    g_szSearchBase = "http://www.google.com/search?hl=en&q="

    Set g_shell = CreateObject("WScript.Shell")
    
    ' Instead of launching InternetExplorer, we'll run the URL, so that the
    ' default browser gets used :).
    if szSelection = "" then
        g_shell.Run chr(34) & "http://www.google.com/" & chr(34)
    else
        g_shell.Run chr(34) & "http://www.google.com/search?hl=en&q=" & szSelection & chr(34)
    end if
end sub

'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Function GetSelectedTextWithOldVersionOfSecureCRT()
    ' send the selected text to the clipboard
    crt.screen.sendspecial "MENU_COPY"

    ' Extract the selected text from the clipboard into a variable as "Text"
    Set objIE = CreateObject("InternetExplorer.Application")
    objIE.Navigate "about:blank"
    szSelection = objIE.document.parentwindow.clipboardData.GetData("text")
    objIE.Quit
    
    GetSelectedTextWithOldVersionOfSecureCRT = szSelection
end Function

