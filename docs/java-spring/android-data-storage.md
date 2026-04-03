---
title: Android Data Storage - SharedPreferences, SQLite, Room
category: concepts
tags: [java-spring, android, room, sqlite, shared-preferences, database, content-provider]
---

# Android Data Storage - SharedPreferences, SQLite, Room

Local data persistence on Android: SharedPreferences for settings, raw SQLite, Room ORM (recommended), Content Providers for cross-app data sharing, and runtime permissions.

## Key Facts

- SharedPreferences: key-value pairs for small primitive data (settings, flags)
- Room = JetPack abstraction over SQLite with compile-time SQL verification
- Room components: `@Entity` (table), `@Dao` (data access), `@Database` (abstract class)
- Room supports `LiveData<List<T>>` and `Flow<List<T>>` return types for reactive updates
- Room database instance should be singleton (double-checked locking pattern)
- Content Providers expose data to other apps (Contacts, MediaStore)
- Runtime permissions required for sensitive data access (Android 6+)

## Patterns

### SharedPreferences
```java
SharedPreferences prefs = getSharedPreferences("app_prefs", MODE_PRIVATE);
prefs.edit().putString("username", "Alice").putBoolean("dark_mode", true).apply();
String user = prefs.getString("username", "default");
boolean dark = prefs.getBoolean("dark_mode", false);
```

### Room Entity
```java
@Entity(tableName = "users")
public class User {
    @PrimaryKey(autoGenerate = true) public int id;
    @ColumnInfo(name = "user_name") public String name;
    public String email;
    @Ignore public String tempField;  // not stored
}
```

### Room DAO
```java
@Dao
public interface UserDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    void insert(User user);

    @Update void update(User user);
    @Delete void delete(User user);

    @Query("SELECT * FROM users ORDER BY user_name ASC")
    List<User> getAllUsers();

    @Query("SELECT * FROM users WHERE email = :email LIMIT 1")
    User findByEmail(String email);

    @Query("SELECT * FROM users")
    LiveData<List<User>> getAllUsersLive();  // reactive

    @Query("SELECT * FROM users")
    Flow<List<User>> getAllUsersFlow();      // Kotlin Flow
}
```

### Room Database (Singleton)
```java
@Database(entities = {User.class}, version = 1)
public abstract class AppDatabase extends RoomDatabase {
    public abstract UserDao userDao();
    private static volatile AppDatabase INSTANCE;

    public static AppDatabase getInstance(Context context) {
        if (INSTANCE == null) {
            synchronized (AppDatabase.class) {
                if (INSTANCE == null) {
                    INSTANCE = Room.databaseBuilder(context.getApplicationContext(),
                        AppDatabase.class, "app_database").build();
                }
            }
        }
        return INSTANCE;
    }
}
```

### Room Relationships
```java
public class UserWithOrders {
    @Embedded public User user;
    @Relation(parentColumn = "id", entityColumn = "user_id")
    public List<Order> orders;
}
```

### Room Migration
```java
static final Migration MIGRATION_1_2 = new Migration(1, 2) {
    @Override
    public void migrate(SupportSQLiteDatabase db) {
        db.execSQL("ALTER TABLE users ADD COLUMN phone TEXT");
    }
};
Room.databaseBuilder(...).addMigrations(MIGRATION_1_2).build();
```

### Runtime Permissions
```java
if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS)
        != PackageManager.PERMISSION_GRANTED) {
    ActivityCompat.requestPermissions(this,
        new String[]{Manifest.permission.READ_CONTACTS}, REQUEST_CODE);
}
```

## Gotchas

- Room database operations must NOT run on main thread (use coroutines, RxJava, or `allowMainThreadQueries()` for testing only)
- SharedPreferences `apply()` is async (preferred), `commit()` is synchronous
- Room `@PrimaryKey(autoGenerate = true)` starts from 1 and auto-increments
- Migration failure causes crash - always provide migration paths or `fallbackToDestructiveMigration()`
- Content Provider queries return `Cursor` that must be closed to prevent memory leaks

## See Also

- [[android-architecture-mvvm]] - Repository pattern with Room
- [[android-networking-retrofit]] - Remote + local caching
- [[spring-data-jpa-hibernate]] - Similar ORM patterns in Spring
