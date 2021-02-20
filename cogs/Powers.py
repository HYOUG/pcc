import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *
from random import choice, uniform, randint


class Powers(commands.Cog):
    """
    Commands : 
    - use
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def use(self, ctx, power: str):
        """Use one of yours powers"""
        author_key = str(ctx.author.id)
        inventories = get_file("inventories")
        if power in inventories[author_key]["powers"]:
            powers = get_file("powers")
            embed = discord.Embed(color=default_color)
            embed.set_author(name="⚡️ Power-up")
            embed = set_footer(embed, ctx)

            target = choice(list(inventories.keys()))

            if power == "steal_random_money":
                if not inventories[target]["shield_active"]:
                    random_money = randint(1, inventories[target]["balance"])
                    inventories[target]["balance"] -= random_money
                    inventories[author_key]["balance"] += random_money
                    embed.add_field(name=powers[power]["name"],
                                    value=f"Vous avez utilisé **{powers[power]['name']}** sur {self.bot.get_user(int(target)).mention} !\n"
                                            f"Vous lui avez volé : `{random_money}` PO (pièces d'or)")
                else:
                    pass

            elif power == "reroll_float":
                items = get_file("items")
                target_item = inventories[author_key]["items"].pop(
                    choice(range(len(inventories[author_key]["items"]))))
                old_float = target_item["float"]
                target_item["float"] = round(uniform(0, 1), 3)
                tier_points, float_multiplicator = get_points(items[target_item["id"]]["tier"][0], float(target_item["float"]))
                target_item["points"] = tier_points * float_multiplicator
                inventories[str(ctx.author.id)]["items"].append(target_item)
                embed.add_field(name=powers[power]["name"], value=f"Vous avez utilisé **{powers[power]['name']}** sur **{target_item['name']}** !\nAncien float : `{old_float}`\nNouveau float : `{target_item['float']}`")


            elif power == "shield":
                if not inventories[author_key]["shield_active"]:
                    inventories[author_key]["shield_active"] = True
                    embed.add_field(name=powers[power]["name"],
                                    value=f"Vous avez utilisé **{powers[power]['name']}** !\n"
                                            f"Vous serez protégé du prochain power-up contre vous")
                else:
                    embed.add_field(name=powers[power]["name"],
                                    value=f"Vous êtes déjà protégé par un bouclier")


            elif power == "-0.050":
                if inventories[author_key]["items"] != []:
                    items = get_file("items")
                    target_item = inventories[author_key]["items"].pop(choice(range(len(inventories[author_key]["items"]))))
                    old_float = target_item["float"]
                    target_item["float"] = round(target_item["float"] - float(power[1:]), 3)
                    if target_item["float"] < 0.000:
                        target_item["float"] = 0.000
                    tier_points, float_multiplicator = get_points(items[target_item["id"]]["tier"][0], target_item["float"])
                    target_item["points"] = tier_points * float_multiplicator
                    inventories[author_key]["items"].append(target_item)
                    embed.add_field(name=powers[power]["name"],
                                    value=f"Vous avez utilisé le power-up **{powers[power]['name']}** !\n"
                                            f"Vous avez réduit le float de **{items[target_item['id']]['name']}** :\n"
                                            f"Ancien float : `{old_float}`\nNouveau float : `{target_item['float']}`")
                else:
                    pass


            elif power == "-10%":
                items = get_file("items")
                target_item = inventories[author_key]["items"].pop(
                    choice(range(len(inventories[author_key]["items"]))))
                old_float = target_item["float"]
                percent = target_item["float"] / 100
                target_item["float"] = round(target_item["float"] - percent * int(power[1:2]), 3)
                if target_item["float"] < 0.000:
                    target_item["float"] = 0.000
                tier_points, float_multiplicator = get_points(items[target_item["id"]]["tier"][0],
                                                                target_item["float"])
                target_item["points"] = tier_points * float_multiplicator
                inventories[author_key]["items"].append(target_item)
                embed.add_field(name=powers[power]["name"],
                                value=f"Vous avez utilisé le power-up **{powers[power]['name']}** !\n"
                                        f"Vous avez réduit le float de **{items[target_item['id']]['name']}** :\n"
                                        f"Ancien float : `{old_float}`\nNouveau float : `{target_item['float']}`")

            inventories[author_key]["powers"].remove(power)
            update_file("inventories", inventories)
            await ctx.send(embed=embed)

        else:
            await gen_error("missing_power", ctx)


def setup(client):
    client.add_cog(Powers(client))