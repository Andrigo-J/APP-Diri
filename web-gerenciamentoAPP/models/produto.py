class Produto:
    def __init__(self, data):
        self.id = str(data.get('_id'))
        self.nome = data.get('nome')
        self.estoque = data.get('estoque', 0)
        self.preco_custo = data.get('preco_custo', 0.0)
        self.preco_venda = data.get('preco_venda', 0.0)
        self.imagem = data.get('imagem')
