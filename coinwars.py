import random
import time

class Player:
    def __init__(self):
        self.money = 20000
        self.debt = 50000
        self.health = 100
        self.wallet = {
            'capacity': 1000,
            'coins': {},
            'NFTs': {}
        }
        self.bank_balance = 0
        self.lawyers = 0
        self.pending_withdrawal = 0
        self.pending_withdrawal_day = 0
        self.tornado_cash = {'coins': {}, 'NFTs': {}}

    def wallet_space_available(self):
        used_space = sum(self.wallet['coins'].values()) + sum(self.wallet['NFTs'].values())
        return self.wallet['capacity'] - used_space

    def add_to_wallet(self, item_type, item_key, quantity):
        if self.wallet_space_available() >= quantity:
            if item_type == 'coins':
                self.wallet['coins'][item_key] = self.wallet['coins'].get(item_key, 0) + quantity
            elif item_type == 'NFTs':
                self.wallet['NFTs'][item_key] = self.wallet['NFTs'].get(item_key, 0) + quantity
            return True
        return False

    def remove_from_wallet(self, item_type, item_key, quantity):
        if item_type in self.wallet and item_key in self.wallet[item_type]:
            if self.wallet[item_type][item_key] >= quantity:
                self.wallet[item_type][item_key] -= quantity
                if self.wallet[item_type][item_key] == 0:
                    del self.wallet[item_type][item_key]
                return True
        return False

