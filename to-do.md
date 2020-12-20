# Tasks (zatwierdzone i do zrobienia)

## Następne spotkanie: 26.12.

## Logika

* [Andrzej] generowanie losowej planszy, ale z określonym prawdopodobieństwem pojawienia się danego gatunku komórki

* [Mierzej] nowa logika 

* [Wojtek] testy oprogramowania (pytest)???

* [Andrzej] ujednolicenie komentarzy i nazewnictwa (jeden styl i jeden język)(commity po polsku, kod po angielsku, komentarze po polsku, małymi literami, komentarze na temat funkci bezpośrednio nad definicją funkcji, estetyczne formatowanie)

* [Andrzej] możliwość zakończenia symulacji, jeśli plansza się zapętli

* [Mierzej] jak już będzie więcej rodzajów komórek, to do poprawy ewaluacja sąsiadów

## GUI

* [ ] rozwój GUI

* [ ] łączenie GUI z backendem <- do nowego pliku main.py

### Propozycje (dalsze kroki itd.)

* [ ] plik uruchamialny, zamiast samego kodu źródłowego

### Niezwiązane z kodem

* gtk?
* GitKraken (?)

## Zrobione

* jak podzielić projekt na pliki
* jak komitować/merge'ować w zespole

* [14.12.2020, Patryś Mazur] funkcja, która generuje planszę o zadanym rozmiarze: generate(rozmiar)

* [14.12.2020, Mierzej] funkcja, która przyjmuje obecny stan planszy (listę list) i zwraca obliczony następujący stan planszy (listę list): next(plansza)

* [14.12.2020, Andrzej] funkcja, która przyjmuje planszę i drukuje ją w konsoli: draw(plansza):
    - '_' dla pustego pola
    - 'o' dla zajętego pola przez żywą komórkę

* [14.12.2020, Michał Mróz] funkcja, która przyjmuje planszę, koordynaty i pod podanymi współrzędnymi zmienia stan pola (żywy > martwy / martwy > żywy): modify(plansza, x, y)

* [18.12., Mierzej] więcej rodzajów jednostek - dopisanie do generatora tych nowych jednostek (numery 1, 2, 3)

* [18.12., Wojtek] pętla o funkcjonalności wyświetlania zmian (pętla z dobrą kolejnością już napisanych funkcji)

* [18.12., Wojtek] wyświetlanie zmian co określoną liczbę pokoleń (póki co - wpisywanie przed symulacją, później (kiedy będzie GUI) - w trakcie trwania)

* [18.12., Patryk] jakaś testowa plansza w formie txt (przekształcana na listę list), żeby dało się sprawdzać, czy ewolucja działa poprawnie

* [18.12. Andrzej] drukowanie planszy z większą liczbą rodzajów jednostek (1 - 'o', 2 - 'x', 3 - '@')

* [18.12. Michał] początek GUI (tkinter): przy odpaleniu programu wyskakuje puste okno (z przyciskami ewentualnie) < gui.py

* [piątek 18.12. @all] przygotowanie propozycji rodzajów żywych komórek i interakcji (3 rodzaje i interakcje: 1 - 2, 1 - 3, 2 - 3)
