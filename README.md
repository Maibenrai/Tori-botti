# TORI-BOTTI

Tori-botti etsii tori.fi kauppapaikasta haluaamasi tuotetta. Jos botti löytää tuotteen, niin halutessaan se lähettää siitä viestin telegram-sovellukseen. 

Idea lähti siitä, että äitini etsi uutta clavinova pianoa kotiinsa.

Tavoitteena oli myös oppia pythonia ja sen kirjastoja. 

## Jos haluat ilmoituksen telegrammiin uudesta tuotteesta, toimi seuraavasti

1. Tee uusi botti telegrammiin (telegramissa käyttäjä BotFather)
2. Laita botin tokeni bot.py tiedostoon token muuttujaan
3. Lähetä jokin viesti uudelle botillesi
4. Mene osoitteeseen "https://api.telegram.org/bot<YourBOTToken>/getUpdates"
5. Ota chat.id talteen, ja laita se bot.py tiedoston chatID muuttujaan

## Käyttöohjeet

1. Laita item.py tiedoston item muuttujaan tuote mitä haluat etsiä torista
2. Aja tori.py, konsoliin tulostuu tiedot kaikista löytyneistä tuotteista
3. Jätä konsoli pyörimään taustalle, uudet tuotteet päivittyvät 2min välein itsestään.
