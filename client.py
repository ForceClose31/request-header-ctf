import socket
import re

HOST = 'fasilkomapp.com'
PORT = 12345
SOAL = 'soal tio'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

request = f"{SOAL}\r\n\r\n"
client_socket.sendall(request.encode('utf-8'))

response = b""
while True:
    chunk = client_socket.recv(2048)
    if not chunk or b"\n" in chunk:
        response += chunk
        break
    response += chunk

decoded = response.decode('utf-8', errors='replace').strip()
print(f"Soal diterima:\n{decoded}\n")

lines = decoded.splitlines()
expression = lines[0]
mappings = lines[1:]

replacements = {}
for line in mappings:
    match = re.match(r"(.+)\s*=\s*(.+)", line)
    if match:
        symbol = match.group(1).strip()
        operator = match.group(2).strip()
        replacements[symbol] = operator

tokens = expression.strip().split()
translated_tokens = [replacements.get(token, token) for token in tokens]
translated_expression = " ".join(translated_tokens)

print(f"Ekspresi setelah diterjemahkan: {translated_expression}")

try:
    answer = eval(translated_expression)
    if isinstance(answer, float):
        if round(answer, 2) == round(answer, 1):
            formatted_answer = f"{answer:.1f}"
        else:
            formatted_answer = f"{answer:.2f}"
    else:
        formatted_answer = str(answer)
except Exception as e:
    print(f"Gagal menghitung jawaban: {e}")
    client_socket.close()
    exit()

client_socket.sendall(f"jawab {formatted_answer}\r\n\r\n".encode('utf-8'))

final_response = b""
while True:
    chunk = client_socket.recv(2048)
    if not chunk:
        break
    final_response += chunk

print(f"Respon akhir dari server:\n{final_response.decode('utf-8', errors='replace')}\n")

client_socket.close()