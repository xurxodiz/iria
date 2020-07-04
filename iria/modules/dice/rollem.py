# LICENSE AND COPYRIGHT NOTICE
#
# Most of the code in this module has been taken
# from rollem-telegram-bot, available online at
# https://github.com/treetrnk/rollem-telegram-bot
#
# That code is protected under a GNU LGPL v3
# You can consult all details about its license at
# https://www.gnu.org/licenses/lgpl-3.0.html


import re
import random


ladder = {
    8  : 'Legendary',
    7  : 'Epic',
    6  : 'Fantastic',
    5  : 'Superb',
    4  : 'Great',
    3  : 'Good',
    2  : 'Fair',
    1  : 'Average',
    0  : 'Mediocre',
    -1 : 'Poor',
    -2 : 'Terrible',
    -3 : 'Catastrophic',
    -4 : 'Horrifying'
}

ladder_rev = {
    'legendary'    : 8,
    'epic'         : 7,
    'fantastic'    : 6,
    'superb'       : 5,
    'great'        : 4,
    'good'         : 3,
    'fair'         : 2,
    'average'      : 1,
    'mediocre'     : 0,
    'poor'         : -1,
    'terrible'     : -2,
    'catastrophic' : -3,
    'horrifying'   : -4
}

fate_options = {
    -1 : '[-]',
    0  : '[  ]',
    1  : '[+]'
}


class InvalidFormatEquationException(Exception):
    pass


def get_ladder(result):
    if result > 8:
        return 'Beyond Legendary'
    elif result < -2:
        return 'Terrible'
    else:
        return ladder[result]


def ladder_to_num(adjective):
    adjective_lower = adjective.lower()
    if adjective_lower in ladder_rev:
        return ladder_rev[adjective_lower]
    else:
        return None


def roll(equation):
    equation_list = re.findall(r'(\w+!?>?\d*)([+*/()-]?)', equation)
    is_fate = False
    use_ladder = False
    result = {
        'visual': [],
        'equation': [],
        'total': ''
    }

    try:
        for pair in equation_list:
            for item in pair:
                if item and len(item) > 1 and 'd' in item:
                    dice = re.search(r'(\d*)d([0-9fF]+)(!)?', item)
                    dice_num = int(dice.group(1)) if dice.group(1) else 1
                    if dice_num > 1000:
                        raise Exception('Maximum number of rollable dice is 1000')
                    sides = dice.group(2)
                    space = ' '
                    result['visual'].append(space + '(')
                    result['equation'].append('(')
                    fate_dice = ''
                    current_die_results = ''
                    plus = ''
                    explode = True if dice.group(3) == '!' and int(dice.group(2)) > 1 else False

                    while dice_num > 0:
                        if sides in ['f', 'F']:
                            is_fate = True
                            use_ladder = True
                            current_fate_die = random.choice(list(fate_options.keys()))
                            current_die_results += plus + str(current_fate_die)
                            fate_dice += fate_options[current_fate_die] + ' '
                            last_roll = False
                        else:
                            sides = int(sides)
                            last_roll = random.randint(1, int(dice.group(2)))
                            current_die_results += plus + str(last_roll)
                        if not (explode and last_roll == sides):
                            dice_num -= 1
                        if len(plus) == 0:  # Adds all results to result unless it is the first one
                            plus = ' + '
                    if is_fate:
                        is_fate = False
                        result['visual'].append(' ' + fate_dice)
                    else:
                        result['visual'].append(current_die_results)
                    result['equation'].append(current_die_results)
                    result['visual'].append(')')
                    result['equation'].append(')')
                else:
                    if item and (item in ['+', '-', '/', '*', ')', '('] or int(item)):
                        result['visual'].append(' ')
                        result['visual'].append(item)
                        result['equation'].append(item)

        result['total'] = str(''.join(result['equation'])).replace(" ", "")
        if bool(re.match('^[0-9+*/ ()-]+$', result['total'])):
            result['total'] = eval(result['total'])
        else:
            raise InvalidFormatEquationException

        if use_ladder:
            # Set if final result is positive or negative
            sign = '+' if result['total'] > -1 else ''
            ladder_result = get_ladder(result['total'])
            result['total'] = sign + str(result['total']) + ' ' + ladder_result

        # Only show part of visual equation if bigger than 300 characters
        result['visual'] = ''.join(result['visual'])
        if len(result['visual']) > 275:
            result['visual'] = result['visual'][0:275] + ' . . . )'

        return result

    except Exception:
        raise InvalidFormatEquationException
