import random
import time

class Creature:
    def __init__(self, name, max_hp=10):
        self.name = name + " the Creature"
        self.max_hp = max_hp
        self.hp = max_hp
        self.abilities = {'Attack': 1, 'Defence': 5, 'Speed': 5}

    def check_life(self):
        if self.hp <= 0:
            print(f"{self.name} fainted...")
            self.hp = 0
        return self.hp
    
    def check_life_silent(self):
        if self.hp <= 0:
            self.hp = 0
        return self.hp

    def attack(self, target):
        if self.check_life_silent() == 0:
            return
        roll = random.randint(1, 20)
        success_threshold = target.abilities['Defence'] + target.abilities['Speed']

        if roll > success_threshold:
            damage = self.abilities['Attack'] + random.randint(1, 4)
            target.hp -= damage
            print(f"{self.name} successfully attacked {target.name} for {damage} damage!")
            target.check_life()
        else:
            print(f"{self.name}'s attack on {target.name} was unsuccessful.")

    def auto_select(self, target_list):
        available_targets = [creature for creature in target_list if creature.check_life_silent() > 0]
        if available_targets:
            return random.choice(available_targets)
        else:
            return None

    def turn(self, round_num, target_list):
        time.sleep(1)
        if self.check_life_silent() == 0:
            return 
        print(f"\nRound {round_num}: {self.name}'s turn")
        target = self.auto_select(target_list)

        if target:
            self.attack(target)
        else:
            print(f"No valid target for {self.name}.")

class Goblin(Creature):
    
    def __init__(self, name, max_hp=15):
        self.name = name + " the Goblin"
        self.max_hp = max_hp
        self.hp = max_hp
        self.abilities = {'Attack': 3, 'Defence': 6, 'Speed': 6}
        

class Orc(Creature):
    
    def __init__(self, name, max_hp=50):
        self.name = name + " the Orc"
        self.max_hp = max_hp
        self.hp = max_hp
        self.abilities = {'Attack': 5, 'Defence': 8, 'Speed': 3}
        self.in_rage = False  # Flag variable for Orc's heavy attack
        self.cooled_down = True  # Flag variable for Orc's cooldown
            
    
    def heavy_attack(self,target):
        if not self.in_rage:
            print(f"{self.name} is in rage! Increasing Attack by 5 and decreasing Defence by 3.")
            self.abilities['Attack'] += 5
            self.abilities['Defence'] -= 3
            self.in_rage = True
        else:
            print(f"{self.name} is still enraged!")
        
        self.attack(target)
        
    def cool_attack(self, target):
        if not self.cooled_down:
            self.reset_stats()
            self.cooled_down = True
        
        #Orc is already cooled down. Cannot stack cooldown attacks.
        # Proceed with a normal attack
        self.attack(target)
        
    def reset_stats(self):
        # Reset stats to their original values
        if self.in_rage:
            print(f"{self.name} cooled down. Resetting Attack and Defence values.")
            self.abilities = {'Attack': 5, 'Defence': 8, 'Speed': 3}
            self.in_rage = False
            self.cooled_down = False
        
    def turn(self, round_num, target_list):
        time.sleep(1)
        # Check if the Orc has fainted
        if self.check_life_silent() == 0:
            return
        print(f"\nRound {round_num}: {self.name}'s turn")
        # Orc's battle strategy repeats every 4 rounds
        if round_num % 4 == 0:
            # Round 4: Use heavy_attack
            target = self.auto_select(target_list)
            if target:
                self.heavy_attack(target)
            else:
                print(f"No valid target for {self.name}.")
        else:
            # Rounds 1, 2, 3: Use normal attack
            target = self.auto_select(target_list)
            if target:
                self.cool_attack(target)
            else:
                print(f"No valid target for {self.name}.")

