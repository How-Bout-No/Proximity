@echo off
setlocal enabledelayedexpansion

:: FLOAT values definition function version 1.0 in batch by KVC [karan Veer Chouhan]
:: Contact : karanveerchouhan@gmail.com
:: 
:: For more Batch Scripts visit : https://batchprogrammers.blogspot.com
:: 
:: This function can calculate float results only upto 6 places of digits (including nos after dot '.')
:: ...and shows error if tried to calculate more than 6 digits precision...
:: for help on using this Function...try 'float /?' in cmd console...
:: If you find any type of calculation mistake or any other error in this function...
:: please do notify me at my email_id (given above)... or if you modified this batch fn...
:: please send me that modified version too...i'll appreciate it... :)


rem Checking WHether this batch function is compatible with your system or not...
if /i "%os%" neq "windows_NT" (Echo. THis batch program is not compatible with the version of windows you have...&pause&goto end)

rem Setting_up version of this function
set ver=1.0

if /i "%~1" == "" (goto help)
if /i "%~1" == "/?" (goto help)
if /i "%~1" == "help" (goto help)
if /i "%~1" == "ver" (echo.Float fn ver.%ver% BY kvc&&goto end)

:: checking whether sufficient variables are defined or not...
if /i "%~2" == "" (goto help)
if /i "%~3" == "" (goto help)
::if /i "%~4" == "" (goto help)
if /i "%~5" neq "" (goto help)

:: checking the defined operation is valid or not...
set valid=False
if /i "%~2" == "+" (set valid=True)
if /i "%~2" == "-" (set valid=True)
if /i "%~2" == "*" (set valid=True)
if /i "%~2" == "/" (set valid=True)

if /i "%valid%" neq "True" (goto help)

:: dividing number 1 and 2 into parts as per the algorithm [by kvc] says...
call :Parts %~1 a.1 a.2
call :Parts %~3 b.1 b.2

:: removing unwanted ending zeros entered by user...
if /i "!a.2!" neq "0" (call :remove_ending_zeros "a.2")
if /i "!b.2!" neq "0" (call :remove_ending_zeros "b.2")

:: Checking string length of all values...(calculating digit count)...it is Modified (by kvc)
:: this string length trick is taken from "ADD" program of 'Brian Williams'...which
:: can add 64 bit integers in 32 bit environment...
FOR %%A IN (a b) DO (
	for /l %%C in (1,1,2) do (
      FOR /L %%B IN (0,1,9) DO (
         SET %%A.%%C=!%%A.%%C:%%B=%%B !
         )
		SET %%A.%%C.len=0
		FOR %%Z IN (!%%A.%%C!) DO SET /A %%A.%%C.len+=1
		SET %%A.%%C=!%%A.%%C: =!
      )
	)

:: Performing required operation...
if /i "%~2" == "+" (goto plus)
if /i "%~2" == "-" (goto minus)
if /i "%~2" == "/" (goto divide)
if /i "%~2" == "*" (goto multiply)
goto help


:plus
rem checking whether digits count after decimal are same or not...
set loop=0
set max_places=!a.2.len!
if /i !a.2.len! gtr !b.2.len! (set "max_places=!a.2.len!" && set "to_inc=b" && set /a loop=!a.2.len!-!b.2.len!)
if /i !b.2.len! gtr !a.2.len! (set "max_places=!b.2.len!" && set "to_inc=a" && set /a loop=!b.2.len!-!a.2.len!)

rem Making both decimal places same...(indirectly cal. L.C.M.)...
for /l %%a in (1,1,!loop!) do (
for %%x in (!to_inc!) do (
set "%%x.2=!%%x.2!0"
)
)

:: Removing Unwanted leading zeros as...in cmd ...the value starting from 0 is considered as hexa-decimal...
:: thus it may result in wrong output..'cuz we are doing calculation in decimal ...
call :remove_leading_zeros "a.1"
call :remove_leading_zeros "b.1"
if /i "!a.1!" == "0" (call :remove_leading_zeros "a.2" && set a.1=)
if /i "!b.1!" == "0" (call :remove_leading_zeros "b.2" && set b.1=)

rem Adding the float values now... As per Kvc's algorithm...
set /a result=!a.1!!a.2!+!b.1!!b.2!

