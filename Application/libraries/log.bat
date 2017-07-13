@echo off
title Chatroom

setlocal enabledelayedexpansion
set pcip=%3

MODE CON COLS=120 LINES=30
libraries\Cmdow\bin\Release\cmdow.exe "Chatroom" /MOV 300 200

for /F "tokens=7 delims== " %%G in ('
    ping -4 -n 1 %pcip%^|findstr /i "TTL="') do if not %%G==TTL @set pingspeed=%%G

:log
ping 1.1.1.1 -n 1 -w 500>nul
for %%i in (\\%pcip%\Proximity-Server\chat.log.bat) do echo %%~ai|find "a">nul || goto :log
>nul find "left" \\%pcip%\Proximity-Server\chat.log.bat && (
call \\%pcip%\Proximity-Server\chat.log.bat
call libraries\soundplayer.bat "C:\Windows\Media\Windows Battery Low.wav" 0 > nul
attrib -a \\%pcip%\Proximity-Server\chat.log.bat
goto log
) || (
>nul find "joined" \\%pcip%\Proximity-Server\chat.log.bat && (
call \\%pcip%\Proximity-Server\chat.log.bat
call libraries\soundplayer.bat "C:\Windows\Media\Windows Battery Critical.wav" 0 > nul
attrib -a \\%pcip%\Proximity-Server\chat.log.bat
goto log
) || (
call \\%pcip%\Proximity-Server\chat.log.bat
call libraries\soundplayer.bat "C:\Windows\Media\Windows Pop-up Blocked.wav" 0 > nul
attrib -a \\%pcip%\Proximity-Server\chat.log.bat
goto log
)
)