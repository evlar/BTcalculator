
import dataclasses
import tkinter as tk
import requests

class ValidatorApp:
    def __init__(self, root):
        self.root = root
        self.validator_info = {}
        self.setup_gui()
        self.loaded_coldkeys = {} 
        #self.root.after(100, self.fetch_and_update_network_stats)
        #self.root.after(100, self.fetch_and_update_validator_stats)

    def setup_gui(self):
        self.root.title("Validator Calculator")
        self.root.minsize(800, 600)

        padx = 10
        pady = 5

        # Network Stats Frame
        self.network_stats_frame = tk.LabelFrame(self.root, text="Network Stats", padx=85, pady=pady)
        self.network_stats_frame.grid(row=0, column=0, sticky="nw", padx=padx, pady=pady)

        # Validator Stats Frame
        self.validator_stats_frame = tk.LabelFrame(self.root, text="Validator Stats", padx=85, pady=pady)
        self.validator_stats_frame.grid(row=0, column=1, sticky="ne", padx=padx, pady=pady)

        # Coldkey Entry Frame
        self.validator_calculator_frame = tk.LabelFrame(self.root, text="", padx=padx, pady=pady)
        self.validator_calculator_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=padx, pady=pady)
        # Coldkey Display Frame extension
    
        self.coldkey_display_frame = tk.LabelFrame(self.validator_calculator_frame, text="Loaded Coldkeys", padx=padx, pady=pady)
        self.coldkey_display_frame.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.coldkey_listbox = tk.Listbox(self.coldkey_display_frame, width=85)
        self.coldkey_listbox.grid(row=0, column=0, sticky="ew")

        # Add a Reset Button next to the Coldkey Listbox
        self.reset_button = tk.Button(self.coldkey_display_frame, text="Reset", command=self.reset_calculator)
        self.reset_button.grid(row=0, column=1, padx=5, pady=5)

        # Submit Coldkey Button
        self.submit_coldkey_button = tk.Button(self.validator_calculator_frame, text="Load Nominator Data", command=self.load_nominator_data)
        self.submit_coldkey_button.grid(row=0, column=2, sticky="w")

        # Status Message Label
        self.status_message_label = tk.Label(self.validator_calculator_frame, text="")
        self.status_message_label.grid(row=3, column=0, columnspan=3)

        # New Frame for Username Entry, Save User Data Button, and Load User Data Button
        self.user_data_frame = tk.LabelFrame(self.validator_calculator_frame, text="User Data", padx=padx, pady=pady)
        self.user_data_frame.grid(row=4, column=0, columnspan=3, sticky="ew")

        # Username Entry
        tk.Label(self.user_data_frame, text="Username:").grid(row=0, column=0, sticky="e")
        self.username_entry = tk.Entry(self.user_data_frame, width=10)  # Set the width to your desired value
        self.username_entry.grid(row=0, column=1, sticky="e")

        # Save User Data Button
        self.save_user_data_button = tk.Button(self.user_data_frame, text="Save User Data", command=self.save_user_data)
        self.save_user_data_button.grid(row=0, column=2, sticky="w", padx=5)

        # Load User Data Button
        self.load_user_data_button = tk.Button(self.user_data_frame, text="Load User Data", command=self.load_user_data)
        self.load_user_data_button.grid(row=0, column=3, sticky="w", padx=5)

        # Nominator Stats Frame
        self.nominator_stats_frame = tk.LabelFrame(self.root, text="Nominator Stats", padx=padx, pady=pady)
        self.nominator_stats_frame.grid(row=2, column=0, sticky="ew", padx=padx, pady=pady)

        # Custom Input Frame
        self.custom_input_frame = tk.LabelFrame(self.root, text="Select a custom input", padx=padx, pady=pady)
        self.custom_input_frame.grid(row=2, column=1, sticky="ew", padx=padx, pady=pady)

        

        # Projected Earnings Frame
        self.projected_earnings_frame = tk.LabelFrame(self.root, text="Projected Earnings", padx=padx, pady=pady)
        self.projected_earnings_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=padx, pady=pady)

        # Projected Balance Frame
        self.projected_balance_frame = tk.LabelFrame(self.root, text="Projected Total Balance", padx=padx, pady=pady)
        self.projected_balance_frame.grid(row=3, column=1, sticky="ew", padx=padx, pady=pady)

        # Populate Frames
        self.populate_frames()

        # Calculate Button
        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=4, column=0, columnspan=2, pady=pady, sticky="ew")
        self.calculate_button["state"] = "disabled"

        # Status Label
        self.status_label = tk.Label(self.root, text="Loading data...")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=pady)

        # Populate Frames
        self.populate_frames()

        # Fetch all data after setting up the GUI
        self.fetch_all_data()

    ################ POPULATE FRAMES ####################################################
    def populate_frames(self):
        # Populate Network Stats
        self.network_stats_labels = {}
        network_labels = ["Price", "24 hr change", "24 hr Volume", "Current Supply", "Total Supply", "Delegated Supply", "Market Cap"]
        for i, label in enumerate(network_labels):
            tk.Label(self.network_stats_frame, text=f"{label}:").grid(row=i, column=0, sticky="w")
            label_widget = tk.Label(self.network_stats_frame, text="0", bg="lightgrey", width=20)
            label_widget.grid(row=i, column=1)

        # Username Entry
        tk.Label(self.validator_calculator_frame, text="Username:").grid(row=2, column=0, sticky="e")
        self.username_entry = tk.Entry(self.validator_calculator_frame, width=10)  # Set the width to your desired value
        self.username_entry.grid(row=2, column=1, sticky="e")

        # Save User Data Button
        self.save_user_data_button = tk.Button(self.validator_calculator_frame, text="Save User Data", command=self.save_user_data)
        self.save_user_data_button.grid(row=2, column=2, sticky="w", padx=5)

        # Load User Data Button
        self.load_user_data_button = tk.Button(self.validator_calculator_frame, text="Load User Data", command=self.load_user_data)
        self.load_user_data_button.grid(row=2, column=3, sticky="w", padx=5)

        # Submit Coldkey Button
        self.submit_coldkey_button = tk.Button(self.validator_calculator_frame, text="Load Nominator Data", command=self.load_nominator_data)
        self.submit_coldkey_button.grid(row=0, column=2, sticky="w")

        # Status Message Label
        self.status_message_label = tk.Label(self.validator_calculator_frame, text="")
        self.status_message_label.grid(row=3, column=0, columnspan=3)




    

        # Nominator Stats Frame
        self.nominator_stats_frame = tk.LabelFrame(self.root, text="Nominator Stats", padx=padx, pady=pady)
        self.nominator_stats_frame.grid(row=2, column=0, sticky="ew", padx=padx, pady=pady)

        # Custom Input Frame
        self.custom_input_frame = tk.LabelFrame(self.root, text="Select a custom input", padx=padx, pady=pady)
        self.custom_input_frame.grid(row=2, column=1, sticky="ew", padx=padx, pady=pady)

        # Projected Earnings Frame
        self.projected_earnings_frame = tk.LabelFrame(self.root, text="Projected Earnings", padx=padx, pady=pady)
        self.projected_earnings_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=padx, pady=pady)

        # Projected Balance Frame
        self.projected_balance_frame = tk.LabelFrame(self.root, text="Projected Total Balance", padx=padx, pady=pady)
        self.projected_balance_frame.grid(row=3, column=1, sticky="ew", padx=padx, pady=pady)

        # Populate Frames
        self.populate_frames()

        # Calculate Button
        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=4, column=0, columnspan=2, pady=pady, sticky="ew")
        self.calculate_button["state"] = "disabled"

        # Status Label
        self.status_label = tk.Label(self.root, text="Loading data...")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=pady)

        # Populate Frames
        self.populate_frames()

        # Fetch all data after setting up the GUI
        self.fetch_all_data()

