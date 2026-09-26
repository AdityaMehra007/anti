@echo off
setlocal enabledelayedexpansion
title COLIBRI - Massive MoE AI Inference Engine Cockpit

set "ROOT=%~dp0"
set "COLI_DIR=%ROOT%colibri\c"
set "PATH=%ROOT%colibri\tools\w64devkit\bin;%PATH%"

:menu
cls
echo ===============================================================================
echo            COLIBRI - FRONTIER MIXTURE-OF-EXPERTS DISK ENGINE
echo ===============================================================================
echo   Running 744B MoE Models on Consumer Hardware via Pure C Streaming
echo ===============================================================================
echo.
echo   [1] Show System Profile and Available Engines
echo   [2] Launch OpenAI-Compatible API Server and Web Dashboard (coli web)
echo   [3] Run System and Engine Diagnostics (coli doctor)
echo   [4] Run Disk Streaming Benchmark (iobench)
echo   [5] Download a Recommended MoE Model (OLMoE 1B-7B / Qwen 3.6 / GLM-5.2)
echo   [6] Plan Resource Requirements for a Model (coli plan)
echo   [7] Start Interactive Terminal Chat (coli chat)
echo   [8] Open Colibri Docs and Guides
echo   [Q] Quit
echo.
echo ===============================================================================
set /p choice="Enter option (1-8, Q): "

if /i "%choice%"=="1" goto profile
if /i "%choice%"=="2" goto web
if /i "%choice%"=="3" goto doctor
if /i "%choice%"=="4" goto bench
if /i "%choice%"=="5" goto download
if /i "%choice%"=="6" goto plan
if /i "%choice%"=="7" goto chat
if /i "%choice%"=="8" goto docs
if /i "%choice%"=="Q" goto end
goto menu

:profile
cls
python "%ROOT%colibri_controller.py" profile
pause
goto menu

:web
cls
echo -------------------------------------------------------------------------------
echo Launching Colibri Web Dashboard + OpenAI Server
echo -------------------------------------------------------------------------------
set /p model_path="Enter path to model directory (or press Enter for default/empty): "
if "%model_path%"=="" (
    python "%COLI_DIR%\coli" web --gpu none
) else (
    python "%COLI_DIR%\coli" web --model "%model_path%" --gpu none
)
pause
goto menu

:doctor
cls
set /p model_path="Enter path to model directory (or press Enter for base check): "
if "%model_path%"=="" (
    python "%COLI_DIR%\coli" doctor --gpu none
) else (
    python "%COLI_DIR%\coli" doctor --model "%model_path%" --gpu none
)
pause
goto menu

:bench
cls
python "%ROOT%colibri_controller.py" bench --size-mb 64
pause
goto menu

:download
cls
echo -------------------------------------------------------------------------------
echo Recommended Pre-Converted Models (Storage on Drive E: 394 GB Free):
echo   1. qwen36       - Qwen 3.6 35B-A3B int4 gs64 [23 GB] - Fast, highly capable
echo   2. glm53_flash  - GLM-5.3 Flash int4 gs64 [195 GB] - Fast frontier MoE
echo   3. glm52_i4     - GLM-5.2 int4 gs64 + MTP [372 GB] - 744B flagship MoE
echo -------------------------------------------------------------------------------
set /p dl_choice="Enter model name (qwen36 / glm53_flash / glm52_i4): "
if not "%dl_choice%"=="" (
    python "%ROOT%colibri_controller.py" download "%dl_choice%"
)
pause
goto menu

:plan
cls
set /p model_path="Enter path to model directory: "
if not "%model_path%"=="" (
    python "%COLI_DIR%\coli" plan --model "%model_path%"
)
pause
goto menu

:chat
cls
set /p model_path="Enter path to model directory: "
if not "%model_path%"=="" (
    python "%COLI_DIR%\coli" chat --model "%model_path%" --gpu none
) else (
    echo Model path is required for interactive chat.
)
pause
goto menu

:docs
cls
echo Opening docs/windows.md...
start "" "%ROOT%colibri\docs\windows.md"
goto menu

:end
exit /b 0
