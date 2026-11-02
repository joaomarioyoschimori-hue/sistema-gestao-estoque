
class Product:
    def __init__(
        self,
        name,
        code,
        description,
        purchase_price,
        sale_price,
        quantity
    ):
        if not name.strip():
            raise ValueError("O nome do produto não pode ser vazio.")

        if not code.strip():
            raise ValueError("O código do produto não pode ser vazio.")

        if purchase_price < 0 or sale_price < 0:
            raise ValueError("Os preços não podem ser negativos.")

        if quantity < 0:
            raise ValueError("A quantidade não pode ser negativa.")

        self.name = name
        self.code = code
        self.description = description
        self.purchase_price = purchase_price
        self.sale_price = sale_price
        self.quantity = quantity

    def add_stock(self, amount):
        if amount <= 0:
            raise ValueError("A quantidade de entrada deve ser maior que zero.")

        self.quantity += amount

    def remove_stock(self, amount):
        if amount <= 0:
            raise ValueError("A quantidade de saída deve ser maior que zero.")

        if amount > self.quantity:
            raise ValueError("Estoque insuficiente.")

        self.quantity -= amount


        