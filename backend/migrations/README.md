# Migracje Bazy Danych

## Przegląd

Ten katalog zawiera skrypty SQL do aktualizacji struktury bazy danych i procedur składowanych.

## Kolejność wykonywania

Migracje powinny być wykonywane w kolejności numerycznej:

1. `000_add_missing_columns.sql` - Dodaje brakujące kolumny do tabel
2. `001_update_sp_PNAGL_Podpisz.sql` - Aktualizuje procedurę składowaną podpisywania protokołów
3. `002_create_config_table.sql` - Tworzy tabelę Config dla konfiguracji aplikacji

## Jak zastosować migracje

### SQL Server Management Studio (SSMS)

1. Otwórz SQL Server Management Studio
2. Połącz się z bazą danych
3. Otwórz plik migracji (File -> Open -> File)
4. **WAŻNE**: W pliku `000_add_missing_columns.sql` zamień `[YourDatabaseName]` na nazwę swojej bazy danych
5. Wykonaj skrypt (F5 lub Execute)
6. Sprawdź komunikaty w oknie Messages, aby upewnić się, że migracja przebiegła pomyślnie

### sqlcmd (wiersz poleceń)

```bash
# Uruchom migrację dodającą kolumny (najpierw edytuj plik i zmień nazwę bazy!)
sqlcmd -S your_server -d your_database -i 000_add_missing_columns.sql

# Uruchom migrację aktualizującą procedurę
sqlcmd -S your_server -d your_database -i 001_update_sp_PNAGL_Podpisz.sql
```

## Zmiany wprowadzone przez migracje

### 000_add_missing_columns.sql

Dodaje następujące kolumny (jeśli nie istnieją):

- **ProtokolNagl.PNAGL_UZT_Id_Ostatni** (SMALLINT) - ID użytkownika, który ostatnio modyfikował/podpisał protokół
- **ProtokolNagl.PNAGL_UzytkownikPodpisujacy** (NVARCHAR(100)) - Pełne imię i nazwisko użytkownika zbierającego podpis
- **ZadanieNagl.ZNAG_DoAktualizacji** (BIT) - Flaga wskazująca, że zadanie wymaga aktualizacji (domyślnie 0)
- **ZadanieNagl.ZNAG_PodpisDoProtokolow** (BIT) - Flaga wskazująca, że podpis z zadania ma być użyty dla wszystkich protokołów (domyślnie 0)

**Uwaga**: Data podpisu jest przechowywana w istniejącym polu **ZNAG_TS_Ostatni** (timestamp ostatniej modyfikacji zadania).

### 001_update_sp_PNAGL_Podpisz.sql

Aktualizuje procedurę składowaną `sp_PNAGL_Podpisz`:

- Dodaje parametry `@user_id` i `@user_name`
- Ustawia nowe pola podczas podpisywania protokołu:
  - `PNAGL_UZT_Id_Ostatni` - ID użytkownika
  - `PNAGL_UzytkownikPodpisujacy` - Imię i nazwisko użytkownika
  - `PNAGL_UZTOstatni` - Imię i nazwisko użytkownika (dla zgodności)
  - `PNAGL_TS` - Timestamp aktualizacji

### 002_create_config_table.sql

Tworzy tabelę **Config** do przechowywania konfiguracji aplikacji (model klucz-wartość):

Struktura tabeli:
- **CONF_Id** (INT, IDENTITY) - Klucz główny
- **CONF_Klucz** (NVARCHAR(100), UNIQUE) - Klucz konfiguracji
- **CONF_Wartosc** (NVARCHAR(500)) - Wartość konfiguracji
- **CONF_Opis** (NVARCHAR(255)) - Opis parametru konfiguracyjnego
- **CONF_TS** (DATETIME2) - Timestamp ostatniej modyfikacji

Domyślne wartości konfiguracji:
- **ZDJECIA_SCIEZKA**: `C:\Zdjecia\Protokoly` - Ścieżka do katalogu ze zdjęciami (może być lokalna lub sieciowa, np. `\\192.168.0.100\katalog\aplikacja\zdjecia`)
- **PDF_SCIEZKA**: `C:\PDF\Raporty` - Ścieżka do katalogu z raportami PDF

## Weryfikacja

Po zastosowaniu migracji zweryfikuj zmiany:

```sql
-- Sprawdź czy kolumny zostały dodane
SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'ProtokolNagl'
AND COLUMN_NAME IN ('PNAGL_UZT_Id_Ostatni', 'PNAGL_UzytkownikPodpisujacy');

SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'ZadanieNagl'
AND COLUMN_NAME IN ('ZNAG_DoAktualizacji', 'ZNAG_PodpisDoProtokolow', 'ZNAG_TS_Ostatni');

-- Sprawdź czy procedura została zaktualizowana
EXEC sp_helptext 'sp_PNAGL_Podpisz';

-- Sprawdź czy tabela Config została utworzona
SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Config';

-- Sprawdź domyślne wartości konfiguracji
SELECT CONF_Klucz, CONF_Wartosc, CONF_Opis FROM Config;
```

## Wycofanie zmian (Rollback)

W razie potrzeby wycofania zmian:

```sql
-- Usuń dodane kolumny
ALTER TABLE ProtokolNagl DROP COLUMN PNAGL_UZT_Id_Ostatni;
ALTER TABLE ProtokolNagl DROP COLUMN PNAGL_UzytkownikPodpisujacy;
ALTER TABLE ZadanieNagl DROP COLUMN ZNAG_DoAktualizacji;
ALTER TABLE ZadanieNagl DROP COLUMN ZNAG_PodpisDoProtokolow;

-- Przywróć starą wersję procedury (bez nowych parametrów)
-- UWAGA: To usunie nową wersję procedury!
```
