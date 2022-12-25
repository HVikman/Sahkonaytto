# Sahkonaytto
Raspberry pi pico w projekti

Tällä hetkellä laite näyttää sähkön hinnan sh1106 näytöllä sekä binäärinä ledeillä. Laitteessa on myös RGB led, joka palaa vihreänä sähkön hinnan ollessa alle raja-arvon ja punaisena muuten.

Laite tunnistaa mikäli asetustiedostossa ei ole määritelty wlan asetuksia ja käynnistää laitteen wlan asetukset-tilaan jolloin laitteen näyttö ohjeistaa yhdistämään laitteen wlan access pointtiin ja menemään laitteen ip-osoitteeseen selaimella asetusten määrittämiseksi.

Laitteen voi myös käynnistää asetuksiin pitämällä nappia pohjassa kunnes keskimmäinen ledi lopettaa vilkkumisen. Tällöin laite opastaa näytöllä yhdistämään samaan verkkoon laitteen kanssa ja menemään selaimella laitteen ip-osoitteeseen. Asetuksissa on nyt määriteltävänä näytöllä olevien lukujen pyöristys ja RGB ledin raja-arvo. Asetuksista näkee myös laitteen ohjelmiston nykyisen version.

Laite tarkistaa myös onko päivitys saatavilla aina, kun hakee uudet hintatiedot ja mikäli uusi versio on saatavilla, päivittää laite ohjelmiston seuraavan käynnistyksen yhteydessä.
