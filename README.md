# JFTT Compiler
__Autor: Sebastian Woźniak__

Kompilator prostego języka imperatywnego do kodu maszyny wirtualnej napisany w języku Python.

## Użyte narzędzia:
- język programowanie Python __3.10+__
- biblioteka 'sly' ( *pip install sly* )

## Uruchomienie:
```sh
python3 kompilator.py <input_file> [<output_file>]
```
Aby wyświetlić pełną liste argumentów:
```sh
python3 kompilator.py -h
lub
python3 kompilator.py --help
```

## Opis dostarczonych plików:

Opis dostarczonych plików:
- __kompilator.py__: Główny plik odpowiedzialny za przetwarzanie argumentów linii poleceń oraz wywoływanie metod lexera i parsera.

- __lexer.py__: Analizator leksykalny, który identyfikuje tokeny w źródłowym kodzie.

- __parser.py__: Analizator składniowy, wywołujący odpowiednie funkcje generatora kodu, odpowiada za strukturalną analizę kodu.

- __code_generator.py__: Klasa odpowiedzialna za generowanie kodu wynikowego, wypisywanie go do pliku wynikowego.

- __code_generator_functions (folder)__:

  * __arithemetic.py__: Funkcje generujące operacje arytmetyczne.
  * __assign.py__: Funkcje generujące operacje przypisania (assign).
  * __blocks.py__: Funkcje generujące bloki kodu takie jak IF, IF ELSE, FOR, WHILE, REPEAT.
  * __io.py__: Funkcje generujące operacje WEJŚCIA/WYJŚCIA (READ/WRITE).
  * __logical.py__: Funkcje generujące operacje logiczne.
- __allocator.py__: Klasa odpowiedzialna za przydzielanie miejsca w pamięci dla deklarowanych zmiennych.

- __procedures (folder)__:

  * __procedure_generator.py__: Klasa zarządzająca generowaniem procedur i przechowująca informacje o nich.
  * __procedure.py__: Klasa reprezentująca pojedynczą procedurę.
- __parser_error_functions.py__: Funkcje sprawdzające, czy nie wystąpił błąd, takie jak używanie niezainicjowanej zmiennej, itp.
## Errors:
- Double declaration (zmienna, procedura, zmienne w procedurze)
- Out of memory
- Syntax error ( parser, lexer )
- Usage of undeclared variable ( program, procedure )
- Usage of unset variable
- Invalid type passed to procedure
- Index out of range
- Double array -> a[b[1]]
- Use of int as array/array as int

## Warnings:
- Usage of unset variable in conditional scope
- Usage of unset variable as procedure argument