################ POPULATE FRAMES ####################################################
    def populate_frames(self):
        # Populate Network Stats
        self.network_stats_labels = {}
        network_labels = ["Price", "24 hr change", "24 hr Volume", "Current Supply", "Total Supply", "Delegated Supply", "Market Cap"]
        for i, label in enumerate(network_labels):
            tk.Label(self.network_stats_frame, text=f"{label}:", font=("Arial", 13)).grid(row=i, column=0, sticky="w")  # Increase font size to 14
            label_widget = tk.Label(self.network_stats_frame, text="0", bg="lightgrey", width=20, font=("Arial", 13))  # Increase font size to 14
            label_widget.grid(row=i, column=1)
            self.network_stats_labels[label] = label_widget

        # Populate Validator Stats
        self.validator_stats_labels = {}
        validator_labels = ["Total Stake", "Total Daily Return", "Payout Pool", "Nominators", "Network", "APY"]
        print(self.validator_info)  # Add this line
        validator_data = self.extract_validator_data(self.validator_info)  # Extract validator data
        if validator_data is None:
            validator_data = {}
        for i, label in enumerate(validator_labels):
            if label == "Total Stake":
                value = validator_data.get("total_stake", "N/A")
            elif label == "Total Daily Return":
                value = validator_data.get("total_daily_return", "N/A")
            elif label == "Payout Pool":
                value = validator_data.get("delegate_stake", "N/A")
            elif label == "Nominators":
                nominators_list = validator_data.get("nominators", [])
                value = str(len(nominators_list))  # Get the total number of nominators
            else:
                value = "0"
            tk.Label(self.validator_stats_frame, text=f"{label}:", font=("Arial", 13)).grid(row=i, column=0, sticky="w")  # Increase font size to 12
            label_widget = tk.Label(self.validator_stats_frame, text=value, bg="lightgrey", width=20, font=("Arial", 13))  # Increase font size to 12
            label_widget.grid(row=i, column=1)
            self.validator_stats_labels[label] = label_widget

        # Add an empty spacer row
        tk.Label(self.validator_stats_frame).grid(row=len(validator_labels), column=0)

        # Populate Validator Calculator
        tk.Label(self.validator_calculator_frame, text="Enter Nominator Coldkey:").grid(row=0, column=0, sticky="w")
        self.coldkey_entry = tk.Entry(self.validator_calculator_frame, width=90)
        self.coldkey_entry.grid(row=0, column=1, sticky="e")


        # Populate Nominator Stats
        self.nominator_stats_labels = {}
        nominator_labels = ["Balance", "USD", "Percent of Stake"]
        for i, label in enumerate(nominator_labels):
            tk.Label(self.nominator_stats_frame, text=f"{label}:").grid(row=i, column=0, sticky="w")
            label_widget = tk.Label(self.nominator_stats_frame, text="0", bg="lightgrey", width=20)
            label_widget.grid(row=i, column=1)
            self.nominator_stats_labels[label] = label_widget

