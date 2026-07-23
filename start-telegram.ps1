# 텔레그램 채널로 Claude Code 실행
# 사용법: 이 파일을 우클릭 → "PowerShell에서 실행"  또는  터미널에서  .\start-telegram.ps1

$ErrorActionPreference = "Stop"

# claude / bun 이 PATH에 없어도 동작하도록 보강
$env:PATH = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.bun\bin;$env:PATH"

Set-Location "C:\Users\SAMSUNG\Desktop\AI agent\claude"

# --- 사전 점검 ---------------------------------------------------------------
$envFile = "$env:USERPROFILE\.claude\channels\telegram\.env"

if (-not (Test-Path $envFile)) {
    Write-Host "[X] 토큰 파일이 없습니다: $envFile" -ForegroundColor Red
    exit 1
}

# .env 의 BOM 은 토큰 인식을 깨뜨린다 (전에 겪은 문제). 있으면 자동으로 제거.
$bytes = [System.IO.File]::ReadAllBytes($envFile)
if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
    Write-Host "[!] .env 에 BOM 발견 → 제거합니다" -ForegroundColor Yellow
    $text = [System.IO.File]::ReadAllText($envFile) -replace "^﻿", ""
    [System.IO.File]::WriteAllText($envFile, $text, (New-Object System.Text.UTF8Encoding($false)))
}

# 이전 세션의 유령 프로세스가 텔레그램 폴링을 선점하면 봇이 먹통이 된다
$staleBun = Get-Process bun -ErrorAction SilentlyContinue
if ($staleBun) {
    Write-Host "[!] 실행 중인 bun 프로세스 $($staleBun.Count)개 발견 — 중복 폴링을 막기 위해 종료합니다" -ForegroundColor Yellow
    $staleBun | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 500
}

Write-Host "[O] 사전 점검 통과. 텔레그램 채널로 Claude Code를 시작합니다." -ForegroundColor Green
Write-Host "    이 창을 닫으면 봇이 응답하지 않습니다." -ForegroundColor DarkGray
Write-Host ""

# --- 실행 --------------------------------------------------------------------
# acceptEdits: 파일 수정은 자동 승인, 그 외 셸 명령은 폰으로 승인 버튼이 온다
claude --channels plugin:telegram@claude-plugins-official --permission-mode acceptEdits
