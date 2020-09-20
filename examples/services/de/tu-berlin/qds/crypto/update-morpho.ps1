$projects = @(
    ".\caeser"
    ".\permutation"
    ".\gateway"
    ".\vigenere"
)

foreach ($path in $projects) {
    Write-Host "Updating: $($path)"
    Push-Location $path
    poetry add morpho@latest
    Pop-Location
}