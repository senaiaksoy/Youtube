# zoom-render.ps1 - Reusable render script for smooth talking-head zooms.
# Default mode keeps the original periodic zoom. Provide -SubtitlePath to
# switch to subtitle-driven emphasis windows.
#
# Examples:
#   .\zoom-render.ps1 -InputPath "C:\path\video.mp4"
#   .\zoom-render.ps1 -InputPath "C:\path\video.mp4" -SubtitlePath "C:\path\video.srt"
#   .\zoom-render.ps1 -InputPath "C:\path\video.mp4" -SubtitlePath "C:\path\video.srt" -PreviewOnly

param(
  [Parameter(Mandatory = $true)][string]$InputPath,
  [string]$OutputPath = $null,
  [string]$SubtitlePath = $null,
  [double]$ZoomAmount = 0.10,
  [double]$PeriodSec = 30,
  [double]$FaceXRatio = 0.50,
  [double]$FaceYRatio = 0.29,
  [double]$LeadInSec = 0.10,
  [double]$TailOutSec = 0.20,
  [double]$MinGapSec = 0.35,
  [int]$MinCueScore = 4,
  [switch]$PreviewOnly,
  [int]$PreviewWidth = 1920,
  [int]$PreviewHeight = 1080
)

function Convert-SrtTimeToSeconds {
  param([string]$Value)

  $parts = $Value.Trim() -split '[:,]'
  if ($parts.Count -ne 4) {
    throw "Gecersiz SRT zaman damgasi: $Value"
  }

  return ([int]$parts[0] * 3600) + ([int]$parts[1] * 60) + [int]$parts[2] + ([int]$parts[3] / 1000.0)
}

function Format-Seconds {
  param([double]$Value)

  $ts = [TimeSpan]::FromSeconds([Math]::Max(0, $Value))
  return "{0:00}:{1:00}:{2:00}.{3:000}" -f $ts.Hours, $ts.Minutes, $ts.Seconds, $ts.Milliseconds
}

function Get-SrtCueScore {
  param([string]$Text)

  $score = 0
  $wordCount = ([regex]::Matches($Text, '\S+')).Count

  if ($Text -match '[?!]') { $score += 3 }
  if ($wordCount -le 4) { $score += 2 } elseif ($wordCount -le 8) { $score += 1 }
  $keywordHits = ([regex]::Matches($Text.ToLowerInvariant(), '\b(varikosel|nedir|neden|niye|ameliyat|fayda|kime|ne zaman|dikkat|onemli|kritik|senaryo|bonus|hata)\b')).Count
  if ($keywordHits -gt 0) { $score += [Math]::Min(3, $keywordHits) }
  if ($Text -match '^\s*[A-Z0-9][A-Z0-9\s,.-]*\s*$') { $score += 1 }

  return $score
}

function Get-SrtCues {
  param([string]$Path)

  $raw = [System.IO.File]::ReadAllText($Path)
  $normalized = $raw -replace "`r`n", "`n" -replace "`r", "`n"
  $blocks = $normalized -split "`n`n+"
  $items = @()

  foreach ($block in $blocks) {
    $lines = @($block -split "`n" | Where-Object { $_.Trim() -ne '' })
    if ($lines.Count -lt 2) { continue }

    $timeLineIndex = if ($lines[0] -match '-->') { 0 } else { 1 }
    if ($lines[$timeLineIndex] -notmatch '^\s*(.+?)\s*-->\s*(.+?)\s*$') { continue }

    $start = Convert-SrtTimeToSeconds $matches[1]
    $end = Convert-SrtTimeToSeconds $matches[2]
    $textStartIndex = $timeLineIndex + 1
    $text = (($lines[$textStartIndex..($lines.Count - 1)]) -join ' ').Trim()
    if (-not $text) { continue }

    $items += [pscustomobject]@{
      Start = $start
      End = $end
      Text = $text
      Score = Get-SrtCueScore $text
    }
  }

  return $items
}

function Merge-EmphasisWindows {
  param(
    [object[]]$Cues,
    [double]$LeadIn,
    [double]$TailOut,
    [double]$MinGap,
    [int]$MinScore
  )

  $selected = $Cues |
    Where-Object { $_.Score -ge $MinScore } |
    Sort-Object Start, End

  if (-not $selected) {
    return @()
  }

  $merged = New-Object System.Collections.Generic.List[object]

  foreach ($cue in $selected) {
    $start = [Math]::Max(0, $cue.Start - $LeadIn)
    $end = [Math]::Max($start + 0.2, $cue.End + $TailOut)

    if ($merged.Count -eq 0) {
      $merged.Add([pscustomobject]@{
        Start = $start
        End = $end
        Text = $cue.Text
        Score = $cue.Score
      })
      continue
    }

    $last = $merged[$merged.Count - 1]
    if ($start -le ($last.End + $MinGap)) {
      $last.End = [Math]::Max($last.End, $end)
      $last.Text = "{0} | {1}" -f $last.Text, $cue.Text
      $last.Score = [Math]::Max($last.Score, $cue.Score)
      continue
    }

    $merged.Add([pscustomobject]@{
      Start = $start
      End = $end
      Text = $cue.Text
      Score = $cue.Score
    })
  }

  return $merged
}

function Get-PeriodicZoomExpression {
  param(
    [double]$Amount,
    [double]$Period,
    [int]$Fps
  )

  $halfAmp = $Amount / 2
  $periodFrames = [Math]::Max(1, [int]([Math]::Round($Period * $Fps)))
  return "1+${halfAmp}*(1-cos(2*PI*on/${periodFrames}))"
}

