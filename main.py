from scrapper_acoes import scrape_acoes
from scrapper_fiis import scrape_fiis
from scrapper_fiagro import scrape_fiagro

def main():
    print("============================================================")
    print("=================== ATIVOS SCRAPPER ========================")
    print("============================================================\n")
    print("Opções: ")
    print("[1] - Buscar Ações")
    print("[2] - Buscar FIIs")
    print("[3] - Buscar FIAGRO")
    print("[4] - Atualizar tudo")
    print("[X] - Sair")

    opcao = input("Escolha uma opção: ").strip()

    match opcao:
        case '1':
            scrape_acoes()
        case '2':
            scrape_fiis()
        case '3':
            scrape_fiagro()
        case '4':
            scrape_acoes()
            scrape_fiis()
            scrape_fiagro()
        case "x" | "X":
            print("Saindo...")
            exit
        case _:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
