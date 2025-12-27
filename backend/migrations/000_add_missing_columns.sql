-- Migration: Dodanie brakujących kolumn do tabel
-- Data: 2025-12-24

USE [YourDatabaseName] -- Zmień na nazwę swojej bazy danych
GO

-- 1. Dodaj PNAGL_UZT_Id_Ostatni do ProtokolNagl (jeśli nie istnieje)
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[ProtokolNagl]') AND name = 'PNAGL_UZT_Id_Ostatni')
BEGIN
    ALTER TABLE [dbo].[ProtokolNagl]
    ADD PNAGL_UZT_Id_Ostatni SMALLINT NULL;
    PRINT 'Kolumna PNAGL_UZT_Id_Ostatni dodana do ProtokolNagl'
END
ELSE
    PRINT 'Kolumna PNAGL_UZT_Id_Ostatni już istnieje w ProtokolNagl'
GO

-- 2. Dodaj PNAGL_UzytkownikPodpisujacy do ProtokolNagl (jeśli nie istnieje)
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[ProtokolNagl]') AND name = 'PNAGL_UzytkownikPodpisujacy')
BEGIN
    ALTER TABLE [dbo].[ProtokolNagl]
    ADD PNAGL_UzytkownikPodpisujacy NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL;
    PRINT 'Kolumna PNAGL_UzytkownikPodpisujacy dodana do ProtokolNagl'
END
ELSE
    PRINT 'Kolumna PNAGL_UzytkownikPodpisujacy już istnieje w ProtokolNagl'
GO

-- 3. Dodaj ZNAG_DoAktualizacji do ZadanieNagl (jeśli nie istnieje)
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[ZadanieNagl]') AND name = 'ZNAG_DoAktualizacji')
BEGIN
    ALTER TABLE [dbo].[ZadanieNagl]
    ADD ZNAG_DoAktualizacji BIT NOT NULL DEFAULT 0;
    PRINT 'Kolumna ZNAG_DoAktualizacji dodana do ZadanieNagl'
END
ELSE
    PRINT 'Kolumna ZNAG_DoAktualizacji już istnieje w ZadanieNagl'
GO

-- 4. Dodaj ZNAG_DataPodpisu do ZadanieNagl (jeśli nie istnieje)
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[ZadanieNagl]') AND name = 'ZNAG_DataPodpisu')
BEGIN
    ALTER TABLE [dbo].[ZadanieNagl]
    ADD ZNAG_DataPodpisu DATETIME2 NULL;
    PRINT 'Kolumna ZNAG_DataPodpisu dodana do ZadanieNagl'
END
ELSE
    PRINT 'Kolumna ZNAG_DataPodpisu już istnieje w ZadanieNagl'
GO

-- 5. Dodaj ZNAG_PodpisDoProtokolow do ZadanieNagl (jeśli nie istnieje)
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[ZadanieNagl]') AND name = 'ZNAG_PodpisDoProtokolow')
BEGIN
    ALTER TABLE [dbo].[ZadanieNagl]
    ADD ZNAG_PodpisDoProtokolow BIT NOT NULL DEFAULT 0;
    PRINT 'Kolumna ZNAG_PodpisDoProtokolow dodana do ZadanieNagl'
END
ELSE
    PRINT 'Kolumna ZNAG_PodpisDoProtokolow już istnieje w ZadanieNagl'
GO

PRINT 'Migracja zakończona pomyślnie'
GO
