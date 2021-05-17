import json

from pankracutils import obsahuje

TYPE_TEXT = 1
TYPE_METHOD = 2

LINK_WEB_STEZKA = "https://stezka.skaut.cz/prohlizej-a-inspiruj-se/"
LINK_WEB_NOVACEK = "https://stezka.skaut.cz/novacek/"
LINK_NOTION_VYZVY = "https://www.notion.so/janzeman3/0995fe1d94a9403e99e667fc2ad15e30?v=3d42ab631c064ce0a16dda28bd06439d"
LINK_NOTION_SPLNENE = "https://www.notion.so/janzeman3/3f6b1919e9bd49eaa46e2e21108ba0ce?v=62bb60897c594cf2ab1d8c30cab459d7"
LINK_SOKOLI_AKCE = "https://ibis.skauting.cz/calendar/skauti/"
LINK_SOKOLI_WEB = "https://ibis.skauting.cz/oddily/skauti-sokoli/"

## Odpovídací logika chatbota
class Pankrac:
    moznosti = {}

    def __init__(self):
        uzel_spln = {'keys': ["spln"],
                         'subnodes': [],
                         'action': {'type': TYPE_TEXT, 'data': "Asi by pomohl seznam splněných výzev a bodů stezky " + LINK_NOTION_SPLNENE}
                         }

        uzel_stezka_na_webu = {'keys': ["stezk"],
                         'subnodes': [uzel_spln],
                         'action': {'type': TYPE_TEXT, 'data':  "Posílám odkaz na stezku " + LINK_WEB_STEZKA}
                         }

        uzel_novacek_na_webu = {'keys': ["nováč"],
                         'subnodes': [uzel_spln],
                         'action': {'type': TYPE_TEXT, 'data':  "Snad Ti pomůže nováček " + LINK_WEB_NOVACEK}
                         }

        uzel_vyzvy = {'keys': ["výzv"],
                         'subnodes': [uzel_spln],
                         'action': {'type': TYPE_TEXT, 'data':  "Tady jsou výzvy " + LINK_NOTION_VYZVY}
                         }

        uzel_generuj_heslo = {'keys': ["heslo"],
                         'subnodes': [],
                         'action': {'type': TYPE_METHOD, 'data':  self.generuj_heslo}
                         }

        uzel_akce = {'keys': ["akce"],
                         'subnodes': [],
                         'action': {'type': TYPE_TEXT, 'data':  ":calendar: Nejbližší akce Sokolů najdeš tady: " + LINK_SOKOLI_AKCE}
                         }

        uzel_sokoli_web = {'keys': ["s sebou"],
                         'subnodes': [],
                         'action': {'type': TYPE_TEXT, 'data':  "Třeba Ti pomůže stránka našich skautů: " + LINK_SOKOLI_WEB}
                         }


        uzel_help = {'keys': ["nápověd", "pomoc", "help", "příkazy", "/"],
                         'subnodes': [],
                         'action': {'type': TYPE_METHOD, 'data':  self.napoveda}
                         }

        uzel_dik = {'keys': ["dík", "dik", "dekuj", "děkuj"],
                         'subnodes': [],
                         'action': {'type': TYPE_METHOD, 'data':  self.nic}
                         }

        self.moznosti = {'keys': ["Pankráci"],
                         'subnodes': [uzel_dik, uzel_sokoli_web, uzel_vyzvy, uzel_stezka_na_webu, uzel_novacek_na_webu, uzel_generuj_heslo, uzel_akce, uzel_help],
                         'action': {'type': TYPE_METHOD, 'data':  self.nevim}
                         }

    ## obdrží akci a vygeneruje její výsledek na základě dané otázky
    def vysledek_akce(self, akce, otazka):
        if akce['type'] == TYPE_METHOD:
            odpoved = akce['data'](otazka)
        elif akce['type'] == TYPE_TEXT:
            odpoved = akce['data']
        else:
            odpoved = "Chyba dat kontaktuj programátory..."
        return odpoved

    ## zpracuje odezvu podle obsahu proměnné self.moznosti
    def zpracuj_odezvu(self, message):
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

    def generuj_hierarchii(self, uzel, odsazeni):
        hierarchie = "".ljust(odsazeni*4, " ") + "- "
        for klicove_slovo in uzel['keys']:
            hierarchie += klicove_slovo + ' '
        hierarchie += '\n'

        for poduzel in uzel['subnodes']:
            hierarchie += self.generuj_hierarchii(poduzel, odsazeni + 1)

        return hierarchie

    def nic(self, message_text):
        return ""

    def nevim(self, message_text):
        return "Tady Pankrác, slyším Tě, ale ale nevím, co po mě chceš. Zkus napsat -Pankráci pomoc!-"

    def napoveda(self, message_text):
        napoveda_text = "Nápověda: \n" \
                    "1. Pankrác reaguje, když se objeví ve větě slovo !Pankráci!\n" \
                    "2. Pankrác hledá klíčová !slova! a podle nich dává odpovědi.\n" \
                    "3. Hledá je postupně v hierarchii.\n\n" \

        hierarchie = "Hierarchie klíčových slov\n"
        hierarchie += self.generuj_hierarchii(self.moznosti, 1)

        return napoveda_text + hierarchie

    def generuj_heslo(self, message_text):
                from dice_heslo import get_password
                heslo = get_password()
                odpoved = "vygeneroval jsem Ti heslo :muscle: \n" + heslo + "\nmezery do hesla nezadávej :wink:"
                return odpoved
