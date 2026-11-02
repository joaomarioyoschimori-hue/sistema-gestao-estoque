import sqlite3
from app.models.product import Product
from app.models.product import Product
from app.database.init_db import create_tables
from app.database.product_repository import (
    insert_product,
    get_all_products
)
from app.database.product_repository import (
    get_product_by_code,
    update_product_stock,
    insert_stock_movement,
    get_stock_movements,
    get_stock_report,
    get_low_stock_products,
    register_stock_movement
)


products = []



def register_product():
    print("\n=== CADASTRO DE PRODUTO ===")

    try:
        name = input("Nome do produto: ")
        code = input("Código do produto: ")

        # Verifica se o código já existe no banco de dados
        if get_product_by_code(code):
            print("\nErro: já existe um produto com esse código!")
            return

        description = input("Descrição: ")

        purchase_price = float(input("Preço de compra: R$ "))
        sale_price = float(input("Preço de venda: R$ "))
        quantity = int(input("Quantidade em estoque: "))

        product = Product(
            name=name,
            code=code,
            description=description,
            purchase_price=purchase_price,
            sale_price=sale_price,
            quantity=quantity
        )

        insert_product(product)

        print("\nProduto cadastrado com sucesso!")

    except ValueError as error:
        print(f"\nErro no cadastro: {error}")

    except sqlite3.IntegrityError:
        print("\nErro: já existe um produto com esse código.")



def list_products():
    print("\n=== PRODUTOS CADASTRADOS ===")

    products = get_all_products()

    if not products:
        print("Nenhum produto cadastrado.")
        return

    for product in products:
        print("----------------------------")
        print(f"Nome: {product['name']}")
        print(f"Código: {product['code']}")
        print(f"Preço de venda: R$ {product['sale_price']:.2f}")
        print(f"Estoque: {product['quantity']}")


def main():
    create_tables()
    while True:
        print("\n================================")
        print("     SISTEMA DE GESTÃO DE ESTOQUE")
        print("================================")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Movimentar estoque")
        print("4 - Consultar histórico de movimentações")
        print("5 - Relatório gerencial de estoque")
        print("0 - Sair")

        option = input("\nEscolha uma opção: ")

        if option == "1":
            register_product()      

        elif option == "2":
            list_products()

        elif option == "3":
            stock_movement()        

        elif option == "4":
            show_stock_history() 

        elif option == "5":
            show_stock_report()  

        elif option == "0":
            print("\nEncerrando o sistema...")
            break

        else:
            print("\nOpção inválida!")

def stock_movement():
    code = input("\nDigite o código do produto: ")

    product = get_product_by_code(code)

    if product is None:
        print("Produto não encontrado.")
        return

    print(f"\nProduto: {product['name']}")
    print(f"Estoque atual: {product['quantity']}")

    print("\n1 - Entrada de estoque")
    print("2 - Saída de estoque")

    option = input("Escolha uma operação: ")

    try:
        amount = int(input("Quantidade: "))

        if amount <= 0:
            print("A quantidade deve ser maior que zero.")
            return

        if option == "1":
            new_quantity = product["quantity"] + amount

        elif option == "2":
            if amount > product["quantity"]:
                print("Estoque insuficiente.")
                return

            new_quantity = product["quantity"] - amount

        else:
            print("Operação inválida.")
            return

        update_product_stock(code, new_quantity)

        if option == "1":
         movement_type = "ENTRADA"
        else:
         movement_type = "SAIDA"

        register_stock_movement(code, new_quantity, movement_type, amount)

        print("Movimentação registrada com sucesso!")
        print(f"Estoque atualizado: {new_quantity}")

    except ValueError:
        print("Informe uma quantidade inteira válida.")

def show_stock_history():
    code = input("\nDigite o código do produto: ")

    product = get_product_by_code(code)

    if product is None:
        print("Produto não encontrado.")
        return

    movements = get_stock_movements(code)

    print(f"\n=== HISTÓRICO: {product['name']} ===")

    if not movements:
        print("Nenhuma movimentação registrada.")
        return

    for movement in movements:
        print("----------------------------")
        print(f"Operação: {movement['movement_type']}")
        print(f"Quantidade: {movement['quantity']}")
        print(f"Data: {movement['created_at']}")

def show_stock_report():
    report = get_stock_report()
    low_stock_products = get_low_stock_products()

    print("\n=== RELATÓRIO GERENCIAL DE ESTOQUE ===")
    print(f"Produtos cadastrados: {report['total_products']}")
    print(f"Unidades em estoque: {report['total_units']}")
    print(f"Valor investido: R$ {report['total_invested']:.2f}")
    print(f"Valor potencial de venda: R$ {report['potential_revenue']:.2f}")

    profit = report["potential_revenue"] - report["total_invested"]

    print(f"Lucro bruto potencial: R$ {profit:.2f}")

    print("\n=== PRODUTOS COM ESTOQUE BAIXO ===")

    if not low_stock_products:
        print("Nenhum produto com estoque baixo.")
        return

    for product in low_stock_products:
        print("----------------------------")
        print(f"Produto: {product['name']}")
        print(f"Código: {product['code']}")
        print(f"Quantidade disponível: {product['quantity']}")

if __name__ == "__main__":
    
    main()
    