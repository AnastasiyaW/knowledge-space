---
title: Android Room Database
category: concepts
tags: [ios-mobile, android, room, database, persistence, dao, entity, livedata]
---

# Android Room Database

Room is Android's SQLite abstraction layer that provides compile-time SQL verification, LiveData integration, and coroutine support. It maps Kotlin data classes to database tables with annotations.

## Key Facts

- Room has three core components: Entity (table), DAO (queries), Database (holder)
- `@Entity` annotates data classes to define database tables
- `@Dao` interface defines CRUD operations with SQL annotations
- Returning `LiveData<T>` from DAO queries auto-updates observers when data changes
- Database class is a singleton using `companion object` + `synchronized` + `@Volatile`
- `fallbackToDestructiveMigration()` recreates DB on schema change (loses data)
- `kapt` annotation processor generates Room implementation code at compile time

## Patterns

### Entity (Table Model)

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

### DAO (Data Access Object)

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

Returning `LiveData<T>` from queries - Room automatically runs the query on a background thread and updates observers when data changes.

### Database Class (Singleton)

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

### Using Room from ViewModel

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

### Room vs SwiftData/Core Data Comparison

| Feature | Room (Android) | SwiftData (iOS 17+) | Core Data (iOS) |
|---------|---------------|---------------------|-----------------|
| Model | `@Entity` data class | `@Model` class | NSManagedObject |
| Queries | `@Dao` interface + SQL | `@Query` property wrapper | `@FetchRequest` |
| Reactive | `LiveData<T>` | Auto-updates view | `FetchedResults<T>` |
| Setup | Singleton + Builder | `.modelContainer()` | `NSPersistentContainer` |

### build.gradle Dependencies

```groovy
implementation "androidx.room:room-runtime:2.5.0"
kapt "androidx.room:room-compiler:2.5.0"
implementation "androidx.room:room-ktx:2.5.0"   // coroutine support
```

## Gotchas

- `fallbackToDestructiveMigration()` deletes ALL data on schema version change - use `addMigrations()` with SQL ALTER TABLE for production
- DAO operations (except LiveData queries) must run on background threads - use `Dispatchers.IO`
- `@Volatile` on INSTANCE is critical - without it, different threads may see stale cached values
- `synchronized(this)` prevents race conditions when multiple threads try to create the database simultaneously
- Room validates SQL queries at compile time - syntax errors cause build failures, not runtime crashes
- `exportSchema = false` suppresses the schema export warning - set to `true` and provide export directory for migration support

## See Also

- [[android-mvvm-architecture]] - ViewModel + LiveData consuming Room data
- [[kotlin-android-fundamentals]] - Kotlin basics, data class, companion object
- [[android-retrofit-networking]] - fetching remote data to store in Room
