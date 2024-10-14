import rsa

def generate_keys():
    public_key, private_key = rsa.newkeys(512)
    return public_key, private_key

def sign_message(message, private_key):
    return rsa.sign(message.encode(), private_key, 'SHA-1')

def reconstruct_private_key(d, n, p, q):
    e = 65537
    return rsa.PrivateKey(n, e, d, p, q)

def verify_signature(message, signature, public_key):
    try:
        return rsa.verify(message.encode(), signature, public_key) == 'SHA-1'
    except rsa.VerificationError:
        return False