#        self.custom_input_vars = {}
 #       custom_input_labels = ["Custom Price", "Custom Balance", "Custom APY"]
  #      for i, label in enumerate(custom_input_labels):
   #         var = tk.IntVar()
    #        checkbutton = tk.Checkbutton(self.custom_input_frame, variable=var)
     #       checkbutton.grid(row=i, column=0, sticky="w")
      #      tk.Label(self.custom_input_frame, text=f"{label}:").grid(row=i, column=1, sticky="w")
       #     entry = tk.Entry(self.custom_input_frame, width=20)
        #    entry.grid(row=i, column=2, sticky="e")
         #   self.custom_input_vars[label] = (var, entry)

        self.custom_input_vars = {}
        custom_input_labels = ["Custom Price", "Custom Balance", "Custom APY"]
        for i, label in enumerate(custom_input_labels):
            var = tk.IntVar()
            checkbutton = tk.Checkbutton(self.custom_input_frame, text=label, variable=var)
            checkbutton.grid(row=i, column=0, sticky="w")
            entry = tk.Entry(self.custom_input_frame, width=20)
            entry.grid(row=i, column=1)
            self.custom_input_vars[label] = (var, entry)

            
        # Populate Projected Earnings
        tk.Label(self.projected_earnings_frame, text="TAO").grid(row=0, column=2, sticky="w")
        tk.Label(self.projected_earnings_frame, text="USD").grid(row=0, column=3, sticky="w")
        tk.Label(self.projected_earnings_frame, text="Day(s)").grid(row=1, column=0, sticky="w") 
        self.day_entry = tk.Entry(self.projected_earnings_frame, width=5)
        self.day_entry.grid(row=1, column=1)
        self.earningsdays_label = tk.Label(self.projected_earnings_frame, text="0", bg="lightgrey", width=20)#.grid(row=1, column=2)
        self.earningsdays_label.grid(row=1, column=2)
        self.earningsdaysUSD_label = tk.Label(self.projected_earnings_frame, text="0", bg="lightgrey", width=20)#.grid(row=1, column=3)
        self.earningsdaysUSD_label.grid(row=1, column=3)

        tk.Label(self.projected_earnings_frame, text="Week(s)").grid(row=2, column=0, sticky="w")
        self.week_entry = tk.Entry(self.projected_earnings_frame, width=5)
        self.week_entry.grid(row=2, column=1)
        self.earningsweeks_label = tk.Label(self.projected_earnings_frame, text="0", bg="lightgrey", width=20)#.grid(row=2, column=2)
        self.earningsweeks_label.grid(row=2, column=2)
        self.earningsweeksUSD_label = tk.Label(self.projected_earnings_frame, text="0", bg="lightgrey", width=20)#.grid(row=2, column=3)
        self.earningsweeksUSD_label.grid(row=2, column=3)

        tk.Label(self.projected_earnings_frame, text="Month(s)").grid(row=3, column=0, sticky="w")
        self.month_entry = tk.Entry(self.projected_earnings_frame, width=5)
        self.month_entry.grid(row=3, column=1)
        self.earningsmonths_label = tk.Label(self.projected_earnings_frame, text="0", bg="lightgrey", width=20)
        self.earningsmonths_label.grid(row=3, column=2)
        self.earningsmonthsUSD_label = tk.Label(self.projected_earnings_frame, text="0", bg="lightgrey", width=20)
        self.earningsmonthsUSD_label.grid(row=3, column=3)

        # Populate Projected Balance
        tk.Label(self.projected_balance_frame, text="TAO").grid(row=0, column=0, sticky="w")
        tk.Label(self.projected_balance_frame, text="USD").grid(row=0, column=1, sticky="w")
        self.balancedays_label = tk.Label(self.projected_balance_frame, text="0", bg="lightgrey", width=20)#.grid(row=1, column=0, sticky="w")
        self.balancedays_label.grid(row=1, column=0, sticky = "w")
        self.balancedaysUSD_label = tk.Label(self.projected_balance_frame, text="0", bg="lightgrey", width=20)#.grid(row=1, column=1, sticky="w")
        self.balancedaysUSD_label.grid(row=1, column=1, sticky = "w")

        self.balanceweeks_label = tk.Label(self.projected_balance_frame, text="0", bg="lightgrey", width=20)#.grid(row=2, column=0, sticky="w")
        self.balanceweeks_label.grid(row=2, column=0, sticky = "w")
        self.balanceweeksUSD_label = tk.Label(self.projected_balance_frame, text="0", bg="lightgrey", width=20)#.grid(row=2, column=1, sticky="w")
        self.balanceweeksUSD_label.grid(row=2, column=1, sticky = "w")

        self.balancemonths_label = tk.Label(self.projected_balance_frame, text="0", bg="lightgrey", width=20)#.grid(row=3, column=0, sticky="w")
        self.balancemonths_label.grid(row=3, column=0, sticky = "w")
        self.balancemonthsUSD_label = tk.Label(self.projected_balance_frame, text="0", bg="lightgrey", width=20)
        self.balancemonthsUSD_label.grid(row=3, column=1, sticky = "w")
        
