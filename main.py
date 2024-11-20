from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def search_wikipedia(browser, query):
    """Переходит на страницу Википедии по запросу."""
    url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"
    browser.get(url)
    time.sleep(2)


def list_paragraphs(browser):
    """Листает параграфы текущей статьи."""
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    print("Параграфы статьи:")
    for i, paragraph in enumerate(paragraphs):
        if paragraph.text.strip():
            print(f"\nПараграф {i + 1}: {paragraph.text.strip()}")
            next_action = input("Нажмите Enter для следующего параграфа или введите 'q' для выхода: ")
            if next_action.lower() == "q":
                break


def choose_link(browser):
    """Выбирает и переходит на одну из связанных страниц."""
    links = browser.find_elements(By.TAG_NAME, "a")
    internal_links = [
        link for link in links if link.get_attribute("href") and "wikipedia.org" in link.get_attribute("href")
    ]

    if not internal_links:
        print("Связанные статьи не найдены.")
        return

    print("\nСвязанные статьи:")
    for i, link in enumerate(internal_links):
        print(f"{i+1}. {link.text} ({link.get_attribute('href')})")

    choice = input("\nВведите номер статьи для перехода (или 'q' для выхода): ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(internal_links):
            chosen_link = internal_links[index].get_attribute("href")
            print(f"Переход по ссылке: {chosen_link}")
            browser.get(chosen_link)
    except:
            print("Неверный номер. Выход в главное меню.")
    else:
        if choice.lower() == "q":
            print("Выход в главное меню.")


browser = webdriver.Firefox()
try:
    # Спрашиваем у пользователя запрос
    initial_query = input("Введите запрос для поиска на Википедии: ")
    search_wikipedia(browser, initial_query)

    while True:
        print("\nЧто вы хотите сделать?")
        print("1. Листать параграфы текущей статьи.")
        print("2. Перейти на одну из связанных страниц.")
        print("3. Выйти из программы.")
        choice = input("Введите номер действия: ")

        if choice == "1":
            list_paragraphs(browser)
        elif choice == "2":
            choose_link(browser)
        elif choice == "3":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")
finally:
    browser.quit()

