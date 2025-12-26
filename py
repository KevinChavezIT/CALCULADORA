Sub ProcesarTodosLosNmon()
    Dim fso As Object
    Dim carpetaBase As String
    Dim archivo As Object
    Dim ws As Worksheet
    Dim rutaArchivo As String
    Dim archivosProcesados As Integer

    Set fso = CreateObject("Scripting.FileSystemObject")
    carpetaBase = "C:\nmon-Vios"  ' Ruta donde están todos los .nmon
    
    Set ws = ThisWorkbook.Sheets("Analyser")
    archivosProcesados = 0

    ' Recorre solo los archivos en la carpeta base (sin subcarpetas)
    For Each archivo In fso.GetFolder(carpetaBase).Files
        If LCase(fso.GetExtensionName(archivo.Name)) = "nmon" Then
            rutaArchivo = archivo.Path

            ' Mostrar en la hoja qué archivo se está procesando
            ws.Range("C2").Value = rutaArchivo
            ws.Range("B2").Value = carpetaBase
            
            Application.StatusBar = "Procesando: " & archivo.Name & " (" & archivosProcesados + 1 & ")"
            DoEvents

            ' Ejecutar el análisis (Batch = 0 para procesar uno a uno)
            Application.Run "Main", 0
            archivosProcesados = archivosProcesados + 1
        End If
    Next archivo

    Application.StatusBar = False
    MsgBox "Proceso completado. Total de archivos procesados: " & archivosProcesados, vbInformation
End Sub