class Warrior(Creature):
    
    def __init__(self, name, max_hp=50):
        self.name = name + " the Warrior"
        self.max_hp = max_hp
        self.hp = max_hp
        self.abilities = {'Attack': 5, 'Defence': 10, 'Speed': 4}
        self.shield = False
        
    def shield_up(self):
        if not self.shield:
            print(f"{self.name} raises shield! Increasing Defence by 4 and decreasing Attack by 4.")
            self.abilities['Attack'] += 4
            self.abilities['Defence'] -= 4
            self.shield = True
        else:
            print(f"{self.name} shield is still raised.")
        
    def shield_down(self):
        if  self.shield:
            print(f"{self.name} lowers shield. Resetting Attack and Defence values.")
            self.reset_stats()
            self.shield = False
        
        else:
            print("Shield is already down.")
        
    def reset_stats(self):
        # Reset stats to their original values
            self.abilities = {'Attack': 5, 'Defence': 10, 'Speed': 4}
            
            
    def turn(self, round_num, target_list):
        time.sleep(1)
        # Check if fainted
        if self.check_life_silent() == 0:
            return
        print(f"\nRound {round_num}: {self.name}'s turn")
        #Warrior's battle strategy repeats every 4 rounds
        if round_num % 4 == 1:
            # Round 1: Attack and use shield_up
            target = self.auto_select(target_list)
            if target:
                self.attack(target)
                self.shield_up()
            else:
                print(f"No valid target for {self.name}.")
        elif round_num % 4 == 2 or round_num % 4 == 3:
            # Rounds 2 and 3: Just attack
            target = self.auto_select(target_list)
            if target:
                self.attack(target)
            else:
                print(f"No valid target for {self.name}.")
        elif round_num % 4 == 0:
            # Round 4: Use shield_down and then attack
            self.shield_down()
            target = self.auto_select(target_list)
            if target:
                self.attack(target)
            else:
                print(f"No valid target for {self.name}.")

class Archer(Creature):
    
    def __init__(self, name, max_hp=30):
        self.name = name + " the Archer"
        self.max_hp = max_hp
        self.hp = max_hp
        self.abilities = {'Attack': 7, 'Defence': 9, 'Speed': 8}
        self.power = False
        
    def power_shot(self, target):
        num1 = random.randint(1,20)
        num2 = random.randint(1,20)
        roll = max(num1,num2)
        success_threshold = target.abilities['Defence'] + target.abilities['Speed']
    
        if self.abilities['Speed'] > target.abilities['Speed']:
            roll += (self.abilities['Speed'] - target.abilities['Speed'])
            
        if not self.power:
            self.abilities['Attack'] += 3
            self.abilities['Defence'] -= 3
            self.power = True
            
        
        if roll > success_threshold:
            damage = self.abilities['Attack'] + random.randint(1, 8)
            target.hp -= damage
            print(f"{self.name} successfully used Power-Shot on {target.name} for {damage} damage!")
            target.check_life()
        else:
            print(f"{self.name}'s Power-Shot on {target.name} was unsuccessful.")  
            
    def cool_attack(self, target):
        if self.power:
            self.reset_stats()
        
        #Archer is already cooled down
        # Proceed with a normal attack
        self.attack(target)
        
    def reset_stats(self):
        # Reset stats to their original values
        if self.power:
            print(f"{self.name} cooled down. Resetting Attack and Defence values.")
            self.abilities = {'Attack': 7, 'Defence': 8, 'Speed': 9}
            self.power = False
            
    def auto_select(self, target_list):
        available_targets = [creature for creature in target_list if creature.check_life_silent() > 0]
        if available_targets:
            # Choose the target with the fewest HP
            target = min(available_targets, key=lambda x: x.hp)
            return target
        else:
            return None
        
        
    def turn(self, round_num, target_list):
        time.sleep(1)
        # Check if fainted
        if self.check_life_silent() == 0:
            return
        print(f"\nRound {round_num}: {self.name}'s turn")
        #Archer's battle strategy repeats every 4 rounds
        if round_num % 4 == 1:
            # Round 1: Normal Attack
            target = self.auto_select(target_list)
            if target:
                self.cool_attack(target)
            else:
                print(f"No valid target for {self.name}.")
        else :
            # Rounds 2 3 4: Power attack
            target = self.auto_select(target_list)
            if target:
                self.power_shot(target)
            else:
                print(f"No valid target for {self.name}.")

