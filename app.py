import streamlit as st
import requests
from vector_memory import VectorMemory
import json


st.set_page_config(page_title="AI Customer Support", page_icon="🤖")

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = "user_" + str(hash("default_user"))

memory = VectorMemory()


st.title("🤖 Support Client IA")
st.markdown("Posez vos questions sur vos commandes, remboursements ou produits")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if user_input := st.chat_input("Comment puis-je vous aider ?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    
    past_conversations = memory.retrieve_memory(st.session_state.user_id, user_input)
    context = "\n".join(past_conversations) if past_conversations else "Aucun historique"
    
    
    with st.chat_message("assistant"):
        with st.spinner("Traitement..."):
            try:
                
                webhook_url = "http://localhost:5678/webhook-test/customer"
                
                response = requests.post(
                    webhook_url,
                    json={
                        "message": user_input,
                        "user_id": st.session_state.user_id,
                        "context": context
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    bot_response = result.get("reply", "Désolé, erreur de traitement")
                    
                    st.markdown(bot_response)
                    st.session_state.messages.append({"role": "assistant", "content": bot_response})
                    
                    
                    memory.add_memory(st.session_state.user_id, user_input, bot_response)
                else:
                    st.error(f"Erreur: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Impossible de se connecter à n8n. Vérifiez que le webhook est actif.")
            except Exception as e:
                st.error(f"Erreur: {str(e)}")


with st.sidebar:
    st.header("ℹ️ Informations")
    st.write(f"**User ID:** {st.session_state.user_id}")
    st.write(f"**Messages:** {len(st.session_state.messages)}")
    
    if st.button("🗑️ Effacer l'historique"):
        st.session_state.messages = []
        st.rerun()