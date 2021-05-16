def obsahuje(word_list, expression):
    return any([True for word in word_list if word in expression])

LINK_WEB_STEZKA = "https://stezka.skaut.cz/prohlizej-a-inspiruj-se/"
LINK_NOTION_VYZVY = "https://www.notion.so/janzeman3/0995fe1d94a9403e99e667fc2ad15e30?v=3d42ab631c064ce0a16dda28bd06439d"
LINK_NOTION_SPLNENE = "https://www.notion.so/janzeman3/3f6b1919e9bd49eaa46e2e21108ba0ce?v=62bb60897c594cf2ab1d8c30cab459d7"

## Odpovídací logika chatbota (verze 1.0 - pěkný fuj)
class Pankrac:
        def zpracuj_odezvu(self, message):
                otazka = message.content

                if "nápověd" in otazka or "pomoc" in otazka:
                        odpoved = self.napoveda()
                elif "akce" in otazka:
                        odpoved = self.web_akce()
                elif "s sebou" in otazka and "schůzk" in otazka:
                        odpoved = self.web_sokoli()
                elif "heslo" in otazka:
                        odpoved = self.generuj_heslo(otazka)
                elif obsahuje(["stezk"], otazka):
                        odpoved = self.web_stezka(otazka)
                elif obsahuje(["nováč", "novac"], otazka):
                        odpoved = self.web_novacek(otazka)
                elif obsahuje(["výzv"], otazka):
                        odpoved = self.web_vyzvy()
                else:
                        odpoved = "Tady Pankrác, slyším Tě, ale ale nevím, co po mě chceš.\n\n" + self.napoveda()

                return odpoved


        def napoveda(self):
                return "Nápověda: \n" \
                       "1. Pankrác reaguje, když se objeví ve větě slovo !Pankráci!\n" \
                       "2. Pankrác hledá klíčová !slova! a podle nich dává odpovědi.\n" \
                       "\nZatím umí:\n" \
                       ":muscle:generovat bezpečné !heslo!, co se dobře pamatuje \n" \
                       ":calendar: poslat odkaz na naše !akce!\n" \
                       ":link: poslat odkaz na stránku !sokol!ů, kde jsou věci, co si máme brát !s sebou! na !schůzk!y.\n"\
                       "na vypsat !nápověd!u, či !pomoc! :wink:"

        def generuj_heslo(self, message_text):
                from dice_heslo import get_password
                heslo = get_password()
                odpoved = "Borče, vygeneroval jsem Ti heslo :muscle: \n" + heslo + "\nmezery do hesla nezadávej :wink:"
                return odpoved

        #webové aktivity
        def web_akce(self):
                return ":calendar: Nejbližší akce Sokolů najdeš tady: https://ibis.skauting.cz/calendar/skauti/"

        def web_sokoli(self):
                return "Třeba Ti pomůže stránka našich skautů: https://ibis.skauting.cz/oddily/skauti-sokoli/"

        def web_stezka(self, message_text):
                if obsahuje(["moj", "spln"], message_text):
                    return "Co seznam Tvých splněných bodů stezky?" + LINK_NOTION_SPLNENE
                else:
                    return "Nepomůže ti stezka? " + LINK_WEB_STEZKA

        def web_novacek(self, message_text):
            if obsahuje(["splň", "spln", "moje"], message_text):
                return "Asi by pomohl seznam splněných výzev: " + LINK_NOTION_SPLNENE
            else:
                return "Snad Ti pomůže nováček: https://stezka.skaut.cz/novacek/"

        def web_vyzvy(self, message_text):
            if "splň" in message_text or "moje" in message_text:
                return "Asi by pomohl seznam splněných výzev: " + LINK_NOTION_SPLNENE
            else:
                return "Tady jsou výzvy: " + LINK_NOTION_VYZVY
