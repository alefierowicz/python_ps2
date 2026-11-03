# Zadanie 2

### cel zadania:
zaprojektowanie & zaimplementowanie mini systemu zarządzania zadaniami (to-do), z naciskiem na zaawansowane koncepcje programowania obiektowego:
- dziedziczenie, kompozycja & polimorfizm
- wlasne metody specjalne (`__str__`, `__lt__`, `__eq__`, itp.)
- klasy abstrakcyjne i interfejsy
- wykorzystanie `__init_subclass__` lub `__new__` w konstrukcji systemu
- ewentualnie metaklasy / dekoratory klas?

### opis problemu:
obiektowy system to-do, umozliwiajacy:
- dodawanie roznych typow zadan (zwykle, priority)
- grupowanie zadan w projekty
- sortowanie, filtrowanie & zmiany statusow
- mozliwosc rozbudowy o nowe typy zadan bez modyfikacji istniejacego kodu