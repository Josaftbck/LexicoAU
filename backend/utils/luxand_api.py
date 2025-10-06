import requests

LUXAND_API_KEY = "bfebdc9abc06459d841e5d10631614a6"

# ✅ Comparar dos rostros directamente (sin registrar)
def verify_face(photo_base64: str, stored_photo_base64: str):
    url = "https://api.luxand.cloud/photo/similarity"  # 👈 CAMBIA AQUÍ
    headers = {
        "token": LUXAND_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "photo1": photo_base64,
        "photo2": stored_photo_base64,
        "threshold": 0.60  # puedes ajustar el umbral
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {
            "success": True,
            "score": data.get("score", 0),
            "similar": data.get("similar", False)
        }
    else:
        return {"success": False, "error": response.text}


# ✅ Registrar un rostro (si algún día quieres usarlo)
def register_face(name: str, photo_base64: str):
    url = "https://api.luxand.cloud/subject"
    headers = {
        "token": LUXAND_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "name": name,
        "photo": photo_base64
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return {"success": True, "embedding": "pendiente"}
    else:
        return {"success": False, "error": response.text}