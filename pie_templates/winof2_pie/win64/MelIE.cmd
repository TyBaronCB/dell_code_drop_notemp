@echo off
setlocal

if %1x == ix goto inventory

@echo Usage: MelIE.cmd command options
@echo Available parameters: 'i' for inventory
@echo Parameters available after 'i': 
@echo 'print' to direct output to standard out, 'file' to direct output to a file.
set errorlevel=1
goto end

:inventory
call %systemroot%\system32\cscript /nologo melinv.vbs %2 %3
goto end

:end
endlocal