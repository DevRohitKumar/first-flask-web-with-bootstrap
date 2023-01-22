import random, string

def generate_aplhanum_str(len=5):
    if len > 10:
        print("""Max length for this random alpha-numeric key generator is set to 10.
            You can increase this upper limit with helper.""")
    elif len > 0:
        
        gas = ''.join(random.choices(string.ascii_lowercase + string.digits, k=len))
        return gas    
    else:
        print("Length required to generate alpha-numeric string")