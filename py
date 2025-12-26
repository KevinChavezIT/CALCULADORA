Sub ProcesarTodosLosNmon()
    Dim fso As Object
    Dim carpetaBase As String
    Dim archivo As Object
    Dim archivosProcesados As Integer
    Dim errores As String
    Dim erroresCount As Integer
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    carpetaBase = "C:\nmon-Vios"  ' Ruta donde están todos los .nmon
    
    archivosProcesados = 0
    erroresCount = 0
    errores = "Errores encontrados:" & vbNewLine
    
    ' Desactivar actualización de pantalla para mayor velocidad
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    ' Recorre solo los archivos en la carpeta base
    For Each archivo In fso.GetFolder(carpetaBase).Files
        If LCase(fso.GetExtensionName(archivo.Name)) = "nmon" Then
            
            ' Mostrar progreso en barra de estado
            Application.StatusBar = "Procesando (" & archivosProcesados + 1 & "): " & archivo.Name
            
            ' Pasar la ruta directamente a través de variable global
            BatchModeFilePath = archivo.Path
            
            ' Ejecutar el análisis
            On Error Resume Next
            Application.Run "Main", 1  ' Modo batch = 1
            On Error GoTo 0
            
            ' Limpiar la variable
            BatchModeFilePath = ""
            
            archivosProcesados = archivosProcesados + 1
            
            ' Pequeña pausa para evitar sobrecarga
            DoEvents
        End If
    Next archivo
    
    ' Restaurar configuración
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    Application.StatusBar = False
    
    ' Mostrar resumen
    If erroresCount > 0 Then
        MsgBox "Proceso completado con " & archivosProcesados & " archivos." & vbNewLine & _
               erroresCount & " errores." & vbNewLine & vbNewLine & errores, vbExclamation
    Else
        MsgBox "Proceso completado exitosamente." & vbNewLine & _
               "Total de archivos procesados: " & archivosProcesados, vbInformation
    End If
End Sub