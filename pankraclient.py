import discord
import pankrac
from pankrac import Pankrac
from pankracutils import now

WRAPPER = '\n===================='

## Třída, která řeší spojení s discordem a výpisy do konzole na straně serveru
#  Jedná se o potomka discord.Client, takže overridujme události a posíláme je do Pankráce
class PankracClient(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)
        self.nasPankrac = Pankrac()

    ## Když Pankrác nastaruje a připojí se k discordu
    async def on_ready(self):
        print(now())
        print('Startuji Pankráce...')
        print("Username:" + self.user.name)
        print("ID:      " + str(self.user.id))
        print('------')

    ## podle typu odpovědi buď odepíše, nebo reaguje
    async def posli_odpoved(self, odpoved, message):
        if odpoved['type'] == pankrac.TYPE_RESPONSE_MESSAGE:
            print("Pankrác odpovídá: " + odpoved['data'])
            await message.channel.send("<@" + str(message.author.id) + ">, " + odpoved['data'])
        elif odpoved['type'] == pankrac.TYPE_RESPONSE_REACTION:
            print("Pankrác dal reakci: " + odpoved['data'])
            await message.add_reaction(odpoved['data'])
        elif odpoved['type'] == pankrac.TYPE_RESPONSE_CLOSE:
            if (message.author.name == "janzeman3"):
                await message.add_reaction(pankrac.REACTION_CRY)
                await message.channel.send("Kluci, loučím se, pro dnešek musím :wave:")
                await self.close()
                print("Končím...")

    ## Zpracování zprávy do diskusního kanálu
    async def on_message(self, message):
        print(WRAPPER)
        print('Čtu zprávu...')
        print(now() + " - {0} (ID {1}): {2}".format(message.author.name, message.author.id, message.content))

        # pankrác nereaguje na sebe a reaguje jen, když je osloven
        osloveni = ['<@!843012795440168962>', 'Pankráci', 'pankráci', 'Pankraci', 'pankraci']
        if (message.author.id == self.user.id) or not any([True for x in osloveni if x in message.content]):
            return

        print('Pankrác osloven!')

        # pokud Pankrác pozná, že je to pro něj, tak dá očko
        print('Pankrác dává očíčka.')
        await message.add_reaction(pankrac.REACTION_EYES)


        odpoved = self.nasPankrac.zpracuj_zpravu(message)
        await self.posli_odpoved(odpoved, message)
