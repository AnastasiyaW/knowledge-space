---
title: "Android-Datenspeicherung – SharedPreferences, SQLite, Room"
category: concepts
tags: [java-spring, android, room, sqlite, shared-preferences, database, content-provider]
level: 3
source_sha256: a552304abdaf44056125f0db2a2ce2cc6f64541eda6984a7f029827b27f81afe
translation: machine
translated_at: '2026-10-24'
---
# Android-Datenspeicherung – SharedPreferences, SQLite, Room {#android-data-storage-sharedpreferences-sqlite-room}

Lokale Datenpersistenz unter Android: SharedPreferences für Einstellungen, reines SQLite, Room ORM (empfohlen), Content Provider für den anwendungsübergreifenden Datenaustausch sowie Laufzeitberechtigungen.

## Key Facts {#key-facts}

- SharedPreferences: Schlüssel-Wert-Paare für kleine primitive Daten (Einstellungen, Flags)
- Room = JetPack-Abstraktion über SQLite mit SQL-Prüfung zur Kompilierzeit
- Room-Komponenten: `@Entity` (Tabelle), `@Dao` (Datenzugriff), `@Database` (abstrakte Klasse)
- Room unterstützt die Rückgabetypen `LiveData<List<T>>` und `Flow<List<T>>` für reaktive Aktualisierungen
- Die Room-Datenbankinstanz sollte ein Singleton sein (Muster mit Double-Checked Locking)
- Content Provider stellen Daten anderen Apps zur Verfügung (Contacts, MediaStore)
- Laufzeitberechtigungen sind für den Zugriff auf sensible Daten erforderlich (Android 6+)

## Patterns {#patterns}

### SharedPreferences {#sharedpreferences}
```java
SharedPreferences prefs = getSharedPreferences("app_prefs", MODE_PRIVATE);
prefs.edit().putString("username", "Alice").putBoolean("dark_mode", true).apply();
String user = prefs.getString("username", "default");
boolean dark = prefs.getBoolean("dark_mode", false);
```

### Room Entity {#room-entity}
```java
@Entity(tableName = "users")
public class User {
    @PrimaryKey(autoGenerate = true) public int id;
    @ColumnInfo(name = "user_name") public String name;
    public String email;
    @Ignore public String tempField;  // not stored
}
```

### Room DAO {#room-dao}
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

### Room Database (Singleton) {#room-database-singleton}
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

### Room Relationships {#room-relationships}
```java
public class UserWithOrders {
    @Embedded public User user;
    @Relation(parentColumn = "id", entityColumn = "user_id")
    public List<Order> orders;
}
```

### Room Migration {#room-migration}
```java
static final Migration MIGRATION_1_2 = new Migration(1, 2) {
    @Override
    public void migrate(SupportSQLiteDatabase db) {
        db.execSQL("ALTER TABLE users ADD COLUMN phone TEXT");
    }
};
Room.databaseBuilder(...).addMigrations(MIGRATION_1_2).build();
```

### Runtime Permissions {#runtime-permissions}
```java
if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS)
        != PackageManager.PERMISSION_GRANTED) {
    ActivityCompat.requestPermissions(this,
        new String[]{Manifest.permission.READ_CONTACTS}, REQUEST_CODE);
}
```

## Gotchas {#gotchas}

- Room-Datenbankoperationen dürfen NICHT auf dem Main-Thread ausgeführt werden (Coroutines, RxJava oder `allowMainThreadQueries()` nur für Tests verwenden)
- SharedPreferences: `apply()` ist asynchron (bevorzugt), `commit()` ist synchron
- Room `@PrimaryKey(autoGenerate = true)` beginnt bei 1 und zählt automatisch hoch
- Ein fehlgeschlagene Migration führt zu einem Absturz – immer Migrationspfade bereitstellen oder `fallbackToDestructiveMigration()` verwenden
- Content-Provider-Abfragen liefern einen `Cursor`, der geschlossen werden muss, um Speicherlecks zu vermeiden

## See Also {#see-also}

- [[android-architecture-mvvm]] - Repository-Muster mit Room
- [[android-networking-retrofit]] - Remote- und lokales Caching
- [[spring-data-jpa-hibernate]] - Ähnliche ORM-Muster in Spring
