"""
$fdir = $args[0]  # e.g. ".\font-m-TaD"
$fstem = $args[1]  # e.g. "Taamey_D"
$in_fea = "$fdir\$fstem.sym.fea"
$ou_fea = "$fdir\$fstem.fea"

Example use:

    main_fill_in_template.py $fstem
        $in_fea
        $ou_fea

    main_fill_in_template.py Taamey_D
        .\font-m-TaD\Taamey_D.sym.fea
        .\font-m-TaD\Taamey_D.fea
"""
import argparse
import string

import my_open
import my_font_version


def _latin_lines(font_str):
    if font_str == 'Keter_D':
        return []
    latin_glyphs_extra_dic = {
        'Taamey_B': ' taken from Century Schoolbook L font,',
        'Taamey_D': ' taken from Century Schoolbook L font,',
        'Shofar_D': '',
        # no Keter_D, intentionally
    }
    latin_glyphs_extra = latin_glyphs_extra_dic[font_str]
    return [
        '',
        f'Latin glyphs (letters and part of punctuation){latin_glyphs_extra}',
        'copyright (c) 1999 by (URW)++ Design & Development.',
    ]


def _indent(lines):
    return ['    ' + line for line in lines]


def _cop_n_lic_lines(font_str):
    return (
        []
        + ['COPYRIGHT', '']
        + _indent(_cop_lines(font_str))
        + ['']
        + ['LICENSE', '']
        + _indent(_lic_lines(font_str)))


def _cop_lines(font_str):
    font_name_dic = {
        'Taamey_B': 'Taamey B',
        'Taamey_D': 'Taamey D',
        'Shofar_D': 'Shofar D',
        'Keter_D': 'Keter D',
    }
    yg_font_name_dic = {
        'Taamey_B': 'Taamey Frank CLM Medium',
        'Taamey_D': 'Taamey Frank CLM Medium',
        'Shofar_D': 'Shofar Regular',
        'Keter_D': 'KeterYG Regular',
    }
    yg_cop_years_dic = {
        'Taamey_B': '2009-2010',
        'Taamey_D': '2009-2010',
        'Shofar_D': '2011-2012',
        'Keter_D': '2009-2010',
    }
    font_name = font_name_dic[font_str]
    yg_font_name = yg_font_name_dic[font_str]
    yg_cop_years = yg_cop_years_dic[font_str]
    main = [
        'Copyright (c) 2021, Ben Denckla (<bdenckla@alum.mit.edu>),',
        f'with Reserved Font Name \'{font_name}\'.',
        '',
        f'{font_name}\'s glyphs are derived from those of {yg_font_name}.',
        f'{font_name}\'s OpenType mark positioning logic is original, i.e. *not* derived from that of {yg_font_name}.',
        f'Below are the relevant parts of the copyright of {yg_font_name}, with minor edits for clarity.',
        '',
        'Hebrew glyphs (letters, vowels, & cantillation marks)',
        f'copyright (c) {yg_cop_years}, Yoram Gnat (<yoram.gnat@gmail.com>).',
    ]
    return main + _latin_lines(font_str)

_LICENSE_URL = 'http://www.gnu.org/licenses/old-licenses/gpl-2.0.html'

def _lic_lines(font_str):
    font_name_dic = {
        'Taamey_B': 'Taamey B',
        'Taamey_D': 'Taamey D',
        'Shofar_D': 'Shofar D',
        'Keter_D': 'Keter D',
    }
    yg_font_name_dic = {
        'Taamey_B': 'Taamey Frank CLM Medium',
        'Taamey_D': 'Taamey Frank CLM Medium',
        'Shofar_D': 'Shofar Regular',
        'Keter_D': 'KeterYG Regular',
    }
    yg_cop_years_dic = {
        'Taamey_B': '2009-2010',
        'Taamey_D': '2009-2010',
        'Shofar_D': '2011-2012',
        'Keter_D': '2009-2010',
    }
    font_name = font_name_dic[font_str]
    yg_font_name = yg_font_name_dic[font_str]
    yg_cop_years = yg_cop_years_dic[font_str]
    license_url = _LICENSE_URL
    main = [
        'This Font Software is licensed under the GNU Public License Version 2.',
        f'The license is available at {license_url}.',
        '',
        'As a special exception,',
        'if you create a document which uses this font, and embed this font or unaltered portions of this font into the document,',
        'this font does not by itself cause the resulting document to be covered by the GNU General Public License.',
        'This exception does not however invalidate any other reasons why the document might be covered by the GNU General Public License.',
        'If you modify this font, you may extend this exception to your version of the font, but you are not obligated to do so.',
        'If you do not wish to do so, delete this exception statement from your version.',
    ]
    return main

