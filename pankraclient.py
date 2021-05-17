import discord
from pankrac import Pankrac
from pankracutils import now

## Třída, která řeší spojení s discordem a výpisy do konzole na straně serveru
#  Jedná se o potomka discord.Client, takže overridujme události a posíláme je do Pankráce
class PankracClient(discord.Client):
    ## Když Pankrác nastaruje a připojí se k discordu
    async def on_ready(self):
        print(now())
        print('Startuji Pankráce...')
        print("Username:" + self.user.name)
        print("ID:      " + str(self.user.id))
        print('------')

    ## Zpracování zprávy
    async def on_message(self, message):
        # pankrác nereaguje na sebe a reaguje jen, když je osloven
        osloveni = ['<@!843012795440168962>', 'Pankráci', 'pankráci', 'Pankraci', 'pankraci']
        if (message.author.id == self.user.id) or not any([True for x in osloveni if x in message.content]):
            return

        # pokud Pankrác pozná, že je to pro něj, tak dá očko
        await message.add_reaction("👀")

        # vypnutí Pankráce, když mu jeho autor napíše, že má jít spát
        if (message.author.name == "janzeman3") and message.content == "Pankráci, spát!":
            await message.add_reaction("😭")
            await message.channel.send("Kluci, loučím se, pro dnešek musím :wave:")
            await self.close()
            print("Končím...")
            return

        print(now() + '\nPankrác osloven')
        print("{0} (ID {1}): {2}".format(message.author.name, message.author.id, message.content))

        nasPankrac = Pankrac()
        nasPankrac.zpracuj_zpravu(message)

        if odpoved:
            print("Pankrác odpoví: " + odpoved + "\n------\n")
            await message.channel.send("<@" + str(message.author.id) + ">, " + odpoved)


    ## Zatím cvičný monitoring reakcí
    async def on_reaction_add(self, reaction, user):
        print(reaction)
        print(user)