#################### LOAD DATA ####################################################
    def fetch_all_data(self):
        network_data = self.fetch_network_stats()
        if network_data:
            self.update_network_stats_gui(*self.extract_network_stats(network_data))
        
        validator_data = self.fetch_validator_data()
        if validator_data:
            validator_info = self.extract_validator_data(validator_data)
            self.update_validator_stats_gui(validator_info)

    def reset_calculator(self):
        # Clear the loaded coldkeys
        self.loaded_coldkeys.clear()

        # Reset the listbox
        self.coldkey_listbox.delete(0, tk.END)

        # Reset the total balance and USD display in Nominator Stats
        self.nominator_stats_labels["Balance"].config(text="0")
        self.nominator_stats_labels["USD"].config(text="0")  # Resetting the USD label

        # Reset the Percent of Stake display in Nominator Stats
        self.nominator_stats_labels["Percent of Stake"].config(text="0")

        # Reset the entry field for coldkeys
        self.coldkey_entry.delete(0, tk.END)

        # Update any other GUI elements as necessary
        self.status_label.config(text="Ready to load new data.")


    def save_user_data(self):
        self.username = self.username_entry.get().strip()
        if not self.username:
            self.status_message_label.config(text="Please enter a username.")
            return

        filename = f"{self.username}_coldkeys_data.txt"
        try:
            with open(filename, 'w') as file:
                for coldkey, balance in self.loaded_coldkeys.items():
                    file.write(f"{coldkey}: {balance}\n")
            self.status_message_label.config(text="Data saved successfully.")
        except Exception as e:
            self.status_message_label.config(text=f"Error saving data: {e}")

    def load_user_data(self):
        self.username = self.username_entry.get().strip()
        if not self.username:
            self.status_message_label.config(text="Please enter a username.")
            return

        filename = f"{self.username}_coldkeys_data.txt"
        try:
            with open(filename, 'r') as file:
                self.loaded_coldkeys.clear()
                for line in file:
                    coldkey, balance = line.strip().split(": ")
                    self.loaded_coldkeys[coldkey] = float(balance)
                self.update_coldkey_listbox()
                self.update_nominator_stats()
            self.status_message_label.config(text="Data loaded successfully.")
        except Exception as e:
            self.status_message_label.config(text=f"Error loading data: {e}")

    def update_nominator_stats(self):
        # Calculate the total balance from all loaded coldkeys
        total_balance = sum(self.loaded_coldkeys.values())
        self.nominator_stats_labels["Balance"].config(text=f"{total_balance:,.2f}")

     #   # Fetch the current price
     #   price_str = self.network_stats_labels["Price"].cget("text").replace('$', '').replace(',', '')
     #   try:
     #       price = float(price_str)
     #   except ValueError:
     #       price = 0  # Handle the case where price is not available or not a valid number

        price_str = self.network_stats_labels["Price"].cget("text").replace(',', '').replace('$', '')
        try:
            price = float(price_str)
        except ValueError:
            print("Invalid price format")
            return


        # Calculate USD value
        total_usd_value = total_balance * price
        self.nominator_stats_labels["USD"].config(text=f"${total_usd_value:,.2f}")

        # Fetch total stake and delegate stake values
        total_stake = float(self.validator_info.get("total_stake", 0))
        delegate_stake = float(self.validator_info.get("delegate_stake", 0))

        # Calculate and update "Percent of Stake" for the total balance
        if total_stake - delegate_stake > 0:
            percent_of_stake = (total_balance / (total_stake - delegate_stake)) * 100
            self.nominator_stats_labels["Percent of Stake"].config(text=f"{percent_of_stake:.2f}%")
        else:
            self.nominator_stats_labels["Percent of Stake"].config(text="N/A")







