
from handlers.customer_handler import *
from handlers.line_item_handler import *
from handlers.order_handler import *
from handlers.payment_handler import *
from handlers.product_handler import *
from handlers.cart_handler import *

from objects.customer_object import *
from objects.line_item_object import *
from objects.order_object import *
from objects.payment_object import *

import curses

try:
    class Meow():
        def __init__(self):
            # init curses
            self.screen = curses.initscr()
            self.current_user = None
            self.unlogged_in_menu()

        def unlogged_in_menu(self):

            # 1. log in to a user (user_menu)
            # 2. create a new user (create_new_user)
            # 3. view available products (shop_menu)
            # 4. generate report (generate_popularity_report)
            # 5. exit.
            self.screen.clear()
            self.screen.border(0)
            self.screen.addstr(12, 40, "1. Log in to a user")
            self.screen.addstr(13, 40, "2. Create a new user")
            self.screen.addstr(14, 40, "3. View available products")
            self.screen.addstr(15, 40, "4. Generate report")
            self.screen.addstr(16, 40, "5. Exit")
            self.screen.refresh()

            try:
                choice = int(chr(self.screen.getch()))

                if (choice == 1):  # Log in
                    self.user_menu()

                elif (choice == 2):  # Create a new user
                    self.create_new_user()

                elif (choice == 3):  # View available products
                    self.shop_menu()

                elif (choice == 4):  # Generate report
                    self.generate_popularity_report()

                elif (choice == 5):  # Exit
                    curses.endwin()
                    exit()
                else:
                    self.unlogged_in_menu()

            except ValueError:
                self.unlogged_in_menu()

        def logged_in_menu(self):
            # print the logged-in menu options.
            # request input.
            # based on input, do:
            # 1. log out (reset_user)
            # 2. shop(shop_menu)
            # 3. payment options(payment_menu)
            # 4. product report (generate_popularity_report)
            # 5. view orders
            # 6. exit.
            pass

        def user_menu(self):
            # generate the user index. (generate_customer )
            # for each index, use get_value to print the name value.
            # request input for which user.
            pass

        def create_new_user(self):
            # request input for all the things.
            # pass all the input into the create_new_user.
            # set the current user to the UID that returns,
            # then print the logged in menu.
            pass

        def set_user(user_id):
            # set user ID to current user.
            pass

        def reset_user(self):
            # set current user to none. that's it.
            pass

        def shop_menu(self):
                """
                This function prints a list of products and prices from products.txt, saved as a index-uid dictionary in a scoped product_menu variable.  Then it requests next_step input from the user. If the user is not logged in, the only subsequent options are to go back or exit. If the user is logged in, they have the option of adding an item to their cart (via product_menu) or completing their order via payment_options_menu.
                ==========
                Method Arguments: none.
                """
                # load_product_library and for each available product index, get_value to print the name and price.
                product_menu = generate_product_list("data/products.txt")
                for index, UID in product_menu.items():
                    info = get_value("data/products.txt", UID)
                    print("{0}. {1}-- ${2}".format(index, info["name"], info["price"]))
                # are you logged in or not?
                if self.current_user is not None:
                    # view your cart or note that it's empty.
                    self.view_cart()
                    print("press the number of the item you'd like to add to your cart,\nOr press'c' to check out, 'b' to go back, 'x' to exit.")
                    next_step = input("\n>>")
                    if next_step == "x":  # Exit.
                        print("goodbye.")
                        exit()
                    elif next_step == "b":  # Go back.
                        self.logged_in_menu()
                    elif next_step == "c":  # Check Out.
                        self.payment_options_menu(True)
                    else:
                        print(next_step)
                        try:  # Add a product to your cart.
                            next_step = int(next_step)
                        except ValueError:
                            self.shop_menu()
                        finally:
                            if next_step in product_menu.keys():
                                self.add_to_cart_menu(product_menu[next_step])
                            else:
                                print("command not recognized.")
                                self.shop_menu()
                else:
                    # if you're not logged in you can view products, but you can't do anything with a cart.
                    print("You are not logged in.\nPress 'b' to go back and choose a login option, or x to exit.")
                    next_step = input("\n>> ")
                    if next_step == "b":
                        self.unlogged_in_menu()
                    elif next_step == "x":
                        print("goodbye.")
                        exit()
                    else:
                        print("command_not_recognized.")
                        self.shop_menu()

        def view_cart():
            """
            Displays the content of the currently logged in user

            Args- None
            """
            # get the user object of the currently logged in user
            current_user_obj = get_value("data/users.txt", self.current_user)
            # get that users cart
            cart = current_user_obj.cart
            # check if cart is not empty
            if cart == {}:
                print("Your cart is empty. Start shopping!")
            else:
                print("Your cart:")
                print("*" * 44)
                # format for columns
                row_string = "{0:<18}{1:<11}${2:<14}"
                total_string = "{0:<29}${1:<14}"
                total_list = []
                # loop over cart items and calculate total (grab price from 'products.txt')
                for prod_id, qty in cart.items():
                    product_obj = get_value("data/products.txt", prod_id)
                    total = qty * product_obj["price"]
                    # append total to list of totals (for amount due calculation)
                    total_list.append(total)
                    # limit product name
                    product_name = product_obj.name
                    product_name = (product_name if len(product_name) <= 17 else product_name[:14] + "...") + " "
                    print(row_string.format(product_name, qty, total))
                print("*" * 44)
                # print out total amount due
                print(total_string.format("Total:", sum(total_list)))

        def convert_to_completed(payment_uid):
            # grab user name top-level variable.
            # generate a new order uid with that user name and the UID argument.
            # for each cart item, for qty number of times, generate a line item with the product number and order number.
            # return the order number.
            pass

        def payment_options_menu(completing=False):
            # pass user name top-level variable to generate_payment_list.
            # for each payment id in payment_list, use get_value to print the name or something.
            # if completing == false
            # request input to either add a new payment or go back.
            # if they'd like to add a new payment, request input for all the data,
            # then pass it to generate_new_payment and restart the function.
            # if completing == true
            # request input to either add a new payment or select a current payment.
            # if they'd like to add a new payment, request input for all the data,
            # then pass it to generate_new_payment and restart the function to print the updated list of payments.
            # if they select a current payment:
            # pass the payment uid to convert to completed.
            # print the order number, and print the top level logged-in menu.
            pass

        def view_orders(self):
            # THIS IS A BITCH. DO IT LATER.
            # pass user_name top_level variable to generate_order_list.
            # for each order, print the order ID then pass it into view_line_items(?)
            # use get_value to print all the order stuff.
            pass

        def generate_popularity_report(self):
            pass

    if __name__ == '__main__':
        # Meow().print_hey()
        # print_hello()
        # Meow().unlogged_in_menu()
        Meow()

except KeyboardInterrupt:
    curses.endwin()
