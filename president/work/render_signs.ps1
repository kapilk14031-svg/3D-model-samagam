param([string]$RecordsPath='', [string]$OutputDirectory='')
Add-Type -AssemblyName System.Drawing
$taskRoot = Split-Path -Parent $PSScriptRoot
if (!$RecordsPath) { $RecordsPath = Join-Path $taskRoot 'work\signs.json' }
if (!$OutputDirectory) { $OutputDirectory = Join-Path $taskRoot 'outputs\sign-textures' }
$signRecords = Get-Content -LiteralPath $RecordsPath -Raw -Encoding utf8 | ConvertFrom-Json
$signDir = $OutputDirectory
[System.IO.Directory]::CreateDirectory($signDir) | Out-Null
foreach ($signRecord in $signRecords) {
  $width = 1536
  $height = [Math]::Max(128,[int]($width * $signRecord.size[1] / $signRecord.size[0]))
  $bitmap = [System.Drawing.Bitmap]::new($width,$height)
  $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
  $graphics.Clear([System.Drawing.ColorTranslator]::FromHtml($signRecord.bg))
  $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
  $brush = [System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml($signRecord.fg))
  $format = [System.Drawing.StringFormat]::new()
  $format.Alignment = [System.Drawing.StringAlignment]::Center
  $format.LineAlignment = [System.Drawing.StringAlignment]::Center
  $lineHeight = $height / $signRecord.lines.Count
  for ($lineIndex=0; $lineIndex -lt $signRecord.lines.Count; $lineIndex++) {
    $fontSize = [single]($lineHeight * .65)
    do {
      $font = [System.Drawing.Font]::new('Nirmala UI',$fontSize,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
      $measured = $graphics.MeasureString([string]$signRecord.lines[$lineIndex],$font)
      if ($measured.Width -le $width*.93) { break }
      $font.Dispose()
      $fontSize -= 2
    } while ($fontSize -gt 8)
    $rectangle = [System.Drawing.RectangleF]::new(20,[single]($lineIndex*$lineHeight),[single]($width-40),[single]$lineHeight)
    $graphics.DrawString([string]$signRecord.lines[$lineIndex],$font,$brush,$rectangle,$format)
    $font.Dispose()
  }
  $bitmap.Save((Join-Path $signDir ($signRecord.key+'.png')),[System.Drawing.Imaging.ImageFormat]::Png)
  $format.Dispose(); $brush.Dispose(); $graphics.Dispose(); $bitmap.Dispose()
}
