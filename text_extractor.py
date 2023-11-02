from os import system; from requests import get; from bs4 import BeautifulSoup
from colorama import init, Fore; init(autoreset = True)

hs = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

print('-' * 100)
print('||| ' + Fore.LIGHTBLUE_EX + 'Page: ', end = '')
site = get(str(input()), headers = hs)
print('||| ' + Fore.LIGHTGREEN_EX + 'Designing (Структура страницы): ', end = '')
designing = bool(int(input()))
print('||| ' + Fore.LIGHTYELLOW_EX + 'Tedesigning (Структура текста): ', end = '')
tedesigning = bool(int(input()))
print('-' * 100)

# Страницы
page = BeautifulSoup(site.text, 'lxml')

# Функции
def leveling(textline):
    if designing: print(f'{"".join("  " for space in range(depth)) + textline}')

def televeling(textline, depth):
    print(f'{"".join("  " for space in range(depth)) + textline}', end = ' ')

def numefind(line):
    for eleline in line:
        verify = False
        for logo in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.'):
            if logo in eleline: verify = True; break
        if not verify: return 0
    return 1

def eternity(codechain, name, nule):
    global depth, syline, sytype, sytage;
    depth += 1; textnume = 0
    leveling('| ' + Fore.LIGHTBLUE_EX + str(depth) + Fore.RESET + ' Уровень - Начало (' + Fore.LIGHTYELLOW_EX + codechain.name + Fore.RESET + ') (' + Fore.LIGHTYELLOW_EX + str(len(codechain)) + Fore.RESET + ')')
    for code in codechain:
        if code.name: # Промежуточная функция
            if code.name != 'script' and code.name != 'style' and len(code):
                reternal = eternity(code, code.name, nule)
                textnume += reternal
        else: # Окончательная функция
            code = code.replace('\n', '').replace('\t', '')
            if code != '' and code != ' ' and code != '-' and code != '–' and code != '+':
                textnume += 1
                line = [s for s in code.split(' ') if s != '']
                sytype.append('nu') if numefind(line[0]) else sytype.append('le')
                syline.append(code); sytage.append(name); sydepth.append(depth)

                if nule == True and sytype[-1] == 'le':
                    leveling(': ' + Fore.LIGHTRED_EX + ' Найдено!')
                nule = True if len(codechain) == 2 and sytype[-1] == 'nu' else False

                leveling(': ' + Fore.LIGHTGREEN_EX + repr(code) + Fore.RESET + ' (' + Fore.LIGHTMAGENTA_EX + sytype[-1] + Fore.RESET + ')')
                
    leveling('| ' + Fore.LIGHTCYAN_EX + str(depth) + Fore.RESET + ' Завершение (' + Fore.LIGHTGREEN_EX + str(textnume) + Fore.RESET + ')')
    depth -= 1
    return textnume

# Выполняемая часть
syline, sytype, sytage, sydepth, depth = [], [], [], [], 0

eternity(page.body, 'body', False)

if tedesigning:
    print('-' * 100); high = 0
    for li, ty, ta, de in zip(syline, sytype, sytage, sydepth):
        deeper = True if de >= high else False
        televeling(' | ' + Fore.LIGHTBLUE_EX + str(de), de) if deeper else televeling(' | ' + Fore.LIGHTCYAN_EX + str(de), de)
        print(Fore.LIGHTYELLOW_EX + repr(li), '(' + Fore.LIGHTMAGENTA_EX + ty + Fore.RESET + ') (' + Fore.LIGHTGREEN_EX + ta + Fore.RESET + ')')
        high = de
    print(repr(' '.join(syline)))
    with open('res.txt', 'w', encoding = 'UTF-8') as file:
        file.write(' '.join(syline))
    print('-' * 100)

system('pause')
