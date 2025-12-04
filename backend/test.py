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

      # for chunk in graph.stream({'user_message': user_input}, thread, stream_mode="updates"):
      #   print(chunk)
      result = graph.invoke({'user_message': user_input}, thread)
      final_answer = result.get('final_answer')
      print(f"Resposta: {final_answer}")

      print("\n" + "-" * 50 + "\n")

