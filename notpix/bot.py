import requests
import json
import os
from colorama import init, Fore, Style

init(autoreset=True)

def read_queries():
    queries = []
    with open('query.txt', 'r') as file:
        for line in file:
            if line.strip():
                queries.append(line.strip())
    return queries

def parse_query(query):
    return f"initData {query}"

def get_headers(auth_string):
    return {
        'authorization': auth_string,
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://app.notpx.app',
        'referer': 'https://app.notpx.app/',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

def submit_secret_word(headers, secret_word):
    payload = {"secret_word": secret_word}
    response = requests.post(
        'https://notpx.app/api/v1/mining/quest/check/secretWord',
        headers=headers,
        json=payload
    )
    return response.json()

def process_account(query, secret_word):
    auth_string = parse_query(query)
    headers = get_headers(auth_string)
    
    response = requests.get(
        'https://notpx.app/api/v1/users/me',
        headers=headers
    )
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"\n{Fore.GREEN}Login berhasil untuk user: {user_data['firstName']} {user_data['lastName']}")
        print(f"{Fore.YELLOW}Balance: {user_data['balance']}")
        print(f"{Fore.CYAN}League: {user_data['league']}")
        
        result = submit_secret_word(headers, secret_word)
        if result.get('secretWord', {}).get('success'):
            print(f"{Fore.GREEN}Success! Reward: {result['secretWord']['reward']}")
        else:
            print(f"{Fore.RED}Failed to submit secret word")
    else:
        print(f"{Fore.RED}Login gagal untuk akun. Status code: {response.status_code}")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.CYAN}=== NotPX Multi Account Bot ==={Style.RESET_ALL}\n")
    
    secret_word = input(f"{Fore.YELLOW}Enter today's keyword: {Style.RESET_ALL}")
    print("\nProcessing accounts...")
    
    queries = read_queries()
    for query in queries:
        try:
            process_account(query, secret_word)
        except Exception as e:
            print(f"{Fore.RED}Error processing account: {str(e)}")
    
    print(f"\n{Fore.CYAN}=== Task Completed ==={Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")