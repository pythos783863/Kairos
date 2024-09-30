import os
import json
import uuid
import sys
import shutil
import threading
import time
import random
import smtplib
from email.message import EmailMessage
import textwrap
from textwrap import wrap
from datetime import datetime
import base64
from colorama import Fore, Style, Back, init
init(autoreset=True)

TRANSACTIONS_FILE = 'transactions.json'
SHOP_FILE = 'shop.json'
USERS_FILE = 'users.json'
MESSAGES_FILE = 'messages.json'
GROUPS_FILE = 'groups.json'
FUSERS_FILE = 'fusers.json'
GMESSAGES_FILE = 'gmessages.json'
THEME_FILE = 'theme.json'
    
width = os.get_terminal_size().columns    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def center_text(text):
    """Center the given text based on the terminal width."""
    terminal_width = get_terminal_width()
    return text.center(terminal_width)    
    
def load_json(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f, indent=4)
        return {}
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                data = {}
                with open(file, 'w') as f:
                    json.dump(data, f, indent=4)
            return data
    except json.JSONDecodeError:
        with open(file, 'w') as f:
            json.dump({}, f, indent=4)
        return {}

def save_json(file, data):
    try:
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(Fore.RED + f"Failed to save data to {file}: {e}")
        
def loading_az():
    """Display loading animation."""
    animation= ['⌛ loading ..... ','⏳ loading ..... ']*10
    for frame in animation:
        time.sleep(0.3)
        sys.stdout.write("\r" + frame)
        sys.stdout.flush()
        
def refresh():
    """Refresh data from all JSON files to update in-memory data."""
    global groups_data, users_data, messages_data, gmessages_data, fusers_data, shop_data, transactions_data
    groups_data = load_json(GROUPS_FILE)
    messages_data = load_json(MESSAGES_FILE)
    users_data = load_json(USERS_FILE)
    gmessages_data = load_json(GMESSAGES_FILE)
    fusers_data = load_json(FUSERS_FILE)
    shop_data = load_json(SHOP_FILE)
    transactions_data = load_json(TRANSACTIONS_FILE)

def auto_refresh(interval=0.1):
    """Automatically refresh JSON data at a specified interval (in seconds)."""
    while True:
        refresh()
        time.sleep(interval)

def start_auto_refresh(interval=0.1):
    """Start a thread for auto-refreshing."""
    refresh_thread = threading.Thread(target=auto_refresh, args=(interval,))
    refresh_thread.daemon = True
    refresh_thread.start()

def register_user(name, email, password, pin):
    users = load_json(USERS_FILE)
    if email in users:
        print(Fore.RED + "You already have an account.")
        time.sleep(2)
        return None
        
    emojis = ["🧛", "👹", "🤡", "👽", "🤖", "🤑", "😎", "🤓", "🥸", "🤕", "🤠", "👻", "🎃", "😈", "😇", "🤩", "❤️", "😺", "😹", "😿", "😸", "💝", "💓", "💘", "💗", "🫂", "❣️", "💌", "💞", "💀", "👀", "👁️", "🗣️", "🧟", "🧌", "🎄", "🥷", "👼", "💂", "🫅", "🤵", "👰", "🚀", "👷", "👮", "🕵️", "✈️", " 🔬", "⚕️", "🧑", "🏭", "🚒", "🧑🌾", "🏫", "🎓", "🧑‍💼", "⚖️", "🧑‍💻", "🎤", "🎨", "🍳", "👳", "🧕", "👲", "🌻", "🏵️", "🌸", "🥀", "🌹", "💐", "🌍", "🌎", "🐯", "🐼", "🐨", "🐻", "🐶", "🐨", "🐹", "🐭", "🐣", "🐥", "🦭", "🦢", "🦀", "🐋", "🐟", "🐞", "🍑", "🎁", "🎊", "🪩", "💰", "🧸"]     

    user_emoji = random.choice(emojis)
    balance= '0.00'
    username = name.replace(" ", "_") + str(uuid.uuid4())[:5]
    users[email] = {
        'name': name,
        'username': username,
        'password': password,
        'pin': pin,
        'country': "",
        'bio': "",
        'sex': "",
        'age': "",
        'balance': balance,
        'user_emoji': user_emoji
    }
    save_json(USERS_FILE, users)
    return username
    
def login_user(email, password):
    if email == admin["email"] and password == admin["password"]:
        loading_az()
        admin_dashboard()
        return "admin"
    
    users = load_json(USERS_FILE)
    user_data = users.get(email)
    if user_data['password'] == password:
        loading_az()
        time.sleep(0.5)
        user_dashboard(users, email)
        return email
    else:
        print(Fore.RED + "\n🚨 Invalid credentials 🙊 ")
        time.sleep(2)
        return None
width = os.get_terminal_size().columns   
def user_dashboard(users, email):
    while True:
        load_json(GROUPS_FILE)
        load_json(FUSERS_FILE)
        load_json(GMESSAGES_FILE)
        load_json(MESSAGES_FILE)
        load_json(SHOP_FILE)
        load_json(TRANSACTIONS_FILE)
        users = load_json(USERS_FILE)
        user_data = users.get(email)
        clear_screen()
        print(Fore.BLUE + "="*width)
        print(Back.CYAN + Style.BRIGHT + Fore.BLUE + "DE WORLD 🌏".center(40))
        print(Fore.BLUE + "="*width)
        print(Fore.GREEN +center_text( f"️${user_data['balance']}"))
        print(Fore.BLUE+"_"*width)
        print(Fore.YELLOW+"\n"+center_text(" What's on your mind?"))
        print(Fore.BLUE+"_"*width)
        print(Fore.CYAN + "\n1. 🛍️ Shoping   |   2. ️🧑‍🔧 Menu")
        print(Fore.BLUE+"_"*width)
        print(Fore.CYAN+"\n3. 📩 Messages   |   4. 👥 Friends")
        print(Fore.BLUE+"_"*width)
        print(Fore.CYAN+"\n5. 🔍 Search   |   6. 📊 WSR-Fund")
        print(Fore.BLUE+"_"*width)
        print(Fore.CYAN+"\n7. 🫂 Groups   |   8. ⚙️ Settings")
        print(Fore.BLUE+"_"*width)
        print(Fore.CYAN+"\n0. 🛑 Logout ")
        print(Fore.BLUE+"_"*width)
        choice= input(Fore.CYAN+"\nPick What's on your mind: "+Style.RESET_ALL)
        if choice == '1':
            Jet_shop(users, email)
        elif choice =='2':
            menu(users, email)
        elif choice == '3':
            my_friends(users, friends)
        elif choice == '4':
            my_friends(users, friends)
        elif choice == '5':
            search(users, group)
        elif choice == '6':
            wsr_fund(users, email)
        elif choice == '7':
            group(users)
        elif choice == '8':
            settings(users)
        elif choice == '0':
            print(Fore.RED+"Logging out...")
            time.sleep(4)
            return main_menu()
        else:
            print(Fore.RED+"No item found with the input")
            time.sleep(3)
            return user_dashboard(users, email)
width = os.get_terminal_size().columns
def menu(users, email):
    users = load_json(USERS_FILE)
    user_data = users.get(email)
    clear_screen()
    print(Fore.BLUE + "=" * width)
    print(Back.CYAN + Style.BRIGHT + Fore.BLUE + "MENU".center(40))
    print(Fore.BLUE + "=" * width)

    print(Fore.GREEN + "\n1. 📠 Pay   |   2. 🏧 Deposit")
    print(Fore.CYAN+"_"*width)
    print(Fore.GREEN + "\n3. My Profile   |   0. Exit")
    print(Fore.CYAN+"_"*width)
    choice = input(Fore.BLUE + "\nSelect an option: ").strip()
    
    if choice == '1':
        pay_user(users, email)
    elif choice == '2':
        deposit(users, email)
    elif choice == '3':
        my_profile(users, email)
    elif choice == '0':
        return user_dashboard(users, email)  # Return to the user dashboard
    else:
        print(Fore.RED + "Invalid option. Please try again.")
        time.sleep(1.5)
        return menu(users, email)

