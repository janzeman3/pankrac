import json

from pankracutils import obsahuje

TYPE_TEXT = 1
TYPE_METHOD = 2

LINK_WEB_STEZKA = "https://stezka.skaut.cz/prohlizej-a-inspiruj-se/"
LINK_NOTION_VYZVY = "https://www.notion.so/janzeman3/0995fe1d94a9403e99e667fc2ad15e30?v=3d42ab631c064ce0a16dda28bd06439d"
LINK_NOTION_SPLNENE = "https://www.notion.so/janzeman3/3f6b1919e9bd49eaa46e2e21108ba0ce?v=62bb60897c594cf2ab1d8c30cab459d7"

## Odpovídací logika chatbota (verze 1.0 - pěkný fuj)
class Pankrac:
    moznosti = {}

    def __init__(self):
        uzel_spln = {'keys': ["spln"],
                         'subnodes': [],
                         'action': {'type': TYPE_METHOD, 'data': self.splnena_stezka}
                         }

        uzel_stezka_na_webu = {'keys': ["stezk"],
                         'subnodes': [uzel_spln],
                         'action': {'type': TYPE_METHOD, 'data':  self.stezka_na_webu}
                         }

        uzel_novacek_na_webu = {'keys': ["nováč"],
                         'subnodes': [uzel_spln],
                         'action': {'type': TYPE_METHOD, 'data':  self.web_novacek}
                         }

        uzel_vyzvy = {'keys': ["výzv"],
                         'subnodes': [uzel_spln],
                         'action': {'type': TYPE_METHOD, 'data':  self.web_vyzvy}
                         }

        uzel_generuj_heslo = {'keys': ["heslo"],
                         'subnodes': [],
                         'action': {'type': TYPE_METHOD, 'data':  self.generuj_heslo}
                         }

        uzel_akce = {'keys': ["akce"],
                         'subnodes': [],
                         'action': {'type': TYPE_METHOD, 'data':  self.web_akce}
                         }

        uzel_sokoli_web = {'keys': ["s sebou"],
                         'subnodes': [],
                         'action': {'type': TYPE_METHOD, 'data':  self.web_sokoli}
                         }


        uzel_help = {'keys': ["nápověd", "pomoc", "help", "příkazy", "/"],
                         'subnodes': [],
                         'action': {'type': TYPE_METHOD, 'data':  self.napoveda}
                         }

        self.moznosti = {'keys': ["Pankráci"],
                         'subnodes': [uzel_sokoli_web, uzel_vyzvy, uzel_stezka_na_webu, uzel_novacek_na_webu, uzel_generuj_heslo, uzel_akce, uzel_help],
                         'action': {'type': TYPE_METHOD, 'data':  self.nevim}
                         }

    def nevim(self, message_text):
        return "Tady Pankrác, slyším Tě, ale ale nevím, co po mě chceš. Zkus napsat -Pankráci pomoc!-"

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
                odpoved = "Borče, vygeneroval jsem Ti heslo :muscle: \n" + heslo + "\nmezery do hesla nezadávej :wink:"
                return odpoved

        #webové aktivity
    def web_akce(self, message_text):
                return ":calendar: Nejbližší akce Sokolů najdeš tady: https://ibis.skauting.cz/calendar/skauti/"

    def web_sokoli(self, message_text):
                return "Třeba Ti pomůže stránka našich skautů: https://ibis.skauting.cz/oddily/skauti-sokoli/"

    def web_novacek(self, message_text):
            return "Snad Ti pomůže nováček: https://stezka.skaut.cz/novacek/"

    def web_vyzvy(self, message_text):
        return "Tady jsou výzvy: " + LINK_NOTION_VYZVY

    def splnena_stezka(self, message_text):
        return "Asi by pomohl seznam splněných výzev a bodů stezky " + LINK_NOTION_SPLNENE

    def stezka_na_webu(self, message_text):
        return "Nepomůže ti stezka? " + LINK_WEB_STEZKA
