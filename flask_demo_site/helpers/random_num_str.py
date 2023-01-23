import random

def generate_num_str(len):
    start = "1"
    end = "9"
    num_str = ""
    if len > 20:
        print("""Max length set for now is 20. Which will generate numeric string of 10 digits.
            You can increase this upper limit with helper""")
    elif len > 0:
        for i in range(len-1):
            start += "0"
            end += "9"
            
        num_str = str(random.randint(int(start), int(end)))
        return num_str
    else:
        print("Length required to generate number string")
