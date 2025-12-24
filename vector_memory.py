import chromadb
from datetime import datetime

class VectorMemory:
    def __init__(self):
        self.client = chromadb.Client()
        try:
            self.collection = self.client.get_collection(name="customer_memory")
        except:
            self.collection = self.client.create_collection(name="customer_memory")
    
    def add_memory(self, user_id, message, response):
        """Ajouter une conversation en mémoire"""
        conversation_id = f"{user_id}_{datetime.now().timestamp()}"
        summary = f"User: {message}\nAssistant: {response}"
        
        self.collection.add(
            documents=[summary],
            metadatas=[{
                "user_id": user_id,
                "timestamp": str(datetime.now())
            }],
            ids=[conversation_id]
        )
        print(f"✅ Mémoire ajoutée pour {user_id}")
    
    def retrieve_memory(self, user_id, query, n_results=3):
        """Récupérer les conversations pertinentes"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where={"user_id": user_id}
            )
            return results['documents'][0] if results['documents'] else []
        except:
            return []


if __name__ == "__main__":
    memory = VectorMemory()
    memory.add_memory("user123", "Où est ma commande?", "Votre commande est en transit")
    print(memory.retrieve_memory("user123", "commande"))