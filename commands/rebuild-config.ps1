param (
    [String]$mode
)

if ($mode) {
    Push-Location $PSScriptRoot\..\docs\sphinx
    poetry run sphinx-build -M $mode . _build -v -W
    Pop-Location
} else {
    poetry run sphinx-build help
}
