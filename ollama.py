import requests
import json

# Definir la URL del servidor local de Ollama
url = "http://localhost:11434/api/generate"

# Definir el cuerpo de la solicitud (prompt para el modelo)
data = {
    "model": "llama3.2:3b",  # Asegúrate de que el modelo esté correctamente nombrado
    "prompt": "Hola, ¿cómo estás?"
}

try:
    # Hacer la solicitud POST a la API de Ollama con streaming habilitado
    with requests.post(url, json=data, stream=True) as response:
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            # Iterar sobre las líneas de la respuesta
            for line in response.iter_lines():
                if line:
                    try:
                        # Decodificar la línea de bytes a string
                        decoded_line = line.decode('utf-8')
                        # Parsear el JSON de la línea
                        obj = json.loads(decoded_line)
                        # Imprimir la parte de la respuesta generada
                        if 'response' in obj:
                            print(obj['response'], end='', flush=True)
                        # Verificar si la generación ha finalizado
                        if obj.get('done'):
                            break
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar JSON: {e}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Error al realizar la solicitud: {e}")
