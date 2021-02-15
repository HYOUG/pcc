import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *
from random import choice, choices, randint, uniform
from time import time


class Claims(commands.Cog):
    """
    Commands :
    - spin
    - daily
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spin(self, ctx):
        """Claim the spin (30 min cooldown)"""
        cooldowns = get_file("cooldowns")

        if time() > (cooldowns[str(ctx.author.id)]['spin'] + (60 * 30)):

            inventories = get_file("inventories")
            items = get_file("items")

            s_tier = []
            a_tier = []
            b_tier = []
            c_tier = []
            d_tier = []

            for key in items.keys():
                if items[key]["tier"] in ["S+", "S", "S-"]:
                    s_tier.append(key)
                elif items[key]["tier"] in ["A+", "A", "A-"]:
                    a_tier.append(key)
                elif items[key]["tier"] in ["B+", "B", "B-"]:
                    b_tier.append(key)
                elif items[key]["tier"] in ["C+", "C", "C-"]:
                    c_tier.append(key)
                else:
                    d_tier.append(key)
                    
            tiers = {"S": s_tier, "A": a_tier, "B": b_tier, "C": c_tier, "D": d_tier}
            reward_tier = choices(["S", "A", "B", "C", "D"], weights=[1, 10, 15, 40, 30], k=1)[0]
            reward_key = choice(tiers[reward_tier])
            reward_float = round(uniform(0, 1), 3)
            tier_points, float_multiplicator = get_points(reward_tier, reward_float)
            reward_points = tier_points * float_multiplicator

            embed = discord.Embed(color=default_color)
            embed.set_author(name="⌛ Item aléatoire")
            embed = set_footer(embed, ctx)
            embed.add_field(name=f"**{items[reward_key]['name']}** ({tier_points} x {float_multiplicator} = {reward_points} PTS)",
                            value=f"*{items[reward_key]['description']}*  •  __{items[reward_key]['from']}__",
                            inline=False)
            embed.add_field(name="Tier", value=f"`{items[reward_key]['tier']}`", inline=True)
            embed.add_field(name="Float", value=f"`{reward_float}`", inline=True)
            embed.add_field(name="ID", value=f"`{reward_key}`", inline=True)
            item_image = discord.File(f"assets/{reward_key}.png", filename=f"{reward_key}.png")
            embed.set_image(url=f"attachment://{reward_key}.png")
            await ctx.send(embed=embed, file=item_image)

            inventories[str(ctx.author.id)]["items"].append({"id": reward_key, "float": reward_float, "points": reward_points})
            cooldowns[str(ctx.author.id)]["spin"] = time()
            update_file("cooldowns", cooldowns)
            update_file("inventories", inventories)

        else:
            await gen_error("cooldown_spin", ctx)


    @commands.command()
    async def daily(self, ctx):
        """Claim the daily reward (24 h cooldown)"""
        cooldowns = get_file("cooldowns")
        id_key = str(ctx.author.id)

        if time() > (cooldowns[id_key]["daily"] + (60 * 60 * 24)):

            inventories = get_file("inventories")
            reward_sum = randint(1, 500)

            embed = discord.Embed(color=default_color)
            embed.set_author(name="📅 Argent quotidien")
            embed.add_field(name="Récompense :", value=f":moneybag: +`{reward_sum}` | Votre bourse : "
                                                   f"`{inventories[id_key]['balance'] + reward_sum}` PO (pièces d'or)")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

            cooldowns[id_key]["daily"] = time()
            inventories[id_key]["balance"] += reward_sum
            update_file("cooldowns", cooldowns)
            update_file("inventories", inventories)

        else:
            await gen_error("cooldown_daily", ctx)


def setup(client):
    client.add_cog(Claims(client))
