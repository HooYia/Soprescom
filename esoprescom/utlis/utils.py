import random
import string

def generate_password(length=8):
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")
    
    # Character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = string.punctuation
    
    # Ensure the password contains at least one of each required character type
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(special)
    ]
    
    # Fill the rest of the password length with a mix of all character types
    all_characters = uppercase + lowercase + digits + special
    password += random.choices(all_characters, k=length-4)
    
    # Shuffle to ensure the password isn't predictable
    random.shuffle(password)
    
    return ''.join(password)

