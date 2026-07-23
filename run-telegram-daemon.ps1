# 텔레그램 채널 상시 실행 데몬
# 작업 스케줄러가 로그온 시 이 스크립트를 실행한다.
# claude 가 죽으면 자동으로 다시 띄우고, 무슨 일이 있었는지 로그에 남긴다.
#
# 수동 확인:  Get-Content "$env:USERPROFILE\.claude\telegram-daemon.log" -Tail 30 -Wait
# 수동 중지:  Stop-ScheduledTask -TaskName "ClaudeTelegramChannel"  (또는 창 닫기)

$ProjectDir = "C:\Users\SAMSUNG\Desktop\AI agent\claude"
$LogFile    = "$env:USERPROFILE\.claude\telegram-daemon.log"
$LockFile   = "$env:USERPROFILE\.claude\telegram-daemon.lock"
$EnvFile    = "$env:USERPROFILE\.claude\channels\telegram\.env"

$env:PATH = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.bun\bin;$env:PATH"

function Log($msg) {
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg
    Write-Host $line
    Add-Content -Path $LogFile -Value $line -Encoding utf8
}

# --- 중복 실행 방지 -----------------------------------------------------------
# 데몬이 두 개 돌면 텔레그램 폴링이 충돌해서 봇이 먹통이 된다.
if (Test-Path $LockFile) {
    $oldPid = Get-Content $LockFile -ErrorAction SilentlyContinue
    if ($oldPid -and (Get-Process -Id $oldPid -ErrorAction SilentlyContinue)) {
        Log "이미 데몬이 실행 중입니다 (PID $oldPid). 이번 실행은 종료합니다."
        exit 0
    }
    Log "오래된 lock 파일 발견 (PID $oldPid, 이미 종료됨) — 정리합니다."
}
Set-Content -Path $LockFile -Value $PID -Encoding ascii

# 창을 강제로 닫는 등 비정상 종료 시에도 lock 을 정리한다
Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action {
    Remove-Item "$env:USERPROFILE\.claude\telegram-daemon.lock" -ErrorAction SilentlyContinue
} | Out-Null

Log "===== 데몬 시작 (PID $PID) ====="

# --- 재시작 루프 --------------------------------------------------------------
$restartCount = 0
$windowStart  = Get-Date

while ($true) {

    # 폭주 방지: 10분 안에 5번 넘게 죽으면 뭔가 근본적으로 잘못된 것이다
    if ((Get-Date) - $windowStart -gt [TimeSpan]::FromMinutes(10)) {
        $restartCount = 0
        $windowStart  = Get-Date
    }
    if ($restartCount -ge 5) {
        Log "10분 내 재시작 5회 초과 — 무한 재시작을 막기 위해 중단합니다."
        Log "로그 위쪽의 오류를 확인하세요. 수동 실행: .\start-telegram.ps1"
        break
    }

    # --- 사전 점검 (start-telegram.ps1 과 동일한 방어) ---
    if (-not (Test-Path $EnvFile)) {
        Log "[중단] 토큰 파일 없음: $EnvFile"
        break
    }

    # .env 의 BOM 은 토큰 인식을 깨뜨린다
    $bytes = [System.IO.File]::ReadAllBytes($EnvFile)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        Log "[수정] .env 에서 BOM 제거"
        $text = [System.IO.File]::ReadAllText($EnvFile) -replace "^﻿", ""
        [System.IO.File]::WriteAllText($EnvFile, $text, (New-Object System.Text.UTF8Encoding($false)))
    }

    # 유령 bun 이 남아 폴링을 선점하면 봇이 응답하지 않는다
    $staleBun = Get-Process bun -ErrorAction SilentlyContinue
    if ($staleBun) {
        Log "[정리] 남아있는 bun 프로세스 $($staleBun.Count)개 종료"
        $staleBun | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 500
    }

    # --- 실행 ---
    Set-Location $ProjectDir
    Log "claude 세션 시작 (재시작 카운트 $restartCount)"

    try {
        & claude --channels plugin:telegram@claude-plugins-official --permission-mode acceptEdits
        $code = $LASTEXITCODE
    } catch {
        $code = -1
        Log "[예외] $($_.Exception.Message)"
    }

    Log "claude 세션 종료 (exit code $code)"

    # 정상 종료(/exit 등)면 데몬도 함께 끝낸다. 의도적으로 끈 것이므로.
    if ($code -eq 0) {
        Log "정상 종료로 판단 — 데몬을 종료합니다."
        break
    }

    $restartCount++
    Log "10초 후 재시작합니다..."
    Start-Sleep -Seconds 10
}

Log "===== 데몬 종료 ====="
Remove-Item $LockFile -ErrorAction SilentlyContinue
