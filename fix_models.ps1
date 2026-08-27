Get-ChildItem -Path "app\src\main\java\com\kush\cachedeal\core\model" -Filter "*.kt" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Remove room imports
    $content = $content -replace 'import androidx\.room\..*?
', ''
    
    # Add serializable import if missing
    if ($content -notmatch 'import kotlinx.serialization.Serializable') {
        $content = $content -replace 'package com.kush.cachedeal.core.model\s*', "package com.kush.cachedeal.core.model

import kotlinx.serialization.Serializable
import kotlinx.serialization.SerialName
"
    }
    
    # Replace @Entity with @Serializable
    $content = $content -replace '@Entity\(tableName = "[^"]+"\)', '@Serializable'
    $content = $content -replace '@Entity', '@Serializable'
    
    # Remove @PrimaryKey
    $content = $content -replace '@PrimaryKey', ''
    
    # Convert @ColumnInfo(name="xyz") to @SerialName("xyz")
    $content = $content -replace '@ColumnInfo\(name = "([^"]+)"\)', '@SerialName("$1")'
    
    Set-Content -Path $_.FullName $content -Encoding UTF8
}
