Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
python -m pip install -r requirements.txt
python -m mkdocs serve
