# Robust local web server for Gyan Mansarovar 3D Viewer with /api/deployment backend support, master merge protection and terrain ground clearance
$port = 8080
$workspaceRoot = $PSScriptRoot
$outputsRoot = Join-Path $workspaceRoot "president\outputs"
if (-not (Test-Path $outputsRoot)) {
    $outputsRoot = $workspaceRoot
}

$draftFile = Join-Path $outputsRoot "deployment-draft.json"
$masterBackupFile = Join-Path $outputsRoot "deployment-master-backup.json"
$metaFile = Join-Path $outputsRoot "deployment-meta.json"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$port/")
$listener.Start()
Write-Host "========================================================"
Write-Host " Gyan Mansarovar 3D Server running at http://localhost:$port/"
Write-Host " Serving files from: $outputsRoot"
Write-Host " Backend API active at: http://localhost:$port/api/deployment"
Write-Host "========================================================"

$mimeTypes = @{
    ".html" = "text/html; charset=utf-8"
    ".htm"  = "text/html; charset=utf-8"
    ".css"  = "text/css; charset=utf-8"
    ".js"   = "application/javascript; charset=utf-8"
    ".json" = "application/json; charset=utf-8"
    ".glb"  = "model/gltf-binary"
    ".gltf" = "model/gltf+json"
    ".png"  = "image/png"
    ".jpg"  = "image/jpeg"
    ".jpeg" = "image/jpeg"
    ".webp" = "image/webp"
    ".svg"  = "image/svg+xml"
    ".txt"  = "text/plain; charset=utf-8"
    ".md"   = "text/markdown; charset=utf-8"
}

function Send-JsonResponse($response, $statusCode, $obj) {
    $response.StatusCode = $statusCode
    $response.ContentType = "application/json; charset=utf-8"
    $response.AddHeader("Access-Control-Allow-Origin", "*")
    $response.AddHeader("Access-Control-Allow-Methods", "GET, PUT, POST, OPTIONS")
    $response.AddHeader("Access-Control-Allow-Headers", "Content-Type, X-GMS-Plan")
    $json = ConvertTo-Json -InputObject $obj -Depth 10 -Compress
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    $response.ContentLength64 = $bytes.Length
    $response.OutputStream.Write($bytes, 0, $bytes.Length)
    $response.OutputStream.Close()
}

function Get-MasterPlan() {
    # If draftFile exists and has items, return draftFile directly (honoring user additions and deletions)
    if (Test-Path $draftFile) {
        try {
            $d = Get-Content $draftFile -Raw -Encoding UTF8 | ConvertFrom-Json
            if ($d.items -ne $null) {
                return $d
            }
        } catch {}
    }
    
    # Baseline from master backup only if draft doesn't exist yet
    if (Test-Path $masterBackupFile) {
        try {
            $m = Get-Content $masterBackupFile -Raw -Encoding UTF8 | ConvertFrom-Json
            if ($m.items) {
                return $m
            }
        } catch {}
    }
    
    return @{
        version = 1
        origin = @(76.848831, 29.413077)
        coordinateFrame = "WGS84 local metres: east X, up Y, south Z"
        status = "Draft - user editable duty order"
        items = @()
    }
}

