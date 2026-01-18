CANDY CRUSH AUTOMATIZAT
MODUL DE RULARE

Proiectul este implementat în Python și este format dintr-un singur fișier. Pentru rulare ai nevoie de Python 3 și biblioteci standard (tkinter, random). Codul și fișierul de intrare (dacă vrei să setezi seed-uri sau configurații) trebuie puse în același folder. Programul se pornește dintr-un IDE sau din linia de comandă, iar interfața grafică va apărea imediat. Programul rulează automat mutările și scorul este afișat în timp real pe ecran.

CUM FUNCȚIONEAZĂ PROIECTUL:

1.Programul generează o tablă 11x11 cu bomboane colorate random. Algoritmul caută automat toate combinațiile de minim 3 bomboane identice în linie (orizontal sau vertical). Dacă există formații, acestea sunt eliminate și se aplică gravitația, astfel încât bomboanele de deasupra cad în golurile create, iar spațiile goale sunt refăcute cu bomboane noi.

2.Dacă nu mai există formații, programul caută mutări valide (swap-uri între două bomboane vecine) care generează cel puțin un match. Dintre acestea se alege prima mutare care dă puncte. Procesul se repetă automat până când nu mai există mutări valide sau tabla nu mai generează combinații.

3.În timpul rulării, celulele mutate sunt evidențiate, iar match-urile sunt animate vizual, astfel încât scorul și numărul de mutări să fie ușor de urmărit.

CE INFORMAȚII SUNT URMĂRITE!!!!!!

Interfața afișează constant:

-scorul total

-numărul de mutări efectuate

-evidențierea celulelor mutate și a match-urilor

Scopul programului este să simuleze complet un joc de Candy Crush, inclusiv detectarea și aplicarea automată a match-urilor și a gravitației, fără intervenție manuală.
