# Koza, Kapusta i Wilk
## Treść zagadki
Popularna zagadka która polega na tym, że rolnik posiadający małą łódkę musi przetransportować przez rwącą rzekę cały swój inwentarz. W klasycznej wersji tej zagadki na jednym z brzegów znajduje się koza, kapusta oraz wilk. Mając miejsce na tylko jedno ze swoich dóbr na swojej łódce musi transportować zwierzęta tak, żeby na żadnym brzegu nie pozostawić pary która mogłaby stanowić dla siebie zagrożenie. Jadłospis jest jasny: wilk, gdyby nie obecność rolnika zje kozę a koza, gdyby nie była odpędzana przez rolnika, to schrupałaby kapustę ze smakiem.  
Skrypt przewoz.py ma za zadanie wypisać sekwencję przewozu zwierząt w zgodzie z powyższymi zasadmi, a skrypt sprawdz.py otrzymując odpowiednią wartość wejściową, wypisze graficzne przedstawienie przewozu, lub określi w którym momencie doszło do pożarcia na którymś z brzegów. Oba skrypty powinny być uruchamiane w wersji Pythona 3.6
## przewoz.py
Skrypt podczas uruchamiania przyjmuje dwa argumenty z czego jeden jest opcjonalny: plik tekstowy w którym jest zapisany inwentarz i zależności pomiędzy zwierzętami oraz pojemność łódki. Przykładowe komendy uruchamiające skrypt:  
```
python przewoz.py koza.txt 3
python przewoz.py inwentarz.txt
```  
Plik tekstowy powinien składać się z lini, które opisują inwentarz oraz zależności pomiędzy zwierzętami. Formatowanie powinno wyglądać następująco:
```
[LICZBA] ZWIERZAK
ZWIERZAK ZWIERZAK_1 ZWIERZAK_2 …. ZWIERZAK_m
```
Gdzie [LICZBA] określa ile zwierząt danego rodzaju znajduje się na początkowym brzegu, a linia zawierająca więcej niż jedno zwierze określa jakie zwierzęta zjada zwierze podane jako pierwsze w danej linii. Przykładowy plik wejściowy:
```
WILK
WILK KOZA
2 KOZA
KOZA KAPUSTA
KAPUSTA
```
Jeżeli program jest uruchamiany bez określenia pojemności łódki to przyjmuje ona wartość domyślną czyli 2.
Po uruchomieniu skrypt tworzy graf z węzłami określającymi kolejne etapy transportu. Po wykonaniu się skrpytu graf jest eksportowany do pliku graph.png.  
Graf może zawierać 4 rodzaje wierzchołków: 
  - ['POCZĄTEK'] - który określa korzeń grafu i z niego wywodzą się wszystkie pozostałe ścieżki
  - ['KONIEC'] - który określa wierzchołek w którym doszło do otrzymania docelowego stanu obu brzegów - brzeg początkowy jest pusty a cały inwentarz znajduje się na przeciwnym brzegu
  - ['ZAPĘTLENIE'] - który oznacza moment, w którym skrypt zaczął się zapętlać i proponować kursy które nie prowadziły do zmianu stanu lub doprowadzał do powtórzenia się stanu brzegów który już wystąpił wcześniej w bieżącej ścieżce
  - ['POŻARCIE'] - który oznacza sytuację w której na jednym z brzegów doszło do zagrożenia życia jednego ze zwierząt.
Najkrótsza ścieżka prowadząca od początku do końca zostanie wyróżniona w postaci powiększenia węzłów wchodzących w skład tej ścieżki oraz odpowiednie węzły będą koloru zielonego. 
Ponadto jeżeli zostały podane odpowiednie argumenty to skrypt zwróci w terminalu sekwencję w postaci listy kolejnych etapów transportu. Jeżeli nie jest możliwe rozwiązanie zagadki z podanymi parametrami to zostanie zwrócony napis: ['NIEMOŻLIWE'].
## sprawdz.py
Skrypt który jako wartość wejściową przyjmuje listę kolejnych etapów transportu, lub zwrot ['NIEMOŻLIWE']. Argumenty te mogą zostać zostać dostarczone jedynie w formie `stnadard input`. Ten program również przyjmuje argumnety określające plik tekstowy zawierający inwentarz i relacje oraz pojemność łódki, podobnie jak skrypt przewoz.py. Przykładowe komendy uruchamiające skrypt:
```
python przewoz.py koza.txt | sprawdz.py koza.txt 2
echo $'[[\'KOZA\',\'KOZA\'],[\'WILK\'],[]]' | python sprawdz.py koza.txt 3
```
Należy zauważyć, że formatem wejściowym jest lista list. Jest to spowodowane koniecznością wymienienia kolejnych pasażerów w wypadku większej pojemności łódki.
Po podaniu sekwencji skrypt zacznie wypisywać kolejne etapy przewozu z graficznym przedstawieniem stanów obu brzegów, oraz komunikatem jaki i, w którą stronę odbywa się dany transport. W przypadku dojścia do momentów, w którym na jednym z brzegów dojdzie do pożarcia się zwierząt skrypt odpowiednio poinformuje użytkownika. Jeżeli skrypt otrzyma w `stdin` zwrot ['NIEMOŻLIWE'] to zareaguje stosownym błędem.
## Wymagania
Do poprawnego działania skryptu przewoz.py potrzebne jest zainstalowanie zewnętrznej biblioteki [NetworkX](https://networkx.github.io/documentation/networkx-1.10/index.html). Do rysowania grafu potrebny jest pakiet [pyplot](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.html) z biblioteki [Matplotlib](https://matplotlib.org/3.1.1/index.html). Ponadto w pliku cabbage.py znajdują się funkcje z których korzystają oba skrypty, więc powinien on być obecny w folderze, z którego się je wykonuje.