rem handling small error...
if /i "!result:~0,1!" == "-" (
	set "sign=-"
	set "result=!result:~1!"
	)

:: checking the digit count of the result...
call :length result max_places result
	
for %%a in (!max_places!) do (
	set "result[1]=!result:~0,-%%a!"
	set "result[2]=!result:~-%%a!"
	)
if not defined result[1] (set result[1]=0)
if not defined result[2] (set result[2]=0)

echo.!sign!!result[1]!.!result[2]!
goto :end


:minus
rem checking whether digits count after decimal are same or not...
set loop=0
set max_places=!a.2.len!
if /i !a.2.len! gtr !b.2.len! (set "max_places=!a.2.len!" && set "to_inc=b" && set /a loop=!a.2.len!-!b.2.len!)
if /i !b.2.len! gtr !a.2.len! (set "max_places=!b.2.len!" && set "to_inc=a" && set /a loop=!b.2.len!-!a.2.len!)

rem Making both decimal places same...(indirectly calculating L.C.M.)...
for /l %%a in (1,1,!loop!) do (
for %%x in (!to_inc!) do (
set "%%x.2=!%%x.2!0"
)
)

:: Removing Unwanted leading zeros as...in cmd ...the value starting from 0 is considered as hexa-decimal...
:: thus it may result in wrong output..'cuz we are doing calculation in decimal ...
call :remove_leading_zeros "a.1"
call :remove_leading_zeros "b.1"
if /i "!a.1!" == "0" (call :remove_leading_zeros "a.2")
if /i "!b.1!" == "0" (call :remove_leading_zeros "b.2")

if /i "!a.1!" == "0" (set a.1=)
if /i "!b.1!" == "0" (set b.1=)

set /a result=!a.1!!a.2!-!b.1!!b.2!

rem handling small error...
if /i "!result:~0,1!" == "-" (
	set "sign=-"
	set "result=!result:~1!"
	)

:: checking the digit count of the result...
call :length result max_places result

for %%a in (!max_places!) do (
	set "result[1]=!result:~0,-%%a!"
	set "result[2]=!result:~-%%a!"
	)
if not defined result[1] (set result[1]=0)
if not defined result[2] (set result[2]=0)

echo.!sign!!result[1]!.!result[2]!
goto :end


:multiply
rem adding digits count after decimal 'cuz no need of checking here...
set /a max_places=!a.2.len!+!b.2.len!

:: Removing Unwanted leading zeros as...in cmd ...the value starting from 0 is considered as hexa-decimal...
:: thus it may result in wrong output..'cuz we are doing calculation in decimal ...
call :remove_leading_zeros "a.1"
call :remove_leading_zeros "b.1"
if /i "!a.1!" == "0" (call :remove_leading_zeros "a.2")
if /i "!b.1!" == "0" (call :remove_leading_zeros "b.2")

if /i "!a.1!" == "0" (set a.1=)
if /i "!b.1!" == "0" (set b.1=)

rem Multiplying the float values now... As per Kvc's algorithm...

set /a result=!a.1!!a.2!*!b.1!!b.2!

rem handling small error...
if /i "!result:~0,1!" == "-" (
	set "sign=-"
	set "result=!result:~1!"
	)

:: checking the digit count of the result...
call :length result max_places result

for %%a in (!max_places!) do (
	set "result[1]=!result:~0,-%%a!"
	set "result[2]=!result:~-%%a!"
	)
if not defined result[1] (set result[1]=0)
if not defined result[2] (set result[2]=0)

echo.!sign!!result[1]!.!result[2]!
goto :end


:divide
rem checking whether digits count after decimal are same or not...
set loop=0
set max_places=!a.2.len!
set multiple=1
if /i !a.2.len! gtr !b.2.len! (set "max_places=!a.2.len!" && set "to_inc=b" && set /a loop=!a.2.len!-!b.2.len!)
if /i !b.2.len! gtr !a.2.len! (set "max_places=!b.2.len!" && set "to_inc=a" && set /a loop=!b.2.len!-!a.2.len!)
if !max_places! lss 3 (set max_places=5)

