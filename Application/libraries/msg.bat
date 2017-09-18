@echo off
title Messenger

setlocal enabledelayedexpansion
set pcip=%3

MODE CON COLS=120 LINES=1
libraries\Cmdow\Cmdow\bin\Release\cmdow.exe "Messenger" /MOV 300 700

echo "[%time:~0,2%:%time:~3,2%:%time:~6,2%] %1 has joined.">>\\%pcip%\Proximity-Server\chat.log
echo "<nul set /p var=[%time:~0,2%:%time:~3,2%:%time:~6,2%] & libraries\out.exe %2 +%1+ & echo  has joined.">libraries\chat.log.bat
libraries\fnr.exe --cl --find "\"" --replace "" --dir "%cd%\libraries" --fileMask "chat.log.bat"
libraries\fnr.exe --cl --find "\"" --replace "" --dir "\\%pcip%\Proximity-Server" --fileMask "chat.log"
libraries\fnr.exe --cl --find "+" --replace "\"" --dir "%cd%\libraries" --fileMask "chat.log.bat"
type libraries\chat.log.bat>\\%pcip%\Proximity-Server\chat.log.bat

:log
set msg=
cls
set /p "msg=%1 > "

set mystring=%msg%
call :getsize %mystring%

if %count% GTR 113 cls & echo Message too long! & timeout 2 /nobreak > nul & goto log 


if "%msg%"==".help" (
echo "<nul set /p var=[%time:~0,2%:%time:~3,2%:%time:~6,2%] & libraries\out.exe %2 "%1" & echo  has left.">libraries\chat.log.bat
) ELSE (
if "%msg%"==".exit" (
echo [%time:~0,2%:%time:~3,2%:%time:~6,2%] %1 has left.>>\\%pcip%\Proximity-Server\chat.log
echo "<nul set /p var=[%time:~0,2%:%time:~3,2%:%time:~6,2%] & libraries\out.exe %2 "%1" & echo  has left.">libraries\chat.log.bat
libraries\fnr.exe --cl --find "%1" --replace "" --dir "\\%pcip%\Proximity-Server" --fileMask "UsersOnline.txt"
libraries\fnr.exe --cl --find "\"" --replace "" --dir "%cd%\libraries" --fileMask "chat.log.bat"
type libraries\chat.log.bat>\\%pcip%\Proximity-Server\chat.log.bat
timeout 1 /nobreak > nul
Taskkill /FI "WINDOWTITLE eq Chatroom"
del libraries\chat.log.bat
exit
) ELSE (
if "%msg%"=="" (
goto log
) ELSE (
echo [%time:~0,2%:%time:~3,2%:%time:~6,2%] %1^> %msg%>>\\%pcip%\Proximity-Server\chat.log
echo "<nul set /p var=[%time:~0,2%:%time:~3,2%:%time:~6,2%] & libraries\out.exe %2 "%1" & echo  ^> %msg%">libraries\chat.log.bat
libraries\fnr.exe --cl --find "\"" --replace "" --dir "%cd%\libraries" --fileMask "chat.log.bat"
libraries\fnr.exe --cl --find "?" --replace "^?" --dir "%cd%\libraries" --fileMask "chat.log.bat"
libraries\fnr.exe --cl --find "!" --replace "^!" --dir "%cd%\libraries" --fileMask "chat.log.bat"
type libraries\chat.log.bat>\\%pcip%\Proximity-Server\chat.log.bat
goto log
)
)
)


:: Get length of mystring line ######### subroutine getsize ########

:getsize

set count=0

for /l %%n in (0,1,2000) do (

    set chars=

    set chars=!mystring:~%%n!

    if defined chars set /a count+=1
)
goto :eof

:: ############## end of subroutine getsize ########################