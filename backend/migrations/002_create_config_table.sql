-- Migration: Utworzenie tabeli Config dla konfiguracji aplikacji
-- Data: 2025-12-27

USE [YourDatabaseName] -- Zmień na nazwę swojej bazy danych
GO

-- Sprawdź czy tabela Config już istnieje
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Config' AND schema_id = SCHEMA_ID('dbo'))
BEGIN
    -- Utwórz tabelę Config
    CREATE TABLE [dbo].[Config] (
        CONF_Id INT IDENTITY(1,1) NOT NULL,
        CONF_Klucz NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
        CONF_Wartosc NVARCHAR(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
        CONF_Opis NVARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
        CONF_TS DATETIME2 NOT NULL DEFAULT GETDATE(),
        CONSTRAINT PK_Config PRIMARY KEY (CONF_Id),
        CONSTRAINT UQ_Config_Klucz UNIQUE (CONF_Klucz)
    );
    PRINT 'Tabela Config utworzona pomyślnie'
END
ELSE
    PRINT 'Tabela Config już istnieje'
GO

-- Dodaj domyślną ścieżkę do zdjęć (jeśli nie istnieje)
IF NOT EXISTS (SELECT * FROM [dbo].[Config] WHERE CONF_Klucz = 'ZDJECIA_SCIEZKA')
BEGIN
    INSERT INTO [dbo].[Config] (CONF_Klucz, CONF_Wartosc, CONF_Opis)
    VALUES (
        'ZDJECIA_SCIEZKA',
        'C:\Zdjecia\Protokoly',
        'Ścieżka do katalogu z zdjęciami protokołów (lokalna lub sieciowa, np. \\192.168.0.100\katalog\aplikacja\zdjecia)'
    );
    PRINT 'Dodano domyślną konfigurację ścieżki zdjęć'
END
ELSE
    PRINT 'Konfiguracja ścieżki zdjęć już istnieje'
GO

-- Dodaj inne domyślne konfiguracje (opcjonalnie)
IF NOT EXISTS (SELECT * FROM [dbo].[Config] WHERE CONF_Klucz = 'PDF_SCIEZKA')
BEGIN
    INSERT INTO [dbo].[Config] (CONF_Klucz, CONF_Wartosc, CONF_Opis)
    VALUES (
        'PDF_SCIEZKA',
        'C:\PDF\Raporty',
        'Ścieżka do katalogu z wygenerowanymi raportami PDF'
    );
    PRINT 'Dodano domyślną konfigurację ścieżki PDF'
END
ELSE
    PRINT 'Konfiguracja ścieżki PDF już istnieje'
GO

PRINT 'Migracja zakończona pomyślnie'
GO
