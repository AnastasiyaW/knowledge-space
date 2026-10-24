---
title: "Android-Room-Datenbank"
category: concepts
tags: [ios-mobile, android, room, database, persistence, dao, entity, livedata]
level: 2
source_sha256: 5346df0cde2c16e5a73e12946579f8481a3fb564bfd3f23f78e7e74c9e98d96a
translation: machine
translated_at: '2026-10-24'
---
# Android-Room-Datenbank {#android-room-database}

Room ist die SQLite-Abstraktionsschicht für Android, die Prüfung von SQL zur Kompilierzeit, LiveData-Integration und Coroutine-Unterstützung bietet. Sie bildet Kotlin-Data-Classes mithilfe von Annotationen auf Datenbanktabellen ab.

## Wichtige Fakten {#key-facts}

- Room besteht aus drei Kernkomponenten: Entity (Tabelle), DAO (Abfragen) und Database (Container)
- `@Entity` annotiert Data-Classes, um Datenbanktabellen zu definieren
- Ein `@Dao`-Interface definiert CRUD-Operationen mit SQL-Annotationen
- Die Rückgabe von `LiveData<T>` aus DAO-Abfragen aktualisiert Observer automatisch, wenn sich die Daten ändern
- Die Database-Klasse ist ein Singleton, das `companion object` + `synchronized` + `@Volatile` verwendet
- `fallbackToDestructiveMigration()` erstellt die DB bei einer Schemaänderung neu (Daten gehen verloren)
- Der Annotation-Prozessor `kapt` generiert den Room-Implementierungscode zur Kompilierzeit

## Muster {#patterns}

### Entity (Tabellenmodell) {#entity-table-model}

```kotlin
import androidx.room.*

@Entity(tableName = "recording_table")
data class RecordingItem(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0L,
    @ColumnInfo(name = "name")
    var name: String = "",
    @ColumnInfo(name = "filePath")
    var filePath: String = "",
    @ColumnInfo(name = "length")
    var length: Long = 0L,
    @ColumnInfo(name = "time")
    var time: Long = 0L
)
```

### DAO (Data Access Object) {#dao-data-access-object}

```kotlin
import androidx.lifecycle.LiveData
import androidx.room.*

@Dao
interface RecordDatabaseDao {
    @Insert
    fun insert(record: RecordingItem)

    @Update
    fun update(record: RecordingItem)

    @Query("SELECT * FROM recording_table WHERE id = :key")
    fun getRecord(key: Long?): RecordingItem?

    @Query("DELETE FROM recording_table WHERE id = :key")
    fun removeRecord(key: Long?)

    @Query("DELETE FROM recording_table")
    fun clearAll()

    @Query("SELECT * FROM recording_table ORDER BY id DESC")
    fun getAllRecords(): LiveData<MutableList<RecordingItem>>

    @Query("SELECT COUNT(*) FROM recording_table")
    fun getCount(): LiveData<Int>
}
```

Die Rückgabe von `LiveData<T>` aus Abfragen – Room führt die Abfrage automatisch in einem Hintergrund-Thread aus und aktualisiert Observer, wenn sich die Daten ändern.

### Database-Klasse (Singleton) {#database-class-singleton}

```kotlin
import androidx.room.*

@Database(
    entities = [RecordingItem::class],
    version = 1,
    exportSchema = false
)
abstract class RecordDatabase : RoomDatabase() {
    abstract val recordDatabaseDao: RecordDatabaseDao

    companion object {
        @Volatile
        private var INSTANCE: RecordDatabase? = null

        fun getInstance(context: Context): RecordDatabase {
            synchronized(this) {
                var instance = INSTANCE
                if (instance == null) {
                    instance = Room.databaseBuilder(
                        context.applicationContext,
                        RecordDatabase::class.java,
                        "record_app_database"
                    )
                    .fallbackToDestructiveMigration()
                    .build()
                    INSTANCE = instance
                }
                return instance
            }
        }
    }
}
```

### Room aus dem ViewModel verwenden {#using-room-from-viewmodel}

```kotlin
class RecordViewModel(app: Application) : AndroidViewModel(app) {
    private val database = RecordDatabase.getInstance(app).recordDatabaseDao
    val allRecords = database.getAllRecords()

    fun insertRecord(item: RecordingItem) {
        viewModelScope.launch {
            withContext(Dispatchers.IO) {
                database.insert(item)
            }
        }
    }

    fun deleteRecord(key: Long) {
        viewModelScope.launch {
            withContext(Dispatchers.IO) {
                database.removeRecord(key)
            }
        }
    }
}
```

### Vergleich: Room vs. SwiftData/Core Data {#room-vs-swiftdatacore-data-comparison}

| Merkmal | Room (Android) | SwiftData (iOS 17+) | Core Data (iOS) |
|---------|---------------|---------------------|-----------------|
| Modell | `@Entity`-Data-Class | `@Model`-Klasse | NSManagedObject |
| Abfragen | `@Dao`-Interface + SQL | `@Query`-Property-Wrapper | `@FetchRequest` |
| Reaktiv | `LiveData<T>` | Automatische Aktualisierung der View | `FetchedResults<T>` |
| Einrichtung | Singleton + Builder | `.modelContainer()` | `NSPersistentContainer` |

### build.gradle-Abhängigkeiten {#buildgradle-dependencies}

```groovy
implementation "androidx.room:room-runtime:2.5.0"
kapt "androidx.room:room-compiler:2.5.0"
implementation "androidx.room:room-ktx:2.5.0"   // coroutine support
```

## Fallstricke {#gotchas}

- `fallbackToDestructiveMigration()` löscht ALLE Daten bei einem Wechsel der Schemaversion – für Produktivbetrieb `addMigrations()` mit SQL-ALTER-TABLE-Anweisungen verwenden
- DAO-Operationen (außer LiveData-Abfragen) müssen in Hintergrund-Threads ausgeführt werden – `Dispatchers.IO` verwenden
- `@Volatile` auf INSTANCE ist entscheidend – ohne es können verschiedene Threads veraltete zwischengespeicherte Werte sehen
- `synchronized(this)` verhindert Race Conditions, wenn mehrere Threads gleichzeitig versuchen, die Datenbank zu erstellen
- Room validiert SQL-Abfragen zur Kompilierzeit – Syntaxfehler führen zu Build-Fehlern, nicht zu Laufzeitabstürzen
- `exportSchema = false` unterdrückt die Warnung zum Schema-Export – auf `true` setzen und ein Exportverzeichnis angeben, um Migrationsunterstützung zu erhalten

## Siehe auch {#see-also}

- [[android-mvvm-architecture]] - ViewModel + LiveData, die Room-Daten konsumieren
- [[kotlin-android-fundamentals]] - Kotlin-Grundlagen, Data-Class, companion object
- [[android-retrofit-networking]] - Abruf von Remote-Daten zur Speicherung in Room
