# Project-Management.launch.launch - Launch setup.py, and main.py, parses errorlevels
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

$py3 = 1
function main
{
    Set-Location -Path ../setup
    if ([System.Environment]::GetEnvironmentVariable('python3'))
    {
        $py3 = 1
        python3 Setup.py
    }
    else    # Assuming python2 isn't installed
    {
        $py3 = 0
        python Setup.py
    }
    Set-Location -Path ..
    Launch
}
function CheckErrorLevel($el)
{
    if ($el -eq 0) {Exit}
    if ($el -eq -1) {Launch}
    elseif ($el -eq -2) {LaunchCUI}
    elseif ($el -eq -3) {LaunchGUI}
    else {Error($el)}
}

function Error($el)
{
    Write-Output ""
    Write-Output "It looks like something went wrong... Error: $el"
    Write-Output "Feel free to submit an issue at 'https://github.com/daavofficial/Project-Management/issues'"
    $UsrInput = Read-Host "Reload? (Y/n) > "
    if ($UsrInput -eq "n") {Exit}
    Launch
}

function Launch
{
    Clear-Host
    if ($py3) {python3 main.py}
    else {python main.py}
    CheckErrorLevel($LASTEXITCODE)
}

function LaunchCUI
{
    Clear-Host
    if ($py3) {python3 main.py -UI CUI}
    else {python main.py -UI CUI}
    CheckErrorLevel($py, $LASTEXITCODE)
}

function LaunchGUI
{
    Clear-Host
    if ($py3) {python3 main.py -UI GUI}
    else {python main.py -UI GUI}
    CheckErrorLevel($py, $LASTEXITCODE)
}

main