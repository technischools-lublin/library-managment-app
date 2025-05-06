Historyjka 1)
- Jako bibliotekarz chcę dodać nową książkę, aby była dostępna do wypożyczenia.

Acceptance criteria
- Wszystkie wymagane pola (ISBN, tytuł, autor, ...) muszą być wypełnione.
- ISBN (International Standard Book Number) musi być unikalny - duplikat => błąd.
- Po sukcesie wyświetla się komunikat "Książka dodana" - Użytkownik dostaje widoczne potwierdzenie.


Historyjka 2)
- Jako bibliotekarz chcę wypożyczyć książkę czytelnikowi, aby mógł ją zabrać do domu.

Acceptance criteria
- System odrzuca wypożyczenie, gdy status = "wypożyczona".
- Czytelnik otrzymuje e‑mail z potwierdzeniem i datą zwrotu.


Historyjka 3)
- Jako system chcę automatycznie naliczać karę za każdy dzień spóźnienia zwrotu, aby egzekwować terminowość.

Acceptance criteria
- Obliczenia wykonywane raz dziennie o 00:00.
- Stawka dzienna pobierana z konfiguracji.
- Jeśli kara istnieje - aktualizowana kwota, jeśli nie - tworzony nowy rekord.