def pay_user(users, email):
    users = load_json(USERS_FILE)
    user_data = users.get(email)
    clear_screen()
    
    print(Fore.CYAN + "=" * width)
    print(Back.MAGENTA + Style.BRIGHT + Fore.BLUE + center_text("Pay a User"))
    print(Fore.CYAN + "=" * width)
    
    sender_email = input(Fore.GREEN + "\nEnter your email or 0 back: " + Style.RESET_ALL)
    if sender_email == '0':
        return menu(user)
    if sender_email != user_data['email']:
        print(Fore.RED+"input your email correctly")
        time.sleep(1)
        return pay_user(user, email)
    if sender_email not in user:
        print(Fore.RED + "Your email is not registered.")
        return pay_user(user, email)

    recipient_email = input(Fore.YELLOW + "\nEnter the recipient's email: " + Style.RESET_ALL)
    if recipient_email not in user:
        print(Fore.RED + "Recipient email is not registered.")
        return pay_user(user, email)
    if recipient_email == sender_email:
        print(Fore.RED+"you cannot pay yourself")
        time.sleep(0.9)
        return pay_user(user, email)
        
    pin = input(Fore.BLUE+"\nWhat is your pin: ")
    if pin != user[sender_email]['pin']:
        print(Fore.RED+"\nIncorrect pin")
        time.sleep(1)
        return pay_user(user, email)
        

    clear_screen()
    
    # Display recipient's information
    print(Fore.GREEN + "=" * width)
    print(Back.YELLOW + Style.BRIGHT + Fore.GREEN + center_text("Recipient"))
    print(Fore.GREEN + "=" * width)
    print("\n"+center_text(f"{user[recipient_email]['user_emoji']}"))
    print(Fore.BLUE + "\n"+center_text(f"{user[recipient_email]['name']}"))
    print(Fore.CYAN + "_" * width)
    
    try:
        amount = float(input(Fore.MAGENTA + "\nHow much do you want to pay this user or (00) to go back: " + Style.RESET_ALL))
        if amount == 0.00:
            return menu(user, email)
        elif amount == '00':
            return menu(user, email)
    except ValueError:
        print(Fore.RED + "\nInvalid input. Please enter a valid number.")
        time.sleep(0.9)
        return pay_user(user, email)

    sender_balance = float(user[sender_email]['balance'])
    recipient_balance = float(user[recipient_email]['balance'])
    
    if amount > sender_balance:
        print(Fore.YELLOW + "\nYou don't have enough balance to pay this user.")
    else:
        # Deduct from sender
        new_sender_balance = sender_balance - amount
        user[sender_email]['balance'] = f"{new_sender_balance:.2f}"
        
        # Add to recipient
        new_recipient_balance = recipient_balance + amount
        user[recipient_email]['balance'] = f"{new_recipient_balance:.2f}"

        save_json(USERS_FILE, user)
        print(Fore.GREEN + f"\nSuccessfully paid {amount:.2f} to {user[recipient_email]['name']}.")
        print(Fore.GREEN + f"\nYour new balance is {user[sender_email]['balance']}.")
        status = 'Successful ✅'
        idx = 'anx-62026gsj5289bst28ojs6wn7jw'
        transaction_id = idx.replace("","8hsg0")+str(uuid.uuid4())[:5] 
        try:
            transaction = load_json(TRANSACTIONS_FILE)  # Load existing transactions
        except FileNotFoundError:
            transaction = {}  # If file not found, initialize an empty dictionary
        
        transaction[sender_email] = {
            'recipient_email': recipient_email,
            'amount': amount,
            'status': status,
            'transaction_id': transaction_id
        }
        save_json(TRANSACTIONS_FILE, transaction)
    
    input(Fore.CYAN + "\nPress Enter to return to the menu..." + Style.RESET_ALL)
    return menu(user, email)
        
    
class PostPrinter:
    def __init__(self, width=None):
        self.width = width or self.get_terminal_width() - 2
        self.post_counter = 0

    def get_terminal_width(self):
        return os.get_terminal_size().columns

    def print_post(self, text):
        if self.post_counter > 0:
            print(Fore.CYAN + "_" * self.width)
        wrapped_text = textwrap.fill(text, self.width)
        print(Fore.BLUE + "\n" + wrapped_text)
        self.post_counter += 1    

def deposit(users):
    clear_screen()
    # Load users data from USERS_FILE
    users = load_json(USERS_FILE)
    print(Fore.RED+"="*width)
    print(Back.GREEN+Style.BRIGHT+Fore.RED+center_text("Deposit to your account"))
    print(Fore.RED+"="*width)
    print (Fore.MAGENTA+"\n  1. BTC   |   0. Back")
    print(Fore.RED+"_"*width)
    vb = input(Fore.BLUE+"\npick an option "+Style.RESET_ALL)
    if vb == '1':
        btc_deposit()
    elif vb == '0':
        return menu(users, email)
    else:
        print(Fore.RED+"Invalid input")
        time.sleep(0.9)
    
    
width = os.get_terminal_size().columns    

def my_profile(users, email):
    while True:
        users = load_json(USERS_FILE)
        user_data = users.get(email)
        clear_screen()
        print(Fore.CYAN + "=" * width)
        print(Back.YELLOW + Style.BRIGHT + Fore.BLUE + "My Profile".center(40))
        print(Fore.CYAN + "=" * width)
        print("\n" +center_text(f"{user_data['user_emoji']}"))
        print(Fore.BLUE + "\n" +center_text( f"{user_data['name']}"))

        # Print user bio
        if user_data['bio']:  # Check if 'bio' exists and is not empty
            print(Fore.YELLOW + "\n" +center_text( f"{user_data['bio']}"))
        else:
            print(Fore.RED + "\n" + center_text ("No bio"))

        # Print user country
        if user_data['country']:  # Check if 'country' exists and is not empty
            print(Fore.BLUE + "\n" + center_text (f"{user_data['country']}"))
        else:
            print(Fore.RED + "\n" +center_text("Add country"))

        # Print user sex/relationship status
        if user_data['sex']:  # Check if 'sex' exists and is not empty
            print(Fore.YELLOW + "\n" + center_text(f"{user_data['sex']}"))
        else:
            print(Fore.RED + "\n" + center_text("Add Relationship Status"))

        print(Fore.CYAN + "_" * width)

        choice = input(Fore.BLUE + "\n0 to back or (/e) to edit: " + Style.RESET_ALL)
        if choice == '0':
            return menu(users, email)  # Go back to the menu
        if choice == '/e':
            return settings(users)  # Go to settings for editing
        else:
            print(Fore.RED + "Invalid input")
            time.sleep(0.9)
            return my_profile(users, email)
    
def btc_deposit():
    user = load_json(USERS_FILE)
    clear_screen()
    print(Fore.GREEN+"="*width)
    print(Back.YELLOW+Style.BRIGHT+Fore.BLUE+center_text("BTC Deposit"))
    print(Fore.GREEN+"="*width)
    print(Fore.MAGENTA+"\n"+center_text("bc1qujwwt6gy9j5tfrapjgz6avfdh5xlt6huh4zk64"))
    print(Fore.CYAN+"_"*width)
    print(Fore.BLUE+"\nMake a Deposit of the amount you need to the BTC address " )
    txn_id= input(Fore.GREEN+"\ninput your payment transaction id or (0) back: "+Style.RESET_ALL)
    if txn_id == '0':
        return deposit(user)
    email= input(Fore.GREEN+"your current email: "+Style.RESET_ALL)
    status = 'Pending ⏳'
    dept_id= 'afgvj80knx4ct0'
    deposit_id = dept_id.replace("", "0fy67b")+str(uuid.uuid4())[:5]
    print(Fore.CYAN+"_"*width)
    print(Fore.YELLOW+"\n"+center_text(f"   {user[email]['name']}"))
    print(Fore.BLUE+f"\n   Deposit: "+Style.RESET_ALL+Fore.RED+f"{status}")
    print(Fore.YELLOW+"   Deposit id: "+Style.RESET_ALL+f"{deposit_id}")
    try:
        transaction = load_json(TRANSACTIONS_FILE)  # Load existing transactions
    except FileNotFoundError:
        transaction = {}  # If file not found, initialize an empty dictionary
    
    transaction[email] = {
        'txn_id': txn_id,
        'email': email,
        'status': status
    }
    save_json(TRANSACTIONS_FILE, transaction)
    
    gh = input(Fore.RED+"input 0 to return ")
    if gh == '0':
        loading_az()
        return deposit(users)
    else:
        print(Fore.RED+"Invalid input")
        return deposit(user, email)    
    
