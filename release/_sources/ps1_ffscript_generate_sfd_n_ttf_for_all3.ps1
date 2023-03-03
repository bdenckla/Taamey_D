$shod = @{dir="font-m-ShoD"; stem="Shofar_D"}
$tab = @{dir="font-m-TaB"; stem="Taamey_B"}
$tad = @{dir="font-m-TaD"; stem="Taamey_D"}
$fonts = $shod, $tab, $tad
foreach ($font in $fonts) {
    & .\ps1_ffscript_generate_sfd_n_ttf_solo.ps1 $font.dir $font.stem
    if (-not $?)
    {
        throw "failed to generate various files for $d"
    }
}
