from app.models.retriever import RetrieverModel


class RetrieverService:
    def __init__(self):
        self.retriever = RetrieverModel()

    def retrieve(self, query: str, user_id: str):
        return self.retriever.retrieve(query, user_id)

    def retrieve_with_history(self, query: str, history: list, user_id: str):
        return self.retriever.retrieve_with_history(query, history, user_id)