def group(users):
    clear_screen()
    print(Fore.CYAN + "=" * 40)
    print(Back.BLUE + Style.BRIGHT + Fore.CYAN + "Groups".center(40))
    print(Fore.CYAN + "=" * 40)
    print(Fore.BLUE + "\na. ➕ Create a group  |  6. 🫂 My Group")
    print(Fore.CYAN + "_" * 40)
    print(Fore.BLUE+"\n0. Back")
    print(Fore.CYAN+"_"*40)
    mo = input(Fore.BLUE + "\nInput an option: "+Style.RESET_ALL)
    
    if mo == 'a':
        create_group(user)
    elif mo == '6':
        my_groups(user, groups)
    elif mo == '0':
        return user_dashboard(users, email)
        
admin = {
    "email": "alexndubuisiaugustine.chat@gmail.com",
    "password": "Alex12345#"
} 
width = os.get_terminal_size().columns  
def admin_dashboard():
    """Display the admin dashboard."""
    while True:
        clear_screen()
        print(Fore.GREEN+"_"*width)
        print(Back.RED+Fore.GREEN+center_text("Admin Dashboard"))
        print(Fore.GREEN+"_"*width)
        print(Fore.BLUE+"\n1. Add Bal   |   2. Deduct Bal")
        print(Fore.RED+"_"*width)
        print(Fore.BLUE+"\n3. Create Page  |   4. Create Group")
        print(Fore.RED+"_"*width)
        print(Fore.BLUE+"\n5. Pst to Pg  |   6. Pst to Gp")
        print(Fore.RED+"_"*width)
        print(Fore.BLUE+"\n7. Add stuff to Shop   |   8.  View Users")
        print(Fore.RED+"_"*width)
        print(Fore.BLUE+"\n0. Logout")
        print(Fore.RED+"_"*width)
        choice = input(Fore.GREEN+"\nChoose an option my Admin: "+Style.RESET_ALL)
        if choice == '0':
            time.sleep(0.9)
            return
        elif choice == '1':
            add_user_balance()
        elif choice == '2':
            deduct_user_balance()
        elif choice == '3':
            create_page()
        elif choice == '4':
            create_group()
        elif choice == '5':
            post_to_page()
        elif choice == '6':
            post_to_group()
        elif choice == '7':
            add_product_to_store()
        elif choice == '8':
            view_users()
        else:
            print(Fore.RED + "Boss your input is wrong")

def add_user_balance():
    clear_screen()
    """Add balance to a user account."""
    print(Fore.RED + "=" * width)
    print(Back.CYAN + Style.BRIGHT + Fore.RED + center_text("Add User Balance"))
    print(Fore.RED + "=" * width)
    
    users = load_json(USERS_FILE)
    email = input(Fore.GREEN + "\nEnter the user email Boss or 0 back: " + Style.RESET_ALL)
    if email =='0':
        return admin_dashboard()
    
    if email in users:
        try:
            amount = float(input(Fore.YELLOW + "\nEnter the amount to add Boss: " + Style.RESET_ALL))
            print(Fore.GREEN + "Adding ......")
            time.sleep(0.9)
            # Convert the string balance to float, add the amount, then convert back to string
            current_balance = float(users[email]['balance'])
            updated_balance = current_balance + amount
            users[email]['balance'] = f"{updated_balance:.2f}"  # Store the balance as a string formatted to 2 decimal places
            save_json(USERS_FILE, users)
            print(Fore.GREEN + f"Added {amount} to {users[email]['name']}'s balance. New balance: {users[email]['balance']}")
        except ValueError:
            print(Fore.RED + "Invalid amount entered. Please enter a valid number.")
    else:
        print(Fore.RED + "User not found Boss.")
    
    time.sleep(0.9)
    return add_user_balance()

def deduct_user_balance():
    clear_screen()
    """Deduct balance from a user account."""
    print(Fore.YELLOW + "=" * width)
    print(Back.RED + Style.BRIGHT + Fore.YELLOW + center_text("Deduct User Balance"))
    print(Fore.YELLOW + "=" * width)
    
    users = load_json(USERS_FILE)
    email = input(Fore.GREEN + "Enter the user's email: " + Style.RESET_ALL)
    
    if email in users:
        try:
            current_balance = float(users[email].get('balance', "0.00"))  # Convert balance to float
            if current_balance == 0.00:
                print(Fore.RED + f"{users[email]['name']} has no balance to deduct boss.")
            else:
                amount = float(input(Fore.YELLOW + "Enter the amount to deduct boss: " + Style.RESET_ALL))
                if current_balance >= amount:
                    updated_balance = current_balance - amount
                    users[email]['balance'] = f"{updated_balance:.2f}"  # Update and store balance as a string
                    save_json(USERS_FILE, users)
                    print(Fore.GREEN + f"Deducted {amount} from {users[email]['name']}'s balance. New balance: {users[email]['balance']}")
                else:
                    print(Fore.RED + "Insufficient balance.")
        except ValueError:
            print(Fore.RED + "Invalid amount entered. Please enter a valid number.")
    else:
        print(Fore.RED + "User not found.")
        time.sleep(0.9)
        r
    
    input(Fore.CYAN + "Press Enter to return to Admin Dashboard..." + Style.RESET_ALL)

def create_page():
    clear_screen()
    """Create a new page."""
    print_banner("Create Page", Fore.CYAN)
    pages = load_json(PAGES_FILE)
    page_name = input("Enter the name of the page: ")
    if page_name not in pages:
        pages[page_name] = {'posts': []}
        save_json(PAGES_FILE, pages)
        print(Fore.GREEN + "Page created successfully.")
    else:
        print(Fore.RED + "Page already exists.")
    input("Press Enter to return to Admin Dashboard...")

def create_group():
    clear_screen()
    """Create a new group."""
    print_banner("Create Group", Fore.CYAN)
    groups = load_json(GROUPS_FILE)
    group_name = input("Enter the name of the group: ")
    if group_name not in groups:
        groups[group_name] = {'messages': []}
        save_json(GROUPS_FILE, groups)
        print(Fore.GREEN + "Group created successfully.")
    else:
        print(Fore.RED + "Group already exists.")
    input("Press Enter to return to Admin Dashboard...")

def post_to_page():
    clear_screen()
    """Post a message to a page."""
    print_banner("Post to Page", Fore.CYAN)
    pages = load_json(PAGES_FILE)
    page_name = input("Enter the name of the page: ")
    if page_name in pages:
        post = input("Enter your post: ")
        pages[page_name]['posts'].append(post)
        save_json(PAGES_FILE, pages)
        print(Fore.GREEN + "Post added successfully.")
    else:
        print(Fore.RED + "Page not found.")
    input("Press Enter to return to Admin Dashboard...")

def post_to_group():
    clear_screen()
    """Post a message to a group."""
    print_banner("Post to Group", Fore.CYAN)
    groups = load_json(GROUPS_FILE)
    group_name = input("Enter the name of the group: ")
    if group_name in groups:
        message = input("Enter your message: ")
        groups[group_name]['messages'].append(message)
        save_json(GROUPS_FILE, groups)
        print(Fore.GREEN + "Message posted successfully.")
    else:
        print(Fore.RED + "Group not found.")
    input("Press Enter to return to Admin Dashboard...")

