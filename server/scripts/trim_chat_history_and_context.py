from crud import chat_crud

if __name__ == '__main__':
    chat_crud.llm_context = chat_crud.llm_context[:2]  # Leave only the first course added
    chat_crud.write_llm_context_to_file()
    chat_crud.chat_history = []
    chat_crud.write_chat_history_to_file()
