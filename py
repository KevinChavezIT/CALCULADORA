                                       'National language settings
Delim = Sheet1.Range("Delim").Value
DecSep = ".": ThouSep = ","
If Delim = ";" Then DecSep = ",": ThouSep = "."
'SortInp = Sheet1.Range("SortInp").Value Like "YES"
'================= Build filelist ====================================
Numfiles = 0
Set MyCells = Worksheets(1).Range("FileList").Offset(0, -1)

Dim SingleFile As Integer
FileName = Trim(FileName)

' =====================================================================
' MODIFICACIÓN: Búsqueda automática en C:\nmon-Vios
' =====================================================================
If FileName = "" Then
    ' Buscar automáticamente archivos .nmon en C:\nmon-Vios
    Dim carpetaNmon As String
    Dim fso As Object, carpeta As Object, archivo As Object
    Dim archivos() As String
    Dim contador As Integer
    
    carpetaNmon = "C:\nmon-Vios\"
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' Verificar si la carpeta existe
    If Not fso.FolderExists(carpetaNmon) Then
        MsgBox "No se encuentra la carpeta: " & carpetaNmon, vbExclamation
        Exit Sub
    End If
    
    Set carpeta = fso.GetFolder(carpetaNmon)
    
    ' Contar archivos .nmon
    contador = 0
    For Each archivo In carpeta.Files
        If UCase(fso.GetExtensionName(archivo.Name)) = "NMON" Then
            contador = contador + 1
        End If
    Next archivo
    
    If contador = 0 Then
        MsgBox "No se encontraron archivos .nmon en: " & carpetaNmon, vbExclamation
        Exit Sub
    End If
    
    ' Crear array con los archivos
    ReDim archivos(contador - 1)
    contador = 0
    
    For Each archivo In carpeta.Files
        If UCase(fso.GetExtensionName(archivo.Name)) = "NMON" Then
            archivos(contador) = archivo.Path
            contador = contador + 1
        End If
    Next archivo
    
    ' Asignar a FileList
    Numfiles = contador
    ReDim FileList(Numfiles)
    
    For I = 1 To Numfiles
        FileList(I) = archivos(I - 1)
        MyCells.Offset(I, 0) = archivos(I - 1)  ' Opcional: escribir en hoja
    Next I
    
    ' Configurar OutDir automáticamente si está vacío
    If OutDir = "" Then
        OutDir = "C:\nmons_analizados\"
        ' Crear carpeta si no existe
        If Not fso.FolderExists(OutDir) Then
            fso.CreateFolder OutDir
        End If
    End If
    ' =====================================================================
    ' FIN MODIFICACIÓN
    ' =====================================================================
    
    Exit Sub  ' Salir para evitar procesamiento adicional
End If