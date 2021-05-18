import discord
import pankrac
from pankrac import Pankrac
from pankracutils import now

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
        discord_response = {"type": pankrac.TYPE_DICORD_RESPONSE_NULL,
                            "data": ""}
        if odpoved['type'] == pankrac.TYPE_RESPONSE_MESSAGE:
            print("Pankrác odpoví: " + odpoved['data'] + "\n------\n")
            discord_response["data"] = await message.channel.send("<@" + str(message.author.id) + ">, " + odpoved['data'])
            discord_response["type"] = pankrac.TYPE_DICORD_RESPONSE_MESSAGE
        elif odpoved['type'] == pankrac.TYPE_RESPONSE_REACTION:
            print("Pankrác dal reakci: " + odpoved['data'] + "\n------\n")
            discord_response["data"] = await message.add_reaction(odpoved['data'])
            discord_response["type"] = pankrac.TYPE_DICORD_RESPONSE_REACTION
        elif odpoved['type'] == pankrac.TYPE_RESPONSE_KVIZ:
            discord_response["type"] = pankrac.TYPE_DICORD_RESPONSE_KVIZ
            discord_response["data"] = []
            for otazka_text in odpoved['data']:
                print("Pankrác dal reakci: " + otazka_text)
                otazka_message = await message.channel.send(otazka_text)
                await otazka_message.add_reaction(pankrac.REACTION_A)
                await otazka_message.add_reaction(pankrac.REACTION_B)
                await otazka_message.add_reaction(pankrac.REACTION_C)
                discord_response["data"].append(otazka_message)
            print("\n------\n")

        return discord_response

    ## Zpracování zprávy do diskusního kanálu
    async def on_message(self, message):
        print("Zpracovávám zprávu:")
        print(message.content)
        # pankrác nereaguje na sebe a reaguje jen, když je osloven
        osloveni = ['<@!843012795440168962>', 'Pankráci', 'pankráci', 'Pankraci', 'pankraci']
        if (message.author.id == self.user.id) or not any([True for x in osloveni if x in message.content]):
            print("Zahazuji")
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

        odpoved = self.nasPankrac.zpracuj_zpravu(message)
        discord_dopoved = await self.posli_odpoved(odpoved, message)
        self.nasPankrac.discord_odezva(discord_dopoved)


    ## Zpracování reakcí
    async def on_reaction_add(self, reaction, user):
        # pouze monitoring
        print(now() + '\nNová reakce')
        print("Zpráva:   " + reaction.message.content)
        print("Reakce:   " + str(reaction))
        print("Uživatel: " + user.name)
        odpoved = self.nasPankrac.zpracuj_reakci(reaction)
        await self.posli_odpoved(odpoved, reaction.message)
