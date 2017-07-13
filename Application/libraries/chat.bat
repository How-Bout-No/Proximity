@echo %1
if "%1"=="" exit

:intro
cd libraries\typo
call typo Pixcel.fo 36 7 22 Proximity
call typo Pixcel.fo 36 6 aa Proximity
batbox /g 36 19
timeout 3 /nobreak > nul
setlocal enabledelayedexpansion
set pcip=%6

set color=%2%3

cd..\..
:boot
echo Connecting to server...
timeout 1 /nobreak > nul
if not exist "\\%pcip%\Proximity-Server\" (
echo.
echo Connection failed^^! Please try again later...
echo.
pause
exit
)
cd libraries\typo
:updatecheck
echo.
batbox /g 36 19
cd..\..
echo Checking for updates...
echo.
"C:\Program Files\curl\curl.exe" -s http://textuploader.com/dkfvz/raw -o output.txt
>nul find "%5" output.txt && (
timeout 1 /nobreak > nul & goto start
) || (
echo A new version is available^^!
echo.
timeout 1 /nobreak > nul
echo You will not be able to connect online unless you update!
echo.
echo.
timeout 1 /nobreak > nul
libraries\cmdmenusel 0ff0 "Update Now" "Update Later"
if %errorlevel%==2 exit /b
)
goto update

:start
del output.txt
cls
echo Proximity ChatRoom v1.0.0
echo.
echo.
echo Please select an option:
libraries\cmdmenusel 0ff0 "1) Log In" "2) Sign Up" "3) Settings" "4) Quit"
if %errorlevel%==1 goto loginn
if %errorlevel%==2 goto signupp
if %errorlevel%==3 goto settings
if %errorlevel%==4 exit /b
goto :start

:loginn
copy \\%pcip%\Proximity-Server\Users.txt libraries\Users.txt > nul
call libraries\cipher.bat decrypt %pcip%

:login
setlocal EnableDelayedExpansion
set vidx=0
for /F "delims=; tokens=1,*" %%x in (libraries\Users.txt) do (
    SET /A vidx=!vidx! + 1
    set user!vidx!=%%x;%%y
)
cls
echo.
set /p user=Username: 
set vidx=0
for /F "delims=; tokens=1,2" %%a in (libraries\Users.txt) do (
    SET /A vidx=!vidx! + 1
    if %user%==%%a goto login1
)
cls
echo.
echo Incorrect Username
timeout 2 > nul
goto login

:login1
cls
echo.
echo Username: %user%
echo.
echo|set /p="Password: " & echo|libraries\mpass libraries\pass.lock
set /p password=<"libraries\pass.lock"
del libraries\pass.lock

for /F "delims=; tokens=1,2" %%a in (libraries\Users.txt) do (
    if %user%==%%a (
      if %password%==%%b (
        goto login2
      )
    )
)

:parse1
cls
echo.
echo Incorrect Password
timeout 2 > nul
goto login1

:login2
cls
echo Establishing connection to server...
echo.
if not exist \\%pcip%\Proximity-Server echo Failed! & pause & goto endit
echo Success!
timeout 2 /nobreak > nul
start "" libraries\log.bat %color% %user% %pcip%
start "" libraries\msg.bat %user% %color% %pcip%
:endit
del libraries\Users.txt
exit

:signupp
if exist \\%pcip%\Proximity-Server\Users.txt call libraries\cipher.bat decrypt
if not exist \\%pcip%\Proximity-Server\Users.txt type nul >\\%pcip%\Proximity-Server\Users.txt

:signup
setlocal EnableDelayedExpansion
cls
echo.
set /p user=Username: 
if "%user%"=="" cls & echo. & echo Invalid username! & timeout 2 > nul & goto signup
set vidx=0
for /F "delims=; tokens=1,*" %%a in (\\%pcip%\Proximity-Server\Users.txt) do (
    SET /A vidx=!vidx! + 1
    if %user%==%%a goto signup1
)
goto signup2

:signup1
cls
echo.
echo Username already taken!
timeout 2 > nul
goto signup

:signup2
cls
echo.
echo Username: %user%
echo.
set /p password=Password: 
if "%password%"=="" cls & echo. & echo Invalid password! & timeout 2 > nul & goto signup2
echo %user%;%password%>>\\%pcip%\Proximity-Server\Users.txt
del libraries\Users.txt
cls
echo.
echo Success^^!
timeout 3 > nul
goto start
echo %var1%
echo %var2%
pause & quit


:settings
if "%4"=="on" goto start
cls
libraries\cmdmenusel 0ff0 "1) Color" "2) Debug" "3) Quit"
if %errorlevel%==1 goto bgc
if %errorlevel%==2 goto debug
if %errorlevel%==3 goto start

:bgc
cls
color 07
for /L %%i in (1,1,5) do echo/
echo     0-Black   1-Blue  2-Green   3-Cyan   4-Red   5-Purple 6-Olive  7-White 
for /L %%i in (1,1,7) do echo/
echo     8-Gray    9-Blue  A-Green   B-Cyan   C-Red   D-Purple E-Yellow F-White 
echo                light    light    light   light     light            bright
for /L %%i in (1,1,3) do echo/

