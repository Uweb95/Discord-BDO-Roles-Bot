import discord
import config as cfg

roles = {}
mainMessageId = 0


class BdoRolesBot(discord.Client):
    async def init_bot(self, channel):
        global mainMessageId, roles

        roles['Kzarka'] = discord.utils.get(channel.guild.roles, name="Kzarka")
        roles['Karanda'] = discord.utils.get(channel.guild.roles, name="Karanda")
        roles['Nouver'] = discord.utils.get(channel.guild.roles, name="Nouver")
        roles['Kutum'] = discord.utils.get(channel.guild.roles, name="Kutum")
        roles['Offin'] = discord.utils.get(channel.guild.roles, name="Offin")
        roles['Garmoth'] = discord.utils.get(channel.guild.roles, name="Garmoth")
        roles['Vell'] = discord.utils.get(channel.guild.roles, name="Vell")
        roles['QuintMuraka'] = discord.utils.get(channel.guild.roles, name="QuintMuraka")
        roles['ImperialTrade'] = discord.utils.get(channel.guild.roles, name="ImperialTrade")
        roles['ImperialCrafting'] = discord.utils.get(channel.guild.roles, name="ImperialCrafting")

        embed = discord.Embed(
            title=cfg.embed['title'],
            colour=discord.Colour(cfg.embed['color']),
            description=cfg.embed['description'])

        for role in roles:
            embed.add_field(name=f"{discord.utils.get(channel.guild.emojis, name=role)}", value=role)

        embed.set_footer(text="Bot by {}#{}".format(client.get_user(cfg.author['id']).name,
                                                    client.get_user(cfg.author['id']).discriminator),
                         icon_url=cfg.author['icon_url'])

        message = await channel.send(embed=embed)
        mainMessageId = message.id

        for role in roles:
            await message.add_reaction(discord.utils.get(channel.guild.emojis, name=role))

    async def on_ready(self):
        print(cfg.general['bot_started_message'])

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith(cfg.general['init_command']):
            await message.delete()

            if message.author.id == cfg.author['id']:
                await self.init_bot(message.channel)
            else:
                await message.channel.send("This command can only be executed by the bot author!")

    async def on_reaction_add(self, reaction, user):
        global mainMessageId, roles

        if user == client.user:
            return

        if mainMessageId == 0:
            print("Main message not found, use " + cfg.general['init_command'] + " to initialize the bot!")
            return

        if reaction.message.id != mainMessageId:
            return

        if str(reaction.emoji.name) in roles:
            if roles[str(reaction.emoji.name)] is not None:
                await user.add_roles(roles[str(reaction.emoji.name)])
            else:
                if cfg.general['create_roles_when_not_exist']:
                    roles[str(reaction.emoji.name)] = await reaction.message.channel.guild.create_role(
                        permissions=discord.Permissions(use_voice_activation=True),
                        name=str(reaction.emoji.name),
                        mentionable=True,
                        colour=discord.Colour(cfg.general['created_role_color']),
                        reason="Created to allow users getting this role.")
                    await user.add_roles(roles[str(reaction.emoji.name)])

                    # Only necessary if the BDO Timers Bot is on the Server
                    if cfg.general['bdo_timers_bot_available']:
                        await reaction.message.channel.send(
                            content="!settings " + str(reaction.emoji.name) + " " + roles[
                                str(reaction.emoji.name)].mention,
                            delete_after=5,
                            allowed_mentions=discord.AllowedMentions(roles=True))

    async def on_reaction_remove(self, reaction, user):
        global mainMessageId, roles

        if mainMessageId == 0:
            print("Main message not found, use " + cfg.general['init_command'] + " to initialize the bot!")
            return

        if reaction.message.id != mainMessageId:
            return

        if str(reaction.emoji.name) in roles and roles[str(reaction.emoji.name)] is not None:
            await user.remove_roles(roles[str(reaction.emoji.name)])


if __name__ == '__main__':
    client = BdoRolesBot()
    client.run(cfg.general['discord_token'])
