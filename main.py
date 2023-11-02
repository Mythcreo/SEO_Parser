from assistant import *
from playwright.sync_api import _generated # Исключительно для подсвечивания синтаксиса

PHRASES = ["нейросети", "youtube"]
DEPTH = 4

def login(page: _generated.Page):
    page.get_by_role("link", name = "Войти").click()
    page.get_by_label("логин").fill(email)
    page.get_by_text("пароль", exact = True).click()
    page.get_by_label("пароль").fill(password)
    page.locator(".b-domik__button >> .b-form-button__input[type=\"submit\"]").click()

def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless = False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://wordstat.yandex.ru/")
    
    login(page)
    console.print("[[bright_cyan]INFO[/]] Авторизация [bright_green]пройдена[/]")
    
    for phrase in PHRASES:
        # Ввод запроса
        console.print(f"[[bright_cyan]INFO[/]] Исследование [bright_cyan]{phrase}[/]")
        page.locator(".b-form-input__input").click()
        print(1)
        page.locator(".b-form-input__input").fill(phrase)
        print(2)
        page.get_by_role("button", name = "Подобрать Submit").get_by_role("button").click(delay = 100)
        print(3)
        
        # На этом этапе может появиться Yandex SmartCaptcha.
        #page.get_by_label("SmartCaptcha нужна проверка пользователя").click()
        
        res_table_phrases = pandas.DataFrame(columns = COLUMNS)
        res_table_similar = pandas.DataFrame(columns = COLUMNS)
        
        for p in range(DEPTH): # Страницы ответа Яндекса
            console.print(f"[[bright_cyan]INFO[/]] Страница [bright_yellow]{p}[/]")
            print(4)
            page.locator(".b-word-statistics__columns").wait_for()
            print(5)
            
            cu_tries, max_tries = 0, 3
            wait_time, pass_time, rep_time = 5, 0, 0.5
            # Ожидание загрузки актуального запроса и номера страницы
            while (f"«{phrase}»" not in page.inner_text(f"{div_phrases} {div_wrapper} {info_selector}")) and (f"{p + 1}" != page.inner_text(".b-pager__current")):
                if cu_tries == max_tries:
                    console.print("[bright_red]Актуальный запрос или номер страницы не загрузился[/]")
                    raise Exception("Актуальный запрос или номер страницы не загрузился")
                time.sleep(rep_time) 
                pass_time += rep_time
                if pass_time >= wait_time:
                    cu_tries += 1
                    console.print(f"[[bright_orange]DEBUG[/]] Перезагрузка страницы")
                    page.reload();
        
            both_tables_div = page.query_selector(".b-word-statistics__columns").inner_html()
            print(6)
            search_results = BeautifulSoup(both_tables_div, "lxml")
            
            # Запросы с данным словом
            table_phrases_code = search_results.select_one(f"{div_phrases} {div_wrapper} {table_selector}")
            table_phrases = pandas.read_html(StringIO(str(table_phrases_code)))[0]
            table_phrases.columns = COLUMNS
            table_phrases = table_phrases.iloc[1:]
            
            # Похожие запросы
            table_similar_code = search_results.select_one(f"{div_similar} {div_wrapper} {table_selector}")
            table_similar = pandas.read_html(StringIO(str(table_similar_code)))[0]
            table_similar.columns = COLUMNS
            table_similar = table_similar.iloc[1:]
            
            res_table_phrases = pandas.concat([res_table_phrases, table_phrases], ignore_index = True)
            res_table_phrases = res_table_phrases.drop_duplicates()
            res_table_similar = pandas.concat([res_table_similar, table_similar], ignore_index = True)
            res_table_similar = res_table_similar.drop_duplicates()
            
            if p != DEPTH - 1:
                try: page.get_by_role("link", name="далее").click(delay = 100)
                except:
                    logging.error(traceback.format_exc())
                    break
        
        save(res_table_phrases, f"{phrase}_phrases.xlsx")
        save(res_table_similar, f"{phrase}_similar.xlsx")
    
    context.close()
    browser.close()

def save(data: pandas.DataFrame, name):
    path = f"{os.path.dirname(sys.argv[0])}/Слова"
    if not os.path.exists(f'{path}'): os.makedirs(f'{path}')
    
    writer = pandas.ExcelWriter(f"{path}/{name}", engine = "xlsxwriter")
    sheet_name = "Результаты"
    
    data.index += 1
    data.to_excel(writer, sheet_name = sheet_name)
    ws = writer.sheets[sheet_name]
    
    ws.set_column("B:B", 45)
    ws.set_column("C:C", 15)
    writer.close()



try:
    # Получить данные аккаунта
    with open('account.txt', 'r') as file:
        email = file.readline().strip()
        password = file.readline().strip()
    
    # Начать работу
    try:
        with sync_playwright() as playwright:
            run(playwright)
    except Exception as exc:
        logging.error(traceback.format_exc())
        console.print(f"[bright_red]{repr(exc)}[/]")
        print(traceback.format_exc())
except Exception as exc:
    logging.debug(traceback.format_exc())
    console.print("[bright_yellow]Не обнаружен account.txt с почтой (1 строка) и паролем (2 строка)[/]")

os.system("pause")
