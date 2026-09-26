@echo off
setlocal
echo ===================================================
echo   OpenCodeReview (OCR) - Alibaba AI Code Review
echo ===================================================
echo.

if "%~1"=="" goto help
if /I "%~1"=="preview" goto delegate_preview
if /I "%~1"=="delegate" goto delegate_preview
if /I "%~1"=="rules" goto rules
if /I "%~1"=="scan" goto scan
if /I "%~1"=="viewer" goto viewer
if /I "%~1"=="review" goto review

:: Pass through any other command
ocr %*
goto end

:delegate_preview
echo Running OCR Delegation Preview (Deterministic file selection)...
ocr delegate preview
goto end

:rules
echo Checking rules for: %2
if "%~2"=="" (
    ocr rules check app.py
) else (
    ocr rules check %2
)
goto end

:scan
echo Scanning target: %2
if "%~2"=="" (
    ocr scan
) else (
    ocr scan --path %2
)
goto end

:viewer
echo Starting WebUI Session Viewer...
ocr viewer
goto end

:review
echo Running OCR diff review (requires configured LLM provider)...
ocr review %2 %3 %4 %5
goto end

:help
echo Usage:
echo   RUN_OPEN_CODE_REVIEW.bat delegate        - Preview reviewable files for agent delegation
echo   RUN_OPEN_CODE_REVIEW.bat rules [file]    - Check matching rules for a file
echo   RUN_OPEN_CODE_REVIEW.bat scan [path]     - Scan full files/directories without diff
echo   RUN_OPEN_CODE_REVIEW.bat viewer          - Launch local browser session viewer
echo   RUN_OPEN_CODE_REVIEW.bat review          - Run diff review with configured LLM
echo.
goto end

:end
endlocal
