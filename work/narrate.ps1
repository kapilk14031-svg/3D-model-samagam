Add-Type -AssemblyName System.Speech
$taskRoot = Split-Path -Parent $PSScriptRoot
$audioFolder = Join-Path $PSScriptRoot 'narration-audio'
New-Item -ItemType Directory -Force -Path $audioFolder | Out-Null
$segments = [IO.File]::ReadAllText((Join-Path $PSScriptRoot 'narration.json'),[Text.Encoding]::UTF8) | ConvertFrom-Json
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.SelectVoice('Microsoft Kalpana')
$speaker.Rate = 0
for ($i=0; $i -lt $segments.Count; $i++) {
    $speaker.SetOutputToWaveFile((Join-Path $audioFolder ($i.ToString()+'.wav')))
    $speaker.Speak($segments[$i].text)
    $speaker.SetOutputToNull()
}
$speaker.Dispose()
Write-Output 'Eight Hindi narration segments generated.'
