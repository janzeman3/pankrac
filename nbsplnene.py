import konstanty

LINK_NOTION_SPLNENE = "https://www.notion.so/janzeman3/3f6b1919e9bd49eaa46e2e21108ba0ce?v=62bb60897c594cf2ab1d8c30cab459d7"

## Node builder - splnene body stezky
def get_node_splnene():
    uzel_spln = {'keys': ["spln"],
                 'subnodes': [],
                 'action': {'type': konstanty.TYPE_RUTINNE_TEXT,
                            'data': "Asi by pomohl seznam splněných výzev a bodů stezky " + LINK_NOTION_SPLNENE}
                 }

    return uzel_spln
