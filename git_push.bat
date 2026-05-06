@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set LC_ALL=en_US.UTF-8
set LANG=en_US.UTF-8

echo ==============================================
echo          RPA项目 - 一键提交Gitee
echo ==============================================

set "PROJECT_PATH=D:\AI_Project\Python_Tauri_Vue"
set "REMOTE_URL=https://gitee.com/little-burger/skilled-hands---tik-tok-rpa.git"

cd /d "%PROJECT_PATH%"
if errorlevel 1 (
    echo 错误：找不到项目路径！
    pause
    exit /b
)

if not exist .git (
    echo 正在初始化Git仓库...
    git init -q
    git remote add origin %REMOTE_URL%
)

echo [1/4] 拉取最新代码...
git pull origin main --allow-unrelated-histories -q 2>nul

echo [2/4] 添加所有文件...
git add . -A

echo [3/4] 提交代码...
set /p "commit_msg=请输入提交说明："
git commit -m "%commit_msg%" -q

echo [4/4] 推送到Gitee...
git branch -M main
git push -u origin main

echo.
echo ✅ 推送成功完成！
echo 仓库地址：%REMOTE_URL%
echo.
pause