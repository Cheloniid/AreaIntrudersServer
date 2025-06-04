import hashlib


HASHED_PASSWORD = hashlib.sha256("password".encode()).hexdigest()
print(HASHED_PASSWORD)

# HASHED_PASSWORD = d74795abc84c7f419c14f888626359743a380a2326c66e6125f4156b81d86074