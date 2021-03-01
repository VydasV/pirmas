def add_aboutus_text_from_file() -> str:
    """grąžina iš failo apie_mus.txt tekstą puslapiui apie,
       arba string tipo kintamąjį text, jei tokio failo nėra
       """
    
    try:
        with open('..\\static\\apie_mus.txt', 'r', encoding='utf-8') as file:
            text = ' '.join(file.readlines())
    except FileNotFoundError:
        text = 'slapta "Kardo ir žagrės" sąjunga - mūsų rankos ilgos!!!'
    return text


if __name__ == "__main__":
    a = add_aboutus_text_from_file()
    print(a)
