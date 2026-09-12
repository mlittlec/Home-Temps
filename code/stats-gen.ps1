$RawRoot = "weather/raw"
$DerivedRoot = "weather/derived"

function Ensure-Dir($path) {
    if (!(Test-Path $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
    }
}

function Get-MonthData($year, $month) {
    $file = "$RawRoot/$year/weather_daily_${year}-${month}.csv"
    if (Test-Path $file) {
        return Import-Csv $file
    }
    return $null
}

function Write-MonthSummary($data, $year, $month) {
    $outdir = "$DerivedRoot/summaries/monthly/$year"
    Ensure-Dir $outdir

    $minTemps = $data.min_temp | ForEach-Object { [double]$_ }
    $maxTemps = $data.max_temp | ForEach-Object { [double]$_ }

    $dominant = $data.conditions `
        | ForEach-Object { $_ -split ";" } `
        | Group-Object `
        | Sort-Object Count -Descending `
        | Select-Object -First 3 `
        | ForEach-Object { $_.Name } `
        -join ";"

    $summary = [PSCustomObject]@{
        year = $year
        month = $month
        avg_min_temp = ($minTemps | Measure-Object -Average).Average
        avg_max_temp = ($maxTemps | Measure-Object -Average).Average
        min_of_min_temp = ($minTemps | Measure-Object -Minimum).Minimum
        max_of_max_temp = ($maxTemps | Measure-Object -Maximum).Maximum
        dominant_conditions = $dominant
    }

    $summary | Export-Csv "$outdir/summary_${year}-${month}.csv" -NoTypeInformation
}

function Write-MonthAnomalies($data, $year, $month) {
    $outdir = "$DerivedRoot/anomalies/$year"
    Ensure-Dir $outdir

    $minTemps = $data.min_temp | ForEach-Object { [double]$_ }
    $maxTemps = $data.max_temp | ForEach-Object { [double]$_ }

    $meanMin = ($minTemps | Measure-Object -Average).Average
    $stdMin = [Math]::Sqrt(($minTemps | ForEach-Object { ($_ - $meanMin) ** 2 } | Measure-Object -Sum).Sum / $minTemps.Count)

    $meanMax = ($maxTemps | Measure-Object -Average).Average
    $stdMax = [Math]::Sqrt(($maxTemps | ForEach-Object { ($_ - $meanMax) ** 2 } | Measure-Object -Sum).Sum / $maxTemps.Count)

    $anomalies = $data | Where-Object {
        (($_.min_temp - $meanMin) / $stdMin) -gt 2 -or
        (($_.max_temp - $meanMax) / $stdMax) -gt 2
    }

    $anomalies | Export-Csv "$outdir/anomalies_${year}-${month}.csv" -NoTypeInformation
}

function Write-MonthChart($data, $year, $month) {
    $outdir = "$DerivedRoot/charts/$year"
    Ensure-Dir $outdir

    # Simple placeholder chart (PowerShell charting is limited)
    $chartFile = "$outdir/temps_${year}-${month}.png"
    Set-Content $chartFile "Chart placeholder for ${year}-${month}"
}

foreach ($yearDir in Get-ChildItem $RawRoot) {
    if ($yearDir.PSIsContainer) {
        $year = [int]$yearDir.Name

        foreach ($month in 1..12) {
            $monthStr = "{0:D2}" -f $month
            $data = Get-MonthData $year $monthStr
            if ($data) {
                Write-MonthSummary $data $year $monthStr
                Write-MonthAnomalies $data $year $monthStr
                Write-MonthChart $data $year $monthStr
            }
        }
    }
}