class Fighter(Creature):
    
    def __init__(self, name, max_hp=50):
        self.name = name + " the Fighter"
        self.max_hp = max_hp
        self.hp = max_hp
        self.abilities = {'Attack': 5, 'Defence': 8, 'Speed': 5}
        
    def auto_select(self, target_list):
        available_targets = [creature for creature in target_list if creature.check_life_silent() > 0]
        if available_targets:
            # Choose the target with the most HP
            target = max(available_targets, key=lambda x: x.hp)
            return target
        else:
            return None
        
    def attack_with_penalty(self, target):
        roll = random.randint(1, 20)
        success_threshold = target.abilities['Defence'] + target.abilities['Speed']

        if roll > success_threshold:
            damage = (self.abilities['Attack'] - 3) + random.randint(1, 4)
            target.hp -= damage
            print(f"{self.name} successfully attacked {target.name} for {damage} damage!")
        else:
            print(f"{self.name}'s attack on {target.name} was unsuccessful.")
    
    def turn(self, round_num, target_list):
        time.sleep(1)
        # Check if fainted
        if self.check_life_silent() == 0:
            return
        print(f"\nRound {round_num}: {self.name}'s turn")
        #Fighter's battle strategy attacks three times a round      
        for attack_num in range(1, 4):
            target = self.auto_select(target_list)

            if target:
                if attack_num == 1:
                    self.attack(target)
                else:
                    # For the last 2 attacks, apply a -3 penalty to the attack ability
                    self.attack_with_penalty(target)
                
                # Check if the target is defeated before finishing all attacks
                if target.check_life_silent() == 0 and attack_num < 3:
                    target = self.auto_select(target_list)  # Select the next target with the most HP

            else:
                print(f"No valid target for {self.name}.")

class OrcGeneral(Orc, Warrior):
    
    def __init__(self, name, max_hp=80):
        self.name = name + " the Orc General"
        self.max_hp = max_hp
        self.hp = max_hp
        self.abilities = {'Attack': 5, 'Defence': 8, 'Speed': 3}
        self.shield = False
        self.in_rage = False  # Flag variable for Orc's heavy attack
        self.cooled_down = True  # Flag variable for Orc's cooldown
    
    def turn(self, round_num, target_list):
        time.sleep(1)
        # Check if fainted
        if self.check_life_silent() == 0:
            return
        print(f"\nRound {round_num}: {self.name}'s turn")
        #Warrior's battle strategy repeats every 4 rounds
        if round_num % 4 == 1:
            # Round 1: Attack and use shield_up
            target = self.auto_select(target_list)
            if target:
                self.attack(target)
                self.shield_up()
            else:
                print(f"No valid target for {self.name}.")
        elif round_num % 4 == 2:
            # Rounds 2: Just attack
            target = self.auto_select(target_list)
            if target:
                self.attack(target)
            else:
                print(f"No valid target for {self.name}.")
        elif round_num % 3 == 0:
            # Round 3: Use shield_down and then attack
            self.shield_down()
            target = self.auto_select(target_list)
            if target:
                self.attack(target)
            else:
                print(f"No valid target for {self.name}.") 
            # Round 4: Heavy attack
        elif round_num % 4 == 0:
            target = self.auto_select(target_list)
            if target:
                self.heavy_attack(target)
            else:
                print(f"No valid target for {self.name}.")

class GoblinKing(Goblin, Archer):
    
    def __init__(self, name, max_hp=50):
        self.name = name + " the Goblin King"
        self.max_hp = max_hp
        self.hp = max_hp
        self.abilities = {'Attack': 3, 'Defence': 6, 'Speed': 6}
        self.power = False
        
    def turn(self, round_num, target_list):
        time.sleep(1)
        # Check if fainted
        if self.check_life_silent() == 0:
            return
        print(f"\nRound {round_num}: {self.name}'s turn")
        #Archer's battle strategy repeats every 4 rounds
        if round_num % 4 == 1:
            # Round 1: Normal Attack
            target = self.auto_select(target_list)
            if target:
                self.cool_attack(target)
            else:
                print(f"No valid target for {self.name}.")
        else :
            # Rounds 2 3 4: Power attack
            target = self.auto_select(target_list)
            if target:
                self.power_shot(target)
            else:
                print(f"No valid target for {self.name}.")
    
