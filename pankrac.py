from pankracutils import obsahuje
from konstanty import ResponseType, Reaction, Odezva
import uzelbuilder

## Odpovídací logika chatbota
class Pankrac:
    moznosti = {}

    def __init__(self):
        self.moznosti = uzelbuilder.hlavni_uzel(self)

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

        if akce['type'] == Odezva.METHOD:
            odpoved['data'], odpoved['type'] = akce['data'](otazka)

        elif akce['type'] == Odezva.TEXT:
            odpoved['data'] = akce['data']

        elif akce['type'] == Odezva.TEXT_BY_USER:
            odpoved['data'] = self.reakce_dle_tabulky(message.author.name, akce['data'])

        elif akce['type'] == Odezva.CLOSE:
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
        return Reaction.THUMB_UP, ResponseType.REACTION

    def reaction_wave(self, message_text):
        return Reaction.WAVE, ResponseType.REACTION

    def reaction_cry(self, message_text):
        return Reaction.CRY, ResponseType.REACTION

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
