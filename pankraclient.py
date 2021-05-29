import discord
import pankrac
from pankrac import Pankrac
from pankracutils import now
from konstanty import ResponseType

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
    async def posli_odezvu(self, odezva, message):
        if odezva['type'] == ResponseType.MESSAGE:
            print("Pankrác odpovídá: " + odezva['data'])
            await message.channel.send("<@" + str(message.author.id) + ">, " + odezva['data'])
        elif odezva['type'] == ResponseType.REACTION:
            print("Pankrác dal reakci: " + odezva['data'])
            await message.add_reaction(odezva['data'])
        elif odezva['type'] == ResponseType.CLOSE:
            if (message.author.name == "janzeman3"):
                await message.add_reaction(pankrac.REACTION_CRY)
                await message.channel.send("Kluci, loučím se, pro dnešek musím :wave:")
                await self.close()
                print("Končím...")

    ## Zpracování zpráv z diskusního kanálu
    async def on_message(self, message):
        # výpist příchozí zprávy
        print(WRAPPER)
        print('Čtu zprávu...')
        print(now() + " - {0} (ID {1}): {2}".format(message.author.name, message.author.id, message.content))

        # test, jestli je Pankác osloven (skončíme, pokud osleven není)
        osloveni = ['<@!843012795440168962>', 'Pankráci', 'pankráci', 'Pankraci', 'pankraci']
        if (message.author.id == self.user.id) or not any([True for x in osloveni if x in message.content]):
            return

        #Pankrác byl osloven
        print('Pankrác osloven!')
        # pokud Pankrác pozná, že je to pro něj, tak dá očko
        print('Pankrác dává očíčka.')
        await message.add_reaction(pankrac.REACTION_EYES)

        # zavolá se zpracování zpráv a odešle se odezva
        odpoved = self.nasPankrac.zpracuj_zpravu(message)
        await self.posli_odezvu(odpoved, message)