def add_product_to_store():
    clear_screen()
    """Add a product to the store."""
    print_banner("Add Product to Store", Fore.CYAN)
    spy_store = load_json(SPY_STORE_FILE)
    product_name = input("Enter the name of the product: ")
    if product_name not in spy_store:
        price = float(input("Enter the price of the product: "))
        spy_store[product_name] = {'price': price}
        save_json(SPY_STORE_FILE, spy_store)
        print(Fore.GREEN + "Product added successfully.")
    else:
        print(Fore.RED + "Product already exists.")
    input("Press Enter to return to Admin Dashboard...")
        
def create_group(user):
    clear_screen()
    print(Fore.BLUE + "=" * 40)
    print(Back.BLUE + Style.BRIGHT + Fore.CYAN + "Create a Group".center(40))
    print(Fore.BLUE + "=" * 40)
    
    groups = load_json(GROUPS_FILE)
    
    while True:
        group_name = input(Fore.BLUE + "Enter the name of your group: ").strip()
        
        # Check if the group name is valid (non-empty)
        if not group_name:
            print(Fore.RED + "Group name cannot be empty.")
            continue
        
        # Check if the group already exists
        if group_name not in groups:
            # Add the new group to the groups file with the creator's username
            groups[group_name] = {
                'members': [user['username']]  # Assuming 'username' is the user's identifier
            }
            
            save_json(GROUPS_FILE, groups)
            print(Fore.GREEN + "Group created successfully.")
            time.sleep(0.8)
            return group(user)
        else:
            # Group already exists
            print(Fore.RED + f"Group already exists with this name: {group_name}")
            fg = input(Fore.BLUE + "Input 0 to create a new group, or 00 to return: ")
            
            if fg == '0':
                return create_group(user)  # Prompt the user again for a new group name
            elif fg == '00':
                return group(user)
            else:
                print(Fore.RED + "Invalid input. Please try again.")

USERS_FILE = 'users.json'

def view_users():
    # Load the users data from the file
    with open(USERS_FILE, 'r') as file:
        users_data = json.load(file)
    
    # Count the number of users
    user_count = len(users_data)
    
    if user_count > 0:
        # Display the number of users
        print(f"Boss, you got {user_count} user{'s' if user_count != 1 else ''}")
        time.sleep(0.9)
        return
    else:
        print("Boss, you got no user yet")
        time.sleep(0.9)
        return
USERS_FILE = 'users.json'

def ban_user(report):
    # Load the users data from the file
    with open(USERS_FILE, 'r') as file:
        users_data = json.load(file)
    
    # Create a list of users to remove
    users_to_remove = []
    
    # Iterate over the users and find the one to remove
    for email, user in users_data.items():
        if report == user['name'] or report == email:
            users_to_remove.append(email)
    
    # Remove the user(s) from the data
    for email in users_to_remove:
        del users_data[email]
    
    # Save the updated data back to the file
    with open(USERS_FILE, 'w') as file:
        json.dump(users_data, file, indent=4)
    
    print(f"User {report} has been banned.")
            
def my_groups(users, groups):
    clear_screen()
    
    groups_data = load_json(GROUPS_FILE)
    user_groups = []  # List to store groups the user has joined or created
    
    # Iterate through all groups and check if the user is either a member or the creator
    for group_name, group_info in groups_data.items():
        if user['username'] in group_info.get('members', []):
            user_groups.append(group_name)

    print(Fore.BLUE + "=" * 40)
    print(Back.CYAN + Style.BRIGHT + Fore.BLUE + "YOUR GROUPS".center(40))
    print(Fore.BLUE + "=" * 40)
    
    if not user_groups:
        print(Fore.CYAN + "\nYou are not a member of any groups.")
        print(Fore.BLUE + "=" * 40)
        time.sleep(1.5)
        return user_dashboard(user)
    
    # Display the list of groups
    print(Fore.BLUE + "\n0. ↩️ Back")
    print(Fore.CYAN + "_" * 40)
    for idx, group in enumerate(user_groups, 1):
        print(Fore.GREEN + f"\n{idx}. {group}")
    
    print(Fore.CYAN + "_" * 40)
    
    # Prompt user to select a group
    cf = input("\nOpen a chat with a specific group (number): "+Style.RESET_ALL)
    
    if cf == '0':  # Option to go back
        return user_dashboard(user)
    
    # Validate the user input and open the chat
    if cf.isdigit() and 1 <= int(cf) <= len(user_groups):
        selected_index = int(cf)
        selected_group = user_groups[selected_index - 1]
        print(f"\nOpening group chat for {selected_group}...")
        time.sleep(1.5)
        return group_chat(user, selected_group)  # Call the chat function with the selected group
    else:
        print("\nInvalid input. Returning to the group list...")
        time.sleep(1.5)
        return my_groups(user)

def clear_screen():
    """Clears the terminal screen."""
    print("\033c", end="")

def get_terminal_width():
    """Get the width of the terminal."""
    try:
        return shutil.get_terminal_size((80, 20)).columns
    except Exception as e:
        print(f"Error detecting terminal size: {e}")
        return 80  # Default width if detection fails

def format_message_box(user, message, width=30, align='left'):
    """Format a message into a box with the sender's username inside."""
    # Combine the username and message, with username at the top
    content = f"{user['username']}:\n{message}"
    
    # Wrap the content based on the provided width
    lines = textwrap.wrap(content, width=width)
    
    # Adjust alignment for each line (left or right)
    if align == 'right':
        lines = [line.rjust(width) for line in lines]
    elif align == 'left':
        lines = [line.ljust(width) for line in lines]

    # Create the message box with borders
    box = '\n'.join(f"║ {line} ║" for line in lines)
    top_bottom_border = '╔' + '═' * (width + 2) + '╗'
    
    return top_bottom_border + '\n' + box + '\n' + '╚' + '═' * (width + 2) + '╝'

def format_time_difference(timestamp):
    """Format time difference from timestamp to now."""
    try:
        message_time = datetime.fromisoformat(timestamp)
        now = datetime.now()
        delta = now - message_time

        seconds = delta.total_seconds()
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24

        if days > 0:
            return f"{int(days)}d"
        elif hours > 0:
            return f"{int(hours)}hr"
        elif minutes > 0:
            return f"{int(minutes)}m"
        else:
            return "0s"
    except ValueError:
        return "Invalid time"

