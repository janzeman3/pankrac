from pankractoken import TOKEN
import discord
import datetime
from pankrac import Pankrac


class MyClient(discord.Client):
    def now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def on_ready(self):
        print(self.now())
        print('Startuji Pankráce...')
        print("Username:" + self.user.name)
        print("ID:      " + str(self.user.id))
        print('------')

    async def on_message(self, message):
        # pankrác nereaguje na sebe a reaguje jen, když je osloven
        osloveni = ['Pankráci', 'pankráci', 'Pankraci', 'pankraci']
        if (message.author.id == self.user.id) or not any([True for x in osloveni if x in message.content]):
            return

        # pokud Pankrác pozná, že je to pro něj, tak dá očko
        await message.add_reaction("👀")

        # vypnutí Pankráce, kdyžm u jeho autor napíše, že má jít spát
        if (message.author.name == "janzeman3") and message.content == "Pankráci, spát!":
            await message.add_reaction("😭")
            await message.channel.send("Kluci, loučím se, pro dnešek musím :wave:")
            await self.close()
            print("Končím...")
            return

        print(self.now() + '\nPankrác osloven')
        print("{0} (ID {1}): {2}".format(message.author.name, message.author.id, message.content))

        nasPankrac = Pankrac()
        odpoved = nasPankrac.zpracuj_odezvu(message)
        print("Pankrác odpoví: " + odpoved + "\n------\n")

        await message.channel.send("<@" + str(message.author.id) + ">, " + odpoved)

    async def on_reaction_add(self, reaction, user):
        print(reaction)
        print(user)


client = MyClient()
client.run(TOKEN)
print("konec")

