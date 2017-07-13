@ECHO OFF
if "%1"=="" exit

setlocal enabledelayedexpansion
set pcip=%2

SET abet=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#-/\ .0123456789
SET cipher1=9876543210. \/-#@!zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA
REM. > libraries\Users.log
goto %1

:encrypt
(
 FOR /f "delims=" %%a IN (\\%pcip%\Proximity-Server\Users.txt) DO (
  SET line=%%a
  CALL :encipher
 )
)>libraries\Users.log
type libraries\Users.log>\\%pcip%\Proximity-Server\Users.txt
del libraries\Users.log
exit /b

:decrypt
(
 FOR /f "delims=" %%a IN (\\%pcip%\Proximity-Server\Users.txt) DO (
  SET line=%%a
  CALL :decipher
 )
)>libraries\Users.txt
exit /b

:decipher
SET morf=%abet%
SET from=%cipher1%
GOTO trans
:encipher
SET from=%abet%
SET morf=%cipher1%
:trans
SET "enil="
:transl
SET $1=%from%
SET $2=%morf%
:transc
IF "%line:~0,1%"=="%$1:~0,1%" SET enil=%enil%%$2:~0,1%&GOTO transnc
SET $1=%$1:~1%
SET $2=%$2:~1%
IF DEFINED $2 GOTO transc
:: No translation - keep
SET enil=%enil%%line:~0,1%
:transnc
SET line=%line:~1%
IF DEFINED line GOTO transl
ECHO %enil%
GOTO :eof