class Boss(Orc):
    
    def __init__(self, name, max_hp=200):
        self.name = name + " the Boss"
        self.max_hp = max_hp
        self.hp = max_hp
        self.abilities = {'Attack': 5, 'Defence': 8, 'Speed': 5}
        self.in_rage = False  # Flag variable for Orc's heavy attack
        self.cooled_down = True  # Flag variable for Orc's cooldown
        
        
    
    def auto_select(self, target_list, mode='Random'):
        available_targets = [creature for creature in target_list if creature.check_life_silent() > 0]
        if available_targets:
            if mode == 'Random':
                mode = random.choice(['Weak', 'Strong'])

            if mode == 'Weak':
                target = min(available_targets, key=lambda x: x.hp)
            elif mode == 'Strong':
                target = max(available_targets, key=lambda x: x.hp)
        else:
            target = None

        return target
        
    def attack_with_penalty(self, target):
        roll = random.randint(1, 20)
        success_threshold = target.abilities['Defence'] + target.abilities['Speed']

        if roll > success_threshold:
            damage = (self.abilities['Attack'] - 3) + random.randint(1, 4)
            target.hp -= damage
            print(f"{self.name} successfully attacked {target.name} for {damage} damage!")
        else:
            print(f"{self.name}'s attack on {target.name} was unsuccessful.")
    
    def turn(self, round_num, target_list):
        time.sleep(1)
        # Check if fainted
        if self.check_life_silent() == 0:
            return
        print(f"\nRound {round_num}: {self.name}'s turn")
        #Fighter's battle strategy round 1
        if round_num % 4 == 1:
            for attack_num in range(1, 4):
                target = self.auto_select(target_list,mode = 'Weak')

                
                if target:
                    if attack_num == 1:
                        self.attack(target)
                    else:
                        # For the last 2 attacks, apply a -3 penalty to the attack ability
                        self.attack_with_penalty(target)

                    # Check if the target is defeated before finishing all attacks
                    if target.check_life_silent() == 0 and attack_num < 3:
                        target = self.auto_select(target_list,mode = 'Random')  # Select the next target with the most HP

                else:
                    print(f"No valid target for {self.name}.")
        else:
            target = self.auto_select(target_list,mode = 'Strong')
            if target:
                self.heavy_attack(target)
            else:
                print(f"No valid target for {self.name}.")