def display_group_chat(messages, chat_key, selected_group, user):
    start_auto_refresh()
    """Display the chat history with sender usernames inside their messages."""
    clear_screen()
    print(Fore.BLUE + "=" * 40)
    print(Back.CYAN + Style.BRIGHT + Fore.BLUE + f"{selected_group} Group Chat".center(40))
    print(Fore.CYAN + "=" * 40)
    
    terminal_width = get_terminal_width()
    message_width = terminal_width - 4  # Leave some padding for borders

    if chat_key in messages:
        print(Fore.BLUE + "\n"+"Chat History".center(40))
        print(Fore.BLUE+"="*40)
        for message in messages[chat_key]:
            sender_username = message['sender']  # Get the actual sender's username

            if sender_username == user['username']:
                # Right-aligned message box with username inside
                formatted_message = format_message_box(message['message'], width=message_width, align='right')
                print(Fore.GREEN + Style.DIM + f"{sender_username}".rjust(message_width) + Style.RESET_ALL)
                print(Fore.BLUE + Back.WHITE + formatted_message + Style.RESET_ALL)
            else:
                # Left-aligned message box with username inside
                formatted_message = format_message_box(message['message'], width=message_width, align='left')
                print(Fore.GREEN + Style.DIM + f"{sender_username}".ljust(message_width) + Style.RESET_ALL)
                print(Fore.WHITE + Back.BLUE + formatted_message + Style.RESET_ALL)
            
            # Display the time difference below the message
            time_diff = format_time_difference(message['timestamp'])
            print(Fore.RED + Style.DIM + f"({time_diff})" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nNo messages yet.")
    print(Fore.CYAN + "_" * 40)
    
def group_chat(user, selected_group):
    clear_screen()
    
    # Load messages from the file
    try:
        with open("gmessages.json", "r") as file:
            messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messages = {}  # Initialize if the file is empty or invalid

    # Generate a unique chat key based on the group name
    chat_key = f"group_{selected_group}"
    
    # Display chat history for the group
    display_group_chat(messages, chat_key, selected_group, user)

    while True:
        user_input = input(Fore.CYAN + "\nType a message, (or type 'exit' to leave the chat): ")
        if user_input.lower()== 'refresh':
            display_group_chat(messages, chat_key, selected_group, user)
        if user_input.lower() == 'exit':
            return my_groups(user, groups)
        
        if user_input.startswith('delete/'):
            command = user_input[7:]
            if command == 'all':
                # Delete all messages sent by the user
                deleted_count = delete_all_user_messages(messages, chat_key, user)
                print(Fore.RED + f"Deleted {deleted_count} messages sent by you.")
            else:
                # Delete messages containing the specified text
                deleted_count = delete_messages(messages, chat_key, command)
                print(Fore.RED + f"Deleted {deleted_count} messages containing '{command}'.")
            
            # Save the updated messages to gmessages.json
            with open("gmessages.json", "w") as file:
                json.dump(messages, file, indent=4)
            
            # Redisplay chat history
            display_group_chat(messages, chat_key, selected_group, user)
            continue
        
        new_message = {
            "sender": user['username'],
            "message": user_input,
            "timestamp": datetime.now().isoformat()  # Store timestamp in ISO format
        }
        
        if chat_key not in messages:
            messages[chat_key] = []
        
        messages[chat_key].append(new_message)
        
        # Save the updated messages to gmessages.json
        with open("gmessages.json", "w") as file:
            json.dump(messages, file, indent=4)
        
        display_group_chat(messages, chat_key, selected_group, user)
        
        print(Fore.RED + Style.DIM + "(just now)" + Style.RESET_ALL)  # Display "just now" in a smaller font style
        time.sleep(0.5)
     
    return my_groups(user)

def delete_all_user_messages(messages, chat_key, user):
    """Delete all messages sent by the current user in a chat."""
    if chat_key in messages:
        original_count = len(messages[chat_key])
        messages[chat_key] = [msg for msg in messages[chat_key] if msg['sender'] != user['username']]
        deleted_count = original_count - len(messages[chat_key])
        return deleted_count
    return 0

def delete_messages(messages, chat_key, text):
    """Delete all messages that contain the specified text."""
    if chat_key in messages:
        original_count = len(messages[chat_key])
        messages[chat_key] = [msg for msg in messages[chat_key] if text not in msg['message']]
        deleted_count = original_count - len(messages[chat_key])
        return deleted_count
    return 0
        
def new_message():
    with open("gmessages.json", "w") as file:
            json.dump(messages, file, indent=4)
  
load_json(GROUPS_FILE)
load_json(USERS_FILE)
load_json(FUSERS_FILE)        
def search(user, group):
    while True:
        load_json(GROUPS_FILE)
        load_json(USERS_FILE)
        load_json(FUSERS_FILE)
        clear_screen()  # Invoke the clear screen function
        print(Fore.CYAN + "=" * 40)
        print(Back.BLUE + Style.BRIGHT + Fore.CYAN + "🔍 SEARCH".center(40))
        print(Fore.CYAN + "=" * 40)
        print(Fore.BLUE+"Discover more".center(40))
        print(Fore.CYAN+"_"*40)
        print(Fore.BLUE+"\n1. 🫂 Groups   |   2. 👥 Friends")
        print(Fore.CYAN+"_"*40)
        print(Fore.BLUE + "\n0. Back")
        print(Fore.CYAN + "_" * 40)
    
        cb = input(Fore.BLUE + "\nwhat do you want to Discover? "+Style.RESET_ALL)
        if cb == '0':
            return user_dashboard(user, email)
        elif cb == '1':
            find_groups(user, groups)
        elif cb == '2':
            find_friends(user, friends)
        else:
            print(Fore.RED+"invalid Input")
            return search(user, group)
  
GROUPS_FILE = 'groups.json'
groups = load_json(GROUPS_FILE)

def find_groups(user, groups):
    while True:
        GROUPS_FILE = 'groups.json'
        groups = load_json(GROUPS_FILE)
        load_json(GROUPS_FILE)
        clear_screen()
        print(Fore.BLUE + "=" * 40)
        print(Back.CYAN + Style.BRIGHT + Fore.BLUE + "Discover Groups".center(40))
        print(Fore.BLUE + "=" * 40)
    
        fg = input(Fore.CYAN + "\nEnter the name of the group to discover or 0 to go back: "+ Style.RESET_ALL).strip()
    
        if fg == '0':
            return search(user, groups)  # Return to search or previous function
    
        group_found = False
    
        # Loop through groups to find a match
        for group_name in groups.keys():
            if fg.lower() == group_name.lower():  # Case-insensitive match
                group_found = True
                print(Fore.CYAN + f"Group found: {group_name}")
            
                # Prompt the user to join the group
                jg = input(Fore.BLUE + "\nDo you want to join this group? (Yes/No): ").strip().lower()
                if jg == 'yes':
                    save_group(user, group_name)
                    return  # Exit after joining
                elif jg == 'no':
                    print(Fore.RED + "Canceling...")
                    time.sleep(0.9)
                    return find_groups(user, groups)  # Allow the user to search again
                else:
                    print(Fore.RED + "Invalid input.")
                    time.sleep(0.9)
                    return find_groups(user, groups)  # Re-prompt after invalid input
    
        # If no group was found
        if not group_found:
            print(Fore.RED + f"No group found with the name '{fg}'.")
            time.sleep(1.5)
            return find_groups(user, groups)  # Return to search again
            
def save_group(user, group_name):
    while True:
        groups = load_json(GROUPS_FILE)
    
        # Check if the user is already a member of the group
        if user['username'] in groups[group_name]['members']:
            print(Fore.RED + "You are already a member of this group.")
            time.sleep(0.7)
            return
    
    # Add the user to the group members list
        groups[group_name]['members'].append(user['username'])
    
    # Save the updated groups to the file
        save_json(GROUPS_FILE, groups)
    
        print(Fore.GREEN + "Joined the group successfully.")
        time.sleep(0.7)
    
        return search(user, group_name)

width = os.get_terminal_size().columns   
USERS_FILE = 'users.json'
FUSERS_FILE = 'friends.json'  # Assuming this is the file where friends are stored

users = load_json(USERS_FILE)
friends = load_json(FUSERS_FILE)

def find_friends(user, group):
    while True:
        clear_screen()
        print(Fore.CYAN + "=" * width)
        print(Back.BLUE + Style.BRIGHT + Fore.CYAN + center_text("Find a Friend"))
        print(Fore.CYAN + "=" * width)
        
        ff = input(Fore.BLUE + "\nWhat is your friend's username or 0 to go Back: " + Style.RESET_ALL)
        
        if ff == '0':
            return search(user, group)

        # Check if the input username is the logged-in user's username
        if ff == user['username']:
            print(Fore.CYAN + "You are trying to search for yourself 🫤")
            time.sleep(1.3)
            return search(user, group)

        # Initialize user_found flag
        user_found = False
        
        # Loop through the users to find the username
        for user_data in users.values():
            if ff == user_data['username']:
                user_found = True
                clear_screen()
                print(Fore.CYAN + "=" * width)
                print(Back.YELLOW + Style.BRIGHT + Fore.BLUE + center_text(f"{user_data['name']}"))
                print(Fore.CYAN + "=" * width)
                print("\n" + center_text(f"{user_data['user_emoji']}"))
                print(Fore.BLUE + center_text(f"{user_data['name']}"))

                # Display bio, country, and sex
                print(Fore.YELLOW + "\n" + center_text(f"{user_data.get('bio', 'No bio')}"))
                print(Fore.BLUE + "\n" + center_text(f"{user_data.get('country', 'No country')}"))
                print(Fore.YELLOW + "\n" + center_text(f"{user_data.get('sex', 'No marital status')}"))

                print(Fore.CYAN + "_" * width)
                cm = input(Fore.BLUE + "\nAdd friend (y/n): " + Style.RESET_ALL)
                
                if cm.lower() == 'y':
                    save_friend(user, ff)
                    print(Fore.GREEN + "Friend added successfully!")
                elif cm.lower() == 'n':
                    print("Cancelling...")
                    time.sleep(0.9)
                    return search(user, group)
                else:
                    print(Fore.RED + "Invalid input")
                    time.sleep(0.9)
                    return search(user, group)

        # If the user is not found
        if not user_found:
            print(Fore.YELLOW + "\nNo user found 🚫")
            time.sleep(0.9)
            return search(user, group)
        
def save_friend(user, friend_username):
    while True:
        friends = load_json(FUSERS_FILE)
    
    # Check if they are already friends
        if user['username'] in friends and friend_username in friends[user['username']]:
            print("\nYou are both already friends")
            time.sleep(1.4)
            return search(user, group)
    
    # Add user to the friends list if they are not already in the file
        if user['username'] not in friends:
            friends[user['username']] = []
    
    # Add the friend's username to the user's friends list
        friends[user['username']].append(friend_username)
    
    # Add the user's username to the friend's list to ensure mutual friendship
        if friend_username not in friends:
            friends[friend_username] = []
    
        if user['username'] not in friends[friend_username]:
            friends[friend_username].append(user['username'])
        
    # Save the updated friends list to the file
        save_json(FUSERS_FILE, friends)
        print(Fore.GREEN+"\nFriend request sent")
        time.sleep(1.6)
    
        return search(user, group)        
        
def my_friends(user, friends):
    while True:
        clear_screen()
        friends_list = load_json(FUSERS_FILE).get(user['username'], [])  # Load the friends list for the user
    
        print(Fore.BLUE+"="*40)
        print(Back.CYAN+Style.BRIGHT+Fore.BLUE+"FRIENDS".center(40))
        print(Fore.BLUE+"="*40)
    
        if not friends_list:  # If the user has no friends
            print(Fore.CYAN+"\nYou have no friends.")
            print(Fore.BLUE+"="*40)
            time.sleep(1.5)
            return user_dashboard(user)
    
    # Display the list of friends
        print(Fore.BLUE+"\n0. ↩️ Back")
        print(Fore.CYAN+"_"*40)
        for idx, friend in enumerate(friends_list, 1):
            print(Fore.GREEN+f"\n{idx}. {friend}")
    
        print(Fore.CYAN+"_"*40)
    
    # Prompt user to select a friend
        cf = input("\nOpen a chat with a specific friend (number): ")
    
        if cf == '0':  # Option to go back
            return user_dashboard(user)
    
    # Validate the user input and open the chat
        if cf.isdigit() and 1 <= int(cf) <= len(friends_list):
            selected_index = int(cf)
            selected_friend = friends_list[selected_index - 1]
            print(f"\nOpening chat with {selected_friend}...")
            time.sleep(1.5)
            return chat(user, selected_friend)  # Call the chat function with the selected friend
        else:
            print("\nInvalid input. Returning to the friends list...")
            time.sleep(1.5)
            return my_friends(user, friends)
width = os.get_terminal_size().columns   
def settings(user):
    clear_screen()
    print(Fore.BLUE+"="*width)
    print(Back.CYAN+Style.BRIGHT+Fore.MAGENTA+"Account settings".center(40))
    print(Fore.BLUE+"="*width)
    print(Fore.GREEN+f"{user['name']}".center(40))
    print(Fore.BLUE+"_"*width)
    print(Fore.CYAN+"\n1. 👤 Change Name  |  2. 🔐 Change Pass")
    print(Fore.BLUE+"_"*width)
    print(Fore.CYAN+"\n3. Change Email   |   4. Help")
    print(Fore.BLUE+"_"*width)
    print(Fore.CYAN+"\n5. Add country   | 6. Add Sex")
    print(Fore.BLUE+"_"*width)
    print(Fore.CYAN+"\n7. Add bio   |   8. Add Age")
    print(Fore.BLUE+"_"*width)
    print(Fore.CYAN+"\n0. Back")
    print(Fore.BLUE+"_"*width)
    st=input(Fore.YELLOW+"\ninput an Option: ")
    if st == '0':
        return user_dashboard(user)
    elif st == '1':
        change_name(user)
    elif st == '2':
        change_password(user)
    elif st == '3':
        change_email(user)
    elif st == '5':
        users = load_json(USERS_FILE)
        country = input(Fore.BLUE + "\nWhat is your country: " + Style.RESET_ALL)
        email = input(Fore.BLUE+"What is your current email: ")
        if email in users:
            users[email]['country'] = country  # Update the user's country
            save_json(USERS_FILE, users)  # Save changes to the JSON file
            print(Fore.GREEN + f"Country updated to {country}")
            time.sleep(0.9)
            return settings(user)
        else:
            print(Fore.RED + "Please input a valid email of yours.")
            time.sleep(0.8)
            return settings(user)
    elif st == '4':
        clear_screen()
        print(Fore.GREEN+"="*width)
        print(Fore.BLUE+"Help Center")
        print(Fore.GREEN+"="*40)
        print(Fore.BLUE+"\nDelete_messages: example: delete/hello bro, will delete hello bro ")
        print(Fore.YELLOW+"deleted_all_message: example:- delete/all will delete all messages ")
        xc=input("input 0 to Return: ")
        if xc == '0':
            return settings(user)
    elif st == '6':
        users = load_json(USERS_FILE)
        sex = input(Fore.BLUE + "\nWhat is your marital status: " + Style.RESET_ALL)
        email = input(Fore.BLUE + "\nYour current email: " + Style.RESET_ALL)

    # Assuming the logged-in user's email is in the 'user' dictionary
        logged_in_email = next((key for key, value in users.items() if value == user), None)

        if email != logged_in_email:  # Validate that the entered email matches the logged-in user
            print(Fore.RED + "\n🚨 This email does not match your logged-in account.")
            time.sleep(0.9)
            return settings(user)
        elif email in users:  # Check if the email exists in users
            users[email]['sex'] = sex  # Update marital status (sex) in the user data
            save_json(USERS_FILE, users)  # Save changes to the file
            print(Fore.GREEN + f"\nYour marital status is updated to {sex}")
            time.sleep(0.8)
            return settings(users[email])  # Pass the updated user's data to the settings function
    elif st == '7':
        users = load_json(USERS_FILE)
        bio = input(Fore.BLUE + "\nWhat is your bio write up: " + Style.RESET_ALL)
        email = input(Fore.BLUE + "\nYour current email: " + Style.RESET_ALL)

    # Assuming the logged-in user's email is in the 'user' dictionary
        logged_in_email = next((key for key, value in users.items() if value == user), None)

        if email != logged_in_email:  # Validate that the entered email matches the logged-in user
            print(Fore.RED + "\n🚨 This email does not match your logged-in account.")
            time.sleep(0.9)
            return settings(user)
        elif email in users:  # Check if the email exists in users
            users[email]['bio'] = bio  # Update marital status (sex) in the user data
            save_json(USERS_FILE, users)  # Save changes to the file
            print(Fore.GREEN + f"\nYour marital status is updated to {bio}")
            time.sleep(0.8)
            return settings(users[email])  # Pass the updated user's data to the settings function
    elif st == '8':
        age(user)
        
    else:
        print(Fore.RED+"Invalid input")
        return settings(user)
    
def change_name(user):
    users = load_json(USERS_FILE)
    new_name = input(Fore.BLUE + "\nWhat is your new name: " + Style.RESET_ALL)
    current_password = input(Fore.BLUE+"What is your current password ")
    if current_password != user['password']:
        print(Fore.RED+"Incorrect password")
        time.sleep(0.9)
        return settings(user)
    elif current_password == user['password']:
        email = input(Fore.BLUE + "\nYour current email: " + Style.RESET_ALL)

    # Assuming the logged-in user's email is in the 'user' dictionary
        logged_in_email = next((key for key, value in users.items() if value == user), None)

        if email != logged_in_email:
        # Validate that the entered email matches the logged-in user
            print(Fore.RED + "\n🚨 This email does not match your logged-in account.")
            time.sleep(0.9)
            return settings(user)
        elif email in users:
        # Check if the email exists in users
            users[email]['name'] = new_name  # Update marital status (sex) in the user data
        save_json(USERS_FILE, users)  # Save changes to the file
        print(Fore.GREEN + f"\nYour name is updated to {new_name}")
        time.sleep(0.8)
        return settings(users[email])  # Pass the updated user's data to the settings function
        
def age(user):
    users = load_json(USERS_FILE)
    age = input(Fore.BLUE + "\nWhat is your age: " + Style.RESET_ALL)
    email = input(Fore.BLUE + "\nYour current email: " + Style.RESET_ALL)

    # Assuming the logged-in user's email is in the 'user' dictionary
    logged_in_email = next((key for key, value in users.items() if value == user), None)

    if email != logged_in_email:
        # Validate that the entered email matches the logged-in user
        print(Fore.RED + "\n🚨 This email does not match your logged-in account.")
        time.sleep(0.9)
        return settings(user)
    elif email in users:
        # Check if the email exists in users
        users[email]['age'] = age  # Update marital status (sex) in the user data
        save_json(USERS_FILE, users)  # Save changes to the file
        print(Fore.GREEN + f"\nYour age is updated to {age}")
        time.sleep(0.8)
        return settings(users[email])  # Pass the updated user's data to the settings function
    
def change_password(user):
    users = load_json(USERS_FILE)
    current_password = input(Fore.BLUE + "\nWhat is your current password 🙈: " + Style.RESET_ALL)
    if user['password'] == current_password:
        new_password =input(Fore.BLUE+"\n Your new password 🙈: "+Style.RESET_ALL)
        if new_password == current_password:
            print(Fore.RED+"\nThis is your old password")
            time.sleep(0.9)
            return settings(user)
        elif new_password != current_password:
            email = input(Fore.BLUE + "\nYour current email: " + Style.RESET_ALL)

    # Assuming the logged-in user's email is in the 'user' dictionary
            logged_in_email = next((key for key, value in users.items() if value == user), None)

            if email != logged_in_email:  # Validate that the entered email matches the logged-in user
                print(Fore.RED + "\n🚨 This email does not match your current email.")
                time.sleep(0.9)
                return settings(user)
            elif email in users:  # Check if the email exists in users
                users[email]['password'] = new_password  # Update marital status (sex) in the user data
                save_json(USERS_FILE, users)  # Save changes to the file
                print(Fore.GREEN + f"\nYour password is updated to {new_password}")
                time.sleep(0.8)
                return settings(users[email])  # Pass the updated user's data to the settings function
    else:
        print(Fore.RED+"Incorrect password")
        time.sleep(0.9)
        return settings(user)
            
def change_email(user):
    users = load_json(USERS_FILE)
    new_email = input(Fore.BLUE + "\nWhat is your new email: " + Style.RESET_ALL)

    if new_email in users:
        print(Fore.RED + "\nThis email already exists with an account.")
        time.sleep(0.9)
        return settings(user)

    # No need for elif new_email not in users since the first condition handles it
    current_password = input(Fore.BLUE + "What is your current Password: " + Style.RESET_ALL)

    if user['password'] == current_password:
        email = input(Fore.BLUE + "\nYour current email: " + Style.RESET_ALL)

        # Assuming the logged-in user's email is in the 'user' dictionary
        logged_in_email = next((key for key, value in users.items() if value == user), None)

        if email != logged_in_email:  # Validate that the entered email matches the logged-in user
            print(Fore.RED + "\n🚨 This email does not match your current email.")
            time.sleep(0.9)
            return settings(user)

        # Check if the email exists in users and update the email
        user_data = users.pop(email)
        users[new_email] = user_data

        # Update the email in the current session (user object)
        user = users[new_email]  # Reflect the email change in the current user object

        # Save the updated users data
        save_json(USERS_FILE, users)

        print(Fore.GREEN + f"\nYour email has been updated to {new_email}.")
        time.sleep(0.8)

        return settings(user)  # Pass the updated user object to the settings function
    else:
        print(Fore.RED + "Incorrect password.")
        time.sleep(0.9)
        return settings(user)
        
def get_terminal_width():
    """Get the width of the terminal."""
    try:
        return shutil.get_terminal_size((80, 20)).columns
    except Exception as e:
        print(f"Error detecting terminal size: {e}")
        return 80  # Default width if detection fails

def format_message_box(message, width=30, align='left'):
    """Format a message into a box with specified width and alignment."""
    lines = textwrap.wrap(message, width=width)
    if align == 'right':
        lines = [line.rjust(width) for line in lines]
    elif align == 'left':
        lines = [line.ljust(width) for line in lines]

    box = '\n'.join(f"║ {line} ║" for line in lines)
    top_bottom_border = '╔' + '═' * (width + 2) + '╗'
    
    return top_bottom_border + '\n' + box + '\n' + '╚' + '═' * (width + 2) + '╝'

def format_time_difference(timestamp):
    """Format time difference from timestamp to now, showing only the largest relevant time unit."""
    try:
        message_time = datetime.fromisoformat(timestamp)
        now = datetime.now()
        delta = now - message_time

        seconds = delta.total_seconds()
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24

        if days > 0:
            return f"{int(days)}d"
        elif hours > 0:
            return f"{int(hours)}hr"
        elif minutes > 0:
            return f"{int(minutes)}ms"
        else:
            return "0ms"

    except ValueError:
        return "Invalid time"

def display_chat_history(messages, chat_key, selected_friend, user):
    """Display the chat history with proper message alignment."""
    clear_screen()
    print(Fore.BLUE + "=" * 40)
    print(Back.CYAN + Style.BRIGHT + Fore.BLUE + f"Chats with {selected_friend}".center(40))
    print(Fore.CYAN + "=" * 40)
    
    terminal_width = get_terminal_width()
    message_width = terminal_width - 4  # Leave some padding for borders

    if chat_key in messages:
        print(Fore.BLUE + "\n"+"Chat History".center(40))
        for message in messages[chat_key]:
            if message['sender'] == user['username']:
                # Sender's message (right-aligned with blue background)
                formatted_message = format_message_box(message['message'], width=message_width, align='right')
                print(Fore.BLUE + Back.WHITE + formatted_message + Style.RESET_ALL)
            else:
                # Receiver's message (left-aligned with white background)
                formatted_message = format_message_box(message['message'], width=message_width, align='left')
                print(Fore.WHITE + Back.BLUE + formatted_message + Style.RESET_ALL)
            
            # Print timestamp in a smaller font style
            time_diff = format_time_difference(message['timestamp'])
            print(Fore.RED + Style.DIM + f"({time_diff})" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nNo messages yet.")
    
    print(Fore.CYAN + "_" * 40)
    time.sleep(0.9)

def delete_messages(messages, chat_key, text):
    """Delete messages containing the specified text."""
    if chat_key in messages:
        original_length = len(messages[chat_key])
        messages[chat_key] = [msg for msg in messages[chat_key] if text not in msg['message']]
        return original_length - len(messages[chat_key])
    return 0

def delete_all_user_messages(messages, chat_key, user):
    """Delete all messages sent by the specified user."""
    if chat_key in messages:
        original_length = len(messages[chat_key])
        messages[chat_key] = [msg for msg in messages[chat_key] if msg['sender'] != user['username']]
        return original_length - len(messages[chat_key])
    return 0

def chat(user, selected_friend):
    clear_screen()
    
    # Try to load the messages from the file, handle if file is empty or missing
    try:
        with open("messages.json", "r") as file:
            messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):  # Catch missing or invalid file
        messages = {}  # Initialize an empty dictionary if file is empty or invalid

    # Generate a unique chat key using both usernames (sorted alphabetically)
    chat_key = f"{min(user['username'], selected_friend)}-{max(user['username'], selected_friend)}"
    
    # Display initial chat history
    display_chat_history(messages, chat_key, selected_friend, user)

    # Input loop to keep the chat active
    while True:
        user_input = input(Fore.CYAN + "\nType a message, (or type 'exit' to leave the chat): ")
        
        if user_input.lower() == 'exit':
            return my_friends(user, friends)
        
        if user_input.startswith('delete/'):
            command = user_input[7:]
            if command == 'all':
                # Delete all messages sent by the user
                deleted_count = delete_all_user_messages(messages, chat_key, user)
                print(Fore.RED + f"Deleted {deleted_count} messages sent by you.")
            else:
                # Delete messages containing the specified text
                deleted_count = delete_messages(messages, chat_key, command)
                print(Fore.RED + f"Deleted {deleted_count} messages containing '{command}'.")
            
            # Save the updated messages to messages.json
            with open("messages.json", "w") as file:
                json.dump(messages, file, indent=4)
            
            # Redisplay chat history
            display_chat_history(messages, chat_key, selected_friend, user)
            continue

        # Create a new message entry
        new_message = {
            "sender": user['username'],
            "message": user_input,
            "timestamp": datetime.now().isoformat()  # Store timestamp in ISO format
        }

        # Add the message to the conversation history
        if chat_key not in messages:
            messages[chat_key] = []
        
        messages[chat_key].append(new_message)
        
        # Save the updated messages to messages.json
        with open("messages.json", "w") as file:
            json.dump(messages, file, indent=4)

        # Immediately display the sent message in chat history
        display_chat_history(messages, chat_key, selected_friend, user)
        
        print(Fore.RED + Style.DIM + "(just now)" + Style.RESET_ALL)  # Display "just now" in a smaller font style
        time.sleep(0.5)  # Simulate message being sent

    return my_friends(user, friends)  # Return to the friends list after exiting the chat

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')    
        
def wsr_fund(user, email):
    while True:
        clear_screen()
        print(Fore.CYAN + "="*40)
        print(Back.CYAN + Style.BRIGHT + Fore.BLUE + "WHISPER FUNDRAISER".center(40))
        print(Fore.CYAN + "="*40)
        print(Fore.BLUE + f"Welcome {user['name']}".center(40))
        print(Fore.CYAN + "_"*40)
        print(Fore.BLUE + "\n1. 🚆 Support WHISPER  |  2. 💲 Monetize")
        print(Fore.CYAN + "_"*40)
        print(Fore.BLUE + "\n0. Back")
        print(Fore.CYAN + "_"*40)

        choice = input("\nPick a choice or press enter 0 to go back....: ")
        
        if choice == '1':
            support(user)  # Ensure this function is defined elsewhere
            break
        elif choice == '2':
            monetize(user)  # Ensure this function is defined elsewhere
            break
        elif choice == '0' or choice == '':
            return user_dashboard(user, email)
        else:
            print(Fore.RED + "Invalid input, please try again.")
            time.sleep(2)
            
def support(user):
    clear_screen()
    btc="bc1qujwwt6gy9j5tfrapjgz6avfdh5xlt6huh4zk64"
    print(Fore.BLUE+"="*40)
    print(Back.CYAN+Style.BRIGHT+Fore.BLUE+"Support WHISPER".center(40))
    print(Fore.BLUE+"="*40)
    print(Fore.CYAN+"\n1. Support With BTC")
    print(Fore.BLUE+"_")
    print(Fore.CYAN+"0. Back")
    print(Fore.BLUE+"_"*40)
    choiice=input("\n pick an option: ")
    if choiice == '0':
        return wsr_fund(user)
    elif choiice == '1':
        print(Fore.GREEN+ f"Make a support to the address: {btc}")
        ret=input("input 0 to go back... ")
        if ret == '0':
            return wsr_fund(user)
        else:
            print(Fore.RED+"Invalid input")
            return wsr_fund(user)
    else:
        print(Fore.RED+"invalid input")
        time.sleep(1.5)
        return support(user) 
        
def monetize(user):
    clear_screen()
    print(Fore.CYAN + "=" * 40)
    print(Back.CYAN+ Style.BRIGHT+Fore.BLUE + f"Welcome to WHISPER Monetizing {user['name']}".center(40))
    print(Fore.CYAN + "=" * 40)
    print(Fore.RED + "\nComing soon...")
    fo = input(Fore.CYAN + "Enter 0 to return... ")
    if fo == '0':
        return wsr_fund(user)
    else:
        print(Fore.RED+"invalid input")
        return monetize(user)             
            
def main_menu():
    while True:
        # Start refreshing data automatically
        start_auto_refresh() 
        clear_screen()
        loading_az()
        clear_screen()
        print(Fore.CYAN + "="*40)
        print(Back.CYAN+ Style.BRIGHT+Fore.BLUE +"️DE WORLD 🌏".center(40))
        print(Fore.CYAN + "="*40)
        print(Fore.RED + "By proceeding, you agree to keep your information encrypted and stored under your service.".center(40))
        print(Fore.CYAN + "_"*40)
        print(Fore.BLUE + "\n1. Login   |   Exit [CTRL+Z]")
        print(Fore.CYAN+"_"*40)
        print(Fore.BLUE + "\n2. Create an account")
        print(Fore.CYAN+"_"*40)
        choice = input(Fore.CYAN + "\nPick a choice: "+Style.RESET_ALL)
        
        if choice == '1':
            clear_screen()
            print(Fore.CYAN + "="*40)
            print(Back.CYAN+ Style.BRIGHT+Fore.BLUE + "DE WORLD 🌏".center(40))
            print(Fore.CYAN + "="*40)
            print(Fore.BLUE + "Login to your account".center(40))
            print(Fore.CYAN + "_"*40)
            email = input(Fore.CYAN + "\nEnter your email: "+Style.RESET_ALL)
            password = input(Fore.GREEN + "\nEnter your password 🙈: "+Style.RESET_ALL)
            login_user(email, password)
            
        elif choice == '2':
            clear_screen()
            print(Fore.CYAN + "="*40)
            print(Back.BLUE+ Style.BRIGHT+Fore.BLUE + "JOIN DE WORLD 🌏".center(40))
            print(Fore.CYAN + "="*40)
            print(Fore.GREEN+"\n Create an account and connect with friends and family privately.".center(40))
            print(Fore.CYAN + "_"*40)
            name = input(Fore.BLUE + "\nWhat is your full name: "+Style.RESET_ALL)
            email = input(Fore.CYAN+"\nWhat is your email: "+Style.RESET_ALL)
            password = input(Fore.BLUE + "\nCreate a password 🙈: "+Style.RESET_ALL)
            pin= input(Fore.GREEN+"\nCreate a pin 🙈: "+Style.RESET_ALL)
            username = register_user(name, email, password, pin)
            if username:
                print(Fore.GREEN + f"\nYour DE WORLD 🌏 account is created successfully! Username: {username}")
                input("\nPress Enter to return to the main menu...")
                
        elif choice == '0':
            loading_az()
            print(Fore.RED + "Exiting...")
            time.sleep(4)
            clear_screen()
            break
            
        else:
            print(Fore.RED + "\nInvalid input.")
            time.sleep(2)
            return main_menu()
            
if __name__ == "__main__":
    main_menu()                    
# Start refreshing data automatically
start_auto_refresh()             
            