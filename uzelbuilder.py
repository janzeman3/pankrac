import uzelbuildersplnene
from konstanty import Odezva, Reaction

LINK_WEB_STEZKA = "https://stezka.skaut.cz/prohlizej-a-inspiruj-se/"
LINK_WEB_NOVACEK = "https://stezka.skaut.cz/novacek/"
LINK_NOTION_VYZVY = "https://www.notion.so/janzeman3/0995fe1d94a9403e99e667fc2ad15e30?v=3d42ab631c064ce0a16dda28bd06439d"
LINK_SOKOLI_AKCE = "https://ibis.skauting.cz/calendar/skauti/"
LINK_SOKOLI_WEB = "https://ibis.skauting.cz/oddily/skauti-sokoli/"

def hlavni_uzel(Pankrac):
    uzel_spln = uzelbuildersplnene.get_node_splnene()

    uzel_stezka_na_webu = {'keys': ["stezk"],
                           'subnodes': [],
                           'action': {'type': Odezva.TEXT, 'data': "Posílám odkaz na stezku " + LINK_WEB_STEZKA}
                           }

    uzel_novacek_na_webu = {'keys': ["nováč"],
                            'subnodes': [],
                            'action': {'type': Odezva.TEXT, 'data': "Snad Ti pomůže nováček " + LINK_WEB_NOVACEK}
                            }

    uzel_vyzvy = {'keys': ["výzv"],
                  'subnodes': [],
                  'action': {'type': Odezva.TEXT, 'data': "Tady jsou výzvy " + LINK_NOTION_VYZVY}
                  }

    uzel_generuj_heslo = {'keys': ["heslo"],
                          'subnodes': [],
                          'action': {'type': Odezva.METHOD, 'data': Pankrac.generuj_heslo}
                          }

    uzel_akce = {'keys': ["akce"],
                 'subnodes': [],
                 'action': {'type': Odezva.TEXT,
                            'data': ":calendar: Nejbližší akce Sokolů najdeš tady: " + LINK_SOKOLI_AKCE}
                 }

    uzel_sokoli_web = {'keys': ["s sebou"],
                       'subnodes': [],
                       'action': {'type': Odezva.TEXT,
                                  'data': "Třeba Ti pomůže stránka našich skautů: " + LINK_SOKOLI_WEB}
                       }

    uzel_help = {'keys': ["nápověd", "pomoc", "help", "příkazy", "/"],
                 'subnodes': [],
                 'action': {'type': Odezva.METHOD, 'data': Pankrac.napoveda}
                 }

    uzel_dik = {'keys': ["dík", "dik", "dekuj", "děkuj"],
                'subnodes': [],
                'action': {'type': Odezva.REACTION, 'data': Reaction.THUMB_UP}
                }

    uzel_ahoj = {'keys': ["ahoj", "nazdar", "dobrou noc", "dobry den"],
                 'subnodes': [],
                 'action': {'type': Odezva.REACTION, 'data': Reaction.WAVE}
                 }

    uzel_close = {'keys': ["spát!"],
                  'subnodes': [],
                  'action': {'type': Odezva.CLOSE, 'data': ""}
                  }

    moznosti = {'keys': ["Pankráci"],
                'subnodes': [uzel_close, uzel_dik, uzel_ahoj, uzel_sokoli_web, uzel_vyzvy, uzel_stezka_na_webu,
                             uzel_novacek_na_webu, uzel_generuj_heslo, uzel_akce, uzel_help, uzel_spln],
                'action': {'type': Odezva.METHOD, 'data': Pankrac.nevim}
                }

    return moznosti
