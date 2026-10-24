---
title: "Fondamentaux Android - Structure du projet et layouts XML"
category: concepts
tags: [java-spring, android, xml-layouts, views, ui, android-studio]
level: 2
source_sha256: b4723c798ed42ad55e21d986e390691355906c4c4ec204db8bbca6d6bf1a70b8
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux Android - Structure du projet et layouts XML {#android-fundamentals-project-structure-and-xml-layouts}

Structure des projets Android, système de layouts XML, hiérarchie des View, widgets courants et ViewGroups (LinearLayout, RelativeLayout, ConstraintLayout).

## Points clés {#key-facts}

- `app/src/main/java/` - code source ; `res/layout/` - layouts XML ; `res/values/` - chaînes, couleurs, styles
- `AndroidManifest.xml` déclare les activités, les permissions et la configuration de l'application
- Tous les éléments d'interface sont des sous-classes de `View` ; les conteneurs sont des `ViewGroup`
- Unités : `dp` (pixels indépendants de la densité) pour la mise en page, `sp` (pixels indépendants de l'échelle) pour le texte
- `wrap_content` = taille adaptée au contenu ; `match_parent` = remplit le parent
- ConstraintLayout est le layout moderne recommandé pour les interfaces complexes
- Système de build : Gradle avec les fichiers `build.gradle`

## Patrons {#patterns}

### Vues courantes {#common-views}
```xml
<TextView android:id="@+id/textView"
    android:text="Hello" android:textSize="24sp" android:textColor="#FF0000" />

<EditText android:id="@+id/input"
    android:hint="Enter name" android:inputType="text" />

<Button android:id="@+id/button"
    android:text="Click Me" android:onClick="onButtonClick" />

<ImageView android:id="@+id/image"
    android:src="@drawable/photo" android:scaleType="centerCrop" />

<Spinner android:id="@+id/spinner" />
```

### Types de layouts {#layout-types}
```xml
<!-- LinearLayout - vertical/horizontal stacking -->
<LinearLayout android:orientation="vertical" android:padding="16dp">
    <TextView ... />
    <Button ... />
</LinearLayout>

<!-- ConstraintLayout - flexible constraint-based positioning -->
<androidx.constraintlayout.widget.ConstraintLayout>
    <Button
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintEnd_toEndOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
```

### Interaction Activity-View {#activity-view-interaction}
```java
public class MainActivity extends AppCompatActivity {
    private TextView quantityText;
    private int quantity = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        quantityText = findViewById(R.id.quantityText);
    }

    public void increaseQuantity(View view) {
        quantity++;
        quantityText.setText(String.valueOf(quantity));
    }
}
```

### Configuration du Spinner (liste déroulante) {#spinner-dropdown-setup}
```java
ArrayAdapter<String> adapter = new ArrayAdapter<>(
    this, android.R.layout.simple_spinner_item, items);
adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
spinner.setAdapter(adapter);
spinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
    @Override
    public void onItemSelected(AdapterView<?> parent, View v, int pos, long id) {
        String selected = parent.getItemAtPosition(pos).toString();
    }
    @Override public void onNothingSelected(AdapterView<?> p) {}
});
```

## Pièges à éviter {#gotchas}

- `dp` ou `sp` : utiliser `sp` uniquement pour le texte (respecte l'échelle de police choisie par l'utilisateur), `dp` pour tout le reste
- `findViewById` renvoie null si l'ID n'existe pas dans le layout courant, ce qui provoque une NPE à l'exécution
- L'attribut `android:onClick` ne fonctionne que pour les Activities, pas pour les Fragments : utiliser des listeners programmatiques
- RelativeLayout peut être plus lent que ConstraintLayout pour les layouts complexes (plusieurs passes de mesure)

## Voir aussi {#see-also}

- [[android-activity-lifecycle]] - Cycle de vie des Activities et navigation par Intent
- [[android-recyclerview]] - Rendu efficace des listes
- [[android-jetpack-compose]] - Alternative déclarative moderne pour l'interface
