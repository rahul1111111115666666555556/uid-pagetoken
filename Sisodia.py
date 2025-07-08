import requests
from colorama import Fore, init
from datetime import datetime, timedelta
import time

# Initialize colorama for colored text output
init(autoreset=True)

# Logo function to display at the beginning
def show_logo():
    logo = """
\033[1;33m
\033[1;33m███████╗ ██████╗ ██╗   ██╗██████╗  █████╗ ██╗   ██╗
\033[1;33m██╔════╝██╔═══██╗██║   ██║██╔══██╗██╔══██╗██║   ██║
\033[1;33m███████╗██║   ██║██║   ██║██████╔╝███████║██║   ██║
\033[1;33m╚════██║██║   ██║██║   ██║██╔══██╗██╔══██║╚██╗ ██╔╝
\033[1;33m███████║╚██████╔╝╚██████╔╝██║  ██║██║  ██║ ╚████╔╝ 
\033[1;33m╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  
          
          
╔═════════════════════════════════════════════════════════════╗
║ \033[1;31mTOOLS      :  GROUP UID 
║ \033[1;34m𝗦𝗢𝗡𝗨     : RAHUL DON 
║ \033[1;32mWHATSAPP   : +919106391471
║ \033[1;82mTOOLS NAME : PAGE TOKEN EXTRACTOR+ GROUP UID
╚═════════════════════════════════════════════════════════════╝
    """
    print(Fore.YELLOW + logo)
    time.sleep(1)  # Add a small delay to make the logo visible

    # Display the message that you want users to see
    print(Fore.CYAN + "RAHUL SIR ME ANSH KI DIDI CHODNE AAYA HU!")
    print(Fore.CYAN + "For support or queries, WhatsApp: +919106391471\n")

# Function to fetch and list only active Messenger Groups for a given Facebook Access Token
def get_active_messenger_groups(access_token):
    url = f'https://graph.facebook.com/v17.0/me/conversations?fields=name,updated_time&access_token={access_token}'  # Fetch name and updated_time
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            print(Fore.GREEN + "\nList of Active Messenger Groups:")
            now = datetime.utcnow()
            active_found = False

            for conversation in data['data']:
                conversation_id = conversation['id']
                conversation_name = conversation.get('name', None)
                updated_time = conversation.get('updated_time', None)

                if updated_time:
                    # Convert updated_time to a datetime object
                    last_updated = datetime.strptime(updated_time, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)

                    # Check if the group was updated in the last 30 days
                    if now - last_updated <= timedelta(days=30):
                        active_found = True
                        if conversation_name:
                            print(Fore.GREEN + f"Group Name: {conversation_name} | Group UID: {conversation_id}")
                        else:
                            print(Fore.YELLOW + f"Group UID: {conversation_id} | Group Name: No Name Available")

            if not active_found:
                print(Fore.YELLOW + "No active Messenger groups found in the last 30 days.")
        else:
            print(Fore.YELLOW + "No Messenger groups found or unable to access group data.")
    else:
        print(Fore.RED + f"Error: {response.status_code}")
        print(response.text)

# Function to display the token details (user info)
def get_token_details(access_token):
    url = f'https://graph.facebook.com/me?access_token={access_token}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'name' in data:
            print(Fore.GREEN + f"\nLogged in as: {data['name']} (User ID: {data['id']})")
        else:
            print(Fore.YELLOW + "Unable to retrieve user details from the access token.")
    else:
        print(Fore.RED + "Error: Invalid or expired token.")
        return False  # Indicate that the token is invalid
    return True  # Token is valid

# Function to fetch and list all Pages and their Access Tokens
def get_page_tokens(access_token):
    url = f'https://graph.facebook.com/v17.0/me/accounts?fields=name,access_token&access_token={access_token}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            print(Fore.GREEN + "\nList of Pages and Their Access Tokens:")
            for page in data['data']:
                page_name = page.get('name', 'Unknown Page')
                page_token = page.get('access_token', 'No Token Available')
                print(Fore.GREEN + f"Page Name: {page_name} | " + Fore.LIGHTMAGENTA_EX + f"Page Access Token: {page_token}")  # Changed to pink
        else:
            print(Fore.YELLOW + "No Pages found or unable to access page data.")
    else:
        print(Fore.RED + f"Error: {response.status_code}")
        print(response.text)

# Main function to execute the script
def main():
    # Display logo and message
    show_logo()

    while True:
        # Input Facebook Access Token
        access_token = input(Fore.BLUE + "Enter your Facebook Access Token: ")

        if not access_token:
            print(Fore.RED + "Error: The access token is empty or invalid.")
            continue

        # Display a preview of the token (first 10 characters)
        token_name = access_token[:10]
        print(Fore.BLUE + f"\nFacebook Access Token (Preview): {token_name}...")

        # Fetch and display token details (user info)
        if not get_token_details(access_token):
            continue  # If token is invalid, ask for a new one

        # Fetch and list only active Messenger Groups
        get_active_messenger_groups(access_token)

        # Fetch and display all Pages with their Access Tokens
        get_page_tokens(access_token)
        break  # Exit the loop after successful execution

if __name__ == "__main__":
    main()