function Get-SubtitleZoomExpression {
  param(
    [object[]]$Windows,
    [double]$Amount,
    [int]$Fps
  )

  if (-not $Windows -or $Windows.Count -eq 0) {
    return $null
  }

  $terms = foreach ($window in $Windows) {
    $startFrame = [Math]::Max(0, [int]([Math]::Floor($window.Start * $Fps)))
    $endFrame = [Math]::Max($startFrame + 1, [int]([Math]::Ceiling($window.End * $Fps)))
    $durationFrames = [Math]::Max(1, $endFrame - $startFrame)
    "${Amount}*if(between(on,${startFrame},${endFrame}),pow(sin(PI*(on-${startFrame})/${durationFrames}),2),0)"
  }

  return "1+(" + ($terms -join '+') + ")"
}

function Get-VideoFilter {
  param(
    [string]$ZoomExpression,
    [int]$Width,
    [int]$Height,
    [int]$CenterX,
    [int]$CenterY,
    [int]$Fps
  )

  $xExpr = "max(0,min(iw-iw/zoom,${CenterX}-iw/zoom/2))"
  $yExpr = "max(0,min(ih-ih/zoom,${CenterY}-ih/zoom/2))"
  return "zoompan=z='$ZoomExpression':d=1:x='$xExpr':y='$yExpr':s=${Width}x${Height}:fps=${Fps}"
}

$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

if (-not (Test-Path -LiteralPath $InputPath)) {
  Write-Error "Input bulunamadi: $InputPath"
  exit 1
}

if ($SubtitlePath -and -not (Test-Path -LiteralPath $SubtitlePath)) {
  Write-Error "SRT bulunamadi: $SubtitlePath"
  exit 1
}

$renderMode = if ($SubtitlePath) { "subtitle" } else { "periodic" }

if (-not $PreviewOnly -and -not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
  Write-Error "FFmpeg bulunamadi. Once 'winget install Gyan.FFmpeg' calistir."
  exit 1
}

if (-not $OutputPath) {
  $dir = Split-Path $InputPath -Parent
  $name = [System.IO.Path]::GetFileNameWithoutExtension($InputPath)
  $ext = [System.IO.Path]::GetExtension($InputPath)
  $suffix = if ($renderMode -eq "subtitle") { "_zoom_srt" } else { "_zoom" }
  $OutputPath = Join-Path $dir "${name}${suffix}${ext}"
}

if ($PreviewOnly) {
  $w = $PreviewWidth
  $h = $PreviewHeight
  $fps = 30
} else {
  if (-not (Get-Command ffprobe -ErrorAction SilentlyContinue)) {
    Write-Error "FFprobe bulunamadi. FFmpeg kurulumunu dogrula."
    exit 1
  }

  $dims = ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of default=noprint_wrappers=1 $InputPath
  $map = @{}
  foreach ($line in ($dims -split "`r?`n")) {
    if ($line -match '=') {
      $parts = $line -split '=', 2
      $map[$parts[0]] = $parts[1]
    }
  }
  $w = [int]$map['width']
  $h = [int]$map['height']
  $rateParts = $map['r_frame_rate'] -split '/'
  if ($rateParts.Count -eq 2 -and [double]$rateParts[1] -ne 0) {
    $fps = [int]([Math]::Round(([double]$rateParts[0]) / ([double]$rateParts[1])))
  } else {
    $fps = 30
  }
}

$cx = [int]($w * $FaceXRatio)
$cy = [int]($h * $FaceYRatio)

$windows = @()
$zoomExpression = $null

if ($renderMode -eq "subtitle") {
  $cues = Get-SrtCues -Path $SubtitlePath
  $windows = Merge-EmphasisWindows -Cues $cues -LeadIn $LeadInSec -TailOut $TailOutSec -MinGap $MinGapSec -MinScore $MinCueScore
  $zoomExpression = Get-SubtitleZoomExpression -Windows $windows -Amount $ZoomAmount -Fps $fps

  if (-not $zoomExpression) {
    Write-Warning "Onemli cue secilemedi, periyodik zoom fallback kullaniliyor."
    $renderMode = "periodic"
  }
}

if ($renderMode -eq "periodic") {
  $zoomExpression = Get-PeriodicZoomExpression -Amount $ZoomAmount -Period $PeriodSec -Fps $fps
}

$filter = Get-VideoFilter -ZoomExpression $zoomExpression -Width $w -Height $h -CenterX $cx -CenterY $cy -Fps $fps

Write-Output "Input:  $InputPath ($w x $h)"
Write-Output "Output: $OutputPath"
Write-Output "Mode:   $renderMode"
Write-Output "Zoom:   $($ZoomAmount * 100)%"
Write-Output "Face center: ($cx, $cy)"

if ($renderMode -eq "subtitle") {
  Write-Output "Selected emphasis windows:"
  foreach ($window in $windows) {
    Write-Output ("  [{0} -> {1}] {2}" -f (Format-Seconds $window.Start), (Format-Seconds $window.End), $window.Text)
  }
}

if ($PreviewOnly) {
  Write-Output "Preview mode - render baslatilmadi."
  Write-Output "Filter:"
  Write-Output $filter
  exit 0
}

Write-Output "Render basliyor..."

$sw = [System.Diagnostics.Stopwatch]::StartNew()

ffmpeg -hide_banner -y -i $InputPath `
  -vf $filter `
  -c:v h264_nvenc -preset p5 -tune hq -rc vbr -cq 22 -b:v 0 -maxrate 80M -bufsize 160M `
  -c:a aac -b:a 192k `
  $OutputPath

$sw.Stop()

if (Test-Path -LiteralPath $OutputPath) {
  $size = (Get-Item -LiteralPath $OutputPath).Length / 1MB
  Write-Output ("Bitti: {0:N0} MB, {1:N1} saniye" -f $size, $sw.Elapsed.TotalSeconds)
} else {
  Write-Error "Render basarisiz oldu."
  exit 1
}