try {
    while ($listener.IsListening) {
        try {
            $context = $listener.GetContext()
            $request = $context.Request
            $response = $context.Response

            $urlPath = $request.Url.LocalPath

            # Handle CORS preflight
            if ($request.HttpMethod -eq "OPTIONS") {
                $response.StatusCode = 204
                $response.AddHeader("Access-Control-Allow-Origin", "*")
                $response.AddHeader("Access-Control-Allow-Methods", "GET, PUT, POST, OPTIONS")
                $response.AddHeader("Access-Control-Allow-Headers", "Content-Type, X-GMS-Plan")
                $response.OutputStream.Close()
                continue
            }

            # Handle /api/deployment
            if ($urlPath -eq "/api/deployment") {
                if ($request.HttpMethod -eq "GET") {
                    $plan = Get-MasterPlan
                    $curRev = 7000
                    $updated = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
                    if (Test-Path $metaFile) {
                        try {
                            $m = Get-Content $metaFile -Raw -Encoding UTF8 | ConvertFrom-Json
                            if ($m.revision) { $curRev = [int]$m.revision }
                            if ($m.updated) { $updated = $m.updated }
                        } catch {}
                    }

                    Send-JsonResponse $response 200 @{
                        revision = $curRev
                        plan = $plan
                        updated = $updated
                    }
                    continue
                }
                elseif ($request.HttpMethod -eq "PUT" -or $request.HttpMethod -eq "POST") {
                    $bodyText = ""
                    $len = $request.ContentLength64
                    if ($len -gt 0) {
                        $buffer = New-Object byte[] $len
                        $read = 0
                        while ($read -lt $len) {
                            $r = $request.InputStream.Read($buffer, $read, $len - $read)
                            if ($r -le 0) { break }
                            $read += $r
                        }
                        $bodyText = [System.Text.Encoding]::UTF8.GetString($buffer, 0, $read)
                    }
                    $body = $null
                    if ($bodyText) {
                        try {
                            $body = $bodyText | ConvertFrom-Json
                        } catch {
                            Send-JsonResponse $response 400 @{ error = "JSON parse error: $_" }
                            continue
                        }
                    }

                    if ($body -and $body.plan -and ($body.plan.items -ne $null)) {
                        $userItems = @($body.plan.items)

                        # Maintain foundation elevation for parking lots
                        foreach ($it in $userItems) {
                            if ($it.kind -eq "parking" -and $it.y -lt 0.30 -and $it.z -lt -150) { $it.y = 0.36 }
                        }

                        $savedPlan = @{
                            version = 1
                            origin = @(76.848831, 29.413077)
                            coordinateFrame = "WGS84 local metres: east X, up Y, south Z"
                            status = "Draft - user editable duty order"
                            items = $userItems
                        }

                        $curRev = 7001
                        if (Test-Path $metaFile) {
                            try {
                                $m = Get-Content $metaFile -Raw -Encoding UTF8 | ConvertFrom-Json
                                if ($m.revision) { $curRev = [int]$m.revision + 1 }
                            } catch {}
                        }
                        $updated = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

                        # Save active draft JSON and backup
                        $planJson = ConvertTo-Json -InputObject $savedPlan -Depth 10
                        [System.IO.File]::WriteAllText($draftFile, $planJson, [System.Text.Encoding]::UTF8)
                        [System.IO.File]::WriteAllText($masterBackupFile, $planJson, [System.Text.Encoding]::UTF8)

                        # Save meta revision
                        $metaJson = ConvertTo-Json -InputObject @{ revision = $curRev; updated = $updated }
                        [System.IO.File]::WriteAllText($metaFile, $metaJson, [System.Text.Encoding]::UTF8)

                        Send-JsonResponse $response 200 @{
                            ok = $true
                            revision = $curRev
                            updated = $updated
                        }
                    } else {
                        Send-JsonResponse $response 400 @{ error = "Invalid plan payload" }
                    }
                    continue
                }
            }

            # Handle Root redirect / default page
            $trimmed = $urlPath.TrimStart('/')
            if ([string]::IsNullOrEmpty($trimmed) -or $trimmed -eq "/") {
                $trimmed = "gyan-mansarovar-3d.html"
            }
            if ($trimmed.StartsWith("outputs/")) {
                $trimmed = $trimmed.Substring("outputs/".Length)
            }

            $decodedPath = [System.Uri]::UnescapeDataString($trimmed)
            $filePath = [System.IO.Path]::Combine($outputsRoot, $decodedPath.Replace('/', [System.IO.Path]::DirectorySeparatorChar))

            if (Test-Path $filePath -PathType Leaf) {
                $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
                $contentType = if ($mimeTypes.ContainsKey($ext)) { $mimeTypes[$ext] } else { "application/octet-stream" }
                $response.ContentType = $contentType
                $response.AddHeader("Access-Control-Allow-Origin", "*")

                $bytes = [System.IO.File]::ReadAllBytes($filePath)
                $response.ContentLength64 = $bytes.Length
                $response.StatusCode = 200

                if ($request.HttpMethod -ne "HEAD") {
                    $response.OutputStream.Write($bytes, 0, $bytes.Length)
                }
            } else {
                $response.StatusCode = 404
                $msg = [System.Text.Encoding]::UTF8.GetBytes("File Not Found: $decodedPath")
                $response.ContentLength64 = $msg.Length
                if ($request.HttpMethod -ne "HEAD") {
                    $response.OutputStream.Write($msg, 0, $msg.Length)
                }
            }
            $response.OutputStream.Close()
        } catch {
            Write-Host "Request warning: $_"
            try {
                if ($response -and $response.OutputStream) {
                    $response.StatusCode = 500
                    $response.OutputStream.Close()
                }
            } catch {}
        }
    }
} finally {
    $listener.Stop()
}
