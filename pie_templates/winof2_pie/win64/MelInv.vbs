'Mellanox Device Driver DUP Inventory
'Author: Ken Bignell
'Version 5.1
'Created: 13 December, 2005
'Modified: 13 August, 2013

Option Explicit
Dim ws, fso, LogName, RegKeyVer, NXDrv, theArgs, strComputer, FilePrint, strValue, SysVar, SysRoot, NXDrvChk, log, RegKeyOne, OSVer, RegKeyTwo, XmlNone, theLine, XmlSome, HrdWarePrsnt, objWMIService, colNetwork, objNetwork, QuoteObj, CrLfObj, XmlOpen, XmlClose, XmlError, ErrorID, ErrorString, VerComp, RegKeyUmbrella, deviceIDs, DrvCount, NoDrvCount, DupNotApp

Const ForReading = 1
Const ForWriting = 2
Const TristateFalse = 0
Const configConst = "MelDUPconfig.xml"
Const HKEY_LOCAL_MACHINE = &H80000002

'Create Object
Set ws = WScript.CreateObject("WScript.Shell")
'Get system environment variables such as the systemroot
set SysVar = ws.Environment ("Process")
SysRoot = SysVar ("SYSTEMROOT")
strComputer = "."

'Check the command line arguments for validity
set theArgs = Wscript.Arguments
if theArgs.count >= 1 then
 'check the arguments for validity
 if theArgs.count > 2 then 
  call UsageHelp()
 end if
 FilePrint = "help"
 if theArgs.Item(0) = "file" then 
  FilePrint = "file"
 elseif theArgs.Item(0) = "print" then 
  FilePrint = "print"
 else 
  call UsageHelp()
 end if
 if theArgs.count < 2 Then
  LogName = ConfigLog()
 else
  LogName = theArgs.Item(1)
 end if
else
 FilePrint = "file"
 LogName = ConfigLog()
end if

Call HardCheck()
Call OSProps()
Call UmbrellaInstall()
if RegKeyVer = "" or RegKeyVer = "0" then
	DupNotApp = PnPInstallerVersion()
	if DupNotApp = "false" then 
		RegKeyVer = "0"
	else
		RegKeyVer = "1"
	end if
end if
call OutPut(FilePrint)

'*****Functions******
'Function to check for hardware
Function HardCheck()
	dim icount, venID
	venID = ConfigVenID()
	ConfigDevIDs()
 	HrdWarePrsnt = "False"
 	set objWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")
 	set colNetwork = objWMIService.ExecQuery ("SELECT * FROM Win32_PnPEntity where pnpdeviceid like '%" & venID & "%'")
 	for each objNetwork in colNetwork
		for icount = 0 to UBound(deviceIDs)
			if instr(LCase(objNetwork.PNPDeviceID), deviceIDs(icount)) <> 0 then
				HrdWarePrsnt = "True"
				DrvCount = DrvCount + 1
				if objNetwork.Status <> "OK" and (objNetwork.ConfigManagerErrorCode = 1 or objNetwork.ConfigManagerErrorCode = 28) and isnull(objNetwork.Service) then
				NoDrvCount = NoDrvCount + 1
				else
					exit for
				end if
			end if
		next
 	next
 	if HrdWarePrsnt = "False" then 
 		call OutPut(FilePrint)
 	end if
End Function

'Function to query WMI for the OS version
Function OSProps()
'need to abstract OS support to get the OS list from the config XML
on error resume next
	Dim colOperatingSystems, objOperatingSystem
  	Set objWMIService = GetObject("winmgmts:" & "{impersonationLevel=impersonate}!\\" & strComputer & "\root\cimv2")
  	Set colOperatingSystems = objWMIService.ExecQuery ("Select * from Win32_OperatingSystem")
  	for each objOperatingSystem in colOperatingSystems
	  	if instr(objOperatingSystem.Caption, "2003") <> 0 then
	  		if instr(objOperatingSystem.Caption, "64") <> 0 then
	  			OSVer = "win200364"
	  		elseif instr(objOperatingSystem.Caption, "64") = 0 then
	  			OSVer = "win200332"
	  		end if
	  	elseif instr(objOperatingSystem.Caption, "2012") <> 0 or instr(objOperatingSystem.Caption, "2008") <> 0 or instr(objOperatingSystem.Caption, "Hyper-V") <> 0 or instr(objOperatingSystem.Caption, "Small Business Server 2011")  then
	  		if instr(objOperatingSystem.OSArchitecture, "64") <> 0 then
	  			OSVer = "win200864"
	  		elseif instr(objOperatingSystem.OSArchitecture, "32") <> 0 then
	  			OSVer = "win200832"
	  		end if
        elseif instr(objOperatingSystem.Caption, "2016") <> 0 then
	  		if instr(objOperatingSystem.OSArchitecture, "64") <> 0 then
	  			OSVer = "win201664"
	  		elseif instr(objOperatingSystem.OSArchitecture, "32") <> 0 then
	  			OSVer = "win201632"
	  		end if
        elseif instr(objOperatingSystem.Caption, "2019") <> 0 then
	  		if instr(objOperatingSystem.OSArchitecture, "64") <> 0 then
	  			OSVer = "win201964"
	  		elseif instr(objOperatingSystem.OSArchitecture, "32") <> 0 then
	  			OSVer = "win201932"
	  		end if
		elseif instr(objOperatingSystem.Caption, "2022") <> 0 then
	  		if instr(objOperatingSystem.OSArchitecture, "64") <> 0 then
	  			OSVer = "win202264"
	  		elseif instr(objOperatingSystem.OSArchitecture, "32") <> 0 then
	  			OSVer = "win202232"
			end if
		elseif instr(objOperatingSystem.Caption, "2025") <> 0 then
	  		if instr(objOperatingSystem.OSArchitecture, "64") <> 0 then
	  			OSVer = "win202564"
	  		elseif instr(objOperatingSystem.OSArchitecture, "32") <> 0 then
	  			OSVer = "win202532"
			end if
		elseif instr(objOperatingSystem.Caption, "HCI") <> 0 then
            OSVer = "winHCI"
		elseif instr(objOperatingSystem.Caption, "HCI2") <> 0 then
            OSVer = "winHCI2"
		elseif instr(objOperatingSystem.Caption, "HCI3") <> 0 then
            OSVer = "winHCI3"
        elseif instr(objOperatingSystem.Caption, "HCI4") <> 0 then
            OSVer = "winHCI4"

	  	else
	  		call OutPut(FilePrint)
	  	end if
  	next
on error goto 0
End Function

