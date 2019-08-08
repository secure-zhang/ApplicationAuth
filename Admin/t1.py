import base64

with open("1.jpg","rb") as f:
    base64_data = base64.b64encode(f.read()).decode()
    print(base64_data)
