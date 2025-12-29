' =====================================================================
' FUNCIONES DE PROCESAMIENTO AUTOMÁTICO
' =====================================================================

Sub ProcesarNmonAutomatico()
    ' Procesa todos los archivos .nmon en C:\nmon-Vios automáticamente
    
    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets("Analyser")
    
    ' Limpiar celda C2 para forzar búsqueda automática
    ws.Range("C2").ClearContents
    
    ' Ejecutar Main con búsqueda automática
    Call Main(1)
    
    MsgBox "Procesamiento automático completado." & vbCrLf & _
           "Archivos guardados en: C:\nmons_analizados\", vbInformation
End Sub

Sub VerificarCarpetas()
    ' Verifica si existen las carpetas necesarias
    
    Dim fso As Object
    Dim msg As String
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    msg = "=== VERIFICACIÓN DE CARPETAS ===" & vbCrLf & vbCrLf
    
    ' Carpeta fuente
    If fso.FolderExists("C:\nmon-Vios\") Then
        msg = msg & "✅ Carpeta NMON: C:\nmon-Vios\" & vbCrLf
        msg = msg & "   (Archivos .nmon para procesar)" & vbCrLf & vbCrLf
    Else
        msg = msg & "❌ Carpeta NMON NO EXISTE: C:\nmon-Vios\" & vbCrLf
        msg = msg & "   Crear esta carpeta y colocar archivos .nmon" & vbCrLf & vbCrLf
    End If
    
    ' Carpeta destino
    If fso.FolderExists("C:\nmons_analizados\") Then
        msg = msg & "✅ Carpeta DESTINO: C:\nmons_analizados\" & vbCrLf
        msg = msg & "   (Aquí se guardarán los resultados)" & vbCrLf
    Else
        msg = msg & "⚠ Carpeta DESTINO NO EXISTE: C:\nmons_analizados\" & vbCrLf
        msg = msg & "   Se creará automáticamente al procesar" & vbCrLf
    End If
    
    MsgBox msg, vbInformation, "Estado de Carpetas"
    Set fso = Nothing
End Sub

Sub AbrirCarpetaNmon()
    ' Abre la carpeta C:\nmon-Vios en el Explorador de Windows
    
    On Error Resume Next
    Shell "explorer.exe C:\nmon-Vios\", vbNormalFocus
    On Error GoTo 0
End Sub

Sub AbrirCarpetaAnalizados()
    ' Abre la carpeta C:\nmons_analizados en el Explorador de Windows
    
    On Error Resume Next
    Shell "explorer.exe C:\nmons_analizados\", vbNormalFocus
    On Error GoTo 0
End Sub

Sub LimpiarCarpetaAnalizados()
    ' Limpia todos los archivos de la carpeta de analizados
    
    Dim fso As Object, carpeta As Object, archivo As Object
    Dim respuesta As VbMsgBoxResult
    Dim contador As Integer
    
    respuesta = MsgBox("¿Eliminar TODOS los archivos en C:\nmons_analizados\?" & _
                      vbCrLf & vbCrLf & _
                      "Esta acción NO se puede deshacer.", _
                      vbYesNo + vbCritical, "Confirmar Limpieza")
    
    If respuesta = vbYes Then
        Set fso = CreateObject("Scripting.FileSystemObject")
        
        If fso.FolderExists("C:\nmons_analizados\") Then
            Set carpeta = fso.GetFolder("C:\nmons_analizados\")
            contador = 0
            
            For Each archivo In carpeta.Files
                archivo.Delete
                contador = contador + 1
            Next archivo
            
            MsgBox "Se eliminaron " & contador & " archivos." & vbCrLf & _
                   "Carpeta: C:\nmons_analizados\", vbInformation
        Else
            MsgBox "La carpeta C:\nmons_analizados\ no existe.", vbExclamation
        End If
    End If
End Sub