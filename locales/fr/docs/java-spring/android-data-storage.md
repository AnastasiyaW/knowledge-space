---
title: "Stockage de données Android - SharedPreferences, SQLite, Room"
category: concepts
tags: [java-spring, android, room, sqlite, shared-preferences, database, content-provider]
level: 3
source_sha256: a552304abdaf44056125f0db2a2ce2cc6f64541eda6984a7f029827b27f81afe
translation: machine
translated_at: '2026-10-24'
---
# Stockage de données Android - SharedPreferences, SQLite, Room {#android-data-storage-sharedpreferences-sqlite-room}

Persistance locale des données sur Android : SharedPreferences pour les paramètres, SQLite brut, ORM Room (recommandé), Content Providers pour le partage de données entre applications, et permissions à l'exécution.

## Points clés {#key-facts}

- SharedPreferences : paires clé-valeur pour de petites données primitives (paramètres, indicateurs)
- Room = abstraction JetPack au-dessus de SQLite avec vérification SQL à la compilation
- Composants de Room : `@Entity` (table), `@Dao` (accès aux données), `@Database` (classe abstraite)
- Room prend en charge les types de retour `LiveData<List<T>>` et `Flow<List<T>>` pour les mises à jour réactives
- L'instance de base de données Room doit être un singleton (motif du double-checked locking)
- Les Content Providers exposent des données aux autres applications (Contacts, MediaStore)
- Les permissions à l'exécution sont requises pour accéder aux données sensibles (Android 6+)

## Motifs {#patterns}

### SharedPreferences {#sharedpreferences}
```java
SharedPreferences prefs = getSharedPreferences("app_prefs", MODE_PRIVATE);
prefs.edit().putString("username", "Alice").putBoolean("dark_mode", true).apply();
String user = prefs.getString("username", "default");
boolean dark = prefs.getBoolean("dark_mode", false);
```

### Entité Room {#room-entity}
```java
@Entity(tableName = "users")
public class User {
    @PrimaryKey(autoGenerate = true) public int id;
    @ColumnInfo(name = "user_name") public String name;
    public String email;
    @Ignore public String tempField;  // not stored
}
```

### DAO Room {#room-dao}
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

### Base de données Room (singleton) {#room-database-singleton}
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

### Relations Room {#room-relationships}
```java
public class UserWithOrders {
    @Embedded public User user;
    @Relation(parentColumn = "id", entityColumn = "user_id")
    public List<Order> orders;
}
```

### Migration Room {#room-migration}
```java
static final Migration MIGRATION_1_2 = new Migration(1, 2) {
    @Override
    public void migrate(SupportSQLiteDatabase db) {
        db.execSQL("ALTER TABLE users ADD COLUMN phone TEXT");
    }
};
Room.databaseBuilder(...).addMigrations(MIGRATION_1_2).build();
```

### Permissions à l'exécution {#runtime-permissions}
```java
if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_CONTACTS)
        != PackageManager.PERMISSION_GRANTED) {
    ActivityCompat.requestPermissions(this,
        new String[]{Manifest.permission.READ_CONTACTS}, REQUEST_CODE);
}
```

## Pièges à éviter {#gotchas}

- Les opérations sur une base Room ne doivent PAS s'exécuter sur le thread principal (utiliser les coroutines, RxJava, ou `allowMainThreadQueries()` uniquement pour les tests)
- `apply()` de SharedPreferences est asynchrone (à privilégier), `commit()` est synchrone
- `@PrimaryKey(autoGenerate = true)` de Room démarre à 1 et s'incrémente automatiquement
- Un échec de migration provoque un plantage : fournissez toujours des chemins de migration ou `fallbackToDestructiveMigration()`
- Les requêtes sur un Content Provider renvoient un `Cursor` qui doit être fermé pour éviter les fuites de mémoire

## Voir aussi {#see-also}

- [[android-architecture-mvvm]] - Patron Repository avec Room
- [[android-networking-retrofit]] - Cache distant + local
- [[spring-data-jpa-hibernate]] - Patrons ORM similaires dans Spring