class Game:
    
    def display_status(self):
        print(f"\nDay: {self.day}/30 | Location: {self.locations[self.day-1]} | Wallet Space Available: {self.player.wallet_space_available()}")
        print(f"Money: ${self.player.money:.2f} | Debt: ${self.player.debt:.2f} | Health: {self.player.health}%")
        print(f"Bank Balance: ${self.player.bank_balance:.2f} | Lawyers: {self.player.lawyers}")
        print("\nWallet Contents:")
        for coin, amount in self.player.wallet['coins'].items():
            print(f"{self.coins[coin]}: {amount}")
        for nft, amount in self.player.wallet['NFTs'].items():
            print(f"{self.nfts[nft]}: {amount}")
        print(f"Bank Balance: ${self.player.bank_balance:.2f}")
        if self.player.pending_withdrawal > 0:
            print(f"Pending Withdrawal: ${self.player.pending_withdrawal:.2f} (available on day {self.player.pending_withdrawal_day})")

    def bank_operations(self):
        while True:
            action = get_valid_menu_choice("\nBank Operations: (D)eposit, (W)ithdraw, (C)heck Balance, or (E)xit Bank? ", ['D', 'W', 'C', 'E'])
            
            if action == 'D':
                self.bank_deposit()
            elif action == 'W':
                self.bank_withdraw()
            elif action == 'C':
                self.check_bank_balance()
            elif action == 'E':
                break

    def bank_deposit(self):
        max_deposit = self.player.money
        amount = get_valid_numeric_input(f"Enter the amount to deposit (max ${max_deposit:.2f}): ", min_value=0.01, max_value=max_deposit)
        self.player.money -= amount
        self.player.bank_balance += amount
        print(f"${amount:.2f} deposited successfully.")

    def bank_withdraw(self):
        if self.player.pending_withdrawal > 0:
            print("You already have a pending withdrawal.")
            return

        max_withdrawal = self.player.bank_balance
        amount = get_valid_numeric_input(f"Enter the amount to withdraw (max ${max_withdrawal:.2f}): ", min_value=0.01, max_value=max_withdrawal)
        self.player.bank_balance -= amount
        self.player.pending_withdrawal = amount
        self.player.pending_withdrawal_day = self.day + 1
        print(f"${amount:.2f} will be available for withdrawal on day {self.player.pending_withdrawal_day}.")

    def process_action(self, action, **kwargs):
        if action == 'buy':
            return self.buy(**kwargs)
        elif action == 'sell':
            return self.sell(**kwargs)
        # Add more actions as needed
        else:
            return {'error': 'Invalid action'}


    def has_sufficient_liquidity(self, item, quantity):
        if item in self.coins:
            # 5-10% chance of insufficient liquidity for coins
            if random.random() < random.uniform(0.05, 0.10):
                # 75-100% of requested quantity is available, or minimum 65%
                available = max(int(quantity * random.uniform(0.75, 1.0)), int(quantity * 0.65))
                return available
        else:  # NFTs
            # 25-65% chance of insufficient liquidity for NFTs
            if random.random() < random.uniform(0.25, 0.65):
                return 0  # No liquidity for NFTs
        return quantity  # Full liquidity

    def check_bank_balance(self):
        print(f"Current Bank Balance: ${self.player.bank_balance:.2f}")
        if self.player.pending_withdrawal > 0:
            print(f"Pending Withdrawal: ${self.player.pending_withdrawal:.2f} (available on day {self.player.pending_withdrawal_day})")

    def apply_bank_interest(self):
        interest = self.player.bank_balance * self.daily_interest_rate
        self.player.bank_balance += interest
        print(f"Your bank balance earned ${interest:.2f} in interest.")

    def handle_pending_withdrawal(self):
        if self.player.pending_withdrawal > 0 and self.day >= self.player.pending_withdrawal_day:
            self.player.money += self.player.pending_withdrawal
            print(f"${self.player.pending_withdrawal:.2f} from your pending withdrawal is now available.")
            self.player.pending_withdrawal = 0
            self.player.pending_withdrawal_day = 0


    def get_valid_numeric_input(prompt, min_value=None, max_value=None):
        while True:
            try:
                value = float(input(prompt))
                if min_value is not None and value < min_value:
                    print(f"Value must be at least {min_value}.")
                elif max_value is not None and value > max_value:
                    print(f"Value must be no more than {max_value}.")
                else:
                    return value
            except ValueError:
                print("Please enter a valid number.")

    # Usage example:
    quantity = int(get_valid_numeric_input("Enter the quantity: ", min_value=1))
    
    def __init__(self):
        self.player = Player()
        self.day = 1
        self.daily_interest_rate = 0.0215  # 2.15% daily interest rate

        self.locations = [
            "Coinbase", "Uniswap", "Robinhood", "Jupiter", "BASE", "1Inch", "Binance",
            "Suhsiswap", "Kraken", "Curve", "Bitmex", "RhinoFi", "Gemini", "Syncswap",
            "OKX", "Pancakeswap", "MEXC", "eToro", "ByBit", "FTX", "Kucoin", "Matcha",
            "Bitstamp", "Cowswap", "Huobi", "Bitfinex", "Bitget", "gate.io", "crypto.com",
            "Wells Fargo"
        ]
        self.coins = {
            'E': 'Ether', 'B': 'Bitcoin', 'D': 'Dogecoin', 'S': 'Shiba Inu',
            'A': 'ADA', 'P': 'PEPE', 'W': 'DogWifHat', 'F': 'Floki Inu',
            'V': 'AAVE', 'C': 'Chainlink', 'S': 'Sand', 'H': 'HEX',
            'X': 'XTZ', 'M': 'MANA', 'U': 'UNI'
        }
        self.nfts = {
            'K': 'Punks', 'R': 'Bored Apes', 'M': 'Meebits', 'G': 'Pudgy Penguins',
            'L': 'Doodles', 'Z': 'Azooki', 'Y': 'Cryptoadz'
        }
        self.market = {}
        self.sec_investigation_chance = 0.05  # Initial 5% chance of SEC investigation    
        self.nft_history = {}  # To track NFT purchase history and opportunities
        self.doj_arrest_chance = 0.05  # 5% base chance of DoJ arrest when using Tornado Cash

    def tornado_cash_transfer(self):
        print("\nTornado Cash - Send assets to a trusted friend")
        
        item_type = input("Do you want to send (C)oins or (N)FTs? ").upper()
        if item_type == 'C':
            available_items = self.player.wallet['coins']
            item_dict = self.coins
        elif item_type == 'N':
            available_items = self.player.wallet['NFTs']
            item_dict = self.nfts
        else:
            print("Invalid option.")
            return

        if not available_items:
            print(f"You don't have any {item_type}s in your wallet.")
            return

        print(f"\nAvailable {item_type}s:")
        for item, amount in available_items.items():
            print(f"{item_dict[item]}: {amount} ({item})")

        item = input(f"Enter the key of the {item_type} you wish to send: ").upper()
        if item not in available_items:
            print("Invalid item.")
            return

        max_quantity = available_items[item]
        quantity = int(input(f"Enter the quantity (max {max_quantity}): "))
        if quantity > max_quantity:
            print(f"You only have {max_quantity} of this item.")
            return

        # Transfer to Tornado Cash
        available_items[item] -= quantity
        if item not in self.player.tornado_cash[item_type+'s']:
            self.player.tornado_cash[item_type+'s'][item] = 0
        self.player.tornado_cash[item_type+'s'][item] += quantity

        print(f"Sent {quantity} {item_dict[item]} to Tornado Cash.")
        
        # Check for DoJ arrest
        self.check_doj_arrest()

    def check_doj_arrest(self):
        if random.random() < self.doj_arrest_chance:
            print("\nALERT: The Department of Justice has arrested you for using Tornado Cash!")
            bail_amount = random.randint(500, 3000)
            print(f"You need to pay ${bail_amount} for bail.")
            
            if self.player.money >= bail_amount:
                self.player.money -= bail_amount
                print(f"You paid ${bail_amount} for bail and have been released.")
            else:
                print("You don't have enough money to pay for bail.")
                print("Game Over!")
                self.end_game()

        # Increase the chance of arrest for next time
        self.doj_arrest_chance = min(self.doj_arrest_chance + 0.24, 0.40)  # Cap at 40%

    def wallet_space_available(self):
        used_space = sum(self.player.wallet['coins'].values()) + sum(self.player.wallet['NFTs'].values())
        return self.player.wallet['capacity'] - used_space

        
    def sec_investigation(self):
        print("\nThe SEC are investigating you for promoting unregistered securities!")
        deputies = random.randint(0, 5)
        print(f"Commissioner Smartass arrives with {deputies} deputies.")

        if self.player.lawyers == 0:
            action = input("Do you run? (Y/N): ").upper()
            if action == 'Y':
                if random.random() > 0.5:
                    print("You managed to escape!")
                    return
                else:
                    print("You couldn't escape. The SEC caught up with you.")
            else:
                print("You decide to face the SEC.")
        else:
            action = input("Do you want to run (R) or fight (F)? ").upper()
            if action == 'R':
                if random.random() > 0.3:  # 70% chance of escape with lawyers
                    print("Your lawyers created a diversion. You escaped!")
                    return
                else:
                    print("Despite your lawyers' efforts, you couldn't escape.")
            elif action == 'F':
                return self.sec_fight(deputies)
  
  # If we reach here, player is facing consequences
        health_loss = {0: 15, 1: 25, 2: 35, 3: 45, 4: 65, 5: 85}[deputies]
        self.player.health -= health_loss
        print(f"The SEC's investigation has decreased your health by {health_loss}%.")

    def sec_fight(self, deputies):
        print("You decide to fight the SEC in court!")
        for i in range(deputies + 1):  # Fight deputies + Commissioner Smartass
            opponent = "Commissioner Smartass" if i == deputies else f"Deputy {i+1}"
            print(f"\nFighting {opponent}...")
            
            player_strength = self.player.lawyers * random.uniform(0.8, 1.2)
            sec_strength = random.uniform(0.5, 1.5)
            
            if player_strength > sec_strength:
                print(f"You successfully sued {opponent}!")
                if opponent == "Commissioner Smartass":
                    compensation = random.randint(10000, 50000)
                    self.player.money += compensation
                    print(f"You recovered legal costs and compensation: ${compensation}")
                    self.player.health = min(100, self.player.health + 20)  # Boost health
                    print("Your successful lawsuit boosted your health!")
            else:
                print(f"You lost the case against {opponent}.")
                health_loss = random.randint(5, 15)
                self.player.health -= health_loss
                print(f"The stress of the loss decreased your health by {health_loss}%")
                break  # Stop fighting if you lose once

    def generate_market(self):
        self.market = {}
        self.liquidity = {}
        for coin in self.coins:
            if random.random() > 0.3:  # 70% chance of coin being available
                self.market[coin] = round(random.uniform(100, 10000), 2)
                self.liquidity[coin] = random.randint(50, 1000)
        
        
        # NFT availability and pricing
        for nft in self.nfts:
            if nft not in self.nft_history:
                if random.random() > 0.7:  # 30% chance of NFT being available
                    self.market[nft] = round(random.uniform(1000, 100000), 2)
                    self.liquidity[nft] = random.randint(1, 10)
                    self.nft_history[nft] = {
                        'purchase_price': self.market[nft],
                        'opportunities': 0,
                        'scenario': self.determine_nft_scenario(),
                        'current_opportunity': 0
                    }               
            else:
                self.handle_nft_resale(nft)
    def determine_nft_scenario(self):
        rand = random.random()
        if rand < 0.2:
            return 'noopp'
        elif rand < 0.65:
            return '1opp'
        elif rand < 0.9:
            return '2opp'
        else:
            return '3opp'

    def handle_nft_resale(self, nft):
        history = self.nft_history[nft]
        if history['scenario'] == 'noopp':
            return  # NFT is not available for resale

        if history['opportunities'] >= {'1opp': 1, '2opp': 2, '3opp': 3}[history['scenario']]:
            return  # All resale opportunities have been used

        history['opportunities'] += 1
        history['current_opportunity'] += 1

        price_factor = self.determine_price_factor(history['scenario'], history['current_opportunity'])
    
        self.market[nft] = round(history['purchase_price'] * price_factor, 2)
        self.liquidity[nft] = random.randint(1, 10)
        
        # Determine price based on scenario and opportunity number
        def determine_price_factor(self, scenario, current_opportunity):
            if scenario == '1opp':
                return self.price_factor_1opp()
            elif scenario == '2opp':
                return self.price_factor_2opp(current_opportunity)
            else:  # '3opp'
                return self.price_factor_3opp(current_opportunity)

        def price_factor_1opp(self):
            rand = random.random()
            if rand < 0.5:
                return random.uniform(0.5, 0.99)  # 50% lower
            elif rand < 0.65:
                return 1  # 15% same
            else:
                return random.uniform(1.01, 1.5)  # 35% higher (up to 50% higher)

        def price_factor_2opp(self, current_opportunity):
            if current_opportunity == 1:
                return self.price_factor_1opp()
            else:  # Second opportunity
                rand = random.random()
                if rand < 0.5:
                    return random.uniform(0.5, 0.99)  # 50% lower
                elif rand < 0.65:
                    return 1  # 15% same
                else:
                    return random.uniform(2, 5)  # 35% higher (200-500% higher)

        def price_factor_3opp(self, current_opportunity):
            if current_opportunity in [1, 2]:
                return self.price_factor_1opp()
            else:  # Third opportunity
                rand = random.random()
                if rand < 0.69:
                    return random.uniform(0.75, 0.9)  # 69% slightly lower
                elif rand < 0.74:
                    return 7  # 5% 700% higher
                else:
                    return random.uniform(2, 3)  # 26% 100-200% higher
                
        self.market[nft] = round(history['purchase_price'] * price_factor, 2)
        self.liquidity[nft] = random.randint(1, 10)
    
    def get_valid_menu_choice(prompt, valid_choices):
        while True:
            choice = input(prompt).upper()
            if choice in valid_choices:
                return choice
            print(f"Invalid choice. Please choose from {', '.join(valid_choices)}.")

    # Usage example:
    action = get_valid_menu_choice("\nEnter action (B: Buy, S: Sell, J: Jet to next location, K: Bank, T: Tornado Cash): ", ['B', 'S', 'J', 'K', 'T'])
        
    def get_non_empty_input(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Input cannot be empty. Please try again.")

    # Usage example:
    item = get_non_empty_input("Enter the key of the item you want to buy: ").upper()

    def display_market(self):
        print("\nAvailable for purchase:")
        for item, price in self.market.items():
            if item in self.nfts:
                history = self.nft_history.get(item, {})
                if history.get('purchase_price'):
                    change = (price - history['purchase_price']) / history['purchase_price'] * 100
                    print(f"{self.nfts[item]}: ${price:.2f} ({item}) - Change: {change:.2f}%")
                else:
                    print(f"{self.nfts[item]}: ${price:.2f} ({item})")
            else:
                print(f"{self.coins[item]}: ${price:.2f} ({item})")
            
    def buy(self):
        item = input("Enter the key of the item you want to buy: ").upper()
        if item not in self.market:
            print("Invalid item or not available in this market.")
            return
    
        max_quantity = min(self.liquidity[item], self.player.wallet_space_available(), int(self.player.money / self.market[item]))
        if max_quantity == 0:
            print("You don't have enough money or wallet space to buy this item.")
            return

        quantity = int(get_valid_numeric_input(f"Enter the quantity (max {max_quantity}): ", min_value=1, max_value=max_quantity))
    
        
        if quantity > max_quantity:
            print(f"Can only buy up to {max_quantity} due to liquidity or wallet space constraints.")
            return
        
        available_quantity = self.has_sufficient_liquidity(item, quantity)
        if available_quantity < quantity:
            print(f"Due to liquidity constraints, you can only buy {available_quantity} units.")
            quantity = available_quantity
        
        if quantity == 0:
            print("Unable to buy due to lack of liquidity.")
            return
        
        total_cost = self.market[item] * quantity
        if total_cost > self.player.money:
            print("Not enough money.")
            return
        
        wallet_space = self.player.wallet_space_available()
        if quantity > wallet_space:
            print(f"Not enough wallet space. You need to free up {quantity - wallet_space} more space.")
            use_tornado = input("Do you want to use Tornado Cash to free up space? (Y/N): ").upper()
            if use_tornado == 'Y':
                self.tornado_cash_transfer()
                # Recalculate available space
                wallet_space = self.player.wallet_space_available()
                if quantity > wallet_space:
                    print("Still not enough space after using Tornado Cash. Cannot complete purchase.")
                    return
            else:
                return

        # Proceed with purchase
        item_type = 'coins' if item in self.coins else 'NFTs'
        if not self.player.add_to_wallet(item_type, item, quantity):
            print("Error adding to wallet.")
            return
        
        self.player.money -= total_cost
        self.liquidity[item] -= quantity
        print(f"Bought {quantity} {self.coins.get(item, self.nfts.get(item))} for ${total_cost:.2f}")

        # Handle NFT purchase history
        if item in self.nfts:
            if item not in self.nft_history:
                self.nft_history[item] = {
                    'purchase_price': self.market[item],
                    'opportunities': 0,
                    'scenario': self.determine_nft_scenario(),
                    'current_opportunity': 0
                }
        return {
            'success': True,
            'message': f"Bought {quantity} {self.coins.get(item, self.nfts.get(item))} for ${total_cost:.2f}",
            'new_balance': self.player.money
        }
        
        self.player.money -= total_cost
        self.liquidity[item] -= quantity
        print(f"Bought {quantity} {self.coins.get(item, self.nfts.get(item))} for ${total_cost:.2f}")

    def sell(self):
        item = get_non_empty_input("Enter the key of the item you want to sell: ").upper()
        item_type = 'coins' if item in self.coins else 'NFTs'
        
        if item not in self.player.wallet[item_type]:
            print("You don't have this item.")
            return
        
        if item not in self.market:
            print("This item is not currently tradeable in this market.")
            return
        
        max_quantity = self.player.wallet[item_type][item]
        quantity = int(get_valid_numeric_input(f"Enter the quantity (max {max_quantity}): ", min_value=1, max_value=max_quantity))
        
        # Liquidity check for selling
        if item in self.coins:
            liquidity = min(quantity, max(int(self.liquidity[item] * random.uniform(0.75, 1.0)), int(quantity * 0.65)))
        else:  # NFTs
            liquidity = quantity if random.random() > 0.35 else 0
        
        if liquidity < quantity:
            print(f"Due to liquidity constraints, you can only sell {liquidity} units.")
            quantity = liquidity
        
        if quantity == 0:
            print("Unable to sell due to lack of liquidity.")
            return
        
        if not self.player.remove_from_wallet(item_type, item, quantity):
            print("Error removing from wallet. This shouldn't happen - please report this bug.")
            return
        
        total_price = self.market[item] * quantity
        self.player.money += total_price
        self.liquidity[item] = self.liquidity.get(item, 0) + quantity
        
        if item in self.nfts:
            self.nft_history[item]['purchase_price'] = self.market[item]
        
        print(f"Sold {quantity} {self.coins.get(item, self.nfts.get(item))} for ${total_price:.2f}")

    def special_event(self):
        if random.random() < self.sec_investigation_chance:
            self.sec_investigation()
        else:
            events = [
            "China bans crypto!",
            "SEC clamping down on DeFi with tough new registration rules!",
            "Binance got hacked!",
            "1. What",
            "Jim Cramer announces that Bitcoin is in retirement portfolio and shouts Buy! Buy! Buy!",
            "Jim Cramer announces that he has sold all his crypto!",
            "Cardano releases yet another academic paper!",
            "Roaring Kitty tweets a picture of himself on the toilet!",
            "Gensler suggests on Twitter that ETH is a commodity. Later he clarifies his remarks!",
            "Your wife's boyfriend offers you a ride in his Lambo this morning!",
            "Peter Schiff appears on CNBC and shouts for a full hour about why Bitcoin sucks!",
            "Vitalik clarifies it's 9.5 inches!",
            "The parabola just broke!",
            "Gary Vee is out there grinding every day, making it, doing it, creating new realities. Living, which is not the same as being. Think about it. He's out there pumping bags bro. For real bruh"
        ]
        event = random.choice(events)
        effect = "Bullish!" if random.random() > 0.5 else "Bearish!"
        print(f"\n{event} {effect}")
        # Implement price changes based on the event

        return {
            'success': True,
            'message': f"Sold {quantity} {self.coins.get(item, self.nfts.get(item))} for ${total_price:.2f}",
            'new_balance': self.player.money
        }

    def play_turn(self):
        self.display_status()
        self.generate_market()
        self.special_event()
        self.display_market()
        
        while True:
            action = input("\nEnter action (B: Buy, S: Sell, J: Jet to next location, K: Bank, T: Tornado Cash): ").upper()
            if action == 'T':
                self.tornado_cash_transfer()
            elif action == 'B':
                self.buy()
            elif action == 'S':
                self.sell()
            elif action == 'J':
                break
            elif action == 'K':
                # Implement banking logic
                pass
            else:
                print("Invalid action.")

        self.player.debt += 1000  # Daily interest
        self.day += 1

    def play_game(self):
        try: 
            while self.day <= 30 and self.player.health > 0:
                self.play_turn()
            self.handle_pending_withdrawal()
            self.apply_bank_interest()
            self.end_game()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Game state has been saved. Please contact support for assistance.")
        
        # Game end logic
        total_worth = self.player.money + self.player.bank_balance
        # Add bank operations to the available actions
        while True:
            action = input("\nEnter action (B: Buy, S: Sell, J: Jet to next location, K: Bank, T: Tornado Cash): ").upper()
            if action == 'K':
                self.bank_operations()
        # Add value of coins and NFTs
        score = total_worth - self.player.debt
        print(f"\nGame Over! Your final score: ${score:.2f}")

    def apply_market_change(self, item_type, min_percent, max_percent):
        for item in self.market:
            if (item_type == 'coins' and item in self.coins) or (item_type == 'NFTs' and item in self.nfts):
                change = random.uniform(min_percent, max_percent) / 100
                self.market[item] *= (1 + change)

    def special_event(self):
        events = [
            ("China bans crypto!", "Bullish!",
             lambda: (self.apply_market_change('coins', 3, 17),
                      self.apply_market_change('NFTs', 20, 20))),
            
            ("SEC clamping down on DeFi with tough new registration rules!", "Bearish!",
             lambda: (self.apply_market_change('coins', -20, -5),
                      self.apply_market_change('NFTs', -20, -5))),
        ]
            
        ("Binance got hacked!", "Oops!"),
        
        
        ("1. What", "Neutral!", lambda: None),
        
        ("Jim Cramer announces that Bitcoin is in retirement portfolio and shouts Buy! Buy! Buy!", "Bearish!",
            lambda: self.apply_market_change('coins', -35, -5)),
        
        ("Jim Cramer announces that he has sold all his crypto!", "Bullish!",
            lambda: self.apply_market_change('coins', 25, 85)),
        
        ("Cardano releases yet another academic paper!", "Neutral!", lambda: None),
        
        ("Roaring Kitty tweets a picture of himself on the toilet!", "Slightly Bullish!",
            lambda: self.apply_market_change('coins', 1, 5)),
        
        ("Gensler suggests on Twitter that ETH is a commodity. Later he clarifies his remarks!", "Bearish for ETH!"),

        
        ("Your wife's boyfriend offers you a ride in his Lambo this morning!", "Bearish for NFTs!",
            lambda: self.apply_market_change('NFTs', -90, -90)),
        
        ("Peter Schiff appears on CNBC and shouts for a full hour about why Bitcoin sucks!", "Slightly Bearish!",
            lambda: self.apply_market_change('coins', -10, -5)),
        
        ("The parabola just broke!", "Bearish!",
            lambda: self.apply_market_change('coins', -20, -15)),
        
        ("Gary Vee is out there grinding every day, making it, doing it, creating new realities. Living, which is not the same as being. Think about it. He's out there pumping bags bro. For real bruh", "Extremely Bullish!",
            lambda: self.apply_market_change('coins', 50, 250)) 
        
    event, effect, action = random.choice(events)
    print(f"\n{event} {effect}")
    action()

    # Special case for Gary Vee event
    if "Gary Vee" in event:
        self.gary_vee_countdown = 1  # Will reset prices next turn

    def play_turn(self):
        self.display_status()
        self.generate_market()
        self.display_market()

        if random.random() <= 0.9:  # 90% chance of special event
            self.special_event()
        
        # Reset prices after Gary Vee event
        if hasattr(self, 'gary_vee_countdown'):
            if self.gary_vee_countdown == 0:
                self.generate_market()  # Reset market to normal
                del self.gary_vee_countdown
            else:
                self.gary_vee_countdown -= 1
       
        # Increase SEC investigation chance based on player's wealth
        player_wealth = self.player.money + sum(self.player.wallet['coins'].values()) + sum(self.player.wallet['NFTs'].values())
        self.sec_investigation_chance = min(0.30, 0.05 + (player_wealth / 1000000) * 0.01)
        
        if self.player.health <= 0:
            print("Your health has dropped to 0. Game Over!")
            return False
        
        return True
    
    def end_game(self):
        total_worth = (
            self.player.money +
            self.player.bank_balance +
            sum(self.market.get(coin, 0) * amount for coin, amount in self.player.wallet['coins'].items()) +
            sum(self.market.get(nft, 0) * amount for nft, amount in self.player.wallet['NFTs'].items())
        )
        
        # Calculate Tornado Cash assets
        tornado_cash_recovery_rate = random.uniform(0, 1)  # Random percentage between 0 and 100%
        tornado_cash_coins_worth = sum(self.market.get(coin, 0) * amount for coin, amount in self.player.tornado_cash['coins'].items())
        tornado_cash_nfts_worth = sum(self.market.get(nft, 0) * amount for nft, amount in self.player.tornado_cash['NFTs'].items())
        tornado_cash_total = tornado_cash_coins_worth + tornado_cash_nfts_worth
        tornado_cash_recovered = tornado_cash_total * tornado_cash_recovery_rate

        # Simulate a pop-up message for Tornado Cash asset recovery
        print("\n" + "="*50)
        print("     TORNADO CASH ASSET RECOVERY REPORT")
        print("="*50)
        print(f"Total assets sent via Tornado Cash: ${tornado_cash_total:.2f}")
        print(f"Recovery rate: {tornado_cash_recovery_rate:.2%}")
        print(f"Assets recovered: ${tornado_cash_recovered:.2f}")
        print("="*50)
        input("Press Enter to continue...")  # This pauses the game until the user presses Enter

        # Add recovered Tornado Cash assets to total worth
        total_worth += tornado_cash_recovered

        final_debt = self.player.debt
        score = total_worth - final_debt

        print("\nGame Over!")
        print(f"Total Worth (excluding Tornado Cash): ${total_worth - tornado_cash_recovered:.2f}")
        print(f"Recovered Tornado Cash Assets: ${tornado_cash_recovered:.2f}")
        print(f"Final Total Worth: ${total_worth:.2f}")
        print(f"Final Debt: ${final_debt:.2f}")
        print(f"Final Score: ${score:.2f}")

        if score >= 0:
            print("Congratulations! You've paid off your debt and made a profit!")
        else:
            print("Unfortunately, you weren't able to pay off your debt. Better luck next time!")

        # Detailed Tornado Cash breakdown
        if tornado_cash_total > 0:
            print("\nTornado Cash Assets Breakdown:")
            print("Coins:")
            for coin, amount in self.player.tornado_cash['coins'].items():
                value = self.market.get(coin, 0) * amount
                recovered_value = value * tornado_cash_recovery_rate
                print(f"  {self.coins[coin]}: {amount} (Total: ${value:.2f}, Recovered: ${recovered_value:.2f})")
            print("NFTs:")
            for nft, amount in self.player.tornado_cash['NFTs'].items():
                value = self.market.get(nft, 0) * amount
                recovered_value = value * tornado_cash_recovery_rate
                print(f"  {self.nfts[nft]}: {amount} (Total: ${value:.2f}, Recovered: ${recovered_value:.2f})")


if __name__ == "__main__":
    game = Game()
    game.play_game()
