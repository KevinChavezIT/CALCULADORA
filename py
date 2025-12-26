#Else  ' Windows
    ' --- PARA AUTOMATIZACIÓN SIN USAR CELDAS ---
    ' Si estamos en modo batch, usamos la variable global FilePath
    If BatchModeFilePath <> "" Then
        FileList = Array(BatchModeFilePath)
        Numfiles = 1
    Else
        ' Modo normal: usar FileList o diálogo
        FileName = Trim(FileName)
        ' ... resto del código original ...
    End If
    ' --- FIN DEL CAMBIO ---
#End If