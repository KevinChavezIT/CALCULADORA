Sub ProcesarTodosLosNmon()
    Dim fso As Object
    Dim carpetaBase As String
    Dim archivo As Object
    Dim archivosProcesados As Integer
    Dim errores As String
    Dim erroresCount As Integer
    
    On Error GoTo ErrorHandler
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    carpetaBase = "C:\nmon-Vios"  ' Ruta donde están todos los .nmon
    
    ' Verificar que la carpeta existe
    If Not fso.FolderExists(carpetaBase) Then
        MsgBox "La carpeta no existe: " & carpetaBase, vbCritical
        Exit Sub
    End If
    
    archivosProcesados = 0
    erroresCount = 0
    errores = "Errores encontrados:" & vbNewLine
    
    ' Desactivar actualización de pantalla para mayor velocidad
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    Application.EnableEvents = False
    
    ' Recorre solo los archivos en la carpeta base
    For Each archivo In fso.GetFolder(carpetaBase).Files
        If LCase(fso.GetExtensionName(archivo.Name)) = "nmon" Then
            
            ' Mostrar progreso en barra de estado
            Application.StatusBar = "Procesando (" & archivosProcesados + 1 & "): " & archivo.Name
            
            ' Pasar la ruta directamente a través de variable global
            BatchModeFilePath = archivo.Path
            
            ' Ejecutar el análisis en modo batch (Batch = 1)
            Call Main(1)
            
            archivosProcesados = archivosProcesados + 1
            
            ' Pequeña pausa para evitar sobrecarga
            DoEvents
        End If
    Next archivo
    
Finalizar:
    ' Restaurar configuración
    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    Application.EnableEvents = True
    Application.StatusBar = False
    
    ' Mostrar resumen
    If erroresCount > 0 Then
        MsgBox "Proceso completado con " & archivosProcesados & " archivos." & vbNewLine & _
               erroresCount & " errores." & vbNewLine & vbNewLine & errores, vbExclamation
    Else
        MsgBox "Proceso completado exitosamente." & vbNewLine & _
               "Total de archivos procesados: " & archivosProcesados, vbInformation
    End If
    Exit Sub
    
ErrorHandler:
    erroresCount = erroresCount + 1
    errores = errores & "Error en " & archivo.Name & ": " & Err.Description & vbNewLine
    Resume Next
End Sub