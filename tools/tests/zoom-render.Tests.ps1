Describe "zoom-render preview mode" {
  It "lists important subtitle cues without requiring ffmpeg" {
    $scriptPath = Join-Path $PSScriptRoot "..\zoom-render.ps1"
    $inputPath = Join-Path $PSScriptRoot "fixtures\sample.mp4"
    $subtitlePath = Join-Path $PSScriptRoot "fixtures\sample.srt"

    $output = & $scriptPath `
      -InputPath $inputPath `
      -SubtitlePath $subtitlePath `
      -PreviewOnly `
      -PreviewWidth 1920 `
      -PreviewHeight 1080 2>&1

    $LASTEXITCODE | Should Be 0
    ($output | Out-String) | Should Match "Preview mode"
    ($output | Out-String) | Should Match "Varikosel nedir\?"
    ($output | Out-String) | Should Match "Kime ameliyat, ne zaman, ne fayda\."
  }
}
