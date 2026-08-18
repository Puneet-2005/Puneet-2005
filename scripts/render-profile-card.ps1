param(
    [string]$AvatarPath = "assets/profile-avatar.png",
    [string]$OutputPath = "assets/profile-card.png"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing

$width = 1200
$height = 500
$bitmap = [System.Drawing.Bitmap]::new($width, $height, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

function Color([string]$hex) { return [System.Drawing.ColorTranslator]::FromHtml($hex) }
function Font([float]$size, [System.Drawing.FontStyle]$style = [System.Drawing.FontStyle]::Regular) {
    return [System.Drawing.Font]::new("Consolas", $size, $style, [System.Drawing.GraphicsUnit]::Pixel)
}
function Text([string]$value, [float]$x, [float]$y, [float]$size, [string]$hex, [System.Drawing.FontStyle]$style = [System.Drawing.FontStyle]::Regular) {
    $font = Font $size $style
    $brush = [System.Drawing.SolidBrush]::new((Color $hex))
    $graphics.DrawString($value, $font, $brush, $x, $y)
    $brush.Dispose(); $font.Dispose()
}
function Panel([float]$x, [float]$y, [float]$w, [float]$h, [string]$stroke = "#20452d") {
    $fill = [System.Drawing.SolidBrush]::new((Color "#070b08"))
    $pen = [System.Drawing.Pen]::new((Color $stroke), 1)
    $graphics.FillRectangle($fill, $x, $y, $w, $h)
    $graphics.DrawRectangle($pen, $x, $y, $w, $h)
    $fill.Dispose(); $pen.Dispose()
}

try {
    $graphics.Clear((Color "#050805"))
    $gridPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(42, 18, 48, 31), 1)
    for ($x = 0; $x -le $width; $x += 24) { $graphics.DrawLine($gridPen, $x, 0, $x, $height) }
    for ($y = 0; $y -le $height; $y += 24) { $graphics.DrawLine($gridPen, 0, $y, $width, $y) }
    $gridPen.Dispose()

    $border = [System.Drawing.Pen]::new((Color "#1d3d29"), 1)
    $graphics.DrawRectangle($border, 1, 1, 1198, 498)
    $graphics.DrawLine($border, 30, 52, 1170, 52)
    $border.Dispose()

    Text "01 // SYSTEM PROFILE" 30 21 14 "#39ff14"
    $onlineBrush = [System.Drawing.SolidBrush]::new((Color "#39ff14"))
    $graphics.FillEllipse($onlineBrush, 1077, 31, 8, 8)
    $onlineBrush.Dispose()
    Text "ONLINE" 1096 22 12 "#39ff14"

    $surface = [System.Drawing.SolidBrush]::new((Color "#07100a"))
    $graphics.FillEllipse($surface, 60, 98, 296, 296)
    $surface.Dispose()
    foreach ($ring in @(@(60, 98, 296, "#173b27", 1), @(69, 107, 278, "#00f5ff", 1), @(75, 113, 266, "#39ff14", 2))) {
        $pen = [System.Drawing.Pen]::new((Color $ring[3]), [float]$ring[4])
        $graphics.DrawEllipse($pen, [float]$ring[0], [float]$ring[1], [float]$ring[2], [float]$ring[2])
        $pen.Dispose()
    }

    $avatar = [System.Drawing.Image]::FromFile((Resolve-Path $AvatarPath))
    $clip = [System.Drawing.Drawing2D.GraphicsPath]::new()
    $clip.AddEllipse(80, 118, 256, 256)
    $oldClip = $graphics.Clip
    $graphics.SetClip($clip)
    $graphics.DrawImage($avatar, [System.Drawing.Rectangle]::new(80, 118, 256, 256))
    $graphics.Clip = $oldClip
    $oldClip.Dispose(); $clip.Dispose(); $avatar.Dispose()

    $targetPen = [System.Drawing.Pen]::new((Color "#00f5ff"), 2)
    $graphics.DrawLine($targetPen, 65, 136, 65, 102); $graphics.DrawLine($targetPen, 65, 102, 99, 102)
    $graphics.DrawLine($targetPen, 317, 102, 351, 102); $graphics.DrawLine($targetPen, 351, 102, 351, 136)
    $graphics.DrawLine($targetPen, 65, 356, 65, 390); $graphics.DrawLine($targetPen, 65, 390, 99, 390)
    $graphics.DrawLine($targetPen, 317, 390, 351, 390); $graphics.DrawLine($targetPen, 351, 390, 351, 356)
    $targetPen.Dispose()
    Panel 108 399 200 28
    Text "GITHUB ID // 208438285" 124 407 10 "#6b7280"

    Text "PUNEET M P BHARADWAJ" 410 84 31 "#e6edf3" ([System.Drawing.FontStyle]::Bold)
    Text "@Puneet-2005" 410 123 16 "#39ff14"
    $line = [System.Drawing.Pen]::new((Color "#173b27"), 1)
    $graphics.DrawLine($line, 410, 162, 1152, 162)
    $line.Dispose()
    Text "SOFTWARE ENGINEER" 410 179 18 "#00f5ff"
    Text "AI // BACKEND // SYSTEMS // DEVELOPER TOOLS" 410 210 14 "#9aa4b2"

    Panel 410 253 232 82
    Text "LOCATION" 426 268 10 "#6b7280"
    Text "Bengaluru, India" 426 298 14 "#e6edf3"
    Panel 658 253 494 82
    Text "INTERESTS" 674 268 10 "#6b7280"
    Text "AI / Backend / Systems / Developer Tools" 674 298 14 "#e6edf3"
    Panel 410 351 742 72
    Text "LANGUAGES" 426 366 10 "#6b7280"
    Text "Python  /  C++  /  Java  /  TypeScript" 426 393 14 "#e6edf3"

    Panel 30 446 1140 34
    Text "STATUS" 46 456 10 "#6b7280"; Text "ONLINE" 112 456 12 "#39ff14"
    Text "MODE" 236 456 10 "#6b7280"; Text "ENGINEERING" 286 456 12 "#00f5ff"
    Text "MISSION" 440 456 10 "#6b7280"; Text "BUILD USEFUL SOFTWARE" 506 456 12 "#e6edf3"
    Text "BUILD. UNDERSTAND. IMPROVE." 932 456 12 "#39ff14"

    $resolvedOutput = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $OutputPath))
    $bitmap.Save($resolvedOutput, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output "Rendered $resolvedOutput"
}
finally {
    $graphics.Dispose()
    $bitmap.Dispose()
}
