# 🐾 Sistema de Gerenciamento de Ração para Pet Shop

Um sistema simples de linha de comando (CLI) para gerenciar o estoque de rações de gatos e cães em um pet shop. Este projeto foi desenvolvido como parte de um estudo inicial em Python, focando em boas práticas de programação, interação com banco de dados SQLite e organização de código.

---

## 🌟 Funcionalidades Principais

* **Cadastro de Rações:** Adicione novas rações com detalhes como nome, tipo de animal (cão/gato), marca, peso, preço e estoque.
* **Listagem de Rações:** Visualize todas as rações cadastradas ou filtre por tipo de animal.
* **Busca por ID:** Encontre detalhes específicos de uma ração usando seu ID.
* **Atualização de Dados:** Modifique informações de rações existentes.
* **Exclusão de Rações:** Remova rações do sistema.
* **Estatísticas do Estoque:** Obtenha insights sobre o inventário, incluindo total de rações, quantidades por tipo de animal, valor total do estoque e produtos com baixo/zero estoque.
* **Backup do Banco de Dados:** Crie cópias de segurança do banco de dados em um arquivo separado.
* **Dados de Teste Automáticos:** O sistema insere um conjunto de dados de exemplo ao ser iniciado pela primeira vez, facilitando o teste.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3:** Linguagem de programação principal.
* **SQLite3:** Banco de dados relacional leve para armazenamento local de dados.

---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para colocar o sistema em funcionamento no seu ambiente:

1.  **Clone o Repositório**:
    ```bash
    git clone [https://github.com/costaendriw/Marte_PetShop_System.git]
    cd Marte_PetShop_System
    ```

2.  **Estrutura de Arquivos**:
    Certifique-se de que seus arquivos estão organizados da seguinte forma na pasta raiz do projeto:
    ```
    Marte_PetShop_System/
    ├── database.py
    ├── system.py
    └── main.py
    ```

3.  **Execute o Programa**:
    Abra o terminal ou prompt de comando na pasta raiz do projeto (`Marte_PetShop_System/`) e execute o seguinte comando:
    ```bash
    python main.py
    ```

    O sistema iniciará e apresentará o menu principal na linha de comando.

---

## 💡 Estrutura do Código e Boas Práticas

Este projeto foi estruturado com foco em **Orientação a Objetos (POO)** e **boas práticas de código**, incluindo:

* **Modularização:** O código é dividido em três módulos principais para melhor organização e separação de responsabilidades:
    * `database.py`: Lida exclusivamente com a interação de baixo nível com o banco de dados (conexão, queries SQL).
    * `system.py`: Contém a lógica de negócio principal do pet shop, utilizando os serviços do `database.py`.
    * `main.py`: Atua como o ponto de entrada da aplicação, gerenciando o menu de interação com o usuário.
* **Encapsulamento:** As classes encapsulam seus dados e comportamentos.
* **Tratamento de Exceções:** Uso extensivo de blocos `try-except` para lidar com erros de banco de dados e entrada do usuário de forma robusta.
* **Context Managers (`with`):** Utilização de `with` statements para gerenciar automaticamente recursos (como conexões de banco de dados), garantindo que sejam fechados corretamente.
* **Tipagem (Type Hints):** Inclusão de *type hints* para melhorar a legibilidade e a manutenção do código.
* **Princípio DRY (Don't Repeat Yourself):** Reuso de código através de funções auxiliares para validações e normalização de dados.
* **Constantes:** Definição de constantes para valores repetidos (ex: tipos de animais) para facilitar a manutenção.

---

## 🧑‍💻 Autor

* **Endriw Costa**
* [Meu GitHub](https://github.com/costaendriw)

---