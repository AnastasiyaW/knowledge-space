---
title: Android Room Database
category: concepts
tags: [android, room, sqlite, database, dao, entity, migration, relationships]
---
# Android Room Database

## Key Facts

- Room is an abstraction layer over SQLite - compile-time SQL verification, less boilerplate
- Three core components: **Entity** (table), **DAO** (data access object), **Database** (holder)
- `@Entity` marks a data class as a database table; `@PrimaryKey(autoGenerate = true)` for auto-increment ID
- `@Dao` interface defines database operations with `@Query`, `@Insert`, `@Update`, `@Delete` annotations
- `@Database` abstract class extends `RoomDatabase` - lists entities and provides DAOs
- Room works with Kotlin coroutines (`suspend` functions) and Flow (`Flow<List<T>>`) for reactive data
- Database migrations handle schema changes between versions; `Migration(fromVersion, toVersion)`
- `@Embedded` for nested objects; `@Relation` for one-to-many and many-to-many relationships
- Room forbids database operations on the main thread - use coroutines, RxJava, or background threads
- See [[android-architecture]] for how Room fits in the data layer
- See [[kotlin-fundamentals]] for coroutines used with Room

## Patterns

### Entity definition

```kotlin
@Entity(tableName = "characters")
data class CharacterEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,

    @ColumnInfo(name = "name")
    val name: String,

    @ColumnInfo(name = "house")
    val hogwartsHouse: String,

    @ColumnInfo(name = "image_url")
    val imageUrl: String?,

    @ColumnInfo(name = "is_favorite")
    val isFavorite: Boolean = false
)

@Entity(tableName = "wands")
data class WandEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,

    @ColumnInfo(name = "character_id")
    val characterId: Long,

    val wood: String,
    val core: String,

    @ColumnInfo(name = "length_inches")
    val lengthInches: Double
)
```

### DAO interface

```kotlin
@Dao
interface CharacterDao {

    @Query("SELECT * FROM characters ORDER BY name ASC")
    fun getAll(): Flow<List<CharacterEntity>>  // reactive stream

    @Query("SELECT * FROM characters WHERE id = :id")
    suspend fun getById(id: Long): CharacterEntity?

    @Query("SELECT * FROM characters WHERE house = :house")
    fun getByHouse(house: String): Flow<List<CharacterEntity>>

    @Query("SELECT * FROM characters WHERE name LIKE '%' || :query || '%'")
    fun search(query: String): Flow<List<CharacterEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(character: CharacterEntity): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(characters: List<CharacterEntity>)

    @Update
    suspend fun update(character: CharacterEntity)

    @Delete
    suspend fun delete(character: CharacterEntity)

    @Query("DELETE FROM characters")
    suspend fun deleteAll()

    @Query("UPDATE characters SET is_favorite = :fav WHERE id = :id")
    suspend fun setFavorite(id: Long, fav: Boolean)
}
```

### Database class

```kotlin
@Database(
    entities = [CharacterEntity::class, WandEntity::class],
    version = 2,
    exportSchema = true
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun characterDao(): CharacterDao
    abstract fun wandDao(): WandDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                )
                .addMigrations(MIGRATION_1_2)
                .build()
                .also { INSTANCE = it }
            }
        }
    }
}
```

### Migrations

```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL(
            "ALTER TABLE characters ADD COLUMN is_favorite INTEGER NOT NULL DEFAULT 0"
        )
    }
}

val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("""
            CREATE TABLE wands (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                character_id INTEGER NOT NULL,
                wood TEXT NOT NULL,
                core TEXT NOT NULL,
                length_inches REAL NOT NULL,
                FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
            )
        """)
    }
}
```

### Relationships

```kotlin
// One-to-many: Character has many Wands
data class CharacterWithWands(
    @Embedded
    val character: CharacterEntity,

    @Relation(
        parentColumn = "id",
        entityColumn = "character_id"
    )
    val wands: List<WandEntity>
)

// In DAO
@Transaction
@Query("SELECT * FROM characters WHERE id = :id")
suspend fun getCharacterWithWands(id: Long): CharacterWithWands

@Transaction
@Query("SELECT * FROM characters")
fun getAllWithWands(): Flow<List<CharacterWithWands>>
```

### Repository with Room + Network

```kotlin
class CharacterRepository(
    private val dao: CharacterDao,
    private val api: HarryPotterApi,
    private val mapper: CharacterMapper
) {
    // Room Flow = automatic UI updates when DB changes
    val allCharacters: Flow<List<Character>> =
        dao.getAll().map { entities ->
            entities.map { mapper.toDomain(it) }
        }

    suspend fun refreshFromNetwork() {
        try {
            val remote = api.getCharacters()
            val entities = remote.map { mapper.toEntity(it) }
            dao.insertAll(entities)
        } catch (e: Exception) {
            // Silently use cached data
        }
    }

    suspend fun toggleFavorite(id: Long, currentFav: Boolean) {
        dao.setFavorite(id, !currentFav)
    }
}
```

### Using in ViewModel

```kotlin
class CharacterListViewModel(
    private val repository: CharacterRepository
) : ViewModel() {

    // Combine database flow with search/filter flow
    private val searchQuery = MutableStateFlow("")
    private val showFavoritesOnly = MutableStateFlow(false)

    val characters: StateFlow<List<Character>> = combine(
        repository.allCharacters,
        searchQuery,
        showFavoritesOnly
    ) { chars, query, favsOnly ->
        chars.filter { c ->
            (query.isEmpty() || c.name.contains(query, ignoreCase = true)) &&
            (!favsOnly || c.isFavorite)
        }
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    init {
        viewModelScope.launch {
            repository.refreshFromNetwork()
        }
    }
}
```

## Gotchas

- **Symptom**: `IllegalStateException: Cannot access database on the main thread` -> **Cause**: Room queries called on UI thread -> **Fix**: Use `suspend` functions with coroutines, or `allowMainThreadQueries()` (dev only!)
- **Symptom**: Data missing after app update -> **Cause**: Schema changed but no Migration provided -> **Fix**: Add `Migration` objects for every schema change; or use `.fallbackToDestructiveMigration()` (dev only - destroys data!)
- **Symptom**: `@Relation` query returns empty list -> **Cause**: Missing `@Transaction` annotation on DAO method -> **Fix**: Always annotate relationship queries with `@Transaction`
- **Symptom**: `autoGenerate = true` doesn't work -> **Cause**: Passing non-zero ID value to insert -> **Fix**: Pass `0` or `0L` as ID for auto-generation; Room treats 0 as "unset"
- **Symptom**: Schema validation fails on build -> **Cause**: Entity class doesn't match existing database schema -> **Fix**: Create proper migration, or increment database version and add migration path

## See Also

- [[android-architecture]] - Room in the data layer of Clean Architecture
- [[android-layouts]] - UI that displays Room data
- [[kotlin-fundamentals]] - Coroutines and Flow used with Room
- [[spring-data-jpa]] - Similar ORM concept in Spring ecosystem
- Android Docs: [Room](https://developer.android.com/training/data-storage/room)
- Android Docs: [Room Migrations](https://developer.android.com/training/data-storage/room/migrating-db-versions)
