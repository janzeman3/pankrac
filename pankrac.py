import json

from pankracutils import obsahuje

TYPE_RUTINNE_TEXT = 1
TYPE_RUTINNE_METHOD = 2

TYPE_RESPONSE_NOTHING = 0
TYPE_RESPONSE_MESSAGE = 1
TYPE_RESPONSE_ANSWER = 2
TYPE_RESPONSE_REACTION = 3
TYPE_RESPONSE_KVIZ = 4

TYPE_DICORD_RESPONSE_NULL = 0
TYPE_DICORD_RESPONSE_MESSAGE = 1
TYPE_DICORD_RESPONSE_REACTION = 2
TYPE_DICORD_RESPONSE_KVIZ = 3

LINK_WEB_STEZKA = "https://stezka.skaut.cz/prohlizej-a-inspiruj-se/"
LINK_WEB_NOVACEK = "https://stezka.skaut.cz/novacek/"
LINK_NOTION_VYZVY = "https://www.notion.so/janzeman3/0995fe1d94a9403e99e667fc2ad15e30?v=3d42ab631c064ce0a16dda28bd06439d"
LINK_NOTION_SPLNENE = "https://www.notion.so/janzeman3/3f6b1919e9bd49eaa46e2e21108ba0ce?v=62bb60897c594cf2ab1d8c30cab459d7"
LINK_SOKOLI_AKCE = "https://ibis.skauting.cz/calendar/skauti/"
LINK_SOKOLI_WEB = "https://ibis.skauting.cz/oddily/skauti-sokoli/"

REACTION_WAVE = "👋"
REACTION_THUMBS = "👍"
REACTION_ONE = "1️⃣"
REACTION_TWO = "2️⃣"
REACTION_THREE = "3️⃣"
REACTION_A = "🇦"
REACTION_B = "🇧"
REACTION_C = "🇨"

