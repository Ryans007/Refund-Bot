from graph.graph import graph

if __name__ == "__main__":
    thread = {"configurable": {"thread_id": "1"}}

    print("Chatbot de Reembolso iniciado! Digite 'sair' para encerrar a conversa!\n")

    while True:
      user_input = input("Você: ").strip()

      if user_input.strip().lower() == 'sair':
        print("Encerrando chatbot...")
        break
      if not user_input:
        print("Por favor, digite uma mensagem válida.\n")
        continue

      print("\nProcessando...\n")

      for s in graph.stream({'user_message': user_input}, thread):
        print(s)

      # result = graph.invoke({'user_message': user_input}, thread)
      # print(result)

      print("\n" + "-" * 50 + "\n")