class Wizard(Creature):
    
    def  __init__(self, name, max_hp = 20, mana = 100 ):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mana = mana
        self.mana = mana
        self.abilities = {'Attack': 3, 'Defence': 5, 'Speed': 5, 'Arcana': 10}
        
    def wiz_attack(self, target):
        print(f"{self.name} casts a magical attack on {target.name}.")
        if target.hp == 0:
            print(f"{target.name} had already fainted. Way to kick a creature while they're down, {self.name}")
        self.attack(target)
        

        # Regain 20 Mana points after the attack
        self.recharge_mana(20)

    def recharge_mana(self, mana=30):
        self.amount = mana
        self.mana += mana
        # Ensure Mana is in the range [0, 100]
        self.mana = max(0, min(self.mana, 100))
        print(f"{self.name} channels magical energy")
        print(f"{self.name} regained {self.amount} Mana points. Current Mana: {self.mana}")
        
    def fire_bolt(self, target):
        print(f"{self.name} casts a fiery bolt at {target.name}.")
        # Add half the Arcana value to the attack roll (rounded down)
        roll = random.randint(1, 20) + self.abilities['Arcana'] // 2
        success_threshold = target.abilities['Defence'] + target.abilities['Speed']

        if roll > success_threshold:
            # Deal damage in the range [1, Arcana value]
            damage = random.randint(1, self.abilities['Arcana'])
            target.hp -= damage
            print(f"{self.name}'s fire bolt hit {target.name} for {damage} damage!")

            # Gain 10 Mana points after a successful fire bolt
            self.recharge_mana(10)
        else:
            print(f"{self.name}'s fire bolt on {target.name} was unsuccessful.")
        if target.hp == 0:
            print(f"{target.name} had already fainted. Way to kick a creature while they're down, {self.name}")
            
    def heal(self, target):
        # Check if there is enough Mana to perform the heal
        if self.mana >= 20:
            # Spend 20 Mana Points
            self.mana -= 20
            print("Mana: -20")
            # Calculate the amount healed
            amount_healed = random.randint(0, 8) + self.abilities['Arcana'] // 2

            # Increase target's HP within their maximum HP limit
            if target.hp == 0:
                print(f" {target.name} had fainted. You revived them! The great healer, {self.name} !")
            
            target.hp = min(target.max_hp, target.hp + amount_healed)

            print(f"{self.name} casts a healing spell on {target.name} and restores {amount_healed} HP.")
            print(f"{self.name}'s Mana: {self.mana}")
        else:
            print(f"{self.name} does not have enough Mana to perform the healing. Turn is skipped")

    def rest(self):
        print(f"{self.name} has decided to rest and skip their turn. Awarding HP and Mana")
        self.recharge_mana(30)
        amount_healed = random.randint(0, 8) + self.abilities['Arcana'] // 2

            # Increase HP within maximum HP limit
        self.hp = min(self.max_hp, self.hp + amount_healed)
        print(f"HP: +{amount_healed}!")
        print(f"Current HP: {self.hp}")
        
            
    def mass_heal(self, allies):
        # Check if there is enough Mana to perform the mass heal
        if self.mana >= 30:
            # Spend 30 Mana Points
            self.mana -= 30
            print("Mana: -30")
            # Calculate the amount healed
            amount_healed = random.randint(0, 10) + self.abilities['Arcana']

            # Increase HP for each ally within their maximum HP limit
            for ally in allies:
                amount_healed = random.randint(0, 10) + self.abilities['Arcana']
                if ally.hp == 0:
                        print(f" {ally.name} had fainted and now has risen. The great healer strikes again!")
                ally.hp = min(ally.max_hp, ally.hp + amount_healed)
                print(f"{self.name} casts a healing spell on {ally.name} and restores {amount_healed} HP.")
            amount_healed = random.randint(0, 10) + self.abilities['Arcana']
            print(f"{self.name} casts a healing spell on themselves and restores {amount_healed} HP.")
            print(f"{self.name}'s Mana: {self.mana}")
                
        else:
            print(f"{self.name} does not have enough Mana to perform the mass healing. Turn is skipped")
            
    def fire_storm(self, enemies):
        # Check if there is enough Mana to perform the fire storm
        if self.mana >= 50:
            # Spend 50 Mana Points
            self.mana -= 50
            print("Mana: -50")
            for target in enemies:
                if target.hp > 0:
                    # Use a random number in the range [1, 20] and add its speed
                    roll = random.randint(1, 20) + target.abilities['Speed']
                    success_threshold = self.abilities['Arcana']

                    # Calculate the full amount of damage
                    full_damage = random.randint(5, 20) + self.abilities['Arcana']

                    # Check if the result is greater or equal to the Wizard’s Arcana value
                    if roll >= success_threshold:
                        # Targets take half damage
                        damage = full_damage // 2
                        print(f"{target.name} is too illusive! {self.name}'s fire storm only hits for {damage}!")
                        target.hp = max(0, target.hp - damage)
                        target.check_life()
                    else:
                        # Targets take the full amount of damage
                        damage = full_damage
                        print(f"{self.name} casts a powerful fire storm, dealing full damage of {damage} to {target.name}.")
                        target.hp = max(0, target.hp - damage)
                        target.check_life()
                    
                    
            print(f"{self.name}'s Mana: {self.mana}")
        else:
            print(f"{self.name} does not have enough Mana to perform the fire storm. Turn is skipped")
            
    def select_target(self, target_list):
        print("Select a target:")
        for index, target in enumerate(target_list):
            print(f"{index + 1}. {target.name}, HP: {target.hp}/{target.max_hp}")

        while True:
            try:
                choice = int(input("Enter choice: "))
                if 1 <= choice <= len(target_list):
                    return target_list[choice - 1]
                else:
                    print("Invalid input. Please enter a valid index.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")



