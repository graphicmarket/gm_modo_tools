# python
# coding=utf8

import re

charsTable = {u'&lt;': '', u'&gt;': '', u'&#039;': '', u'&': '', u'&quot;': '', u'À': 'A', u'Á': 'A', u'Â': 'A', u'Ã': 'A', u'Ä': 'Ae', u'&Auml;': 'A', u'Å': 'A', u'Ā': 'A', u'Ą': 'A', u'Ă': 'A', u'Æ': 'Ae', u'Ç': 'C', u'Ć': 'C', u'Č': 'C', u'Ĉ': 'C', u'Ċ': 'C', u'Ď': 'D', u'Đ': 'D', u'Ð': 'D', u'È': 'E', u'É': 'E', u'Ê': 'E', u'Ë': 'E', u'Ē': 'E', u'Ę': 'E', u'Ě': 'E', u'Ĕ': 'E', u'Ė': 'E', u'Ĝ': 'G', u'Ğ': 'G', u'Ġ': 'G', u'Ģ': 'G', u'Ĥ': 'H', u'Ħ': 'H', u'Ì': 'I', u'Í': 'I', u'Î': 'I', u'Ï': 'I', u'Ī': 'I', u'Ĩ': 'I', u'Ĭ': 'I', u'Į': 'I', u'İ': 'I', u'Ĳ': 'IJ', u'Ĵ': 'J', u'Ķ': 'K', u'Ł': 'K', u'Ľ': 'K', u'Ĺ': 'K', u'Ļ': 'K', u'Ŀ': 'K', u'Ñ': 'N', u'Ń': 'N', u'Ň': 'N', u'Ņ': 'N', u'Ŋ': 'N', u'Ò': 'O', u'Ó': 'O', u'Ô': 'O', u'Õ': 'O', u'Ö': 'Oe', u'&Ouml;': 'Oe', u'Ø': 'O', u'Ō': 'O', u'Ő': 'O', u'Ŏ': 'O', u'Œ': 'OE', u'Ŕ': 'R', u'Ř': 'R', u'Ŗ': 'R', u'Ś': 'S', u'Š': 'S', u'Ş': 'S', u'Ŝ': 'S', u'Ș': 'S', u'Ť': 'T', u'Ţ': 'T', u'Ŧ': 'T', u'Ț': 'T', u'Ù': 'U', u'Ú': 'U', u'Û': 'U', u'Ü': 'Ue', u'Ū': 'U', u'&Uuml;': 'Ue', u'Ů': 'U', u'Ű': 'U', u'Ŭ': 'U', u'Ũ': 'U', u'Ų': 'U', u'Ŵ': 'W', u'Ý': 'Y', u'Ŷ': 'Y', u'Ÿ': 'Y', u'Ź': 'Z', u'Ž': 'Z', u'Ż': 'Z', u'Þ': 'T', u'à': 'a', u'á': 'a', u'â': 'a', u'ã': 'a', u'ä': 'ae', u'&auml;': 'ae', u'å': 'a', u'ā': 'a', u'ą': 'a', u'ă': 'a', u'æ': 'ae', u'ç': 'c', u'ć': 'c', u'č': 'c', u'ĉ': 'c', u'ċ': 'c', u'ď': 'd', u'đ': 'd', u'ð': 'd', u'è': 'e', u'é': 'e', u'ê': 'e', u'ë': 'e', u'ē': 'e', u'ę': 'e', u'ě': 'e', u'ĕ': 'e', u'ė': 'e',
              u'ƒ': 'f', u'ĝ': 'g', u'ğ': 'g', u'ġ': 'g', u'ģ': 'g', u'ĥ': 'h', u'ħ': 'h', u'ì': 'i', u'í': 'i', u'î': 'i', u'ï': 'i', u'ī': 'i', u'ĩ': 'i', u'ĭ': 'i', u'į': 'i', u'ı': 'i', u'ĳ': 'ij', u'ĵ': 'j', u'ķ': 'k', u'ĸ': 'k', u'ł': 'l', u'ľ': 'l', u'ĺ': 'l', u'ļ': 'l', u'ŀ': 'l', u'ñ': 'n', u'ń': 'n', u'ň': 'n', u'ņ': 'n', u'ŉ': 'n', u'ŋ': 'n', u'ò': 'o', u'ó': 'o', u'ô': 'o', u'õ': 'o', u'ö': 'oe', u'&ouml;': 'oe', u'ø': 'o', u'ō': 'o', u'ő': 'o', u'ŏ': 'o', u'œ': 'oe', u'ŕ': 'r', u'ř': 'r', u'ŗ': 'r', u'š': 's', u'ù': 'u', u'ú': 'u', u'û': 'u', u'ü': 'ue', u'ū': 'u', u'&uuml;': 'ue', u'ů': 'u', u'ű': 'u', u'ŭ': 'u', u'ũ': 'u', u'ų': 'u', u'ŵ': 'w', u'ý': 'y', u'ÿ': 'y', u'ŷ': 'y', u'ž': 'z', u'ż': 'z', u'ź': 'z', u'þ': 't', u'ß': 'ss', u'ſ': 'ss', u'ый': 'iy', u'А': 'A', u'Б': 'B', u'В': 'V', u'Г': 'G', u'Д': 'D', u'Е': 'E', u'Ё': 'YO', u'Ж': 'ZH', u'З': 'Z', u'И': 'I', u'Й': 'Y', u'К': 'K', u'Л': 'L', u'М': 'M', u'Н': 'N', u'О': 'O', u'П': 'P', u'Р': 'R', u'С': 'S', u'Т': 'T', u'У': 'U', u'Ф': 'F', u'Х': 'H', u'Ц': 'C', u'Ч': 'CH', u'Ш': 'SH', u'Щ': 'SCH', u'Ъ': '', u'Ы': 'Y', u'Ь': '', u'Э': 'E', u'Ю': 'YU', u'Я': 'YA', u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g', u'д': 'd', u'е': 'e', u'ё': 'yo', u'ж': 'zh', u'з': 'z', u'и': 'i', u'й': 'y', u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n', u'о': 'o', u'п': 'p', u'р': 'r', u'с': 's', u'т': 't', u'у': 'u', u'ф': 'f', u'х': 'h', u'ц': 'c', u'ч': 'ch', u'ш': 'sh', u'щ': 'sch', u'ъ': '', u'ы': 'y', u'ь': '', u'э': 'e', u'ю': 'yu', u'я': 'ya'}

# Slugify a string

def slugify(string):
    string = translate(string.decode('utf-8'))
    string = string.lower()
    string = re.sub('(\s)', '-', string)
    string = re.sub('([^\w\s-])', '', string)
    string = re.sub('(-+)', '-', string)

    return string.strip()


def translate(string):
    result = ''
    for i, v in enumerate(string):
        try:
            result += charsTable[u'%s' % v]
        except:
            result += v

    return result
