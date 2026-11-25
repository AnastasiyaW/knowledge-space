---
title: "Base de données Android Room"
category: concepts
tags: [ios-mobile, android, room, database, persistence, dao, entity, livedata]
level: 2
source_sha256: 5346df0cde2c16e5a73e12946579f8481a3fb564bfd3f23f78e7e74c9e98d96a
translation: machine
translated_at: '2026-10-24'
---
# Base de données Android Room {#android-room-database}

Room est la couche d'abstraction SQLite d'Android qui fournit la vérification SQL à la compilation, l'intégration avec LiveData et la prise en charge des coroutines. Il mappe des data classes Kotlin vers des tables de base de données à l'aide d'annotations.

## Points clés {#key-facts}

- Room comporte trois composants principaux : Entity (table), DAO (requêtes), Database (conteneur)
- `@Entity` annote les data classes pour définir les tables de base de données
- L'interface `@Dao` définit les opérations CRUD avec des annotations SQL
- Renvoyer `LiveData<T>` depuis les requêtes DAO met automatiquement à jour les observateurs lorsque les données changent
- La classe Database est un singleton utilisant `companion object` + `synchronized` + `@Volatile`
- `fallbackToDestructiveMigration()` recrée la base lors d'un changement de schéma (perte de données)
- Le processeur d'annotations `kapt` génère le code d'implémentation de Room à la compilation

## Modèles {#patterns}

### Entity (modèle de table) {#entity-table-model}

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

Renvoyer `LiveData<T>` depuis les requêtes : Room exécute automatiquement la requête sur un thread d'arrière-plan et met à jour les observateurs lorsque les données changent.

### Classe Database (singleton) {#database-class-singleton}

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

### Utiliser Room depuis un ViewModel {#using-room-from-viewmodel}

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

### Comparaison Room vs SwiftData/Core Data {#room-vs-swiftdatacore-data-comparison}

| Fonctionnalité | Room (Android) | SwiftData (iOS 17+) | Core Data (iOS) |
|---------|---------------|---------------------|-----------------|
| Modèle | data class `@Entity` | classe `@Model` | NSManagedObject |
| Requêtes | interface `@Dao` + SQL | wrapper de propriété `@Query` | `@FetchRequest` |
| Réactivité | `LiveData<T>` | Mise à jour automatique de la vue | `FetchedResults<T>` |
| Configuration | Singleton + Builder | `.modelContainer()` | `NSPersistentContainer` |

### Dépendances build.gradle {#buildgradle-dependencies}

```groovy
implementation "androidx.room:room-runtime:2.5.0"
kapt "androidx.room:room-compiler:2.5.0"
implementation "androidx.room:room-ktx:2.5.0"   // coroutine support
```

## Pièges à éviter {#gotchas}

- `fallbackToDestructiveMigration()` supprime TOUTES les données lors d'un changement de version de schéma : utilisez `addMigrations()` avec des instructions SQL ALTER TABLE en production
- Les opérations DAO (hors requêtes LiveData) doivent s'exécuter sur des threads d'arrière-plan : utilisez `Dispatchers.IO`
- `@Volatile` sur INSTANCE est essentiel : sans lui, différents threads peuvent voir des valeurs en cache obsolètes
- `synchronized(this)` empêche les conditions de concurrence lorsque plusieurs threads tentent de créer la base de données simultanément
- Room valide les requêtes SQL à la compilation : les erreurs de syntaxe provoquent des échecs de build, et non des plantages à l'exécution
- `exportSchema = false` supprime l'avertissement d'export du schéma : passez-le à `true` et fournissez un répertoire d'export pour la prise en charge des migrations

## Voir aussi {#see-also}

- [[android-mvvm-architecture]] - ViewModel + LiveData consommant les données Room
- [[kotlin-android-fundamentals]] - bases de Kotlin, data class, companion object
- [[android-retrofit-networking]] - récupération de données distantes à stocker dans Room
