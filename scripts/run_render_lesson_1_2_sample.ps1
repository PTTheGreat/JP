$ErrorActionPreference = 'Stop'

$photoshopCandidates = @(
  "D:\software\photoshop2024\Adobe Photoshop 2024\Photoshop.exe",
  "D:\software\photoshop2023\Adobe Photoshop 2023\Photoshop.exe"
)

$photoshopExe = $null
foreach ($candidate in $photoshopCandidates) {
  if (Test-Path -LiteralPath $candidate) {
    $photoshopExe = $candidate
    break
  }
}

if (-not $photoshopExe) {
  throw "Photoshop not found in known paths."
}

$projectRoot = Split-Path $PSScriptRoot -Parent
$jsxPath = Join-Path $projectRoot "photoshop\render_lesson_1_2_sample.jsx"

$existing = Get-Process | Where-Object { $_.ProcessName -like '*Photoshop*' }
if ($existing) {
  $existing | Stop-Process -Force
}

Start-Process -FilePath $photoshopExe -WindowStyle Hidden
Start-Sleep -Seconds 20

$app = New-Object -ComObject Photoshop.Application
$app.DisplayDialogs = 3
$app.DoJavaScriptFile($jsxPath)

Get-Process | Where-Object { $_.ProcessName -like '*Photoshop*' } | Stop-Process -Force
Write-Output "Lesson 1-2 sample render finished"
