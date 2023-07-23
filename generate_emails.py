import random
import string


def generate_random_string(length):
    characters = string.ascii_lowercase + string.digits
    return random.choice(string.ascii_lowercase) + ''.join(random.choice(characters) for _ in range(length))


def generate_random_email(domain='gmail.com'):
    username = generate_random_string(random.randint(8, 16))
    return f"{username}@{domain}"


def write_emails_to_file(filename, num_emails=10):
    with open(filename, 'w') as file:
        for _ in range(num_emails):
            email = generate_random_email()
            file.write(email + '\n')


# Example usage to generate 10 random email addresses and write to a file
write_emails_to_file('data\\inputs\\emails.txt', num_emails=1000)
