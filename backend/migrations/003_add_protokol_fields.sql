-- Migration: Dodanie pól do tabeli ProtokolNagl
-- Data: 2026-01-10
-- Opis: Dodanie pól Dopuszczenie urządzenia, Dane klienta (Nazwisko, Dział, Data zatwierdzenia)

USE [YourDatabaseName] -- Zmień na nazwę swojej bazy danych
GO

-- Dodanie pola PNAGL_Dopuszczenie
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[ProtokolNagl]') AND name = 'PNAGL_Dopuszczenie')
BEGIN
    ALTER TABLE [dbo].[ProtokolNagl]
    ADD PNAGL_Dopuszczenie NVARCHAR(200) COLLATE SQL_Latin1_General_CP1_CI_AS NULL;
    PRINT 'Dodano pole PNAGL_Dopuszczenie do tabeli ProtokolNagl';
END
ELSE
BEGIN
    PRINT 'Pole PNAGL_Dopuszczenie już istnieje w tabeli ProtokolNagl';
END
GO

-- Dodanie pola PNAGL_KlientNazwisko
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[ProtokolNagl]') AND name = 'PNAGL_KlientNazwisko')
BEGIN
    ALTER TABLE [dbo].[ProtokolNagl]
    ADD PNAGL_KlientNazwisko NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL;
    PRINT 'Dodano pole PNAGL_KlientNazwisko do tabeli ProtokolNagl';
END
ELSE
BEGIN
    PRINT 'Pole PNAGL_KlientNazwisko już istnieje w tabeli ProtokolNagl';
END
GO

-- Dodanie pola PNAGL_KlientDzial
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[ProtokolNagl]') AND name = 'PNAGL_KlientDzial')
BEGIN
    ALTER TABLE [dbo].[ProtokolNagl]
    ADD PNAGL_KlientDzial NVARCHAR(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL;
    PRINT 'Dodano pole PNAGL_KlientDzial do tabeli ProtokolNagl';
END
ELSE
BEGIN
    PRINT 'Pole PNAGL_KlientDzial już istnieje w tabeli ProtokolNagl';
END
GO

-- Dodanie pola PNAGL_KlientDataZatw
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[dbo].[ProtokolNagl]') AND name = 'PNAGL_KlientDataZatw')
BEGIN
    ALTER TABLE [dbo].[ProtokolNagl]
    ADD PNAGL_KlientDataZatw DATETIME2 NULL;
    PRINT 'Dodano pole PNAGL_KlientDataZatw do tabeli ProtokolNagl';
END
ELSE
BEGIN
    PRINT 'Pole PNAGL_KlientDataZatw już istnieje w tabeli ProtokolNagl';
END
GO

PRINT 'Migracja 003_add_protokol_fields zakończona pomyślnie';
GO
