import itertools


class User:
    __id_counter = itertools.count(1)  # Генератор ID

    def __init__(self, first_name, last_name, login, password, email):
        self.__user_id = f"{next(self.__id_counter):07d}"
        self.__first_name = first_name
        self.__last_name = last_name
        self.__login = login
        self.__password = password
        self.__email = email
        self.__access_level = "user"


    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_login(self):
        return self.__login

    def get_email(self):
        return self.__email

    def get_access_level(self):
        return self.__access_level

    def get_password(self):
        return self.__password

    def set_access_level(self, level):
        self.__access_level = level

    def get_public_info(self):
        return (f"ID: {self.__user_id}, Name: {self.__first_name} {self.__last_name}, "
                f"Email: {self.__email}, Access: {self.__access_level}")

    def check_password(self, password):
        return self.__password == password


class Admin(User):
    def __init__(self, first_name, last_name, login, password, email):
        super().__init__(first_name, last_name, login, password, email)
        self.set_access_level("admin")

    def add_user(self, users_list, first_name, last_name, login, password, email):
        new_user = User(first_name, last_name, login, password, email)
        users_list.append(new_user)
        print(f"User {new_user.get_user_id()} added.")

    def remove_user(self, users_list, user_id):
        for user in users_list:
            if user.get_user_id() == user_id:
                if isinstance(user, Admin) or isinstance(user, Owner):
                    print("⚠️ Admins and Owners cannot be deleted!")
                    return
                users_list.remove(user)
                print(f"User {user_id} has been removed.")
                return
        print("User not found.")


class Owner(Admin):
    def __init__(self, first_name, last_name, login, password, email):
        super().__init__(first_name, last_name, login, password, email)
        self.set_access_level("owner")

    def promote_to_admin(self, users_list, user_id):
        for i, user in enumerate(users_list):
            if user.get_user_id() == user_id and not isinstance(user, Admin):
                new_admin = Admin(user.get_first_name(), user.get_last_name(), user.get_login(),
                                  user._User__password, user.get_email())
                users_list[i] = new_admin
                print(f"✅ User {user_id} is now an Admin.")
                return
        print("❌ User not found or already an Admin.")

    def demote_admin(self, users_list, user_id):
        for i, user in enumerate(users_list):
            if user.get_user_id() == user_id and isinstance(user, Admin):
                new_user = User(user.get_first_name(), user.get_last_name(), user.get_login(),
                                user.get_password(), user.get_email())
                users_list[i] = new_user
                print(f"⚠️ Admin {user_id} has been demoted to User.")
                return
        print("❌ User not found or not an Admin.")

    def remove_user(self, users_list, user_id):
        for user in users_list:
            if user.get_user_id() == user_id:
                if isinstance(user, Owner):
                    print("🚫 Owners cannot be deleted!")
                    return
                if isinstance(user, Admin):
                    print("⚠️ Convert Admin to User before deletion.")
                    return
                users_list.remove(user)
                print(f"✅ User {user_id} has been removed.")
                return
        print("❌ User not found.")


users = []
owner = Owner("Nikolai", "Sokolov", "niksok", "123", "sokolov_nik@gmail.com")
users.append(owner)


def login():
    login = input("Enter login: ")
    password = input("Enter password: ")

    for user in users:
        if user.get_login() == login and user.check_password(password):
            print(f"Welcome, {user.get_first_name()}!")
            return user
    print("Invalid login or password.")
    return None


def register():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    login = input("Login: ")
    password = input("Password: ")
    email = input("Email: ")

    new_user = User(first_name, last_name, login, password, email)
    users.append(new_user)
    print(f"Registration complete! Your ID: {new_user.get_user_id()}")


# Основное меню
def main_menu(user):
    while True:
        print("\n1. View my info")
        print("2. View all users")
        if isinstance(user, Admin):
            print("3. Add user")
            print("4. Remove user")
        if isinstance(user, Owner):
            print("5. Promote to Admin")
            print("6. Demote Admin")
        print("7. Logout")

        choice = input("Select an option: ")
        if choice == "1":
            print(user.get_public_info())
        elif choice == "2":
            for u in users:
                print(u.get_public_info())
        elif choice == "3" and isinstance(user, Admin):
            first_name = input("First name: ")
            last_name = input("Last name: ")
            login = input("Login: ")
            password = input("Password: ")
            email = input("Email: ")
            user.add_user(users, first_name, last_name, login, password, email)
        elif choice == "4" and isinstance(user, Admin):
            user_id = input("Enter user ID to remove: ")
            user.remove_user(users, user_id)
        elif choice == "5" and isinstance(user, Owner):
            user_id = input("Enter user ID to promote: ")
            user.promote_to_admin(users, user_id)
        elif choice == "6" and isinstance(user, Owner):
            user_id = input("Enter user ID to demote: ")
            user.demote_admin(users, user_id)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid option.")


while True:
    print("\n1. Login")
    print("2. Register")
    print("3. Exit")

    option = input("Choose an option: ")
    if option == "1":
        user = login()
        if user:
            main_menu(user)
    elif option == "2":
        register()
    elif option == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")
