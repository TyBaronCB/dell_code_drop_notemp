@echo off
call mlxfwmanager.exe %*
set ERRL=%ERRORLEVEL%
REM if all devices were updated successfully then call UpdRollBack.exe
IF %ERRL%==0 GOTO Label0
REM if at least one image was updated then call UpdRollBack.exe
IF %ERRL%==254 GOTO Label0
GOTO End


:Label0
call UpdRollBack.exe

:End
exit /b %ERRL%