#################### VALIDATOR DATA ####################################################
    def fetch_validator_data(self):
        url = "http://167.86.67.152:8088/delegate_info/5HK5tp6t2S59DywmHRWPBVJeJ86T61KjurYqeooqj8sREpeN"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            print(data)  # Add this line
            return data
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
        

    def extract_validator_data(self, data):
        if not data:
            return None

        extracted_data = {
            "delegate_stake": data.get("delegate_stake", "N/A"),
            "total_daily_return": data.get("total_daily_return", "N/A"),
            "total_stake": data.get("total_stake", "N/A"),
            "nominators": data.get("nominators", []),  # Corrected the spelling here
        }

        print("Extracted Validator Data:", extracted_data)  # Add this line
        return extracted_data

    def load_nominator_data(self):
        entered_coldkey = self.coldkey_entry.get().strip()
        if not entered_coldkey:
            return  # Do nothing if no coldkey is entered

        nominators = self.validator_info.get("nominators", [])
        if not nominators:
            self.status_label.config(text="Nominator data not loaded. Please wait...")
            return

        balance = self.find_nominator_balance(entered_coldkey, nominators)
        if balance is not None:
            self.loaded_coldkeys[entered_coldkey] = balance
            self.update_coldkey_listbox()
            self.update_nominator_stats()  # Recalculate and update "Percent of Stake"
            self.coldkey_entry.delete(0, tk.END)  # Clear the entry field
        else:
            self.status_label.config(text="No matching nominator found for entered coldkey.")


    def update_coldkey_listbox(self):
        self.coldkey_listbox.delete(0, tk.END)  # Clear existing entries
        for coldkey, balance in self.loaded_coldkeys.items():
            self.coldkey_listbox.insert(tk.END, f"{coldkey}: {balance}")
            

    def find_nominator_balance(self, coldkey, nominators):
        for nominator in nominators:
            if nominator['address'] == coldkey:  # Replace 'address' with the actual key for the address in your data
                return nominator['balance']  # Replace 'balance' with the actual key for the balance in your data
        return None


    def update_validator_stats_gui(self, validator_info):
        self.validator_info = validator_info
        validator_data = self.extract_validator_data(self.validator_info)
        if validator_data is None:
            validator_data = {}
        
        network_data = self.fetch_network_stats()  # Ensure you have the latest network stats
        if network_data:
            network_stats = self.extract_network_stats(network_data)
            # Make sure to get the delegated_supply as a float for calculations
            delegated_supply = float(network_stats[5])  # This index might change depending on how you're storing it
            
            # Initialize total_stake and total_daily_return outside the loop for use in APY calculation
            total_stake = float(validator_data.get("total_stake", 0))
            total_daily_return = float(validator_data.get("total_daily_return", 0))

            for label, widget in self.validator_stats_labels.items():
                if label == "Total Stake":
                    # The formatting is applied here
                    value = f"{total_stake:,.2f}" if total_stake else "N/A"
                    widget.config(text=value)
                elif label == "Total Daily Return":
                    # If you want to format Total Daily Return as well, you can apply similar formatting
                    value = f"{total_daily_return:,.2f}" if total_daily_return else "N/A"
                    widget.config(text=value)
                elif label == "Payout Pool":
                    value = validator_data.get("delegate_stake", "N/A")
                    value = "{:,.2f}".format(float(value)) if value != "N/A" else value
                    widget.config(text=value)
                elif label == "Nominators":
                    nominators_list = validator_data.get("nominators", [])
                    value = str(len(nominators_list))  # Count the number of nominators
                    widget.config(text=value)
                elif label == "Network":
                    if delegated_supply and total_stake:  # Make sure not to divide by zero
                        network_percentage = (total_stake / delegated_supply) * 100
                        value = f"{network_percentage:.2f}%"
                    else:
                        value = "N/A"
                    widget.config(text=value)
                elif label == "APY":
                    if total_stake:  # Prevent division by zero
                        # APY Calculation
                        daily_return_rate = total_daily_return / total_stake if total_stake else 0
                        apy = ((1 + daily_return_rate) ** 365) - 1
                        value = f"{apy:.2%}"  # Format as a percentage
                    else:
                        value = "N/A"
                    widget.config(text=value)
                else:
                    value = "0"  # Or any other default value
                    widget.config(text=value)

    def fetch_and_update_validator_stats(self):
        data = self.fetch_validator_data()
        if data:
            validator_info = self.extract_validator_data(data)
            self.update_validator_stats_gui(validator_info)
            self.calculate_button["state"] = "normal"
            self.status_label.config(text="Data loaded. Ready to calculate.")
        else:
            print("Failed to fetch validator data")
            self.status_label.config(text="Failed to load data. Please try again.")

    def find_nominator_balance(self, coldkey, nominators):
        for nominator in nominators:
            address, balance = nominator
            if address == coldkey:
                return balance
        return None
