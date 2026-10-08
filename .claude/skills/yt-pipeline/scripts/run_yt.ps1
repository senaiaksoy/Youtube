param(
  [Parameter(Mandatory = $true)]
  [string]$Script,

  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$Args
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$target = Join-Path $scriptDir $Script

if (-not (Test-Path -LiteralPath $target)) {
  throw "Script not found: $target"
}

& py -3.12 $target @Args
