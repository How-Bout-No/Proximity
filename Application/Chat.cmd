@echo off
title Chat
echo Initializing...

for /f "delims=" %%# in  ('"wmic path Win32_VideoController  get CurrentHorizontalResolution,CurrentVerticalResolution /format:value"') do (
  set "%%#">nul
)

call libraries\float.bat %CurrentHorizontalResolution% / 6.4 > a.txt
for /f "tokens=*" %%A in (a.txt) do (set "result=%%A")
set horires=%result%
call libraries\float.bat %CurrentVerticalResolution% / 5.4 > a.txt
for /f "tokens=*" %%A in (a.txt) do (set "result=%%A")
del /q "a.txt"
set vertires=%result%

libraries\Cmdow\bin\Release\cmdow.exe "Chat" /MOV %horires% %vertires%
setlocal ENABLEDELAYEDEXPANSION
set vidx=-1
for /F "delims== tokens=1,*" %%x in (Settings.cfg) do (
    SET /A vidx=!vidx! + 1
    set var!vidx!=%%y
)


FOR /F "tokens=2,3" %%A IN ('ping %computername% -n 1 -4') DO IF "from"== "%%A" set "IP=%%~B"
set pcip=%IP:~0,-1%

getmac /fo table /nh > libraries\mac.txt
set vidx=0
for /F "tokens=1,*" %%x in (libraries\mac.txt) do (
    SET /A vidx=!vidx! + 1
    set mac!vidx!=%%x
)

FOR /F "tokens=1,2" %%A IN ('arp -a') DO IF NOT "%pcip%"== "%%A" FOR /F "tokens=1,2" %%A IN ('arp -a') DO IF "%mac3%"== "%%B" set "pcip=%%A"

cls
if "%var3%"=="false" (
  call libraries\chat.bat off %var1% %var2% %var3% %var4% %pcip%
) ELSE (
  set num=1
  call libraries\chat.bat on > "logs\%DATE:~4,2%-%DATE:~7,2%-%DATE:~-4%_%num%.log"
  set /a num1=%num% + 1
  libraries\fnr.exe --cl --find "set num=%num%" --replace "set num=%num1%" --dir "%cd%" --fileMask "Chat.cmd" >nul 2>nul
)
exit