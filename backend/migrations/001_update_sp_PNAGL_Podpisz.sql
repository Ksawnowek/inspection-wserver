-- Migration: Aktualizacja procedury składowanej sp_PNAGL_Podpisz
-- Dodano parametry: @user_id (ID użytkownika) i @user_name (pełne imię i nazwisko)
-- Data: 2025-12-24

-- Usuń starą procedurę jeśli istnieje
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_PNAGL_Podpisz]') AND type in (N'P', N'PC'))
DROP PROCEDURE [dbo].[sp_PNAGL_Podpisz]
GO

-- Utwórz nową procedurę z dodatkowymi parametrami
CREATE PROCEDURE [dbo].[sp_PNAGL_Podpisz]
    @pnagl_id INT,
    @podpis NVARCHAR(MAX),
    @akcept NVARCHAR(50),
    @user_id INT = NULL,
    @user_name NVARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE dbo.ProtokolNagl
    SET
        PNAGL_PodpisKlienta = @podpis,
        PNAGL_Zaakceptowal = @akcept,
        PNAGL_CzyZaakceptowany = 1,
        PNAGL_DataAkceptacji = GETDATE(),
        -- Dodane nowe pola
        PNAGL_UZT_Id_Ostatni = @user_id,
        PNAGL_UzytkownikPodpisujacy = @user_name,
        PNAGL_UZTOstatni = @user_name,
        PNAGL_TS = GETDATE()
    WHERE PNAGL_Id = @pnagl_id;
END
GO

-- Sprawdź czy procedura została utworzona
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[sp_PNAGL_Podpisz]') AND type in (N'P', N'PC'))
PRINT 'Procedura sp_PNAGL_Podpisz została pomyślnie zaktualizowana'
ELSE
PRINT 'BŁĄD: Nie udało się utworzyć procedury sp_PNAGL_Podpisz'
GO