class Battle(Boss):
    def __init__(self, player, allies, enemies):
        self.player = player
        self.enemies = enemies
        self.allies = allies
        self.boss = None

    def sort_turn_order(self):
        # Sort creatures based on their Speed, from highest to lowest
        all_creatures = self.enemies + self.allies
        all_creatures.sort(key=lambda creature: creature.abilities['Speed'], reverse=True)
        return all_creatures
    
    def help(self):
        print("\nAvailable Actions:")
        print("1. Attack = Performs a weak attack on target of choice. Also regains 20 Mana ")
        print("2. Fire Bolt = Fires a more powerful fiery arrow at target of choice. Also regains 10 Mana")
        print("3. Heal = Heals an Ally of choice. Must have 20 Mana to perform or will fail")
        print("4. Mass Heal = Heals all allies and player at once. Must have 30 Mana or will fail")
        print("5. Fire Storm = Showers down powerful destructive arrows on enemies. Must have 50 Mana to perform or will fail")
        print("6. Rest = Skips Turn but in doing so player gains HP and Mana")
        print("Q. Quit = Ends Game")
        print("H. Help = Shows options descriptions")
        print(" ")
        
    
    def player_turn(self):
        # Display UI for the player
        print("\n--- Player's Turn ---")
        print(f"Name: {self.player.name}   HP: {self.player.hp}/{self.player.max_hp}")
        print(f"Mana Points: {self.player.mana}/{self.player.max_mana}")

        print("\nAllies:")
        for ally in self.allies:
            print(f"{ally.name}   HP: {ally.hp}/{ally.max_hp}")

        print("\nEnemies:")
        for enemy in self.enemies:
            print(f"{enemy.name}   HP: {enemy.hp}/{enemy.max_hp}")

        # Display available actions and spells
        print("\nAvailable Actions:")
        print("1. Attack")
        print("2. Fire Bolt")
        print("3. Heal **Must have 20 Mana**")
        print("4. Mass Heal ** Must have 30 Mana **")
        print("5. Fire Storm ** Must have 50 Mana **")
        print("6. Rest")
        print("H. Help")
        print("Q. Quit")

        # Ask for input from the player
        while True:
            choice = input("Choose an action (1-6), H for Help or Q to quit): ").lower()

            if choice == '1':
                target = self.player.select_target(self.enemies)
                self.player.wiz_attack(target)
                break
            elif choice == '2':
                target = self.player.select_target(self.enemies)
                self.player.fire_bolt(target)
                break
            elif choice == '3':
                target = self.player.select_target(self.allies)
                self.player.heal(target)
                break
            elif choice == '4':
                allies_to_heal = self.allies.copy()
                self.player.mass_heal(allies_to_heal)
                break
            elif choice == '5':
                self.player.fire_storm(self.enemies)
                break
            elif choice == '6':
                self.player.rest()
                break
            elif choice == 'h':
                battle.help()
            elif choice == 'q':
                print("Player chose to quit the game.")
                exit()  # Terminate the game
            else:
                print("Invalid choice. Please enter a valid option.")

    def friends_foes(self):
        print(" ")
        print("We shall begin with the fearsome grunts we will face today")
        enemy1 = GoblinKing("Robert")
        print(" ")
        print(f"{enemy1.name} - The fearsome Goblin King, Robert, leads his goblin horde with ruthless cunning and dark magic.")
        print(" ")
        enemy2 = OrcGeneral("Emmet")
        print(f"{enemy2.name} - Emmet, the formidable Orc General, commands the orcish forces with strategic brilliance and raw strength.")
        print(" ")
        enemy3 = Orc("Brock")
        print(f"{enemy3.name} - Brock, a fierce Orc warrior, stands ready for battle, wielding a brutal strength and tenacity.")
        print(" ")
        enemy4 = Goblin("Smithers")
        print(f"{enemy4.name} - Smithers, a cunning goblin, lurks in the shadows, using sly tactics to outsmart his foes.")
        print(" ")
        time.sleep(3)
        print("And finally our brave valiant friends who will defend our land")
        print(" ")
        Ally1 = Archer("Archie")
        print(f"{Ally1.name} - Archie, the skilled Archer, provides deadly precision from a distance, piercing enemies with accurate arrows.")
        print(" ")
        Ally2 = Creature("John")
        print(f"{Ally2.name} - John, a valiant and versatile ally, contributes to the battle with a variety of skills and abilities.")
        print(" ")
        Ally3 = Fighter("Jimmy")
        print(f"{Ally3.name} - Jimmy, the Fighter, excels in close combat, delivering powerful strikes and defending his allies with unwavering bravery.")
        print(" ")
        Ally4 = Warrior("Gerard")
        print(f"{Ally4.name} - Gerard, the mighty Warrior, combines strength and resilience, charging into battle to crush adversaries with unmatched force.")
        time.sleep(3)

        

    def start(self):
        round_num = 1
        print("The battle begins!")

        while True:
            print(f"\n--- Round {round_num} ---")
            print('===' * 30)

            # Sort creatures based on Speed for this round
            turn_order = self.sort_turn_order()

            for creature in turn_order:
                # Check for conditions to add the boss
                if sum(enemy.check_life_silent() <= 0 for enemy in self.enemies) == len(self.enemies) - 1 and not self.boss:
                    print("\n--- Boss Appears! ---")
                    self.boss = Boss(name="Python")
                    self.enemies.append(self.boss)

                # Check for battle end conditions
                if all(ally.check_life_silent() == 0 for ally in self.allies):
                    print("\n--- Allies Defeated! Game Over! ---")
                    print(f" As the dust settles on the battlefield, a somber atmosphere envelops the once-hopeful heroes. Alas, the indomitable wizard {playerName} and his brave crew have fallen, and with him, the last flicker of resistance against the encroaching darkness. \nThe enemies' malevolent forces have proven too formidable, and the realm succumbs to the looming shadow. \nThe loss is palpable, and a chilling silence descends, marking the end of a valiant struggle. \nThe adversaries celebrate their triumph, leaving a grim reminder of the consequences that befall a world bereft of its champions.")
                    again = input("Would you like to play again? Y/N ").lower
                    if again == 'y':
                        break
                        battle.start()
                    elif again == 'n':
                        break
                        exit()
                            
                    
                elif all(enemy.check_life_silent() == 0 for enemy in self.enemies):
                    print("\n--- Victory! All enemies defeated! ---")
                    print(f"As the final echoes of spells and clashes subside, a triumphant silence settles over the battlefield.\nThe heroes, led by the indomitable wizard {playerName}, stand victorious amidst the vanquished foes. \nThe once-menacing enemies lie defeated, their dark intentions thwarted. The realm is saved, and a newfound sense of peace descends. \nThe valor and resilience of our champions have prevailed, securing a brighter future for all. \nThe echoes of this hard-fought victory resonate throughout the land, a testament to the unwavering spirit that stood against the encroaching darkness.")

                    
                    again = input("Would you like to play again? Y/N ").lower
                    if again == 'y':
                        break
                        battle.start()
                    elif again == 'n':
                        break
                        exit()
                    
                elif self.player.check_life_silent() <= 0:
                    print("\n--- Game Over! Player defeated! ---")
                    print(f"As the dust settles on the battlefield, a somber atmosphere envelops the once-hopeful heroes. Alas, the indomitable wizard {playerName} has fallen, and with him, the last flicker of resistance against the encroaching darkness. \nThe enemies' malevolent forces have proven too formidable, and the realm succumbs to the looming shadow. \nThe loss is palpable, and a chilling silence descends, marking the end of a valiant struggle. \nThe adversaries celebrate their triumph, leaving a grim reminder of the consequences that befall a world bereft of its champions.")

                    again = input("Would you like to play again? Y/N ").lower
                    if again == 'y':
                        break
                        battle.start()
                            
                    elif again == 'n':
                        break
                        exit()
                        

                if creature.check_life_silent() > 0:
                    if creature == self.player:
                        self.player_turn()
                    elif creature in self.allies:
                        creature.turn(round_num, self.enemies)
                    elif creature in self.enemies:
                        creature.turn(round_num, self.allies)
                # Check for battle end conditions
                if all(ally.check_life_silent() == 0 for ally in self.allies):
                    print("\n--- Allies Defeated! Game Over! ---")
                    print(f" As the dust settles on the battlefield, a somber atmosphere envelops the once-hopeful heroes. Alas, the indomitable wizard {playerName} and his brave crew have fallen, and with him, the last flicker of resistance against the encroaching darkness. \nThe enemies' malevolent forces have proven too formidable, and the realm succumbs to the looming shadow. \nThe loss is palpable, and a chilling silence descends, marking the end of a valiant struggle. \nThe adversaries celebrate their triumph, leaving a grim reminder of the consequences that befall a world bereft of its champions.")
                    again = input("Press Enter to exit.") 
                    exit()
                            
                    
                elif all(enemy.check_life_silent() == 0 for enemy in self.enemies):
                    print("\n--- Victory! All enemies defeated! ---")
                    print(f"As the final echoes of spells and clashes subside, a triumphant silence settles over the battlefield.\nThe heroes, led by the indomitable wizard {playerName}, stand victorious amidst the vanquished foes. \nThe once-menacing enemies lie defeated, their dark intentions thwarted. The realm is saved, and a newfound sense of peace descends. \nThe valor and resilience of our champions have prevailed, securing a brighter future for all. \nThe echoes of this hard-fought victory resonate throughout the land, a testament to the unwavering spirit that stood against the encroaching darkness.")
                    again = input("Press Enter to exit.") 
                    exit()
                    
                elif self.player.check_life_silent() <= 0:
                    print("\n--- Game Over! Player defeated! ---")
                    print(f"As the dust settles on the battlefield, a somber atmosphere envelops the once-hopeful heroes. Alas, the indomitable wizard {playerName} has fallen, and with him, the last flicker of resistance against the encroaching darkness. \nThe enemies' malevolent forces have proven too formidable, and the realm succumbs to the looming shadow. \nThe loss is palpable, and a chilling silence descends, marking the end of a valiant struggle. \nThe adversaries celebrate their triumph, leaving a grim reminder of the consequences that befall a world bereft of its champions.")
                    again = input("Press Enter to exit.") 
                    exit()

            
            print(f"\n--- End of Round {round_num} ---")
            print('===' * 30)
            round_num += 1

