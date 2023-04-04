
def remove_character(string, index):
    s = list(string)
    del s[index]
    return "".join(s)


def find_in(char, string):
    for i in range(len(string)):
        if char == string[i]:
            return i
    return -1


def replace(string, char, int):
    string = remove_character(string, int)
    string = ''.join((string[:int], char, string[int:]))
    return string


ru = "йцукеёнгшщзхъфывапролджэячсмитьбюЙЦУКЕЁНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ1234567890"
en_ru = "qwert`yuiop[]asdfghjkl;'zxcvbnm,.QWERT~YUIOP{}ASDFGHJKL:\"ZXCVBNM<>!@#$%^&*()"
ukr = "іІїЇєЄґҐ"
en_ukr = "sS]}'\"uU"


def get_ready(string):
    length = int(len(string))
    counter = -1
    is_able_change = True
    i = 0
    while i < length:
        if 33 <= ord(string[i]) <= 126:

            if i > 0 and (33 <= ord(string[i - 1]) <= 126 or ord(string[i - 1]) in (1, 2, 3)):
                is_able_change &= False
            else:
                is_able_change |= True

            if counter == -1:
                counter = 0
            if counter == 0 or is_able_change:
                length += 1
                counter = -2
                string = ''.join((string[:i], chr(1), string[i:]))

        if (1040 <= ord(string[i]) <= 1070
                or 1072 <= ord(string[i]) <= 1103
                or ord(string[i]) in (1105, 1025)):

            if (i > 0 and (1040 <= ord(string[i - 1]) <= 1070
                           or 1072 <= ord(string[i - 1]) <= 1103
                           or ord(string[i - 1]) in (1, 2, 3, 1105, 1025))):
                is_able_change &= False
            else:
                is_able_change |= True

            if counter == -1:
                counter = 1
            if counter == 1 or is_able_change:
                length += 1
                counter = -2
                string = ''.join((string[:i], chr(2), string[i:]))

        if ord(string[i]) in (1110, 1030, 1111, 1031, 1108, 1028, 1169, 1168):

            if i > 0 and (ord(string[i - 1]) in (1, 2, 3, 1110, 1030, 1111, 1031, 1108, 1028, 1169, 1168)):
                is_able_change &= False
            else:
                is_able_change |= True

            if counter == -1:
                counter = 2
            if counter == 2 or is_able_change:
                length += 1
                counter = -2
                string = ''.join((string[:i], chr(3), string[i:]))

        i += 1

    length = int(len(string))
    mode = -1
    for i in range(length):
        if string[i] == chr(1):
            mode = 0

        if string[i] == chr(2):
            mode = 1

        if string[i] == chr(3):
            mode = 2

        if mode == 0:
            continue
        elif mode == 1:
            rus_ind = int(find_in(string[i], ru))
            if rus_ind == -1:
                continue
            string = replace(string, en_ru[rus_ind], i)
        elif mode == 2:
            ukr_ind = int(find_in(string[i], ukr))
            if ukr_ind == -1:
                continue
            string = replace(string, en_ukr[ukr_ind], i)
        else:
            continue

    return string


def fix(string):
    length = int(len(string))
    i = 0
    mode = -1
    while i < length:
        if string[i] == chr(1):
            string = remove_character(string, i)
            length -= 1
            i -= 1
            mode = 0

        if string[i] == chr(2):
            string = remove_character(string, i)
            length -= 1
            i -= 1
            mode = 1

        if string[i] == chr(3):
            string = remove_character(string, i)
            length -= 1
            i -= 1
            mode = 2

        if mode == 0:
            i += 1
            if i == length:
                break
            continue

        elif mode == 1:
            i += 1
            if i == length:
                break
            en_ind = int(find_in(string[i], en_ru))
            if en_ind == -1:
                continue
            string = replace(string, ru[en_ind], i)

        elif mode == 2:
            i += 1
            if i == length:
                break
            en_ind = int(find_in(string[i], en_ukr))
            if en_ind == -1:
                continue
            string = replace(string, ukr[en_ind], i)
        else:
            continue
    return string
