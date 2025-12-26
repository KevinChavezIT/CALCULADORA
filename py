EndLoop:
    ' === RESETEAR VARIABLE PARA SIGUIENTE ARCHIVO ===
    If Batch = 1 Then
        BatchModeFilePath = ""
    End If
    ' === FIN RESETEO ===
    
    'delete the sortfile if needed