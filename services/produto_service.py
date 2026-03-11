def verificar_existencia(self, nome: str, nome_categoria: str) -> bool:
        """Método para verificar se o produto já está cadastrado, comparando nome e categoria."""
        return self.nome == nome and self.nome_categoria == nome_categoria