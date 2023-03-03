$fdir = $args[0]  # e.g. ".\font-m-TaD"
$fstem = $args[1]  # e.g. "Taamey_D"
$in_fea = "$fdir\$fstem.sym.fea"
$ou_fea = "$fdir\$fstem.fea"
$in_sfd = "$fdir\$fstem-nofea.sym.sfd"
$ou_sfd = "$fdir\$fstem-nofea.sfd"
$in_lic = "$fdir\license.sym.txt"
$ou_lic = "$fdir\license.txt"
#
$io_pair_fea = @{in=$in_fea; out=$ou_fea}
$io_pair_sfd = @{in=$in_sfd; out=$ou_sfd}
$io_pair_lic = @{in=$in_lic; out=$ou_lic}
#
$io_pairs = $io_pair_fea, $io_pair_sfd, $io_pair_lic
foreach ($io_pair in $io_pairs) {
    attrib -r $io_pair.out
    python main_fill_in_template.py $fstem $io_pair.in $io_pair.out
    if (-not $?)
    {
        throw "failed to generate $io_pair.out"
    }
    attrib +r $io_pair.out
}
$pf6 = [Environment]::GetFolderPath("ProgramFilesX86")
$ffbat = "$pf6\FontForgeBuilds\fontforge.bat"
& $ffbat -script $fdir\ffscript_generate_sfd_n_ttf.py
