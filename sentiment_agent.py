import requests
import json

def analyze_sentiment(message: str) -> dict:
    """
    Analyse le sentiment d'un message client
    Retourne: positive, negative, ou neutral
    """
    prompt = f"""
Analyse le sentiment de ce message client.
Réponds uniquement par un seul mot: positive, negative, ou neutral

Message: {message}

Sentiment:"""
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        
        # Vérifier le statut de la réponse
        if response.status_code != 200:
            print(f"❌ Erreur HTTP {response.status_code}: {response.text}")
            return {"sentiment": "neutral", "confidence": 0.5}
        
        result = response.json()
        
        # Debug : Afficher la réponse complète
        print(f"🔍 Réponse Ollama complète: {json.dumps(result, indent=2)}")
        
        # Extraire le texte de la réponse
        sentiment_text = result.get("response", "").strip().lower()
        
        if not sentiment_text:
            print("⚠️ Réponse vide de Ollama")
            return {"sentiment": "neutral", "confidence": 0.5}
        
        print(f"📝 Texte analysé: '{sentiment_text}'")
        
        # Analyser le sentiment
        if "positiv" in sentiment_text:
            return {"sentiment": "positive", "confidence": 0.9}
        elif "negativ" in sentiment_text or "négatif" in sentiment_text:
            return {"sentiment": "negative", "confidence": 0.9}
        else:
            return {"sentiment": "neutral", "confidence": 0.7}
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à Ollama. Vérifiez qu'Ollama est démarré:")
        print("   → Commande: ollama serve")
        return {"sentiment": "neutral", "confidence": 0.5}
    
    except requests.exceptions.Timeout:
        print("⏱️ Timeout de la requête Ollama")
        return {"sentiment": "neutral", "confidence": 0.5}
    
    except KeyError as e:
        print(f"❌ Clé manquante dans la réponse Ollama: {e}")
        print(f"   Réponse reçue: {result}")
        return {"sentiment": "neutral", "confidence": 0.5}
    
    except Exception as e:
        print(f"❌ Erreur inattendue: {type(e).__name__}: {e}")
        return {"sentiment": "neutral", "confidence": 0.5}


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TEST DE L'ANALYSE DE SENTIMENT")
    print("=" * 60)
    
    # Vérifier qu'Ollama est accessible
    try:
        test_response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if test_response.status_code == 200:
            print("✅ Ollama est accessible")
            models = test_response.json().get("models", [])
            print(f"📋 Modèles disponibles: {[m['name'] for m in models]}")
        else:
            print("⚠️ Ollama répond mais statut anormal")
    except:
        print("❌ ERREUR : Ollama n'est pas démarré !")
        print("   Lancez : ollama serve")
        exit(1)
    
    print("\n" + "=" * 60)
    
    # Test 1 : Message positif
    print("\n📨 Test 1 : Message positif")
    result1 = analyze_sentiment("Je suis très content du service")
    print(f"✅ Résultat: {result1}")
    
    # Test 2 : Message négatif
    print("\n📨 Test 2 : Message négatif")
    result2 = analyze_sentiment("C'est inadmissible ! Je veux un remboursement")
    print(f"✅ Résultat: {result2}")
    
    # Test 3 : Message neutre
    print("\n📨 Test 3 : Message neutre")
    result3 = analyze_sentiment("Où est ma commande ?")
    print(f"✅ Résultat: {result3}")
    
    print("\n" + "=" * 60)
    print("✅ Tests terminés")
    print("=" * 60)