from konstanty import PREFIX, SUFFIX, NOT_FOUND, Odezva

LINK_NOTION_SPLNENE_DB = "https://www.notion.so/janzeman3/3f6b1919e9bd49eaa46e2e21108ba0ce?v=62bb60897c594cf2ab1d8c30cab459d7"
LINK_NOTION_SPLNENE_VSICHNI = "https://www.notion.so/janzeman3/Co-m-m-spln-n-f2bfced1bcc44d5588ad54568b11dca0"
LINK_NOTION_SPLNENE_RON = "https://www.notion.so/janzeman3/Ron-d14d48bfcafb4c73bd104d9f32a1730a"
LINK_NOTION_SPLNENE_VOJTA = "https://www.notion.so/janzeman3/Vojta-380e865bce234d85b6f1b11d7933ed3c"
LINK_NOTION_SPLNENE_HARRY = "https://www.notion.so/janzeman3/Harry-32051382aae14e66b3043f1f13a70b78"

## Node builder - splnene body stezky
def get_node_splnene():
    tabulka_odpovedi = {PREFIX: "asi by pomohl seznam splněných výzev a bodů stezky... ",
                        SUFFIX: "",
                        NOT_FOUND: LINK_NOTION_SPLNENE_VSICHNI,
                        'janzeman3': "ty nic neplniš, tak Ti dám odkaz na všechny kluky " + LINK_NOTION_SPLNENE_DB,
                        'TOXIC_vetracek': LINK_NOTION_SPLNENE_RON,
                        'Pooky': LINK_NOTION_SPLNENE_VOJTA,
                        'RoVeR': LINK_NOTION_SPLNENE_HARRY}

    uzel_spln = {'keys': ["spln"],
                 'subnodes': [],
                 'action': {'type': Odezva.TEXT_BY_USER,
                            'data': tabulka_odpovedi}
                 }

    return uzel_spln
