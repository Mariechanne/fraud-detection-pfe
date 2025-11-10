param(
    [ValidateSet("fmt", "lint", "test", "all")]
    [string]$task = "all"
)

switch ($task) {
    "fmt" { black .; isort .; break }
    "lint" { flake8 .; break }
    "test" { pytest; break }
    "all" { black .; isort .; flake8 .; pytest; break }
}
