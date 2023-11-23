import ast
import logging
import shutil
import argparse

def print_and_log(*string):
    string = string[0] if string else ""
    logging.info(string)
    print(string)


def input_and_log(*string):
    string = string[0] if string else ""
    logging.info(string)
    message = input(string)
    logging.info(message)
    return message


def duplicated_field(_deck, _field, _input):
    for _card in _deck:
        if _card[_field] == _input:
            return _card
    return False


def add_card(_deck):
    _deck = list(_deck)
    _card = {}
    _card.setdefault("mistakes", 0)
    print_and_log(f"The card:")
    while True:
        _card["term"] = input_and_log()
        if duplicated_field(_deck, "term", _card["term"]) is False:
            break
        else:
            print_and_log(f'The term "{_card["term"]}" already exists. Try again:')
    print_and_log(f"The definition of the card:")
    while True:
        _card["definition"] = input_and_log()
        if duplicated_field(_deck, "definition", _card["definition"]) is False:
            break
        else:
            print_and_log(f'The definition "{_card["definition"]}" already exists. Try again:')
    _deck.append(_card)
    print_and_log(f'The pair ("{_card["term"]}":"{_card["definition"]}") has been added')
    return _deck


def ask(_deck):
    total_questions = int(input_and_log("How many times to ask?"))
    question_number = 0
    while True:
        if question_number == total_questions:
            break
        for card in _deck:
            question_number += 1
            answer = input_and_log(f'Print the definition of "{card["term"]}"\n')
            if answer == card["definition"]:
                print_and_log("Correct!")
            else:
                duplicated_card = duplicated_field(_deck, "definition", answer)
                if duplicated_card:
                    print_and_log(f'Wrong. The right answer is "{card["definition"]}", '
                          f'but your definition is correct for "{duplicated_card["term"]}".')
                else:
                    print_and_log(f'Wrong. The right answer is "{card["definition"]}".')
                    card["mistakes"] += 1
            if question_number == total_questions:
                break
    return _deck


def remove(_deck):
    _deck = list(_deck)
    removing_card = input_and_log("Which card?")
    for card in _deck:
        if removing_card == card["term"]:
            _deck.remove(card)
            print_and_log("The card has been removed.")
            return _deck
        print_and_log(f'Can\'t remove "{removing_card}": there is no such card.')
        return _deck


def export(_deck, file_name=None):
    if not file_name:
        file_name = input_and_log("File name:")
    n = 0
    with open(file_name, "w") as file:
        for card in _deck:
            n += 1
            print(card, end="\n", file=file)
    print_and_log(f"{n} cards have been saved.")
    return _deck


def _exit(_deck, file_name=None):
    print("file_path", file_name)
    if not file_name:
        print_and_log("Bye bye!")
    else:
        export(_deck, file_name)
    exit()


def _import(_deck, file_name=None):
    if not file_name:
        file_name = input_and_log("File name:")
    n = 0
    try:
        with open(file_name, "r") as file:
            for line in file:
                if line.strip():
                    n += 1
                    card = ast.literal_eval(line)
                    card.setdefault("mistakes", 0)
                    duplicated = duplicated_field(_deck, "term", card["term"])
                    if duplicated:
                        # n -= 1
                        _deck.remove(duplicated)
                    _deck.append(card)
            print_and_log(f"{n} cards have been loaded.")
        return _deck
    except Exception as e:
        print_and_log(e)
        print_and_log("File not found.")
    return _deck


def log(_deck):
    file_name = input_and_log("File name:")
    temp_log = 'temp_log.txt'
    shutil.copy(temp_log, file_name)
    print_and_log("The log has been saved.")
    pass


def hardest_card(_deck):
    if _deck:
        max_mistakes = max(card["mistakes"] for card in _deck)
        max_list = [card for card in _deck if card["mistakes"] == max_mistakes]
        if len(max_list) == 1:
            print_and_log(f'The hardest card is "{max_list[0]["term"]}". You have {max_mistakes} errors answering it')
        elif len(max_list) > 1:
            string = ""
            for e in max_list:
                string += f'"{e["term"]}", '
            print_and_log(f"The hardest cards are {string[:-2]}.")
        else:
            print_and_log("There are no cards with errors.")
    else:
        print_and_log("There are no cards with errors.")
    return _deck


def reset_stats(_deck):
    for card in _deck:
        card["mistakes"] = 0
    print_and_log("Card statistics have been reset.")


def get_args_from_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--import_from", type=str, help="parse importing file path")
    parser.add_argument("--export_to", type=str, help="parse exporting path")
    args = parser.parse_args()
    _import_file_path = args.import_from
    _export_file_path = args.export_to
    return _import_file_path, _export_file_path


def menu(_deck):
    import_file_path, export_file_path = get_args_from_parse()
    if import_file_path:
        _import(_deck, import_file_path)
    logging.basicConfig(filename="temp_log.txt", filemode="w", format="%(message)s", level="INFO")
    menu_dict = {"add": add_card, "remove": remove, "import": _import, "export": export, "ask": ask, "exit": _exit,
                 "log": log, "hardest card": hardest_card, "reset stats": reset_stats}
    while True:
        choice = input_and_log("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        if choice == "exit":
            menu_dict[choice](_deck, export_file_path)
        else:
            _deck = menu_dict[choice](_deck)


deck = []
menu(deck)
