@echo off
chcp 65001
for /f "delims=" %%i in ('powershell -NoProfile -Command "Get-Date -Format \"提交时间：yyyy-MM-dd HH时mm分\""') do set CurrentDateTime=%%i
rem 当前日期时间是：%CurrentDateTime%

git add *
git commit -m "%CurrentDateTime%
git push origin master

timeout /t 5