#################### NETWORK DATA ####################################################
    def fetch_network_stats(self):
        url = "https://taostats.io/data.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_and_update_network_stats(self):
        data = self.fetch_network_stats()
        if data:
            stats = self.extract_network_stats(data)
            self.update_network_stats_gui(*stats)
        else:
            print("Failed to fetch network stats")
            self.status_label.config(text="Failed to load data. Please try again.")


    def extract_network_stats(self, data):
        if data and len(data) > 0:
            network_data = data[0]
            return (network_data.get("price", "N/A"), network_data.get("24h_change", "N/A"),
                    network_data.get("24h_volume", "N/A"), network_data.get("current_supply", "N/A"),
                    network_data.get("total_supply", "N/A"), network_data.get("delegated_supply", "N/A"),
                    network_data.get("market_cap", "N/A"))
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"


    def update_network_stats_gui(self, price, change_24h, volume_24h, current_supply, total_supply, delegated_supply, market_cap):
        # Format price and 24 hr Volume as USD currency with two decimal places
        self.network_stats_labels["Price"].config(text=f"${float(price):,.2f}")
        self.network_stats_labels["24 hr change"].config(text=change_24h)
        self.network_stats_labels["24 hr Volume"].config(text=f"${float(volume_24h):,.2f}")

        # Format other labels if necessary, for example:
        self.network_stats_labels["Current Supply"].config(text=f"{float(current_supply):,.0f}")  # No decimals for supply figures
        self.network_stats_labels["Total Supply"].config(text=f"{float(total_supply):,.0f}")
        self.network_stats_labels["Delegated Supply"].config(text=f"{float(delegated_supply):,.0f}")
        self.network_stats_labels["Market Cap"].config(text=f"${float(market_cap):,.2f}")  # Assuming market cap should also be formatted as currency