rem Making both decimal places same...(indirectly cal. L.C.M.)...
for /l %%a in (1,1,!loop!) do (
for %%x in (!to_inc!) do (
set "%%x.2=!%%x.2!0"
)
)
for /l %%a in (1,1,!max_places!) do (set "multiple=!multiple!0")

:: Removing Unwanted leading zeros as...in cmd ...the value starting from 0 is considered as hexa-decimal...
:: thus it may result in wrong output..'cuz we are doing calculation in decimal ...
call :remove_leading_zeros "a.1"
call :remove_leading_zeros "b.1"
if /i "!a.1!" == "0" (call :remove_leading_zeros "a.2")
if /i "!b.1!" == "0" (call :remove_leading_zeros "b.2")

if /i "!a.1!" == "0" (set a.1=)
if /i "!b.1!" == "0" (set b.1=)

rem Adding the float values now... As per Kvc's algorithm...
set /a result=!a.1!!a.2!*!multiple!
set /a result=!result!/!b.1!!b.2!

rem handling small error...
if /i "!result:~0,1!" == "-" (
	set "sign=-"
	set "result=!result:~1!"
	)

:: checking the digit count of the result...
call :length result max_places result

for %%a in (!max_places!) do (
	set "result[1]=!result:~0,-%%a!"
	set "result[2]=!result:~-%%a!"
	)
if not defined result[1] (set result[1]=0)
if not defined result[2] (set result[2]=0)

echo.!sign!!result[1]!.!result[2]!
goto :end



:end
goto :eof


rem ====================================================================================================
:: This is a sub-function which divides the given number into two parts...
:: i.e. before decimal, and after decimal... :)
rem Here... [ %1 : the number to divide ]
rem 		[ %2 : The first part's value returning variable ]
rem 		[ %3 : The second part's value returning variable ]

:Parts [%1] [%2] [%3]
for /f "tokens=1,2 delims=. " %%a in ("%~1") do (set "%~2=%%a"&&set "%~3=%%b")
if not defined %~2 (set "%~2=0")
if not defined %~3 (set "%~3=0")
goto :eof

rem ====================================================================================================


:help
cls
echo.
echo.
echo. Hey, hello there...i'm kvc.
echo. This is float values definition in batch by algorithm created by kvc... v.1.0
echo. You can use this float function in cmd console or in any of your batch program.
echo.
echo. Syntax :
echo. Float ^<value_1^> [operation] ^<value_2^>
echo.
echo. operations can be : + =^> For adding both values
echo.                   : - =^> For subtracting both values
echo.                   : / =^> For Dividing both values
echo.                   : * =^> For Multiplying both values
echo.
echo. E.g. : Float 355 / 113		[for calculating original value of pi]
echo.	Float 3.134 + -4.332			[Random calculation]
echo.	Float 4.66 - 0.04			[Random calculation]
echo.	Float 0.02 * 0.02 			[Random calculation]
goto end


rem ====================================================================================================
:: Removing Unwanted leading zeros as...in cmd ...the value starting from 0 is considered as hexa-decimal...
:: thus it may result in wrong output..'cuz we are doing calculation in decimal ...
:remove_leading_zeros
if /i "!%~1:~0,1!" == "0" (
	set "%~1=!%~1:~1!"
	rem Using recursive technique here... calling itself
	call :remove_leading_zeros "%~1"
	)
goto :eof
rem ====================================================================================================

rem ====================================================================================================
:: Removing Unwanted ending zeros as...after '.' ending zeros don't have any meaning...
:: thus it may result in wrong output..
:remove_ending_zeros
if /i "!%~1:~-1!" == "0" (
	set "%~1=!%~1:~0,-1!"
	rem Using recursive technique here... calling itself
	call :remove_ending_zeros "%~1"
	)
goto :eof
rem ====================================================================================================


rem ====================================================================================================
:length
for %%A in (%~1) do (
    FOR /L %%B IN (0,1,9) DO (
       SET %%A=!%%A:%%B=%%B !
       )
		SET %%A.len=0
		FOR %%Z IN (!%%A!) DO SET /A %%A.len+=1
		SET %%A=!%%A: =!
      )
:result_len
if !%~1.len! lss !%~2! (
	set /a %~1.len+=1
	set "%~1=0!%~1!"
	goto result_len
	)
set %~3=!%~1!
goto :eof
rem ====================================================================================================

