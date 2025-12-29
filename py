#Else
    ' --- MODIFICACIÓN: GUARDAR EN C:\nmons_analizados\ ---
    Dim nombreArchivo As String
    Dim carpetaDestino As String
    Dim fsoDest As Object
    Dim rutaDestino As String
    
    ' Extraer solo el nombre del archivo
    nombreArchivo = Mid(FileName, InStrRev(FileName, "\") + 1)
    
    ' Determinar carpeta destino
    If OutDir <> "" Then
        carpetaDestino = OutDir
    Else
        carpetaDestino = "C:\nmons_analizados\"
    End If
    
    ' Asegurar que termine con \
    If Right(carpetaDestino, 1) <> "\" Then
        carpetaDestino = carpetaDestino & "\"
    End If
    
    ' Crear carpeta si no existe
    Set fsoDest = CreateObject("Scripting.FileSystemObject")
    If Not fsoDest.FolderExists(carpetaDestino) Then
        fsoDest.CreateFolder carpetaDestino
    End If
    
    ' Construir ruta completa de destino
    rutaDestino = carpetaDestino & Left(nombreArchivo, InStrRev(nombreArchivo, ".")) & "nmon" & fileExtension
    
    ' Si el archivo ya existe, agregar timestamp
    If fsoDest.FileExists(rutaDestino) Then
        Output_Filename = carpetaDestino & Left(nombreArchivo, InStrRev(nombreArchivo, ".")) & _
                        "nmon_" & Format(Now, "yyyymmdd_hhmmss") & fileExtension
    Else
        Output_Filename = rutaDestino
    End If
    
    Set fsoDest = Nothing
    ' --- FIN MODIFICACIÓN ---
#End If