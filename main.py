def run_menu():
    while True:
        print("1. Approve request")
        print("2. Issue card")
        print("3. Return card")
        print("4. Quit") 
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("Request Approved!")
            print()
        elif choice == "2":
            print("Card Issued")
            print()
        elif choice == "3":
            print("Card Returned")
            print()
        elif choice == "4":
            print("Exitting...")
            break
        else:
            print(f"\n'{choice}' is not a valid option. Please enter 1, 2, 3 or 4.")
            print()

if __name__ == "__main__":
    run_menu()    