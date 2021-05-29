from pankracutils import obsahuje
from konstanty import TYPE_RUTINNE_CLOSE, TYPE_RUTINNE_METHOD, TYPE_RUTINNE_TEXT, TYPE_RUTINNE_TEXT_BY_USER
from konstanty import ResponseType

LINK_WEB_STEZKA = "https://stezka.skaut.cz/prohlizej-a-inspiruj-se/"
LINK_WEB_NOVACEK = "https://stezka.skaut.cz/novacek/"
LINK_NOTION_VYZVY = "https://www.notion.so/janzeman3/0995fe1d94a9403e99e667fc2ad15e30?v=3d42ab631c064ce0a16dda28bd06439d"
LINK_SOKOLI_AKCE = "https://ibis.skauting.cz/calendar/skauti/"
LINK_SOKOLI_WEB = "https://ibis.skauting.cz/oddily/skauti-sokoli/"

REACTION_WAVE = "👋"
REACTION_THUMB_UP = "👍"
REACTION_CRY = "😭"
REACTION_EYES = "👀"

## Odpovídací logika chatbota
class Pankrac:
    moznosti = {}

    def __init__(self):
        import nbsplnene
        uzel_spln = nbsplnene.get_node_splnene()

        uzel_stezka_na_webu = {'keys': ["stezk"],
                         'subnodes': [],
                         'action': {'type': TYPE_RUTINNE_TEXT, 'data': "Posílám odkaz na stezku " + LINK_WEB_STEZKA}
                         }

        uzel_novacek_na_webu = {'keys': ["nováč"],
                         'subnodes': [],
                         'action': {'type': TYPE_RUTINNE_TEXT, 'data': "Snad Ti pomůže nováček " + LINK_WEB_NOVACEK}
                         }

        uzel_vyzvy = {'keys': ["výzv"],
                         'subnodes': [],
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

        uzel_close = {'keys': ["spát!"],
                         'subnodes': [],
                         'action': {'type': TYPE_RUTINNE_CLOSE, 'data': ""}
                         }

        self.moznosti = {'keys': ["Pankráci"],
                         'subnodes': [uzel_close, uzel_dik, uzel_ahoj, uzel_sokoli_web, uzel_vyzvy, uzel_stezka_na_webu,
                                      uzel_novacek_na_webu, uzel_generuj_heslo, uzel_akce, uzel_help, uzel_spln],
                         'action': {'type': TYPE_RUTINNE_METHOD, 'data':  self.nevim}
                         }

    ## TODO
    def reakce_dle_tabulky(self, uzivatel, tabulka_odpovedi):
        odpoved = ""

        klice = tabulka_odpovedi.keys()

        from konstanty import PREFIX, SUFFIX, NOT_FOUND

        if PREFIX in klice:
            odpoved += tabulka_odpovedi[PREFIX]

        if uzivatel in klice:
            odpoved += tabulka_odpovedi[uzivatel]
        else:
            odpoved += tabulka_odpovedi[NOT_FOUND]

        if SUFFIX in klice:
            odpoved += tabulka_odpovedi[SUFFIX]

        return odpoved

    ## obdrží akci a vygeneruje její výsledek na základě dané otázky
    def vysledek_akce(self, akce, message):
        otazka = message.content
        odpoved = {}
        odpoved['type'] = ResponseType.MESSAGE
        odpoved['data'] = ""

        if akce['type'] == TYPE_RUTINNE_METHOD:
            odpoved['data'], odpoved['type'] = akce['data'](otazka)

        elif akce['type'] == TYPE_RUTINNE_TEXT:
            odpoved['data'] = akce['data']

        elif akce['type'] == TYPE_RUTINNE_TEXT_BY_USER:
            odpoved['data'] = self.reakce_dle_tabulky(message.author.name, akce['data'])

        elif akce['type'] == TYPE_RUTINNE_CLOSE:
            odpoved['type'] = ResponseType.CLOSE

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
        return self.vysledek_akce(uzel['action'], message)

    def zpracuj_reakci(self, reakce):
        return {'type': ResponseType.NOTHING}

    def generuj_hierarchii(self, uzel, odsazeni):
        hierarchie = "".ljust(odsazeni*4, " ") + "- "
        for klicove_slovo in uzel['keys']:
            hierarchie += klicove_slovo + ' '
        hierarchie += '\n'

        for poduzel in uzel['subnodes']:
            hierarchie += self.generuj_hierarchii(poduzel, odsazeni + 1)

        return hierarchie

    def reaction_thumbs_up(self, message_text):
        return REACTION_THUMB_UP, ResponseType.REACTION

    def reaction_wave(self, message_text):
        return REACTION_WAVE, ResponseType.REACTION

    def reaction_cry(self, message_text):
        return REACTION_CRY, ResponseType.REACTION

    def nevim(self, message_text):
        return 'slyším Tě, ale ale nevím, co po mě chceš. Zkus napsat "Pankráci pomoc!"', ResponseType.MESSAGE

    def napoveda(self, message_text):
        napoveda_text = "Nápověda: \n" \
                    "1. Pankrác reaguje, když se objeví ve větě slovo !Pankráci!\n" \
                    "2. Pankrác hledá klíčová !slova! a podle nich dává odpovědi.\n" \
                    "3. Hledá je postupně v hierarchii.\n\n" \

        hierarchie = "Hierarchie klíčových slov\n"
        hierarchie += self.generuj_hierarchii(self.moznosti, 1)

        return napoveda_text + hierarchie, ResponseType.MESSAGE

    def generuj_heslo(self, message_text):
        from dice_heslo import get_password
        heslo = get_password()
        odpoved = "vygeneroval jsem Ti heslo :muscle: \n" + heslo + "\nmezery do hesla nezadávej :wink:"
        return odpoved, ResponseType.MESSAGE