'Function to get umbrella installer version
Function UmbrellaInstall()
	dim ret, file64, valKey, strRegKey, altValue
 	On Error Resume Next
 	strRegKey = GetRegKey("umb", "1")
 	if instr(OSVer, "64") <> 0 then
 		dim strRegKeyPath, strRegKeyValue
 		strRegKeyPath = left(strRegKey, (instrrev(strRegKey, "\") - 1))
 		strRegKeyPath = right(strRegKeyPath, (len(strRegKeyPath) - (instr(strRegKeyPath, "\"))))
 		strRegKeyValue = right(strRegKey, (len(strRegKey) - (instrrev(strRegKey, "\"))))
 		strValue = ws.RegRead("HKLM\SOFTWARE\Dell\MUP\MLNX_WinOF2\build version")
	end if
 	If strValue = "" Then
 		if DrvCount = NoDrvCount then 
 			RegKeyVer = "0"
 		elseif altValue <> "" then
 			RegKeyVer = altValue
 		else 
 			RegKeyVer = "0"
  		end if
 	Else
  		RegKeyVer = strValue
 	End If
 	on error goto 0
End Function

'Function to output success to required place
Function OutPut(varA)
 Call SetXml("clear")
 if varA = "print" then
  if RegKeyVer = "" then
   WScript.Echo XmlNone
  else
   WScript.Echo XmlOpen + XmlSome + XmlCLose
  end if
 elseif varA = "file" then
  CreateFile
  set log = fso.OpenTextFile (LogName, ForWriting, True, TriStateFalse)
  if RegKeyVer = "" then
   log.Write XmlNone
  else
   log.Write XmlOpen + XmlSome + XmlClose
  end if
  log.Close
  DestroyFile
 end if
 WScript.Quit 0
End Function

'Function to create File System Object
Function CreateFile()
  set fso = WScript.CreateObject("Scripting.FileSystemObject")
End Function

'Function to destroy File System Object
Function DestroyFile()
  set fso = Nothing
End Function

'Function to display command line help
Function UsageHelp()
  WScript.Echo "Usage: " & wscript.scriptname & " [option...] [path and logfile name]" + CrLfObj + CrLfObj + "Options:" + CrLfObj + CrLfObj + CrLfObj + "Print - Prints to the screen." + CrLfObj + "File - Creates a log file" + CrLfObj + CrLfObj + "Path and logfile name is the full path and name of the log file to be created.  If the path or file name has any spaces, you must include the entire string in quotes." + CrLfObj
 ErrorID = "2"
 WScript.Quit ErrorID
 End Function

'Function to set up XML output variables
Function SetXml(status)
 QuoteObj = (Chr(34))
 CrLfObj = (Chr(13)) + (Chr(10))
 XmlOpen = "<?xml version=" + QuoteObj + "1.0" + QuoteObj + "  encoding=" + QuoteObj + "UTF-8" + QuoteObj + "?>" + CrLfObj + "<SVMInventory lang=" + QuoteObj + "en" + QuoteObj + ">"
 XmlClose = CrLfObj + "</SVMInventory>"
 XmlNone = XmlOpen +  XmlClose
 if status <> "error" then
 	XmlSome = CrLfObj + "  <Device componentID=" + QuoteObj + ComponentID() + QuoteObj + " enum=" + QuoteObj + EnumString() + QuoteObj + " display=" + QuoteObj + DisplayString() + QuoteObj + ">" + CrLfObj + "    <Application componentType=" + QuoteObj + "DRVR" + QuoteObj + " version=" + QuoteObj + RegKeyVer + QuoteObj + " display=" + QuoteObj + DisplayString() + QuoteObj + "/>" + CrLfObj +"  </Device>"
 end if
 XmlError = CrLfObj + "  <SPStatus result=" + QuoteObj + "false" + QuoteObj + ">" + CrLfObj + "    <Message id=" + QuoteObj + ErrorID + QuoteObj + ">" + ErrorString + "</Message>" + CrLfObj + "  </SPStatus>"
End Function

'Function to output error
Function ErrorOut(varA, varB)
 if varB = "1" then ErrorString = "OS is not supported"
 if varB = "2" then ErrorString = "Incorrect command line parameters used"
 if varB = "3" then ErrorString = "General Failure, specifics not known"
 if varB = "4" then ErrorString = "No supported hardware found"
 if varB = "5" then ErrorString = "Config file not found"
 Call SetXml("error")
 if varA = "print" then 
  WScript.Echo XmlOpen + XmlError + XmlClose
 else
  CreateFile
  set log = fso.OpenTextFile (LogName, ForWriting, True, TriStateFalse)
  log.Write XmlOpen + XmlError + XmlClose
  log.Close
  DestroyFile
 end if
 Wscript.Quit ErrorID
End Function

'Function to process the config file for the default log name
Function ConfigLog()
dim configFile, fileLine, endcomment
	CreateFile()
	if fso.FileExists(configConst) then
		set configFile = fso.OpenTextFile(configConst, ForReading, True, TriStateFalse)
		do until configFile.AtEndOfStream
			fileLine = configFile.ReadLine
			if instr(fileLine, "<!--") <> 0 then 
				endcomment = 0
				do while endcomment = 0
					fileLine = configFile.ReadLine
					if instr(fileLine, "-->") <> 0 then 
						endcomment = 1
					end if
				loop
			elseif instr(fileLine, "<invlogname>") <> 0 then
				if instr(fileLine, Chr(9)) <> 0 then 
					fileLine = replace(fileLine, Chr(9), "")
				end if
				LogName = replace(fileLine, "<invlogname>", "")
				LogName = replace(LogName, "</invlogname>", "")
				LogName = trim(LogName)
				ConfigLog = LogName
				exit do
			end if
		loop
		configFile.close
	else
		LogName = "BcomInv.xml"
		call ErrorOut(FilePrint, "5")
	end if
	DestroyFile()
end function

'Function to process the config file for the vendor ID
Function ConfigVenID()
dim configFile, fileLine, endcomment
	CreateFile()
	if fso.FileExists(configConst) then
		set configFile = fso.OpenTextFile(configConst, ForReading, True, TriStateFalse)
		do until configFile.AtEndOfStream
			fileLine = configFile.ReadLine
			if instr(fileLine, "<!--") <> 0 then 
				endcomment = 0
				do while endcomment = 0
					fileLine = configFile.ReadLine
					if instr(fileLine, "-->") <> 0 then 
						endcomment = 1
					end if
				loop
			elseif instr(lcase(fileLine), "<udupconfig vendor") <> 0 then
				if instr(fileLine, Chr(9)) <> 0 then 
					fileLine = replace(fileLine, Chr(9), "")
				end if
				ConfigVenID = replace(lcase(fileLine), "<udupconfig vendor=" & Chr(34), "")
				ConfigVenID = replace(ConfigVenID, Chr(34) & ">", "")
				ConfigVenID = LTrim(ConfigVenID)
				ConfigVenID = RTrim(ConfigVenID)
				exit do
			end if
		loop
		configFile.close
	else
		call ErrorOut(FilePrint, "5")
	end if
	DestroyFile()
end function

'Function to process the config file for the device IDs
Function ConfigDevIDs()
dim configFile, fileLine, endcomment, NumDevs, i
	CreateFile()
	if fso.FileExists(configConst) then
		set configFile = fso.OpenTextFile(configConst, ForReading, True, TriStateFalse)
		do until configFile.AtEndOfStream
			fileLine = configFile.ReadLine
			if instr(fileLine, "<!--") <> 0 then 
				endcomment = 0
				do while endcomment = 0
					fileLine = configFile.ReadLine
					if instr(fileLine, "-->") <> 0 then 
						endcomment = 1
					end if
				loop
			elseif instr(lcase(fileLine), "<numberdevices total") <> 0 then
				if instr(fileLine, Chr(9)) <> 0 then 
					fileLine = replace(fileLine, Chr(9), "")
				end if
				NumDevs = replace(lcase(fileLine), "<numberdevices total=" & Chr(34), "")
				NumDevs = replace(NumDevs, Chr(34) & ">", "")
				NumDevs = LTrim(NumDevs)
				NumDevs = RTrim(NumDevs)
				exit do
			end if
		loop
		redim deviceIDs(NumDevs - 1)
		i = 0
		do while i <= (NumDevs - 1)
			fileLine = configFile.ReadLine
			if instr(fileLine, Chr(9)) <> 0 then 
				fileLine = replace(fileLine, Chr(9), "")
			end if
			if instr(fileLine, "<deviceid>") then
				deviceIDs(i) = replace(fileLine, "<deviceid>", "")
				deviceIDs(i) = replace(deviceIDs(i), "</deviceid>", "")
				i = i + 1
			end if
		loop
		configFile.close
	else
		call ErrorOut(FilePrint, "5")
	end if
	DestroyFile()
end function

'Function to process the config file for the device IDs
Function GetRegKey(varA, varB)
dim configFile, fileLine, strOSkey, endcomment
	CreateFile()
	if fso.FileExists(configConst) then
		set configFile = fso.OpenTextFile(configConst, ForReading, True, TriStateFalse)
		do until configFile.AtEndOfStream
			fileLine = configFile.ReadLine
			if instr(fileLine, "<!--") <> 0 then 
				endcomment = 0
				do while endcomment = 0
					fileLine = configFile.ReadLine
					if instr(fileLine, "-->") <> 0 then 
						endcomment = 1
					end if
				loop
			elseif instr(fileLine, "<" & varA & "regkey OS") <> 0 then
				if instr(fileLine, Chr(9)) <> 0 then 
					fileLine = replace(fileLine, Chr(9), "")
				end if
				strOSkey = replace(fileLine, "<" & varA & "regkey OS=" & Chr(34), "")
				if left(strOSkey, 3) = "all" then
					strOSkey = replace(strOSkey, "all" & Chr(34) & " NumKeys=" & Chr(34) & varB & Chr(34) & ">", "")
					strOSkey = replace(strOSkey, "</" & varA & "regkey>", "")
					exit do
				elseif instr(strOSkey, OSVer) then
					strOSkey = replace(strOSkey, OSVer & Chr(34) & " NumKeys=" & Chr(34) & varB & Chr(34) & ">", "")
					strOSkey = replace(strOSkey, "</" & varA & "regkey>", "")
					exit do
				end if
			end if
		loop
		GetRegKey = strOSkey
		configFile.close
	else
		call ErrorOut(FilePrint, "5")
	end if
	DestroyFile()
end function

'Function to process the config file for the Component ID
Function ComponentID()
dim configFile, fileLine, CompID, endcomment
	CreateFile()
	if fso.FileExists(configConst) then
		set configFile = fso.OpenTextFile(configConst, ForReading, True, TriStateFalse)
		do until configFile.AtEndOfStream
			fileLine = configFile.ReadLine
			if instr(fileLine, "<!--") <> 0 then 
				endcomment = 0
				do while endcomment = 0
					fileLine = configFile.ReadLine
					if instr(fileLine, "-->") <> 0 then 
						endcomment = 1
					end if
				loop
			elseif instr(fileLine, "<componentid>") <> 0 then
				if instr(fileLine, Chr(9)) <> 0 then 
					fileLine = replace(fileLine, Chr(9), "")
				end if
				CompID = replace(fileLine, "<componentid>", "")
				CompID = replace(CompID, "</componentid>", "")
				CompID = LTrim(CompID)
				CompID = RTrim(CompID)
				exit do
			end if
		loop
		ComponentID = CompID
		configFile.close
	else
		call ErrorOut(FilePrint, "5")
	end if
	DestroyFile()
end function

'Function to process the config file for the Enumeration String
Function EnumString()
dim configFile, fileLine, strEnum, endcomment
	CreateFile()
	if fso.FileExists(configConst) then
		set configFile = fso.OpenTextFile(configConst, ForReading, True, TriStateFalse)
		do until configFile.AtEndOfStream
			fileLine = configFile.ReadLine
			if instr(fileLine, "<!--") <> 0 then 
				endcomment = 0
				do while endcomment = 0
					fileLine = configFile.ReadLine
					if instr(fileLine, "-->") <> 0 then 
						endcomment = 1
					end if
				loop
			elseif instr(fileLine, "<enumstring>") <> 0 then
				if instr(fileLine, Chr(9)) <> 0 then 
					fileLine = replace(fileLine, Chr(9), "")
				end if
				strEnum = replace(fileLine, "<enumstring>", "")
				strEnum = replace(strEnum, "</enumstring>", "")
				strEnum = LTrim(strEnum)
				strEnum = RTrim(strEnum)
				exit do
			end if
		loop
		EnumString = strEnum
		configFile.close
	else
		call ErrorOut(FilePrint, "5")
	end if
	DestroyFile()
end function

'Function to process the config file for the Display String
Function DisplayString()
dim configFile, fileLine, strDisplay, endcomment
	CreateFile()
	if fso.FileExists(configConst) then
		set configFile = fso.OpenTextFile(configConst, ForReading, True, TriStateFalse)
		do until configFile.AtEndOfStream
			fileLine = configFile.ReadLine
			if instr(fileLine, "<!--") <> 0 then 
				endcomment = 0
				do while endcomment = 0
					fileLine = configFile.ReadLine
					if instr(fileLine, "-->") <> 0 then 
						endcomment = 1
					end if
				loop
			elseif instr(fileLine, "<displaystring>") <> 0 then
				if instr(fileLine, Chr(9)) <> 0 then 
					fileLine = replace(fileLine, Chr(9), "")
				end if
				strDisplay = replace(fileLine, "<displaystring>", "")
				strDisplay = replace(strDisplay, "</displaystring>", "")
				strDisplay = LTrim(strDisplay)
				strDisplay = RTrim(strDisplay)
				exit do
			end if
		loop
		DisplayString = strDisplay
		configFile.close
	else
		call ErrorOut(FilePrint, "5")
	end if
	DestroyFile()
end function

'Funciton to get PnP UInstallerVersion
Function PnPInstallerVersion()
	dim strRegKey, numRegKeys, PnPBaseFlag
 	On Error Resume Next
 	PnPBaseFlag = "false"
 		numRegKeys = GetNumRegKeys("inf")
 		if numRegKeys = "1" then
	 		strRegKey = GetRegKey("inf", numRegKeys)
			strValue = ws.RegRead(strRegKey)
	   		if strValue <> "" then 
	     		PnPBaseFlag = "true"
	   		end if
	   	else
	   		dim arrRegKeys(), i, strAllRegKeys, arrProdVersions(), j, k, ProdVerStore, l
   			strAllRegKeys = GetRegKey("inf", numRegKeys)
	   		for i = 0 to (numRegKeys - 1)
	   			redim preserve arrRegKeys(i)
	   			arrRegKeys(i) = left(strAllRegKeys, (instr(strAllRegKeys, ",") - 1))
	   			strAllRegKeys = replace(strAllRegKeys, arrRegKeys(i) & ", ", "")
	   		next
	   		for j = lbound(arrRegKeys) to ubound(arrRegKeys)
	   			strValue = ws.RegRead(arrRegKeys(j))
	   			if strValue <> "" then 
	   				PnPBaseFlag = strValue
	   			end if
	   		next
	   	end if
	   	PnPInstallerVersion = PnPBaseFlag
   		on error goto 0
End Function

'Function to process the config file for the device IDs
Function GetNumRegKeys(varA)
dim configFile, fileLine, strOSkey, endcomment
	CreateFile()
	if fso.FileExists(configConst) then
		set configFile = fso.OpenTextFile(configConst, ForReading, True, TriStateFalse)
		do until configFile.AtEndOfStream
			fileLine = configFile.ReadLine
			if instr(fileLine, "<!--") <> 0 then 
				endcomment = 0
				do while endcomment = 0
					fileLine = configFile.ReadLine
					if instr(fileLine, "-->") <> 0 then 
						endcomment = 1
					end if
				loop
			elseif instr(fileLine, "<" & varA & "regkey OS") <> 0 then
				if instr(fileLine, Chr(9)) <> 0 then 
					fileLine = replace(fileLine, Chr(9), "")
				end if
				strOSkey = replace(fileLine, "<" & varA & "regkey OS=" & Chr(34), "")
				if left(strOSkey, 3) = "all" then
					strOSkey = replace(strOSkey, "all" & Chr(34) & " NumKeys=" & Chr(34), "")
					strOSkey = left(strOSkey, (instr(strOSkey, Chr(34)) - 1))
					exit do
				elseif instr(strOSkey, OSVer) then
					strOSkey = replace(strOSkey, OSVer & Chr(34) & " NumKeys=" & Chr(34), "")
					strOSkey = left(strOSkey, (instr(strOSkey, Chr(34)) - 1))
					exit do
				end if
			end if
		loop
		GetNumRegKeys = strOSkey
		configFile.close
	else
		call ErrorOut(FilePrint, "5")
	end if
	DestroyFile()
end function
'' SIG '' Begin signature block
'' SIG '' MIImIwYJKoZIhvcNAQcCoIImFDCCJhACAQExDzANBglg
'' SIG '' hkgBZQMEAgEFADB3BgorBgEEAYI3AgEEoGkwZzAyBgor
'' SIG '' BgEEAYI3AgEeMCQCAQEEEE7wKRaZJ7VNj+Ws4Q8X66sC
'' SIG '' AQACAQACAQACAQACAQAwMTANBglghkgBZQMEAgEFAAQg
'' SIG '' ruJT7414SlpoxOf1VYsSAVK0Dyl2gK5EDVkawovxOHCg
'' SIG '' gg2lMIIGsDCCBJigAwIBAgIQCK1AsmDSnEyfXs2pvZOu
'' SIG '' 2TANBgkqhkiG9w0BAQwFADBiMQswCQYDVQQGEwJVUzEV
'' SIG '' MBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
'' SIG '' d3cuZGlnaWNlcnQuY29tMSEwHwYDVQQDExhEaWdpQ2Vy
'' SIG '' dCBUcnVzdGVkIFJvb3QgRzQwHhcNMjEwNDI5MDAwMDAw
'' SIG '' WhcNMzYwNDI4MjM1OTU5WjBpMQswCQYDVQQGEwJVUzEX
'' SIG '' MBUGA1UEChMORGlnaUNlcnQsIEluYy4xQTA/BgNVBAMT
'' SIG '' OERpZ2lDZXJ0IFRydXN0ZWQgRzQgQ29kZSBTaWduaW5n
'' SIG '' IFJTQTQwOTYgU0hBMzg0IDIwMjEgQ0ExMIICIjANBgkq
'' SIG '' hkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA1bQvQtAorXi3
'' SIG '' XdU5WRuxiEL1M4zrPYGXcMW7xIUmMJ+kjmjYXPXrNCQH
'' SIG '' 4UtP03hD9BfXHtr50tVnGlJPDqFX/IiZwZHMgQM+TXAk
'' SIG '' ZLON4gh9NH1MgFcSa0OamfLFOx/y78tHWhOmTLMBICXz
'' SIG '' ENOLsvsI8IrgnQnAZaf6mIBJNYc9URnokCF4RS6hnyzh
'' SIG '' GMIazMXuk0lwQjKP+8bqHPNlaJGiTUyCEUhSaN4QvRRX
'' SIG '' XegYE2XFf7JPhSxIpFaENdb5LpyqABXRN/4aBpTCfMjq
'' SIG '' GzLmysL0p6MDDnSlrzm2q2AS4+jWufcx4dyt5Big2MEj
'' SIG '' R0ezoQ9uo6ttmAaDG7dqZy3SvUQakhCBj7A7CdfHmzJa
'' SIG '' wv9qYFSLScGT7eG0XOBv6yb5jNWy+TgQ5urOkfW+0/tv
'' SIG '' k2E0XLyTRSiDNipmKF+wc86LJiUGsoPUXPYVGUztYuBe
'' SIG '' M/Lo6OwKp7ADK5GyNnm+960IHnWmZcy740hQ83eRGv7b
'' SIG '' UKJGyGFYmPV8AhY8gyitOYbs1LcNU9D4R+Z1MI3sMJN2
'' SIG '' FKZbS110YU0/EpF23r9Yy3IQKUHw1cVtJnZoEUETWJrc
'' SIG '' JisB9IlNWdt4z4FKPkBHX8mBUHOFECMhWWCKZFTBzCEa
'' SIG '' 6DgZfGYczXg4RTCZT/9jT0y7qg0IU0F8WD1Hs/q27Iwy
'' SIG '' CQLMbDwMVhECAwEAAaOCAVkwggFVMBIGA1UdEwEB/wQI
'' SIG '' MAYBAf8CAQAwHQYDVR0OBBYEFGg34Ou2O/hfEYb7/mF7
'' SIG '' CIhl9E5CMB8GA1UdIwQYMBaAFOzX44LScV1kTN8uZz/n
'' SIG '' upiuHA9PMA4GA1UdDwEB/wQEAwIBhjATBgNVHSUEDDAK
'' SIG '' BggrBgEFBQcDAzB3BggrBgEFBQcBAQRrMGkwJAYIKwYB
'' SIG '' BQUHMAGGGGh0dHA6Ly9vY3NwLmRpZ2ljZXJ0LmNvbTBB
'' SIG '' BggrBgEFBQcwAoY1aHR0cDovL2NhY2VydHMuZGlnaWNl
'' SIG '' cnQuY29tL0RpZ2lDZXJ0VHJ1c3RlZFJvb3RHNC5jcnQw
'' SIG '' QwYDVR0fBDwwOjA4oDagNIYyaHR0cDovL2NybDMuZGln
'' SIG '' aWNlcnQuY29tL0RpZ2lDZXJ0VHJ1c3RlZFJvb3RHNC5j
'' SIG '' cmwwHAYDVR0gBBUwEzAHBgVngQwBAzAIBgZngQwBBAEw
'' SIG '' DQYJKoZIhvcNAQEMBQADggIBADojRD2NCHbuj7w6mdNW
'' SIG '' 4AIapfhINPMstuZ0ZveUcrEAyq9sMCcTEp6QRJ9L/Z6j
'' SIG '' fCbVN7w6XUhtldU/SfQnuxaBRVD9nL22heB2fjdxyyL3
'' SIG '' WqqQz/WTauPrINHVUHmImoqKwba9oUgYftzYgBoRGRjN
'' SIG '' YZmBVvbJ43bnxOQbX0P4PpT/djk9ntSZz0rdKOtfJqGV
'' SIG '' WEjVGv7XJz/9kNF2ht0csGBc8w2o7uCJob054ThO2m67
'' SIG '' Np375SFTWsPK6Wrxoj7bQ7gzyE84FJKZ9d3OVG3ZXQIU
'' SIG '' H0AzfAPilbLCIXVzUstG2MQ0HKKlS43Nb3Y3LIU/Gs4m
'' SIG '' 6Ri+kAewQ3+ViCCCcPDMyu/9KTVcH4k4Vfc3iosJocsL
'' SIG '' 6TEa/y4ZXDlx4b6cpwoG1iZnt5LmTl/eeqxJzy6kdJKt
'' SIG '' 2zyknIYf48FWGysj/4+16oh7cGvmoLr9Oj9FpsToFpFS
'' SIG '' i0HASIRLlk2rREDjjfAVKM7t8RhWByovEMQMCGQ8M4+u
'' SIG '' KIw8y4+ICw2/O/TOHnuO77Xry7fwdxPm5yg/rBKupS8i
'' SIG '' bEH5glwVZsxsDsrFhsP2JjMMB0ug0wcCampAMEhLNKhR
'' SIG '' ILutG4UI4lkNbcoFUCvqShyepf2gpx8GdOfy1lKQ/a+F
'' SIG '' SCH5Vzu0nAPthkX0tGFuv2jiJmCG6sivqf6UHedjGzqG
'' SIG '' VnhOMIIG7TCCBNWgAwIBAgIQC2vPUnYL/EP1UsyYoLxE
'' SIG '' EDANBgkqhkiG9w0BAQsFADBpMQswCQYDVQQGEwJVUzEX
'' SIG '' MBUGA1UEChMORGlnaUNlcnQsIEluYy4xQTA/BgNVBAMT
'' SIG '' OERpZ2lDZXJ0IFRydXN0ZWQgRzQgQ29kZSBTaWduaW5n
'' SIG '' IFJTQTQwOTYgU0hBMzg0IDIwMjEgQ0ExMB4XDTIyMDIx
'' SIG '' OTAwMDAwMFoXDTI1MDIxOTIzNTk1OVowcjELMAkGA1UE
'' SIG '' BhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFDASBgNV
'' SIG '' BAcTC1NhbnRhIENsYXJhMRswGQYDVQQKExJOVklESUEg
'' SIG '' Q29ycG9yYXRpb24xGzAZBgNVBAMTEk5WSURJQSBDb3Jw
'' SIG '' b3JhdGlvbjCCAaIwDQYJKoZIhvcNAQEBBQADggGPADCC
'' SIG '' AYoCggGBAMSiDsfFNa5hVA5ZBwGkZ1ycenLDkYd8HsCx
'' SIG '' AGSfDl3/MHWTLFnZzcOkFW7FaK04eCZR9ZhAs8g9J03a
'' SIG '' dONs0nKWmccFZQGGMQPghhw+cfjZWY3h2xKEiLX2XphC
'' SIG '' pGgDc4PKOWe3zFmLFcK1U14GgngSnbM/xtNtvs72Vkdn
'' SIG '' X/13apYYVg+qpDu58O/9NRQqPjaqtBgI/5deS60VrNUY
'' SIG '' 2azHkHteywFd8MAyxXEKsUc5eyQYVPSRLcE40hiILIqL
'' SIG '' 5Silyp4UMy7beSWN+cATHrueAjHrZo2wmM4T7+CJ8KG3
'' SIG '' 8KdEVYQQCDPazLHH50iRxacGajSm7pUMKThkg67Kr8MM
'' SIG '' 6hRJ0IMSv00P3gC5Ok3lSJI0Pg0MMqYDZytRz5ykuaD6
'' SIG '' FoQU+23bY2Hq25vzTkfRIIbXt3pe+HZkzVaLAYi9vy8k
'' SIG '' oBkCtSI5VWkvpMhHnPkrIFOYYug5g9ROZvNQXIidnPsC
'' SIG '' OTGxR7J6xHUJoOUSXQSEWi4AqLTI3dV8fIWK4wIDAQAB
'' SIG '' o4ICBjCCAgIwHwYDVR0jBBgwFoAUaDfg67Y7+F8Rhvv+
'' SIG '' YXsIiGX0TkIwHQYDVR0OBBYEFN6XMNWcjDiCB2C7uE4D
'' SIG '' WNVrP6CrMA4GA1UdDwEB/wQEAwIHgDATBgNVHSUEDDAK
'' SIG '' BggrBgEFBQcDAzCBtQYDVR0fBIGtMIGqMFOgUaBPhk1o
'' SIG '' dHRwOi8vY3JsMy5kaWdpY2VydC5jb20vRGlnaUNlcnRU
'' SIG '' cnVzdGVkRzRDb2RlU2lnbmluZ1JTQTQwOTZTSEEzODQy
'' SIG '' MDIxQ0ExLmNybDBToFGgT4ZNaHR0cDovL2NybDQuZGln
'' SIG '' aWNlcnQuY29tL0RpZ2lDZXJ0VHJ1c3RlZEc0Q29kZVNp
'' SIG '' Z25pbmdSU0E0MDk2U0hBMzg0MjAyMUNBMS5jcmwwPgYD
'' SIG '' VR0gBDcwNTAzBgZngQwBBAEwKTAnBggrBgEFBQcCARYb
'' SIG '' aHR0cDovL3d3dy5kaWdpY2VydC5jb20vQ1BTMIGUBggr
'' SIG '' BgEFBQcBAQSBhzCBhDAkBggrBgEFBQcwAYYYaHR0cDov
'' SIG '' L29jc3AuZGlnaWNlcnQuY29tMFwGCCsGAQUFBzAChlBo
'' SIG '' dHRwOi8vY2FjZXJ0cy5kaWdpY2VydC5jb20vRGlnaUNl
'' SIG '' cnRUcnVzdGVkRzRDb2RlU2lnbmluZ1JTQTQwOTZTSEEz
'' SIG '' ODQyMDIxQ0ExLmNydDAMBgNVHRMBAf8EAjAAMA0GCSqG
'' SIG '' SIb3DQEBCwUAA4ICAQDUJbX3F23a0jvvclOLvzKxv6R0
'' SIG '' sDht0V7hu0NdWKpq2plh5Fy64J7AYH+UAqYJdiXa/awq
'' SIG '' a3O7Mqir9xVC+4k7IhCSp9+yiWYUBpP9avC7DH4da0SP
'' SIG '' 9A4eNRIchI/EYc8HdGtVSzLPSbKjO7nYLmhlxnXP64Bw
'' SIG '' onffTKXDmAfOS0nIgiRPUefsxdi2VPE75QY9skcCxnJp
'' SIG '' EumPdGwd5Phvx+HDIX+I90wZC39pZkhaPLxwVTPxpNc/
'' SIG '' X4LRLe31wH82dwTuGgZ9Quy3pGJq2dCGkcXkQzDB1LDh
'' SIG '' GvVgctk1E5cG7aCLghsJ6rqnmdame7ctX3rOXMj73IsU
'' SIG '' C3tcmHVufD7T3NoKPKSjIP25b8E90TZk92p5pthB795y
'' SIG '' CV3eOjoia0aBQI9kXkUH1grFRHGrYxxAaymk0wOJ4SDR
'' SIG '' BkGnt/GDj/TIUx8ymREUjz/hnL7B9GDKwsMrknPUXdVx
'' SIG '' hcJ6RQeW7cZ0lwvs8bPEoBJPEyoPoMi+/goRuNE/TT9+
'' SIG '' qDT9XG6ECIfcuRwjy6OdEdOcO7JzOLIFRLz+xAXVg5Ov
'' SIG '' cQiz621KcjF3NL2QeZC/U21YcncJLSmgZMIBBAw8WU7a
'' SIG '' CdCOnP+HEUyqt3MoLvmGUN3vN+LR9UzuBePqYkjem0SY
'' SIG '' zfjWVBeuBBzvSaulWpsGMIQkeSu/3/atL6+VkfoveTGC
'' SIG '' F9YwghfSAgEBMH0waTELMAkGA1UEBhMCVVMxFzAVBgNV
'' SIG '' BAoTDkRpZ2lDZXJ0LCBJbmMuMUEwPwYDVQQDEzhEaWdp
'' SIG '' Q2VydCBUcnVzdGVkIEc0IENvZGUgU2lnbmluZyBSU0E0
'' SIG '' MDk2IFNIQTM4NCAyMDIxIENBMQIQC2vPUnYL/EP1UsyY
'' SIG '' oLxEEDANBglghkgBZQMEAgEFAKB8MBAGCisGAQQBgjcC
'' SIG '' AQwxAjAAMBkGCSqGSIb3DQEJAzEMBgorBgEEAYI3AgEE
'' SIG '' MBwGCisGAQQBgjcCAQsxDjAMBgorBgEEAYI3AgEVMC8G
'' SIG '' CSqGSIb3DQEJBDEiBCAqslooydnJbKUVALQN2Vi+DKTr
'' SIG '' lUrs27pnXjugcQDvOjANBgkqhkiG9w0BAQEFAASCAYBX
'' SIG '' 5H2/Ui3IIhSOYjx8c9mxAa7G2PtKhJ5FiKhpctf97qF0
'' SIG '' JA3+y9pogQs0m3JUTGD8bquucMDmw8fkFr635Ym4Tc+d
'' SIG '' 8qzmc8DmWOQMyIsWyy/jOBbiD+ws+F7C4qOmlGhMabhA
'' SIG '' cwGYcP7AItTcf1ny4Y9iRGmRNMnx3HTc+foSmSIvx9KF
'' SIG '' +PAhY9OGmBdFhHBuAhuyDyNFJQ1N5pfm64mXhiyzjtjc
'' SIG '' Iquk33CnpzhFu8VKy+wfrEL3q25xaBtXPD3BT60+tDn/
'' SIG '' AQDqEeU8zBKp0W46mF4PJdNxQ85Kv4yN/w9wQa4j2dcB
'' SIG '' OLKqr8+ueWaFdZ1v3H5MTHkWaZEZrjAQqx/8R9CBT/nX
'' SIG '' lqVRB0LoYJ4Imatxx8HQe31VYovcbLDGjedEPzzD5d9p
'' SIG '' DNXFgIbwatjkSxJ/pMtkZ/sWXNe4w/1d3lRh3z1Euhug
'' SIG '' AHIfgFAsUJ2l2KST5rg41uWVgNjD53ptVGOprCb5bmKI
'' SIG '' lA/42Vst0qKIJvD+cScVNzOaZLyhghUsMIIVKAYKKwYB
'' SIG '' BAGCNwMDATGCFRgwghUUBgkqhkiG9w0BBwKgghUFMIIV
'' SIG '' AQIBAzENMAsGCWCGSAFlAwQCATCB9AYLKoZIhvcNAQkQ
'' SIG '' AQSggeQEgeEwgd4CAQEGCmCGSAGG+mwKAwUwMTANBglg
'' SIG '' hkgBZQMEAgEFAAQgvmzWgG6GWPtohUdnDEZijNQW6E31
'' SIG '' KIWQQgi1FMhPfr4CCQCNxaWKHqGB/BgPMjAyNDA1MDEx
'' SIG '' MzE2MTVaMAMCAQGgeaR3MHUxCzAJBgNVBAYTAkNBMRAw
'' SIG '' DgYDVQQIEwdPbnRhcmlvMQ8wDQYDVQQHEwZPdHRhd2Ex
'' SIG '' FjAUBgNVBAoTDUVudHJ1c3QsIEluYy4xKzApBgNVBAMT
'' SIG '' IkVudHJ1c3QgVGltZXN0YW1wIEF1dGhvcml0eSAtIFRT
'' SIG '' QTGggg9YMIIEKjCCAxKgAwIBAgIEOGPe+DANBgkqhkiG
'' SIG '' 9w0BAQUFADCBtDEUMBIGA1UEChMLRW50cnVzdC5uZXQx
'' SIG '' QDA+BgNVBAsUN3d3dy5lbnRydXN0Lm5ldC9DUFNfMjA0
'' SIG '' OCBpbmNvcnAuIGJ5IHJlZi4gKGxpbWl0cyBsaWFiLikx
'' SIG '' JTAjBgNVBAsTHChjKSAxOTk5IEVudHJ1c3QubmV0IExp
'' SIG '' bWl0ZWQxMzAxBgNVBAMTKkVudHJ1c3QubmV0IENlcnRp
'' SIG '' ZmljYXRpb24gQXV0aG9yaXR5ICgyMDQ4KTAeFw05OTEy
'' SIG '' MjQxNzUwNTFaFw0yOTA3MjQxNDE1MTJaMIG0MRQwEgYD
'' SIG '' VQQKEwtFbnRydXN0Lm5ldDFAMD4GA1UECxQ3d3d3LmVu
'' SIG '' dHJ1c3QubmV0L0NQU18yMDQ4IGluY29ycC4gYnkgcmVm
'' SIG '' LiAobGltaXRzIGxpYWIuKTElMCMGA1UECxMcKGMpIDE5
'' SIG '' OTkgRW50cnVzdC5uZXQgTGltaXRlZDEzMDEGA1UEAxMq
'' SIG '' RW50cnVzdC5uZXQgQ2VydGlmaWNhdGlvbiBBdXRob3Jp
'' SIG '' dHkgKDIwNDgpMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A
'' SIG '' MIIBCgKCAQEArU1LqRKGsuqjIAcVFmQqK0vRvwtKTY7t
'' SIG '' gHalZ7d4QMBzQshowNtTK91euHaYNZOLGp18EzoOH1u3
'' SIG '' Hs/lJBQesYGpjX24zGtLA/ECDNyrpUAkAH90lKGdCCmz
'' SIG '' iAv1h3edVc3kw37XamSrhRSGlVuXMlBvPci6Zgzj/L24
'' SIG '' ScF2iUkZ/cCovYmjZy/Gn7xxGWC4LeksyZB2ZnuU4q94
'' SIG '' 1mVTXTzWnLLPKQP5L6RQstRIzgUyVYr9smRMDuSYB3Xb
'' SIG '' f9+5CFVghTAp+XtIpGmG4zU/HoZdenoVve8AjhUiVBcA
'' SIG '' kCaTvA5JaJG/+EfTnZVCwQ5N328mz8MYIWJmQ3DW1cAH
'' SIG '' 4QIDAQABo0IwQDAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0T
'' SIG '' AQH/BAUwAwEB/zAdBgNVHQ4EFgQUVeSB0RGAvtiJuQij
'' SIG '' MfmhJAkWuXAwDQYJKoZIhvcNAQEFBQADggEBADubj1ab
'' SIG '' MOdTmXx6eadNl9cZlZD7Bh/KM3xGY4+WZiT6QBshJ8rm
'' SIG '' cnPyT/4xmf3IDExoU8aAghOY+rat2l098c5u9hURlIIM
'' SIG '' 7j+VrxGrD9cv3h8Dj1csHsm7mhpElesYT6YfzX1XEC+b
'' SIG '' BAlahLVu2B064dae0Wx5XnkcFMXj0EyTO2U87d89vqbl
'' SIG '' lRrDtRnDvV5bu/8j72gZyxKTJ1wDLW8w0B62GqzeWvfR
'' SIG '' qqgnpv55gcR5mTNXuhKwqeBCbJPKVt7+bYQLCIt+jerX
'' SIG '' mCHG8+c8eS9enNFMFY3h7CI3zJpDC5fcgJCNs2ebb0gI
'' SIG '' FVbPv/ErfF6adulZkMV8gzURZVEwggUTMIID+6ADAgEC
'' SIG '' AgxY2hP/AAAAAFHODfcwDQYJKoZIhvcNAQELBQAwgbQx
'' SIG '' FDASBgNVBAoTC0VudHJ1c3QubmV0MUAwPgYDVQQLFDd3
'' SIG '' d3cuZW50cnVzdC5uZXQvQ1BTXzIwNDggaW5jb3JwLiBi
'' SIG '' eSByZWYuIChsaW1pdHMgbGlhYi4pMSUwIwYDVQQLExwo
'' SIG '' YykgMTk5OSBFbnRydXN0Lm5ldCBMaW1pdGVkMTMwMQYD
'' SIG '' VQQDEypFbnRydXN0Lm5ldCBDZXJ0aWZpY2F0aW9uIEF1
'' SIG '' dGhvcml0eSAoMjA0OCkwHhcNMTUwNzIyMTkwMjU0WhcN
'' SIG '' MjkwNjIyMTkzMjU0WjCBsjELMAkGA1UEBhMCVVMxFjAU
'' SIG '' BgNVBAoTDUVudHJ1c3QsIEluYy4xKDAmBgNVBAsTH1Nl
'' SIG '' ZSB3d3cuZW50cnVzdC5uZXQvbGVnYWwtdGVybXMxOTA3
'' SIG '' BgNVBAsTMChjKSAyMDE1IEVudHJ1c3QsIEluYy4gLSBm
'' SIG '' b3IgYXV0aG9yaXplZCB1c2Ugb25seTEmMCQGA1UEAxMd
'' SIG '' RW50cnVzdCBUaW1lc3RhbXBpbmcgQ0EgLSBUUzEwggEi
'' SIG '' MA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDZI+YU
'' SIG '' pOh8S4VxWPv4geZyi11Gw4gAHzjQiuHWblYw5a/aZFB9
'' SIG '' whM5+71mtNqE+4PQKB/LduhgUGmb885PE+LBPsHfEssy
'' SIG '' o/heRCIOzDrpjUm5YHTI3lQ9QV5DXyhGqaa3yhArIrxb
'' SIG '' TVuMF2UShv0sd9XFoIzKwoPgR1d853CuYkUnMRgK1MCk
'' SIG '' GFVS92DGBEuz3WgybhAfNBG4Enhk8e6p4PfjsSKPNFpl
'' SIG '' y4r04UVQdN+Tl6Y05tBMO583SVKnU06fLmdc7Zb8pb90
'' SIG '' UYjjqo692bEvX1AwFvRRYCJrmcv/4VQ7uftEOKUIOSOb
'' SIG '' aUf6PMTQ56rfRrLs8ooZrCmyOJV1AgMBAAGjggEjMIIB
'' SIG '' HzASBgNVHRMBAf8ECDAGAQH/AgEAMA4GA1UdDwEB/wQE
'' SIG '' AwIBBjA7BgNVHSAENDAyMDAGBFUdIAAwKDAmBggrBgEF
'' SIG '' BQcCARYaaHR0cDovL3d3dy5lbnRydXN0Lm5ldC9ycGEw
'' SIG '' MwYIKwYBBQUHAQEEJzAlMCMGCCsGAQUFBzABhhdodHRw
'' SIG '' Oi8vb2NzcC5lbnRydXN0Lm5ldDAyBgNVHR8EKzApMCeg
'' SIG '' JaAjhiFodHRwOi8vY3JsLmVudHJ1c3QubmV0LzIwNDhj
'' SIG '' YS5jcmwwEwYDVR0lBAwwCgYIKwYBBQUHAwgwHQYDVR0O
'' SIG '' BBYEFMPCcdJ712gFrjs5mzQlDGIDx1doMB8GA1UdIwQY
'' SIG '' MBaAFFXkgdERgL7YibkIozH5oSQJFrlwMA0GCSqGSIb3
'' SIG '' DQEBCwUAA4IBAQAdJOeadFuqcPyxDjFF1ywAf2Y6K6Ca
'' SIG '' NKqsY22J+Z/fDXf9JCP8T5y3b4/z9B+2wf3WHMSMiGbB
'' SIG '' Y426V3fTuBoeyFGtzGA2GodqKOoRZd7MPCyMdLfoUEPT
'' SIG '' zCjoFWwRKp8UlSnJBVe1ZzboPKmD70HBIRbTfvctEUdm
'' SIG '' dmCCEmmMdlVzD98vS13pbCP4B/a1fdZpRZxYfWEu/HhL
'' SIG '' Q06JkUZELKBTqEWh9hZYu5ET8kvF3wvA564per1Fs+dw
'' SIG '' MOc0jut69tO10d5rE5lGs4vSTZN1tfFvv9wAKMIlv7zn
'' SIG '' o2U07D8NHZeM+qqIIqQYNdsFjnbjEMgpj2PQrqwY2drE
'' SIG '' n1ESMIIGDzCCBPegAwIBAgIQB9cTU9olYbRh6ZBHikzO
'' SIG '' BDANBgkqhkiG9w0BAQsFADCBsjELMAkGA1UEBhMCVVMx
'' SIG '' FjAUBgNVBAoTDUVudHJ1c3QsIEluYy4xKDAmBgNVBAsT
'' SIG '' H1NlZSB3d3cuZW50cnVzdC5uZXQvbGVnYWwtdGVybXMx
'' SIG '' OTA3BgNVBAsTMChjKSAyMDE1IEVudHJ1c3QsIEluYy4g
'' SIG '' LSBmb3IgYXV0aG9yaXplZCB1c2Ugb25seTEmMCQGA1UE
'' SIG '' AxMdRW50cnVzdCBUaW1lc3RhbXBpbmcgQ0EgLSBUUzEw
'' SIG '' HhcNMjQwMTE5MTY0NjI4WhcNMjkwNjAxMDAwMDAwWjB1
'' SIG '' MQswCQYDVQQGEwJDQTEQMA4GA1UECBMHT250YXJpbzEP
'' SIG '' MA0GA1UEBxMGT3R0YXdhMRYwFAYDVQQKEw1FbnRydXN0
'' SIG '' LCBJbmMuMSswKQYDVQQDEyJFbnRydXN0IFRpbWVzdGFt
'' SIG '' cCBBdXRob3JpdHkgLSBUU0ExMIICIjANBgkqhkiG9w0B
'' SIG '' AQEFAAOCAg8AMIICCgKCAgEAx5I4QTn/oD9fTU2KlzHj
'' SIG '' m4fDeAVpNgtSs6qDXbDSvX6+g6BfXp6X89s1F6n52xVi
'' SIG '' fMr2xck0FeIRpZKxLuBpVF0OK75VxgGMhWOySS01X+VO
'' SIG '' Q8RxC6S0HjRN/0XI/k/hMOjpZWxrZdO+1Cxo0K0Em2q5
'' SIG '' 0FT7NQCQMcbYaGpdr+p+0PmdE+/OnWNkQnIHhfsGMYvj
'' SIG '' nQum1TLbUqVODDzBwJrRfwJ3YxPN8z08HgJLNobgBLR4
'' SIG '' d+SbL+GJKt6CXevkGtyNunukn4+ObHXrA+CABL+xCRz6
'' SIG '' YXqzm4G3C8kTCnjtCPbMpl9CRxI6R3h2/rzamT9k6zde
'' SIG '' Kt9S4pmw/e+EypE6orCnsbZWHD9E+H6R73imJP7eKR74
'' SIG '' 9fdRf7Z4LYe0vQC5xh7g6OET7u5f117upHx1YM6hNZBY
'' SIG '' wqu1SEN76cd3iYmLxqGMaZfPbnpD/vRf+2PlJOrf4BCQ
'' SIG '' pxKQzButCIrRjYUgom6hixYnlTHTz24DKZ9EwicIrLf0
'' SIG '' iU035CWJWlMsUw2CFHPG7MWw2YfYmxLuJjpfly9wyTB4
'' SIG '' oVpKbdJISg9Van72W+KHX9oRG3e+Gl73SAqYcQx9riqB
'' SIG '' fbKekWAO0dlqMBKK5JrspktvhQZJEA6FSD8u5hTPWuNP
'' SIG '' OCqv1zEAvCyWlZKtc896HFHL/i3pwC5YDgoVZcuIezIb
'' SIG '' YA0CAwEAAaOCAVswggFXMAwGA1UdEwEB/wQCMAAwHQYD
'' SIG '' VR0OBBYEFENoH2+fItD4Xwn3/LjlI8aOB0KSMB8GA1Ud
'' SIG '' IwQYMBaAFMPCcdJ712gFrjs5mzQlDGIDx1doMGgGCCsG
'' SIG '' AQUFBwEBBFwwWjAjBggrBgEFBQcwAYYXaHR0cDovL29j
'' SIG '' c3AuZW50cnVzdC5uZXQwMwYIKwYBBQUHMAKGJ2h0dHA6
'' SIG '' Ly9haWEuZW50cnVzdC5uZXQvdHMxLWNoYWluMjU2LmNl
'' SIG '' cjAxBgNVHR8EKjAoMCagJKAihiBodHRwOi8vY3JsLmVu
'' SIG '' dHJ1c3QubmV0L3RzMWNhLmNybDAOBgNVHQ8BAf8EBAMC
'' SIG '' B4AwFgYDVR0lAQH/BAwwCgYIKwYBBQUHAwgwQgYDVR0g
'' SIG '' BDswOTA3BgpghkgBhvpsCgEHMCkwJwYIKwYBBQUHAgEW
'' SIG '' G2h0dHBzOi8vd3d3LmVudHJ1c3QubmV0L3JwYTANBgkq
'' SIG '' hkiG9w0BAQsFAAOCAQEAvrDc/bz6Zqf8Ix3z2Vdi9CTf
'' SIG '' HS/5WMvKzAx9z26H9W6CWive41/GzhrkCK+OBAEe/wL4
'' SIG '' BVO4qGKFe5mrRXvZqrEXg9EpfpMh6DaIQiE4+/sNgcnD
'' SIG '' iozKKl5mr/mc9I18Evt6bTqKsAD3O3ClD7u1U6nhxikm
'' SIG '' 6twSSi9dWgS4quOHC33Ingb+aWZLjqf0vjDJpeKQoaiB
'' SIG '' DT5HIZJQXTLk8lbPqZQhuzDCdxgRmiau8eI+L/w/iTM3
'' SIG '' XZTn3RrF5cxmbPoAzpbigO34LKfFaBNpfARErQjV+avJ
'' SIG '' rRdm1S8LV/Cbz1weqw0nRmn+qLcFJY7gshUzSl+6nIvQ
'' SIG '' KAk8tYWy4TGCBJgwggSUAgEBMIHHMIGyMQswCQYDVQQG
'' SIG '' EwJVUzEWMBQGA1UEChMNRW50cnVzdCwgSW5jLjEoMCYG
'' SIG '' A1UECxMfU2VlIHd3dy5lbnRydXN0Lm5ldC9sZWdhbC10
'' SIG '' ZXJtczE5MDcGA1UECxMwKGMpIDIwMTUgRW50cnVzdCwg
'' SIG '' SW5jLiAtIGZvciBhdXRob3JpemVkIHVzZSBvbmx5MSYw
'' SIG '' JAYDVQQDEx1FbnRydXN0IFRpbWVzdGFtcGluZyBDQSAt
'' SIG '' IFRTMQIQB9cTU9olYbRh6ZBHikzOBDALBglghkgBZQME
'' SIG '' AgGgggGlMBoGCSqGSIb3DQEJAzENBgsqhkiG9w0BCRAB
'' SIG '' BDAcBgkqhkiG9w0BCQUxDxcNMjQwNTAxMTMxNjE1WjAp
'' SIG '' BgkqhkiG9w0BCTQxHDAaMAsGCWCGSAFlAwQCAaELBgkq
'' SIG '' hkiG9w0BAQswLwYJKoZIhvcNAQkEMSIEIIgedXgk9PCv
'' SIG '' nD+17Zc/R0p0D7rHLVvbd4W4mM1hQVIIMIIBCwYLKoZI
'' SIG '' hvcNAQkQAi8xgfswgfgwgfUwgfIEIChJ9zEY10FFBWFz
'' SIG '' zT7sy71TS14O8PoGFo2w4nNJA+6PMIHNMIG4pIG1MIGy
'' SIG '' MQswCQYDVQQGEwJVUzEWMBQGA1UEChMNRW50cnVzdCwg
'' SIG '' SW5jLjEoMCYGA1UECxMfU2VlIHd3dy5lbnRydXN0Lm5l
'' SIG '' dC9sZWdhbC10ZXJtczE5MDcGA1UECxMwKGMpIDIwMTUg
'' SIG '' RW50cnVzdCwgSW5jLiAtIGZvciBhdXRob3JpemVkIHVz
'' SIG '' ZSBvbmx5MSYwJAYDVQQDEx1FbnRydXN0IFRpbWVzdGFt
'' SIG '' cGluZyBDQSAtIFRTMQIQB9cTU9olYbRh6ZBHikzOBDAL
'' SIG '' BgkqhkiG9w0BAQsEggIAsQnnuYYFQAuAPwvq9Mi1GK1s
'' SIG '' ZcxB4qD+nGzzKAJM9sD0Zl2uvwIlCXSKbJlsjAcwRxA2
'' SIG '' y1RM5Anftq5XJklISfut8jm+a3fPuwX03F6oM1/NWXZb
'' SIG '' PBRMQV+qpTUi5QXt4eG0v9AqS1bw4BobR4F6xZaVLj5s
'' SIG '' TJmzLzEna1G93YXuM2ni+dNau/qnDKPeGjomERkcUbZn
'' SIG '' vjkg8r2xVlxju/XMGNHXGig0dnJqy5V1kelAwVEjfugm
'' SIG '' pyHDORpj0CkF4i+uuxQIfM/yGy0TjpjIHccTulfG/gnL
'' SIG '' KYZln9+Y+iqCySjTA22ZYQf1PMUh373aP39y7JQZ9/uP
'' SIG '' 18inUrsGaVukEchkzCOWqxO0+6yr+gvnGKiSUUlUzs8m
'' SIG '' 3NyasT3wsqmDTBNxSV8QcXFb8TL73T6cQU7pyNd0mU3k
'' SIG '' DUsWnRZAJXdXLltrMKX0/eRyqRcy34VAmN/DLMGAfIGK
'' SIG '' Ctwt8hqKUPnLpW6O4UZeX3XHFgPyhcF8q45ZY6Py7veN
'' SIG '' PK1cCtQKJ7kYGPkfLMZApCS0GAkRDoVBuCQVtxX2k7l3
'' SIG '' xLykQot4FfKXx/HqCWLi54775YOg3GjkkRtscdZgPO7n
'' SIG '' YSIwDNWDlQFGBZhsFDhxHXDdJqWadCWNqDSMwePA741+
'' SIG '' Jnli9diL4wFye4/w/KrLn8N2g2MbLQuZS0SA1BeQV10=
'' SIG '' End signature block
