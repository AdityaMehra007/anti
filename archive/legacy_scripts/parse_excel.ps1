Add-Type -AssemblyName System.IO.Compression.FileSystem

function Inspect-Xlsx-Sheets($filePath) {
    Write-Host "=================================================="
    Write-Host "INSPECTING WORKSHEET XML: $filePath"
    Write-Host "=================================================="
    
    if (-not (Test-Path $filePath)) {
        Write-Host "File not found: $filePath"
        return
    }

    $zip = [System.IO.Compression.ZipFile]::OpenRead($filePath)
    
    foreach ($entry in $zip.Entries) {
        if ($entry.FullName -like "xl/worksheets/*.xml") {
            Write-Host "Found Worksheet Entry: $($entry.FullName)"
            $stream = $entry.Open()
            $reader = New-Object System.IO.StreamReader($stream)
            $content = $reader.ReadToEnd()
            $reader.Close()
            $stream.Close()
            
            Write-Host "Sheet Content Size: $($content.Length) bytes"
            
            # Extract cell values using regex
            $cells = [regex]::Matches($content, "<v>(.*?)</v>")
            Write-Host "Cell <v> Value Elements Found: $($cells.Count)"
            for ($i = 0; $i -lt [Math]::Min(20, $cells.Count); $i++) {
                Write-Host "  Cell[$i] = $($cells[$i].Groups[1].Value)"
            }

            # Extract inline string values if any
            $inlines = [regex]::Matches($content, "<t[^>]*>(.*?)</t>")
            Write-Host "Inline Text <t> Elements Found: $($inlines.Count)"
            for ($i = 0; $i -lt [Math]::Min(20, $inlines.Count); $i++) {
                Write-Host "  Inline[$i] = $($inlines[$i].Groups[1].Value)"
            }
        }
    }
    
    $zip.Dispose()
}

Inspect-Xlsx-Sheets "e:\anti\BBA_International_Business_1400_Companies.xlsx"
Inspect-Xlsx-Sheets "e:\anti\BBA_International_Business_Bangalore_Job_Pipeline.xlsx"
