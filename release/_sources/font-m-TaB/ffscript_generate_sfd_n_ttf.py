# This script is meant to be run ("driven") by an outer PowerShell script,
# like this:
#
#    .\ps1_ffscript_generate_sfd_n_ttf_solo.ps1 .\font-m-TaB Taamey_B

import fontforge  # pyright: reportMissingImports=false
base = 'font-m-TaB/Taamey_B'
font = fontforge.open(base + '-nofea.sfd')
font.mergeFeature(base + '.fea')
font.save(base + '.sfd')
font.generate(base + '.ttf')
font.generate(base + '.woff')
font.generate(base + '.woff2')