#################### CALCULATE ####################################################

    def calculate(self):
        try:
            entered_days = self.day_entry.get().strip()
            entered_weeks = self.week_entry.get().strip()
            entered_months = self.month_entry.get().strip()
            projected_earnings = 0

            # Check and use custom inputs if checked
            custom_price_var, custom_price_entry = self.custom_input_vars["Custom Price"]
            custom_balance_var, custom_balance_entry = self.custom_input_vars["Custom Balance"]
            custom_apy_var, custom_apy_entry = self.custom_input_vars["Custom APY"]

            # Use custom price if checkbox is checked
            if custom_price_var.get():
                try:
                    price = float(custom_price_entry.get())
                except ValueError:
                    print("Invalid Custom Price")
                    return
            else:
                price = self.network_stats_labels["Price"].cget("text").replace(',', '').replace('$', '')

            # Use custom balance if checkbox is checked
            if custom_balance_var.get():
                try:
                    balance = float(custom_balance_entry.get())
                except ValueError:
                    print("Invalid Custom Balance")
                    return
            else:
                balance_text = self.nominator_stats_labels["Balance"].cget("text").replace(',', '').replace('$', '')
                balance = float(balance_text) if balance_text not in ["N/A", ""] else 0

            # Get the total daily return and total stake for calculation
            total_daily_return = self.validator_info.get("total_daily_return", 0)
            total_stake = self.validator_info.get("total_stake", 0)
#################################### Days ##########################################################
            if entered_days.isdigit() and balance > 0:
                days = int(entered_days)

                # Use custom APY if checkbox is checked
                if custom_apy_var.get():
                    try:
                        apy_input = custom_apy_entry.get().replace("%", "").strip()  # Remove percentage sign and strip whitespace
                        apy = float(apy_input) / 100  # Convert percentage to a decimal
                        projected_earnings = self.calculate_projected_earnings_APY_days(days, balance, apy)
                    except ValueError:
                        print("Invalid Custom APY")
                        return
                else:
                    projected_earnings = self.calculate_projected_earnings_days(days, total_daily_return, total_stake, balance)

                self.earningsdays_label.config(text=f"{projected_earnings:,.2f}")
                self.earningsdaysUSD_label.config(text=f"${projected_earnings * float(price):,.2f}")
                self.balancedays_label.config(text=f"{projected_earnings + balance:,.2f}") # Add the projected earnings to the balance
                self.balancedaysUSD_label.config(text=f"${(projected_earnings + balance) * float(price):,.2f}") # Add the projected USD earnings to the USD balance
            else:
                self.earningsdays_label.config(text="0")
                self.earningsdaysUSD_label.config(text="0")
                self.balancedays_label.config(text="0")
                self.balancedaysUSD_label.config(text="0")

##################################### Weeks ##########################################################################
            if entered_weeks.isdigit() and balance > 0:
                weeks = int(entered_weeks)
                # Use custom APY if checkbox is checked
                if custom_apy_var.get():
                    try:
                        apy_input = custom_apy_entry.get().replace("%", "").strip()  # Remove percentage sign and strip whitespace
                        apy = float(apy_input) / 100  # Convert percentage to a decimal
                        projected_earnings = self.calculate_projected_earnings_APY_weeks(weeks, balance, apy)
                    except ValueError:
                        print("Invalid Custom APY")
                        return
                else:
                    projected_earnings = self.calculate_projected_earnings_weeks(weeks, total_daily_return, total_stake, balance)

                self.earningsweeks_label.config(text=f"{projected_earnings:,.2f}")
                self.earningsweeksUSD_label.config(text=f"${projected_earnings * float(price):,.2f}")
                self.balanceweeks_label.config(text=f"{projected_earnings + balance:,.2f}") # Add the projected earnings to the balance
                self.balanceweeksUSD_label.config(text=f"${(projected_earnings + balance) * float(price):,.2f}") # Add the projected USD earnings to the USD balance
            else:
                self.earningsweeks_label.config(text="0")
                self.earningsweeksUSD_label.config(text="0")
                self.balanceweeks_label.config(text="0")
                self.balanceweeksUSD_label.config(text="0")
