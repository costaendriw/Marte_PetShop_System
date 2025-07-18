from system import PetShopSystem # Importa a classe PetShopSystem

def menu_principal():
    """Menu interativo do sistema Pet Shop."""
    sistema = PetShopSystem()
    
    while True:
        print(f"\n🐕 SISTEMA MARTE PETSHOP 🐱 ")
        print(f"{'='*35}")
        print("1. Cadastrar ração")
        print("2. Listar rações")
        print("3. Buscar ração por ID")
        print("4. Atualizar ração")
        print("5. Deletar ração")
        print("6. Estatísticas")
        print("7. Fazer backup")
        print("8. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n📝 CADASTRAR NOVA RAÇÃO")
            nome = input("Nome da ração: ").strip()
            tipo_animal = input("Tipo de animal (gato/cão): ").strip()
            marca = input("Marca: ").strip()
            
            try:
                peso = float(input("Peso (kg): "))
                preco = float(input("Preço (R$): "))
                
                estoque_input = input("Estoque inicial (0 se não informado): ").strip()
                estoque = int(estoque_input) if estoque_input else 0
                
                sistema.cadastrar_racao(nome, tipo_animal, marca, peso, preco, estoque)
            except ValueError:
                print("❌ Valores numéricos inválidos para peso, preço ou estoque! Tente novamente.")
        
        elif opcao == "2":
            filtro = input("\nFiltrar por animal (gato/cão/enter para todos): ").strip()
            sistema.listar_racoes(filtro if filtro else None)
        
        elif opcao == "3":
            try:
                id_produto = int(input("\nID da ração: "))
                racao = sistema.buscar_racao(id_produto)
                
                if racao:
                    print(f"\n📦 DETALHES DA RAÇÃO")
                    print(f"ID: {racao['id']}")
                    print(f"Nome: {racao['nome']}")
                    print(f"Tipo: {racao['tipo_animal']}")
                    print(f"Marca: {racao['marca']}")
                    print(f"Peso: {racao['peso']}kg")
                    print(f"Preço: R$ {racao['preco']:.2f}")
                    print(f"Estoque: {racao['estoque']}")
                    print(f"Cadastrado em: {racao['data_cadastro']}")
                else:
                    print("❌ Ração não encontrada!")
            except ValueError:
                print("❌ ID deve ser um número inteiro! Tente novamente.")
        
        elif opcao == "4":
            try:
                id_produto = int(input("\nID da ração a atualizar: "))
                
                # Buscar a ração para verificar se existe e imprimir mensagem se não
                if not sistema.buscar_racao(id_produto): 
                    continue # Já imprime a mensagem de erro dentro de buscar_racao
                
                print("Deixe em branco para manter o valor atual:")
                kwargs = {}
                
                nome = input("Novo nome: ").strip()
                if nome: kwargs["nome"] = nome
                
                tipo_animal = input("Novo tipo (gato/cão): ").strip()
                if tipo_animal: kwargs["tipo_animal"] = tipo_animal
                
                marca = input("Nova marca: ").strip()
                if marca: kwargs["marca"] = marca
                
                peso_str = input("Novo peso (kg): ").strip()
                if peso_str: 
                    try: kwargs["peso"] = float(peso_str)
                    except ValueError: 
                        print("❌ Peso inválido, este campo será ignorado na atualização.")
                        # Não continua, para permitir que outros campos válidos sejam atualizados
                
                preco_str = input("Novo preço (R$): ").strip()
                if preco_str: 
                    try: kwargs["preco"] = float(preco_str)
                    except ValueError: 
                        print("❌ Preço inválido, este campo será ignorado na atualização.")
                
                estoque_str = input("Novo estoque: ").strip()
                if estoque_str: 
                    try: kwargs["estoque"] = int(estoque_str)
                    except ValueError: 
                        print("❌ Estoque inválido, este campo será ignorado na atualização.")
                
                if kwargs:
                    sistema.atualizar_racao(id_produto, **kwargs)
                else:
                    print("❌ Nenhum campo foi alterado!")
                            
            except ValueError:
                print("❌ ID inválido. Por favor, insira um número inteiro.")
        
        elif opcao == "5":
            try:
                id_produto = int(input("\nID da ração a deletar: "))
                sistema.deletar_racao(id_produto)
            except ValueError:
                print("❌ ID deve ser um número inteiro! Tente novamente.")
        
        elif opcao == "6":
            sistema.estatisticas()
        
        elif opcao == "7":
            nome_backup = input("\nNome do arquivo de backup (ou enter para automático): ").strip()
            sistema.backup_database(nome_backup if nome_backup else None)
        
        elif opcao == "8":
            print("👋 Obrigado por usar o Sistema Pet Shop!")
            break
        
        else:
            print("❌ Opção inválida! Tente novamente.")


if __name__ == "__main__":
    menu_principal()