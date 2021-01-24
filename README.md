# Game of Life PWI Edition

## Tematyka

Interaktywna graficzna implementacja automatu komórkowego *The Game of Life* Johna Conwaya. Posiada ona kilka ciekawych rozszerzeń opisanych poniżej.
 
## Szczegółowy opis symulacji

Symulacja ma miejsce na planszy 20 na 20, na której mogą występować 3 gatunki komórek:
* żółty
* czerwony
* niebieski

Plansza początkowa może zostać zdefiniowana przez użytkownika lub zostać losowo wygenerowana. Każdy z gatunków może pojawić się na danym polu losowo wygenerowanej planszy z prawdopodobieństwem 10%. Dodatkowo, w trakcie rozgrywki komórka danego gatunku może pojawić się na określonym polu, jeśli wokół niego znajduje się wystarczająca liczba sprzymierzeńców oraz bezpieczna liczba wrogów. Pola sąsiednie, to wszystkie pola, które przylegają do wybranego pola bokiem lub rogiem. Jeśli w trakcie rozgrywki sąsiadami zostaną komórki różnych gatunków, przebiegają między nimi potyczki opisane następującymi zasadami:
* żółty pokonuje czerwonego
* czerwony pokonuje niebieskiego
* niebieski pokonuje żółtego
* wygrany otrzymuje 1 punkt życia, przegranemu odejmowany jest 1 punkt życia
* jeśli komórka straci wszystkie punkty życia, to zajmowane przez nią pole staje się wolne

Na przebieg symulacji wpływ mają parametry:
* Quake - trzęsienie ziemi, które odejmuje każdej żywej komórce 1 punkt życia
* Mutacje - losowe pole zmienia swój stan
* Tempo - określa przybliżoną prędkość rozgrywki

Wyświetlane są informacje o liczbie wykonanych iteracji symulacji *(Czas)* oraz o liczbie żywych komórek danego gatunku.

Użytkownik ma wpływ na przebieg symulacji (nawet w trakcie jej trwania): może wstrzymać oraz wznowić rozgrywkę, edytować stan pól, wpływać na parametry symulacji.

## Wymagania

### Linux

Uruchomienie gry na systemach opartych na jądrze Linux wymaga interpretera języka Python3. Jeżeli system domyślnie nie zawiera interpretera, należy go zainstalować za pomocą polecenia odpowiedniego dla danej dystrybucji systemu.


## Instalacja 

Należy pobrać zawartość repozytorium do wybranego folderu poleceniem:

~~~ 
git clone git@github.com:IIUWr20/projekt-zespol-6.git
~~~

Możliwe jest również pobranie projektu w archiwum .zip za pośrednictwem GitHub'a - zielony przycisk "Code" -> "Download Zip" na stronie repozytorium.

<strong>Uwaga!</strong>
Jeżeli antywirus uznaje plik .exe za szkodliwe oprogramowanie, należy dodać ten plik do wyjątków lub wyłączyć antywirusa.

## Uruchomianie programu

### Windows
Aby uruchomić grę należy uruchomić plik "Gra w życie.exe".



### Linux

Będąc w katalogu, do którego pobrano repozytorium, należy wykonać polecenie:
~~~ 
./run_game_of_life.sh
~~~

## Instrukcja obsługi

![](https://i.imgur.com/abQ20Nq.png)

### Interfejs użytkownika

* Rozpocznij - rozpoczyna symulację (jeżeli plansza jest pusta, generuje nową)
* Generuj - generuje nową planszę
* Wyczyść - powoduje wyczyszczenie planszy (jeżeli trwa symulacja - zatrzymuje ją)
* 1, 5, 10 ruch/-ów - wykonuje podaną liczbę iteracji symulacji
* Lewy przycisk myszy na polu - zmienia gatunek komórki
* Prawy przycisk myszy na polu - odejmuje komórce 1 punkt życia
* Punkty życia - określa liczbę punktów życia, z którą rodzi się komórka danego gatunku
* Sąsiedzi - wymagana liczba sprzymierzeńców, aby komórka danego gatunku mogła się narodzić
* Reprodukcja - liczba iteracji, po których może się narodzić nowa komórka danego gatunku

