# One-time job: apply the approved metadata + schedule to the three Clomid EN Shorts once the YouTube API quota has reset.
# Approved by Dr. Aksoy on 2026-10-22 ("5-6-9 yap", "kota gelince yaz"). Content: youtube-api\clomid-en-shorts-fixes-2026-10-22.json
$ErrorActionPreference = 'Continue'
$env:PYTHONIOENCODING = 'utf-8'
$root = 'D:\A-klasör\Youtube'
$script = "$root\.claude\skills\yt-pipeline\scripts\yt_metadata.py"
$fixes = "$root\youtube-api\clomid-en-shorts-fixes-2026-10-22.json"
$log = "$root\youtube-api\clomid-en-shorts-apply-log.txt"
function Log($m) { Add-Content -Path $log -Value ("[{0}] {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $m) -Encoding UTF8 }
Log 'start'
$done = $false
for ($i = 1; $i -le 8 -and -not $done; $i++) {
    $out = & py -3.12 $script --channel en update --fixes $fixes --go 2>&1 | Out-String
    Log ("attempt $i`n" + $out.Trim())
    if ($out -notmatch 'API ERROR' -and $out -notmatch 'quotaExceeded' -and $out -notmatch 'Traceback') { $done = $true } else { Start-Sleep -Seconds 1800 }
}
if ($done) {
    foreach ($v in 'bdEFB26X4m4', 'uL01tbAJQ0E', 'gXl0y9h6kIE') {
        $o = "$root\youtube-api\verify-$v.json"
        & py -3.12 $script --channel en get --video $v --out $o 2>&1 | Out-Null
        if (Test-Path $o) {
            $d = Get-Content $o -Raw -Encoding UTF8 | ConvertFrom-Json
            Log ("verify $v | title: {0} | privacy: {1} | publishAt: {2} | desc length: {3} | tags: {4}" -f $d.snippet.title, $d.status.privacyStatus, $d.status.publishAt, $d.snippet.description.Length, $d.snippet.tags.Count)
        } else { Log "verify $v | could not read back" }
    }
    Log 'finished OK'
} else { Log 'gave up after 8 attempts (quota still exhausted?). Re-run this script manually.' }
Unregister-ScheduledTask -TaskName 'ClomidEnShortsMetadata' -Confirm:$false -ErrorAction SilentlyContinue
