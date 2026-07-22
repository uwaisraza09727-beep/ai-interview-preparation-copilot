from app.core.security.password import (
    hash_password,
    verify_password,
)

password = "MyPassword123"

hashed = hash_password(password)

print("Original :", password)
print("Hashed   :", hashed)

print(
    "Verify :",
    verify_password(password, hashed),
)