## Odpovídací logika chatbota
class Pankrac:
    ## hlavní rozhodovací struktura
    moznosti = {}

    ## data kvízů
    running_kviz = False
    data_kviz = {}

    def __init__(self):
        uzel_spln = {'keys': ["spln"],
                         'subnodes': [],
                         'action': {'type': TYPE_RUTINNE_TEXT, 'data': "Asi by pomohl seznam splněných výzev a bodů stezky " + LINK_NOTION_SPLNENE}
                         }

        uzel_stezka_na_webu = {'keys': ["stezk"],
                         'subnodes': [uzel_spln],
                         'action': {'type': TYPE_RUTINNE_TEXT, 'data': "Posílám odkaz na stezku " + LINK_WEB_STEZKA}
                         }

        uzel_novacek_na_webu = {'keys': ["nováč"],
                         'subnodes': [uzel_spln],
                         'action': {'type': TYPE_RUTINNE_TEXT, 'data': "Snad Ti pomůže nováček " + LINK_WEB_NOVACEK}
                         }

        uzel_vyzvy = {'keys': ["výzv"],
                         'subnodes': [uzel_spln],
                         'action': {'type': TYPE_RUTINNE_TEXT, 'data': "Tady jsou výzvy " + LINK_NOTION_VYZVY}
                         }

        uzel_generuj_heslo = {'keys': ["heslo"],
                         'subnodes': [],
                         'action': {'type': TYPE_RUTINNE_METHOD, 'data':  self.generuj_heslo}
                         }

        uzel_akce = {'keys': ["akce"],
                         'subnodes': [],
                         'action': {'type': TYPE_RUTINNE_TEXT, 'data': ":calendar: Nejbližší akce Sokolů najdeš tady: " + LINK_SOKOLI_AKCE}
                         }

        uzel_sokoli_web = {'keys': ["s sebou"],
                         'subnodes': [],
                         'action': {'type': TYPE_RUTINNE_TEXT, 'data': "Třeba Ti pomůže stránka našich skautů: " + LINK_SOKOLI_WEB}
                         }

        uzel_help = {'keys': ["nápověd", "pomoc", "help", "příkazy", "/"],
                         'subnodes': [],
                         'action': {'type': TYPE_RUTINNE_METHOD, 'data':  self.napoveda}
                         }

        uzel_dik = {'keys': ["dík", "dik", "dekuj", "děkuj"],
                         'subnodes': [],
                         'action': {'type': TYPE_RUTINNE_METHOD, 'data':  self.reaction_thumbs_up}
                         }

        uzel_ahoj = {'keys': ["ahoj", "nazdar", "dobrou noc", "dobry den"],
                         'subnodes': [],
                         'action': {'type': TYPE_RUTINNE_METHOD, 'data':  self.reaction_wave}
                         }

        uzel_kviz_konec = {'keys': ["konec", "off", "vypni"],
                         'subnodes': [],
                         'action': {'type': TYPE_RUTINNE_METHOD, 'data':  self.kviz_konec}
                         }
        uzel_kviz = {'keys': ["kviz", "kvíz"],
                         'subnodes': [uzel_kviz_konec],
                         'action': {'type': TYPE_RUTINNE_METHOD, 'data':  self.kviz}
                         }

        self.moznosti = {'keys': ["Pankráci"],
                         'subnodes': [uzel_dik, uzel_ahoj, uzel_kviz, uzel_sokoli_web, uzel_vyzvy, uzel_stezka_na_webu,
                                      uzel_novacek_na_webu, uzel_generuj_heslo, uzel_akce, uzel_help],
                         'action': {'type': TYPE_RUTINNE_METHOD, 'data':  self.nevim}
                         }

    ## obdrží akci a vygeneruje její výsledek na základě dané otázky
    def vysledek_akce(self, akce, otazka):
        odpoved = {}
        odpoved['type'] = TYPE_RESPONSE_MESSAGE
        odpoved['data'] = ""

        if akce['type'] == TYPE_RUTINNE_METHOD:
            odpoved['data'], odpoved['type'] = akce['data'](otazka)
        elif akce['type'] == TYPE_RUTINNE_TEXT:
            odpoved['data'] = akce['data']
        else:
            odpoved['data'] = "Chyba dat kontaktuj programátory..."

        return odpoved

    ## zpracuje odezvu podle obsahu proměnné self.moznosti
    def zpracuj_zpravu(self, message):
        otazka = message.content

        # ridici proměnná, která říká, jeslti jsme na konci
        nejde_jit_dal = False
        # poslední uzel, kde jsme skončili
        uzel = self.moznosti

        while not nejde_jit_dal:
            # do noveho uzlu dam stavajici
            novy_uzel = uzel

            #projdu všechny pod-uzly
            for poduzel in uzel['subnodes']:
                if obsahuje(poduzel['keys'], otazka):
                    # pokud najdu pokračování, dám kandidáta na nový uzel
                    # !!! v případě shody to vybere poslední shodu
                    novy_uzel = poduzel

            if novy_uzel == uzel:
                # pokud jsem se neposunul, nejde jít dál
                nejde_jit_dal = True
            else:
                # jinak upadutuju uzel a frčím znovu
                uzel = novy_uzel

        # nakonec provedu akci z finálního uzlu
        return self.vysledek_akce(uzel['action'], otazka)

    def zpracuj_reakci(self, reakce):
        if self.running_kviz:
            self.kviz_odpoved(reakce)
        return {'type': TYPE_RESPONSE_NOTHING}

    def discord_odezva(self, discord_response):
        if discord_response["type"] == TYPE_RESPONSE_KVIZ:
            pass


    def generuj_hierarchii(self, uzel, odsazeni):
        hierarchie = "".ljust(odsazeni*4, " ") + "- "
        for klicove_slovo in uzel['keys']:
            hierarchie += klicove_slovo + ' '
        hierarchie += '\n'

        for poduzel in uzel['subnodes']:
            hierarchie += self.generuj_hierarchii(poduzel, odsazeni + 1)

        return hierarchie

    def reaction_thumbs_up(self, message_text):
        return REACTION_THUMBS, TYPE_RESPONSE_REACTION

    def reaction_wave(self, message_text):
        return REACTION_WAVE, TYPE_RESPONSE_REACTION

    def nevim(self, message_text):
        return 'slyším Tě, ale ale nevím, co po mě chceš. Zkus napsat "Pankráci pomoc!"', TYPE_RESPONSE_MESSAGE

    def napoveda(self, message_text):
        napoveda_text = "Nápověda: \n" \
                    "1. Pankrác reaguje, když se objeví ve větě slovo !Pankráci!\n" \
                    "2. Pankrác hledá klíčová !slova! a podle nich dává odpovědi.\n" \
                    "3. Hledá je postupně v hierarchii.\n\n" \

        hierarchie = "Hierarchie klíčových slov\n"
        hierarchie += self.generuj_hierarchii(self.moznosti, 1)

        return napoveda_text + hierarchie, TYPE_RESPONSE_MESSAGE

    def generuj_heslo(self, message_text):
        from dice_heslo import get_password
        heslo = get_password()
        odpoved = "vygeneroval jsem Ti heslo :muscle: \n" + heslo + "\nmezery do hesla nezadávej :wink:"
        return odpoved, TYPE_RESPONSE_MESSAGE

    def kviz(self, message_text):
        if not self.running_kviz:
            self.running_kviz = True
            otazka1 = ":question: Jak se jmenuje nejlepší skaut na světě?\n" \
                      ":one: Honza\n" \
                      ":two: Hejkal\n" \
                      ":three: Blanka"
            otazka2 = ":question: Kolik nohou má pavouk\n" \
                      ":one: 6\n" \
                      ":two: 8\n" \
                      ":three: podle toho kolik mu jich necháš"
            self.data_kviz["otazky"] = {otazka1: REACTION_THREE, otazka2: REACTION_TWO}
            return self.data_kviz["otazky"].keys(), TYPE_RESPONSE_KVIZ
        else:
            return "Kvíz už běží, nejdřív ukonči předchozí", TYPE_RESPONSE_MESSAGE


    def kviz_konec(self, message_text):
        if not self.running_kviz:
            return "Není, co končit, žádný kvíz neběžel.", TYPE_RESPONSE_MESSAGE

        vyhodnoceni = "Vyhrál ten nejlepší"

        self.running_kviz = False
        self.data_kviz ={}
        return "Kvíz ukončen!\n" + vyhodnoceni, TYPE_RESPONSE_MESSAGE

    async def kviz_odpoved(self, reaction):
        otazka = reaction.message.content
        if otazka in self.data_kviz["otazky"].keys():
            if self.data_kviz["otazky"][otazka] == reaction.emoji:
                print("Někdo odpověděl správně!")
            else:
                print("Někdo odpověděl špatně.")
            print(reaction.emoji)

