import httpx
from selectolax.parser import HTMLParser


def get_html():
    url = 'https://www.tipp3.at/sportwetten/eventdetails?eventID=2933345&caller=PRO'
    resp = httpx.get(url)
    return HTMLParser(resp.text)


def parse_element(html):
    bets = html.css("div.t3-match-details__entry")
    bet_types = []
    bet_dsic = []
    beT_odd = []
    for item in bets:
        bet_types.append(item.css_first("div.t3-match-details__entry-header").text())
        dsic = item.css("div.t3-bet-element__label")
        for a in dsic:
            bet_dsic.append(a.text())
        bet =  item.css("div.t3-bet-element__field")
        for a in bet:
            beT_odd.append(a.text())
        i = 1
    print(bet_types)


def main():
    html = get_html()
    parse_element(html)


if __name__ == '__main__':
    main()

