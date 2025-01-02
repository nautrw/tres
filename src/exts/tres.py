import random

import disnake
from disnake.ext import commands

colors = ['r', 'g', 'b', 'y']


class Tres(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def solitary_tres(self,
                            inter: disnake.ApplicationCommandInteraction,
                            target: disnake.User):
        players = [[inter.author.id, []], [target.id, []]]
        turn = 0
        game_won = False

        for player in players:
            for _ in range(5):
                player[1].append((random.choice(colors), random.randint(1, 9)))

        while not game_won:
            for player in players:
                class CardsDropdown(disnake.ui.StringSelect):
                    def __init__(self):
                        options = [
                            disnake.SelectOption(label=f"{card[0]}, {card[1]}") for card in player[1]
                        ]

                        super().__init__(
                            placeholder="Choose a card",
                            min_values=1,
                            max_values=1,
                            options=options,
                        )

                    async def callback(self, inter: disnake.MessageInteraction):
                        await inter.response.send_message("Played card")

                class CardsDropdownView(disnake.ui.View):
                    def __init__(self):
                        super().__init__()

                        self.add_item(CardsDropdown())

                await inter.send(view=CardsDropdownView(), ephemeral=True)


def setup(bot):
    bot.add_cog(Tres(bot))