_WIDTH = {
    'alef': (1048, 1229),
    'bet': (967, 1056),
    'gimel': (665, 737),
    'dalet': (879, 1071),
    'he': (1071, 1218),
    'vav': (510, 588),
    'zayin': (656, 585),
    'xet': (1065, 1160),
    'tet': (1015, 1082),
    'yod': (464, 627),
    'finalkaf': (846, 1055),
    'kaf': (942, 973),
    'lamed': (901, 964),
    'finalmem': (1004, 1159),
    'mem': (1094, 1187),
    'finalnun': (459, 532),
    'nun': (614, 746),
    'samekh': (1038, 1099),
    'ayin': (920, 1040),  # XXX Shofar D ayin.alt is 1050 wide
    'finalpe': (886, 995),
    'pe': (912, 981),
    'finaltsadi': (990, 951),
    'tsadi': (968, 1013),
    'qof': (997, 1013),
    'resh': (883, 1021),
    'shinfamily': (1292, 1435),
    'shin': (1292, 1435),
    'sin': (1292, 1435),
    'tav': (1026, 1319),
    'dottedcircle': (1150, 1244),
    #
    'sheva': (140, 140),
    'tsere': (356, 356),
    'segol': (376, 376),
    'patax': (300, 300),
    'qamats': (296, 296),
    'qubuts': (444, 444),
    'hsegol': (608, 608),
    'hqamats': (532, 532),
    'hpatax': (532, 532),
    #
    'meteg': (72, 72),
    'tipxa': (176, 176),
    'merkha': (174, 174),
    'darga': (208, 208),
    'munax': (243, 243),
    'atnax': (304, 304),
    'mahapakh': (276, 276),
    'tevir': (284, 284),
    'merkhakefula': (368, 368),
}

def _halfwidth_minus_room_for_xolam(fnt, letter):
    return _halfwidth_plus(fnt, letter, -530)

def _mkmk1_pm(fnt, mark):  # pm: pos mark ...
    return 0 - _halfwidth_plus(fnt, mark, 180)

def _mkmk1_mc(fnt, mark):  # mc: markClass ...
    return _halfwidth_plus(fnt, mark, -80)

def _mkmk2_pm(fnt, mark):  # pm: pos mark ...
    return 0 - _halfwidth_plus(fnt, mark, 262)

def _mkmk2_mc(fnt, mark):  # mc: markClass ...
    return _halfwidth_plus(fnt, mark, -140)

def _halfwidth(fnt, letter):
    return _halfwidth_plus(fnt, letter, 0)

def _halfwidth_plus(fnt, letter, amount_to_add):
    return _width(fnt, letter) // 2 + amount_to_add  # // is the "floor division" operator

_FONT_INTEGER = {
    'Taamey_B': 0,
    'Taamey_D': 0,
    'Shofar_D': 1,
    'Keter_D': 1,  # XXX totally bogus, just doing this temporarily
}

def _width(fnt_str, letter):
    fnt_int = _FONT_INTEGER[fnt_str]
    return _WIDTH[letter][fnt_int]  # XXX use a fn of fnt, not 0!


