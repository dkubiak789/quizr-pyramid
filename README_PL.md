Quizr
=====

Aplikacja pozwalająca na rozwiązywanie quizów. 

To jest tylko szkielet aplikaji, jaką studenci muszą rozwinąć w ramach ćwiczeń
podczas podyplomowych studiów "Programowanie aplikacji internetowych" na Wyższej
Szkole Nauk Humanistycznych i Dziennikarstwa w Poznaniu.


Instalacja
----------

Wejdź na github do [repozytorium projektu](https://github.com/sargo/quizr-pyramid)
i stwórz forka.

Następnie przygotuj virtualenv i sklonuj Twojego forka repozytorium:

```
source /opt/python/2.7/bin/virtualenvwrapper.sh
mkvirtualenv --python=/opt/python/2.7/bin/python quizr-pyramid
cdvirtualenv
git clone git@github.com:username/quizr-pyramid.git
cd quizr-pyramid
python setup.py develop
initialize_quizr_db development.ini
```

Użycie
------

Przygotowanie do pracy:

```
workon quizr-pyramid
cdvirtualenv
cd quizr-pyramid
```

Uruchomienie aplikacji:

```
pserve development.ini
```

Uruchomienie testów jednostkowych:

```
python setup.py test -q
```

Treść zadania
-------------

Używając frameworka Pyramid, należy stworzyć aplikację, dzięki której użytkownik
będzie mógł wziąć udział w quizie. Użytkownik, po wejściu na stronę główną
powinien zobaczyć krótki opis zasad quizu oraz formularz logowania (gdy nie
zalogowany) lub przycisk “Start” (gdy zalogowany). Po rozpoczęciu, aplikacja
losuje jedno z pytań i pokazuje je użytkownikowi wraz z możliwymi odpowiedziami.
Po udzieleniu odpowiedzi przez użytkownika, losowane jest kolejne pytanie (nie
są brane pod uwagę pytania które wcześniej padły). Po udzieleniu odpowiedzi na 5
pytanie, użytkownikowi pokazywany jest ekran podziękowania, wraz z ilością
zdobytych punktów wraz z maksymalną wartością oraz jako procent maksymalnej
wartości - przykład 12 / 15 (80%) prezentowana jest także lista najlepszych
osób (top 10).

Punktacja:
 * 3 punkty za poprawną odpowiedź w czasie krótszym niż 10 sekund od
     wyświetlenia pytania
 * 2 punkty za poprawną odpowiedź pomiędzy 10 a 30 sekundą od wyświetlenia
     pytania
 * 1 punkt za poprawną odpowiedź w czasie powyżej 30 sekund

Wynik (punktacja) zostaje zapisana w bazie danych. Dane to posłużą do stworzenia
listy najlepszych osób (top 10).

Pytania mogą mieć 2 do 5 możliwych odpowiedzi, ale tylko jedna jest prawidłowa. 
Pytania do quizu aplikacja pobierać będzie z pliku w formacie CSV.
Przykładowy plik znajduje się w folderze `quizr/data`.

Struktura CSV:
 * Pierwsza kolumna - pytanie
 * Ostatnia kolumna - prawidłowa odpowiedź (wartość A, B, C, D lub E)
 * Pozostałe kolumny - możliwe odpowiedzi

Aplikacja powinna posiadać testy jednostkowe.
