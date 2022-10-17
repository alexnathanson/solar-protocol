import secrets

password = secrets.token_hex()

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)

print(f"PW: ${password}")
print(f"HASH: ${hashed}")