set "box1=4 3  11 7"
set "box2=4 11 11 15"
for /L %%l in (12,9,57) do (
   set /A r=%%l+9, lef=%%l+1, rig=r-1
   libraries\ColorBox %%l 2  !r! 8  194 194 193 193
   libraries\ColorBox %%l 10 !r! 16 194 194 193 193
   set "box1=!box1! !lef! 3  !rig! 7"
   set "box2=!box2! !lef! 11 !rig! 15"
)
libraries\ColorBox 3 2  12 8   218 194 193 192 & libraries\ColorBox 66 2  75 8   194 191 217 193
libraries\ColorBox 3 10 12 16  218 194 193 192 & libraries\ColorBox 66 10 75 16  194 191 217 193
set "box1=!box1! 67 3  74 7"
set "box2=!box2! 67 11 74 15"

set /P "=Select background color: " < NUL
set "color= 0123456789ABCDEF"
libraries\GetInput /I "%color:~1%"  /M %box1% %box2%  /H F0 1F 2F 3F 4F 5F 6F 70 8F 9F A0 B0 CF DF E0 F0
set bgc=!color:~%errorlevel%,1!

libraries\out.exe %bgc%%3 "Is this Ok? " 
echo.
echo.
libraries\cmdmenusel 0ff0 "Yes" "No"
if %errorlevel%==1 goto tc
if %errorlevel%==2 goto bgc

:tc
cls
color 07
for /L %%i in (1,1,5) do echo/
echo     0-Black   1-Blue  2-Green   3-Cyan   4-Red   5-Purple 6-Olive  7-White 
for /L %%i in (1,1,7) do echo/
echo     8-Gray    9-Blue  A-Green   B-Cyan   C-Red   D-Purple E-Yellow F-White 
echo                light    light    light   light     light            bright
for /L %%i in (1,1,3) do echo/

set "box1=4 3  11 7"
set "box2=4 11 11 15"
for /L %%l in (12,9,57) do (
   set /A r=%%l+9, lef=%%l+1, rig=r-1
   libraries\ColorBox %%l 2  !r! 8  194 194 193 193
   libraries\ColorBox %%l 10 !r! 16 194 194 193 193
   set "box1=!box1! !lef! 3  !rig! 7"
   set "box2=!box2! !lef! 11 !rig! 15"
)
libraries\ColorBox 3 2  12 8   218 194 193 192 & libraries\ColorBox 66 2  75 8   194 191 217 193
libraries\ColorBox 3 10 12 16  218 194 193 192 & libraries\ColorBox 66 10 75 16  194 191 217 193
set "box1=!box1! 67 3  74 7"
set "box2=!box2! 67 11 74 15"

set /P "=Select text color: " < NUL
set "color= 0123456789ABCDEF"
libraries\GetInput /I "%color:~1%"  /M %box1% %box2%  /H F0 1F 2F 3F 4F 5F 6F 70 8F 9F A0 B0 CF DF E0 F0
set tc=!color:~%errorlevel%,1!

libraries\out.exe %bgc%%tc% "Is this Ok? "  
echo.
echo.
libraries\cmdmenusel 0ff0 "Yes" "No"
if %errorlevel%==2 goto tc

set code=B
set code1=0
libraries\fnr.exe --cl --find "BGColor=%code%" --replace "BGColor=%bgc%" --dir "%cd%" --fileMask "Settings.cfg" > nul
libraries\fnr.exe --cl --find "TextColor=%code1%" --replace "TextColor=%tc%" --dir "%cd%" --fileMask "Settings.cfg" > nul

libraries\fnr.exe --cl --find "set code=%code%" --replace "set code=%bgc%" --dir "%cd%\libraries" --fileMask "chat.bat" > nul
libraries\fnr.exe --cl --find "set code1=%code1%" --replace "set code1=%tc%" --dir "%cd%\libraries" --fileMask "chat.bat" > nul
set color=%bgc%%tc%
goto settings

:debug
cls
echo.
echo Debug mode is currently off.
echo.
echo.Would you like to turn on debug mode? Note that you will have to manually change this in the Settings.cfg!
echo.
echo.
libraries\cmdmenusel 0ff0 "Yes" "No"
if %errorlevel%==1 goto debugon
goto settings

:debugon
cls
echo Restarting in debug mode...
timeout 2 /nobreak > nul
libraries\fnr.exe --cl --find "Debug=false" --replace "Debug=true" --dir "%cd%" --fileMask "Settings.cfg" > nul 2>nul
start "" Chat.cmd
exit

:update
cls
title Updating...
for %%a in ("%~dp0..\..") do set "curdir=%%~fa"
echo.
echo Downloading Update...
bitsadmin.exe /transfer "Update" https://www.dropbox.com/s/io09c0mbkiiznf5/CR_App.zip?dl=1 "C:\Temp\CR_App.zip" > nul 2>&1
start cmd.exe /c "@echo off & title Applying Update... & cls & echo. & echo Applying Update... & Taskkill /FI "WINDOWTITLE eq Updating..." & cd %curdir% & rd /s /q "%curdir%\Application" & call C:\Temp\zipjs.bat unzip -source "C:\Temp\CR_App.zip" -destination "%curdir%\Application" -keep no -force yes & cls & echo. & echo Complete! & pause & exit"