####################################### Months ########################################################################
            if entered_months.isdigit() and balance > 0:
                months = int(entered_months)
                # Use custom APY if checkbox is checked
                if custom_apy_var.get():
                    try:
                        apy_input = custom_apy_entry.get().replace("%", "").strip()  # Remove percentage sign and strip whitespace
                        apy = float(apy_input) / 100  # Convert percentage to a decimal
                        projected_earnings = self.calculate_projected_earnings_APY_months(months, balance, apy)
                    except ValueError:
                        print("Invalid Custom APY")
                        return
                else:
                    projected_earnings = self.calculate_projected_earnings_months(months, total_daily_return, total_stake, balance)

                self.earningsmonths_label.config(text=f"{projected_earnings:,.2f}")
                self.earningsmonthsUSD_label.config(text=f"${projected_earnings * float(price):,.2f}")
                self.balancemonths_label.config(text=f"{projected_earnings + balance:,.2f}")
                self.balancemonthsUSD_label.config(text=f"${(projected_earnings + balance) * float(price):,.2f}")
            else:
                self.earningsmonths_label.config(text="0")
                self.earningsmonthsUSD_label.config(text="0")
                self.balancemonths_label.config(text="0")
                self.balancemonthsUSD_label.config(text="0")
###############################################################################################################
        except Exception as e:
            print("Error in calculate function:", e)
            self.earningsdays_label.config(text="Error occurred")
            self.earningsdaysUSD_label.config(text="Error occurred")
            self.balancedays_label.config(text="Error occurred")
            self.balancedaysUSD_label.config(text="Error occurred")
            self.earningsweeks_label.config(text="Error occurred")
            self.earningsweeksUSD_label.config(text="Error occurred")
            self.balanceweeks_label.config(text="Error occurred")
            self.balanceweeksUSD_label.config(text="Error occurred")
            self.earningsmonths_label.config(text="Error occurred")
            self.earningsmonthsUSD_label.config(text="Error occurred")
            self.balancemonths_label.config(text="Error occurred")
            self.balancemonthsUSD_label.config(text="Error occurred")

#################################################################################################################################
 



    def calculate_projected_earnings_days(self, days, total_daily_return, total_stake, balance,):
        try:
            days = float(days)
            total_daily_return = float(total_daily_return)
            total_stake = float(total_stake)
            balance = float(balance)
            earningsdays = (((1 + (total_daily_return / total_stake)) ** days) - 1) * balance
            return earningsdays
        except ValueError as e:
            print(f"Invalid input for projected earnings calculation: {e}")
            return 0
        
    def calculate_projected_earnings_weeks(self, weeks, total_daily_return, total_stake, balance,):
        try:
            weeks = float(weeks)
            total_daily_return = float(total_daily_return)
            total_stake = float(total_stake)
            balance = float(balance)
            earningsweeks = (((1 + (total_daily_return / total_stake)) ** (weeks * (365/52))) - 1) * balance
            return earningsweeks
        except ValueError as e:
            print(f"Invalid input for projected earnings calculation: {e}")
            return 0
    
    def calculate_projected_earnings_months(self, months, total_daily_return, total_stake, balance,):
        try:
            months = float(months)
            total_daily_return = float(total_daily_return)
            total_stake = float(total_stake)
            balance = float(balance)
            earningsmonths = (((1 + (total_daily_return / total_stake)) ** (months * (365/12))) - 1) * balance
            return earningsmonths
        except ValueError as e:
            print(f"Invalid input for projected earnings calculation: {e}")
            return 0
        
    def calculate_projected_earnings_APY_days(self, days, balance, custom_apy):
        try:
            days = float(days)
            balance = float(balance)
            custom_apy = float(custom_apy)
            earningsdays = (((1 + (custom_apy / 365)) ** days) - 1) * balance
            return earningsdays
        except ValueError as e:
            print(f"Invalid input for projected earnings calculation: {e}")
            return 0
        
    def calculate_projected_earnings_APY_weeks(self, weeks, balance, custom_apy):
        try:
            weeks = float(weeks)
            balance = float(balance)
            custom_apy = float(custom_apy)
            earningsweeks = (((1 + (custom_apy / 365)) ** (weeks * (365/52))) - 1) * balance
            return earningsweeks
        except ValueError as e:
            print(f"Invalid input for projected earnings calculation: {e}")
            return 0
        
    def calculate_projected_earnings_APY_months(self, months, balance, custom_apy):
        try:
            months = float(months)
            balance = float(balance)
            custom_apy = float(custom_apy)
            earningsmonths = (((1 + (custom_apy / 365)) ** (months * (365/12))) - 1) * balance
            return earningsmonths
        except ValueError as e:
            print(f"Invalid input for projected earnings calculation: {e}")
            return 0

####################################################################################
def main():
    root = tk.Tk()
    app = ValidatorApp(root)
    root.after(100, app.fetch_and_update_network_stats)
    root.after(100, app.fetch_and_update_validator_stats)
    root.mainloop()

if __name__ == "__main__":
    main()