def _symdefs(fnt):
    return {
        #
        'copyright': '\n'.join(_cop_lines(fnt)),
        'license': '\n'.join(_lic_lines(fnt)),
        'license_url': _LICENSE_URL,
        'copyright_and_license': r'\n'.join(_cop_n_lic_lines(fnt)),
        'copyright_and_license_real_newlines': '\n'.join(_cop_n_lic_lines(fnt)),
        #
        'version': my_font_version.VERSION,
        #
        'mkmk1_pm_sheva': _mkmk1_pm(fnt, 'sheva'),
        'mkmk1_pm_tsere': _mkmk1_pm(fnt, 'tsere'),
        'mkmk1_pm_patax': _mkmk1_pm(fnt, 'patax'),
        'mkmk1_pm_qubuts': _mkmk1_pm(fnt, 'qubuts'),
        'mkmk1_pm_qamats': _mkmk1_pm(fnt, 'qamats'),
        'mkmk1_pm_segol': _mkmk1_pm(fnt, 'segol'),
        'mkmk1_pm_hsegol': _mkmk1_pm(fnt, 'hsegol'),
        'mkmk1_pm_hqamats': _mkmk1_pm(fnt, 'hqamats'),
        'mkmk1_pm_hpatax': _mkmk1_pm(fnt, 'hpatax'),
        #
        'mkmk1_mc_meteg': _mkmk1_mc(fnt, 'meteg'),
        'mkmk1_mc_tipxa': _mkmk1_mc(fnt, 'tipxa'),
        'mkmk1_mc_merkha': _mkmk1_mc(fnt, 'merkha'),
        'mkmk1_mc_darga': _mkmk1_mc(fnt, 'darga'),
        'mkmk1_mc_sheva': _mkmk1_mc(fnt, 'sheva'),
        'mkmk1_mc_patax': _mkmk1_mc(fnt, 'patax'),
        'mkmk1_mc_munax': _mkmk1_mc(fnt, 'munax'),
        'mkmk1_mc_atnax': _mkmk1_mc(fnt, 'atnax'),
        'mkmk1_mc_mahapakh': _mkmk1_mc(fnt, 'mahapakh'),
        'mkmk1_mc_tevir': _mkmk1_mc(fnt, 'tevir'),
        'mkmk1_mc_merkhakefula': _mkmk1_mc(fnt, 'merkhakefula'),
        #
        'mkmk2_mc_sheva': _mkmk2_mc(fnt, 'sheva'),
        'mkmk2_mc_tsere': _mkmk2_mc(fnt, 'tsere'),
        'mkmk2_mc_segol': _mkmk2_mc(fnt, 'segol'),
        'mkmk2_mc_qamats': _mkmk2_mc(fnt, 'qamats'),
        'mkmk2_mc_qubuts': _mkmk2_mc(fnt, 'qubuts'),
        'mkmk2_mc_hpatax': _mkmk2_mc(fnt, 'hpatax'),
        'mkmk2_mc_meteg': _mkmk2_mc(fnt, 'meteg'),
        'mkmk2_mc_tipxa': _mkmk2_mc(fnt, 'tipxa'),
        'mkmk2_mc_merkha': _mkmk2_mc(fnt, 'merkha'),
        'mkmk2_mc_munax': _mkmk2_mc(fnt, 'munax'),
        'mkmk2_mc_atnax': _mkmk2_mc(fnt, 'atnax'),
        'mkmk2_mc_mahapakh': _mkmk2_mc(fnt, 'mahapakh'),
        'mkmk2_mc_tevir': _mkmk2_mc(fnt, 'tevir'),
        #
        'mkmk2_pm_meteg': _mkmk2_pm(fnt, 'meteg'),
        'mkmk2_pm_tipxa': _mkmk2_pm(fnt, 'tipxa'),
        'mkmk2_pm_merkha': _mkmk2_pm(fnt, 'merkha'),
        'mkmk2_pm_munax': _mkmk2_pm(fnt, 'munax'),
        'mkmk2_pm_atnax': _mkmk2_pm(fnt, 'atnax'),
        'mkmk2_pm_mahapakh': _mkmk2_pm(fnt, 'mahapakh'),
        'mkmk2_pm_tevir': _mkmk2_pm(fnt, 'tevir'),
        #
        'mkmk3_mc_atnax': _mkmk1_mc(fnt, 'atnax') - 90,
        'mkmk3_mc_tipxa': _mkmk1_mc(fnt, 'tipxa') - 90,
        #
        'A42_finalkafqamats': _halfwidth_plus(fnt, 'finalkaf', -150),
        #
        #
        'A4_finalkaf': _halfwidth_plus(fnt, 'finalkaf', -50),
        'A4_finalnun': -29,
        'A4_qof': _halfwidth_plus(fnt, 'qof', 120),
        #
        #
        # XXX gimel doesn't need similar adjustment?
        'A41_yetiv_dexi_vav': _width(fnt, 'vav') + 100,
        'A41_yetiv_dexi_zayin': _width(fnt, 'zayin') + 100,
        'A41_yetiv_dexi_yod': _width(fnt, 'yod') + 100,
        'A41_yetiv_dexi_nun': _width(fnt, 'nun') + 100,
        #
        #
        'A68_dexi_vav': _width(fnt, 'vav') + 150,
        'A68_dexi_yod': _width(fnt, 'yod') + 150,
        #
        #
        'A22_gimel': _halfwidth_minus_room_for_xolam(fnt, 'gimel'),
        'A22_vav': _halfwidth_minus_room_for_xolam(fnt, 'vav'),
        'A22_zayin': _halfwidth_minus_room_for_xolam(fnt, 'zayin'),
        'A22_yod': _halfwidth_minus_room_for_xolam(fnt, 'yod'),
        'A22_nun': _halfwidth_minus_room_for_xolam(fnt, 'nun'),
        'A22_dalet': _halfwidth_minus_room_for_xolam(fnt, 'dalet'),
        'A22_resh': _halfwidth_minus_room_for_xolam(fnt, 'resh'),
        'A22_pe': _halfwidth_minus_room_for_xolam(fnt, 'pe'),
        'A22_ayin': _halfwidth_minus_room_for_xolam(fnt, 'ayin'),
        #
        #
        'A23_lamed': _halfwidth_plus(fnt, 'lamed', 150),
        #
        #
        'halfwidth_alef': _halfwidth(fnt, 'alef'),
        'halfwidth_bet': _halfwidth(fnt, 'bet'),
        'halfwidth_gimel': _halfwidth(fnt, 'gimel'),
        'halfwidth_dalet': _halfwidth(fnt, 'dalet'),
        'halfwidth_he': _halfwidth(fnt, 'he'),
        'halfwidth_vav': _halfwidth(fnt, 'vav'),
        'halfwidth_zayin': _halfwidth(fnt, 'zayin'),
        'halfwidth_xet': _halfwidth(fnt, 'xet'),
        'halfwidth_tet': _halfwidth(fnt, 'tet'),
        'halfwidth_yod': _halfwidth(fnt, 'yod'),
        'halfwidth_finalkaf': _halfwidth(fnt, 'finalkaf'),
        'halfwidth_kaf': _halfwidth(fnt, 'kaf'),
        'halfwidth_lamed': _halfwidth(fnt, 'lamed'),
        'halfwidth_finalmem': _halfwidth(fnt, 'finalmem'),
        'halfwidth_mem': _halfwidth(fnt, 'mem'),
        'halfwidth_finalnun': _halfwidth(fnt, 'finalnun'),
        'halfwidth_nun': _halfwidth(fnt, 'nun'),
        'halfwidth_samekh': _halfwidth(fnt, 'samekh'),
        'halfwidth_ayin': _halfwidth(fnt, 'ayin'),
        'halfwidth_finalpe': _halfwidth(fnt, 'finalpe'),
        'halfwidth_pe': _halfwidth(fnt, 'pe'),
        'halfwidth_finaltsadi': _halfwidth(fnt, 'finaltsadi'),
        'halfwidth_tsadi': _halfwidth(fnt, 'tsadi'),
        'halfwidth_qof': _halfwidth(fnt, 'qof'),
        'halfwidth_resh': _halfwidth(fnt, 'resh'),
        'halfwidth_shin': _halfwidth(fnt, 'shin'),
        'halfwidth_tav': _halfwidth(fnt, 'tav'),
        'halfwidth_dottedcircle': _halfwidth(fnt, 'dottedcircle'),
        #
        #
        'width_alef': _width(fnt, 'alef'),
        'width_bet': _width(fnt, 'bet'),
        'width_gimel': _width(fnt, 'gimel'),
        'width_dalet': _width(fnt, 'dalet'),
        'width_he': _width(fnt, 'he'),
        'width_vav': _width(fnt, 'vav'),
        'width_zayin': _width(fnt, 'zayin'),
        'width_xet': _width(fnt, 'xet'),
        'width_tet': _width(fnt, 'tet'),
        'width_yod': _width(fnt, 'yod'),
        'width_finalkaf': _width(fnt, 'finalkaf'),
        'width_kaf': _width(fnt, 'kaf'),
        'width_lamed': _width(fnt, 'lamed'),
        'width_finalmem': _width(fnt, 'finalmem'),
        'width_mem': _width(fnt, 'mem'),
        'width_finalnun': _width(fnt, 'finalnun'),
        'width_nun': _width(fnt, 'nun'),
        'width_samekh': _width(fnt, 'samekh'),
        'width_ayin': _width(fnt, 'ayin'),
        'width_finalpe': _width(fnt, 'finalpe'),
        'width_pe': _width(fnt, 'pe'),
        'width_finaltsadi': _width(fnt, 'finaltsadi'),
        'width_tsadi': _width(fnt, 'tsadi'),
        'width_qof': _width(fnt, 'qof'),
        'width_resh': _width(fnt, 'resh'),
        'width_shin': _width(fnt, 'shin'),
        'width_tav': _width(fnt, 'tav'),
        'width_dottedcircle': _width(fnt, 'dottedcircle'),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("value_set")  # e.g. Taamey_B, Shofar_D, etc.
    # Value set selects which set of values should be used to substitute in
    # for dollar-signed symbols.
    parser.add_argument("template_file")  # e.g. foo.sym.fea
    # The input file has dollar-signed symbols sprinkled throughout.
    # I.e. it has symbols rather than literal values in some places.
    # I.e. it is a kind of template.
    parser.add_argument("literal_file")  # e.g. foo.fea
    # The output file has values substituted in for dollar-signed symbols.
    # I.e. the symbols have become literal values.
    args = parser.parse_args()
    with open(args.template_file, encoding='utf-8', newline='') as infp:
        with my_open.openw(args.literal_file, newline='') as outfp:
            for line in infp:
                sds = _symdefs(args.value_set)
                after_dollar_subs = string.Template(line).substitute(sds)
                outfp.write(after_dollar_subs)


if __name__ == '__main__':
    main()
