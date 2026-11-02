from fastapi import FastAPI, HTTPException
from app.database.product_repository import get_all_products
from app.product_schema import ProductCreate
from app.models.product import Product
from app.database.product_repository import insert_product, get_product_by_code
from app.stock_schema import StockMovementCreate
from app.database.product_repository import register_stock_movement

app = FastAPI(
    title="Sistema de Gestão de Estoque",
    description="API para gerenciamento de produtos e movimentações de estoque.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "mensagem": "API de Gestão de Estoque está funcionando!",
        "status": "online"
    }


@app.get("/produtos")
def listar_produtos():
    produtos = get_all_products()

    return [dict(produto) for produto in produtos]

@app.get("/produtos/{codigo}")
def buscar_produto(codigo: str):

    produto = get_product_by_code(codigo)

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    return dict(produto)

@app.post("/produtos/{codigo}/movimentacoes")
def movimentar_estoque(codigo: str, movimentacao: StockMovementCreate):

    produto = get_product_by_code(codigo)

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    if movimentacao.movement_type not in ["entrada", "saida"]:
        raise HTTPException(
            status_code=400,
            detail="Tipo de movimentação inválido. Use 'entrada' ou 'saida'."
        )

    if movimentacao.movement_type == "entrada":
        nova_quantidade = produto["quantity"] + movimentacao.quantity
    else:
        nova_quantidade = produto["quantity"] - movimentacao.quantity

        if nova_quantidade < 0:
            raise HTTPException(
                status_code=400,
                detail="Estoque insuficiente."
            )

    register_stock_movement(
        code=codigo,
        new_quantity=nova_quantidade,
        movement_type=movimentacao.movement_type,
        amount=movimentacao.quantity
    )

    return {
        "mensagem": "Movimentação registrada com sucesso!",
        "produto": codigo,
        "tipo": movimentacao.movement_type,
        "quantidade_movimentada": movimentacao.quantity,
        "estoque_atualizado": nova_quantidade
    }

@app.post("/produtos", status_code=201)
def cadastrar_produto(produto: ProductCreate):

    if get_product_by_code(produto.code):
     raise HTTPException(
        status_code=409,
        detail="Já existe um produto com esse código."
    )

    novo_produto = Product(
        name=produto.name,
        code=produto.code,
        description=produto.description,
        purchase_price=produto.purchase_price,
        sale_price=produto.sale_price,
        quantity=produto.quantity
    )

    insert_product(novo_produto)

    return {
        "mensagem": "Produto cadastrado com sucesso!",
        "produto": produto.model_dump()
    }