enemy1 = GoblinKing("Robert")
enemy2 = OrcGeneral("Emmet")
enemy3 = Orc("Brock")
enemy4 = Goblin("Smithers")
Ally1 = Archer("Archie")
Ally2 = Creature("John")
Ally3 = Fighter("Jimmy")
Ally4 = Warrior("Gerard")
playerName = input("Elvis the TownCrier: Mr. Wizard what is your name? ")
Player = Wizard(playerName)
battle = Battle(player = Player, allies = [Player, Ally1, Ally2, Ally3, Ally4],enemies=[enemy1, enemy2, enemy3, enemy4])
time.sleep(2)
print(" ")
counter_name = 0
print(f"Elvis the TownCrier: Ah yes! I have heard of you! The most powerful wizard this land has ever seen! {playerName}, it is an honour to battle alongside you.")
print(" ")
while True:
    story = input("Elvis the TownCrier: Would you like to hear the story behind the battle that is about to break out?? Y/N : ").lower()
    if story == 'y':
        time.sleep(1)
        print(" ")
        print("Elvis the TownCrier: As the first rays of dawn illuminate the battlefield, a sense of foreboding looms in the air.")
        time.sleep(5)
        print(" ")
        print(f"The clash between our valiant hero , the renowned wizard {playerName}, and the menacing forces of darkness is imminent.")
        time.sleep(5)
        print(" ")
        print("The enemies, led by formidable creatures, Robert the Goblin King, Emmet the Orc General, Brock the Orc, and Smithers the Goblin, have gathered with nefarious intent.")
        time.sleep(5)
        print(" ")
        print(f"The fate of the realm hangs in the balance, and defeat is not an option. {playerName}, with his mystical powers and allies by his side, must navigate through the treacherous")
        print("battle ahead.")
        time.sleep(5)
        print(" ")
        print("The foes are relentless, and a formidable boss, Python, awaits in the wings to join the fray. The very essence of our world hinges on this confrontation, and the consequences")
        print("of failure are dire.")
        time.sleep(5)
        print(" ")
        print("The battlefield echoes with the urgency of the impending struggle, and only through strategic prowess and unwavering determination can our heroes hope to emerge victorious and")
        print("safeguard the realm from impending doom.")
        time.sleep(5)
        print(" ")
        print("===" * 30)
        break
    elif story == 'n':
        time.sleep(2)
        print(" ")
        counter_name += 1
        print("Elvis the TownCrier: Very well. I suppose you're too busy to listen to little ole me")
        print(" ")
        print("===" * 30)
        time.sleep(3)
        break
    else:
        print("Invalid Input. Please Try again")

