from app.models.product import Product
from app.models.product import Product


products = []


def register_product():
    print("\n=== CADASTRO DE PRODUTO ===")

    try:
        name = input("Nome do produto: ")
        code = input("Código do produto: ")

        # Verifica se o código já existe
        for product in products:
            if product.code == code:
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

        products.append(product)

        print("\nProduto cadastrado com sucesso!")

    except ValueError as error:
        print(f"\nErro no cadastro: {error}")


def list_products():
    print("\n=== PRODUTOS CADASTRADOS ===")

    if not products:
        print("Nenhum produto cadastrado.")
        return

    for product in products:
        print("----------------------------")
        print(f"Nome: {product.name}")
        print(f"Código: {product.code}")
        print(f"Preço de venda: R$ {product.sale_price:.2f}")
        print(f"Estoque: {product.quantity}")


def main():
    while True:
        print("\n================================")
        print("     SISTEMA DE GESTÃO DE ESTOQUE")
        print("================================")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("0 - Sair")

        option = input("\nEscolha uma opção: ")

        if option == "1":
            register_product()      

        elif option == "2":
            list_products()

        elif option == "0":
            print("\nEncerrando o sistema...")
            break

        else:
            print("\nOpção inválida!")


if __name__ == "__main__":
    main()
    