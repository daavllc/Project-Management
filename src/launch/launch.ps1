$PyFolder = "Python310" # This is the folder name of the required python version
$Version = "3.10"
$PyPath = 0 # This stores absolute path to python executable
function main
{
    if ( -not (Test-Path -Path .\..\..\settings)) { New-Item -Path .\..\..\settings -ItemType Directory}

    if ( -not (Test-Path -Path .\..\..\settings\launch.txt))
    {
        $PathList = [Environment]::GetEnvironmentVariable("Path").split(";")
        $pathIndex
        foreach ($item in $PathList) # Check $Path for $PyFolder
        {
            $index = 0
            $size = $item.split("\").length - 1 # this accounts for the \ at the end
            foreach ($section in $item.split("\"))
            {
                $index += 1
                if ($index -ne $size) {continue}
                if ($section -match $PyFolder)
                {
                    $PyPath = $item
                    Write-Host Found Python Path: $PyPath
                    $PyPath.Replace("\", "/") | Out-File  .\..\..\settings\launch.txt -Encoding utf8
                    break
                }
            }
            if ($PyPath -ne 0) {break}
        }
        if ($PyPath -eq 0)
        {
            Write-Host "Unable to find Python $Version"
            Write-Host "Please download Python $Version or add it to your Path variable"
            Exit
        }
    }
    else
    {
        $PyPath = (Get-Content .\..\..\settings\launch.txt | Select-Object -First 1).Replace("/", "\")
    }
    Set-Location -Path ../setup
    & $PyPath\python.exe Setup.py
    Set-Location -Path ..
    Launcher
}

function Launcher
{
    $returnValue = -2
    while (1)
    {
        if ($returnValue -eq 0) { exit }
        elseif ($returnValue -eq -1) { Clear-Host; Set-Location -Path .\..\; Start-Process powershell -args "Write-Host Waiting to ensure deletion...; Start-Sleep -s 3; & $PyPath\python.exe FinishUpdate.py; Start-Process Win-Launch.bat"; exit }
        elseif ($returnValue -eq -2) { Clear-Host; & $PyPath\python.exe main.py }
        elseif ($returnValue -eq -3) { Clear-Host; & $PyPath\python.exe main.py -UI CUI }
        elseif ($returnValue -eq -4) { Clear-Host; & $PyPath\python.exe main.py -UI GUI }
        else
        {
            Write-Output ""
            Write-Output "It looks like something went wrong... Error: $returnValue"
            Write-Output "Feel free to submit an issue at 'https://github.com/daavofficial/Project-Management/issues'"
            $UsrInput = Read-Host "Reload? (Y/n) > "
            if ($UsrInput -eq "n") {Exit}
                $returnValue = -1
        }
        $returnValue = $LASTEXITCODE
    }
}

main