while True:
    story = input("Elvis the TownCrier: Would you like to hear about the attack options your almighty wizardly powers have granted you?? Y/N : ").lower()
    if story == 'y':
        print(" ")
        battle.help()
        print("===" * 30)
        time.sleep(10)
        break
    elif story == 'n':
        print(" ")
        counter_name += 1
        print("Elvis the TownCrier: Very well. In a rush are we?")
        print("===" * 30)
        break
    else:
        print("Invalid input. Please Try Again")

while True:
    story = input("Elvis the TownCrier: Would you like to hear about our enemies who we will slaughter and the mighty soldiers who are to fight alongside you?? Y/N : ").lower()
    if story == 'y':
        print(" ")
        print("===" * 30)
        battle.friends_foes()
        print("Elvis the TownCrier: Let the games begin!")
        time.sleep(15)
        break
    elif story == 'n':
        counter_name += 1
        print(" ")
        print("===" * 30)
        print("Elvis the TownCrier: Very well. A bit rude but anyway, Let the games begin!")
        time.sleep(2)
        break
    else:
        print("Invalid input. Please Try Again")

        
if counter_name == 3:
    Player.name = Player.name + ' the Impatient'
elif counter_name == 2:
    Player.name = Player.name + ' the Rude'
elif counter_name == 1:
    Player.name = Player.name + ' the Wise'
else:
    Player.name = Player.name + ' the Listener'
    
print(f"Elvis the TownCrier: I hope you enjoy your new nickname. {Player.name} :)")
time.sleep(4)
battle.start()
