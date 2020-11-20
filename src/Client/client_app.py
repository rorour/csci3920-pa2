from client import Client


def display_menu():
    print("=" * 30)
    print(f'{"Message Board:":^30}')
    print("1. Connect to server")
    print("2. Login")
    print("3. Send Message")
    print("4. Print Received Messages")
    print("5. Disconnect")
    return int(input("Select option [1-5]"))


if __name__ == "__main__":
    # client = Client("127.0.0.1", 10000)
    keep_running = True
    is_connected = False
    is_logged_in = False

    while keep_running:
        option = display_menu()
        if option == 1:
            """Requests server and port and will connect to server"""
        elif option == 2:
            if is_connected:
                """Asks for user credentials and will authenticate the user to connected server"""
            else:
                print("Please connect to server first before logging in")
        elif option == 3:
            if is_connected and is_logged_in:
                """Sends message to target username"""
            else:
                print("Please connect to server and/or log in first")
        elif option == 4:
            if is_connected and is_logged_in:
                """Prints all pending messages and once done, returns to main menu"""
            else:
                print("Please connect to server and/or log in first")
        elif option == 5:
            """Disconnects from server"""
            is_connected = False
            is_logged_in = False
            keep_running = False

        else:
            print("Invalid input")
