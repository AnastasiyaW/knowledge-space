---
title: "Android RecyclerView und benutzerdefinierte Views"
category: concepts
tags: [java-spring, android, recyclerview, adapter, viewholder, diffutil, custom-view]
level: 3
source_sha256: eb25f0d2052eaaee8d4fbc47df3e3e2f36da586111d44e1c0e711a0209feb0f4
translation: machine
translated_at: '2026-10-24'
---
# Android RecyclerView und benutzerdefinierte Views {#android-recyclerview-and-custom-views}

RecyclerView für effiziente scrollbare Listen, Adapter/ViewHolder-Muster, LayoutManager, DiffUtil für effiziente Aktualisierungen, Wischen-zum-Löschen und benutzerdefiniertes View-Zeichnen.

## Wichtige Fakten {#key-facts}

- RecyclerView recycelt ViewHolder für effizientes Scrollen - ersetzt das veraltete ListView
- Drei Komponenten: Adapter (erstellt/bindet ViewHolder), ViewHolder (hält View-Referenzen), LayoutManager (Positionierung)
- `LinearLayoutManager` = Liste, `GridLayoutManager` = Raster, `StaggeredGridLayoutManager` = Pinterest-artiges Layout
- DiffUtil berechnet minimale Änderungen - deutlich effizienter als `notifyDataSetChanged()`
- Benutzerdefinierte Views erben von `View` und überschreiben `onDraw(Canvas)` für eigenes Rendering

## Muster {#patterns}

### RecyclerView-Einrichtung {#recyclerview-setup}
```java
// 1. ViewHolder
public class UserViewHolder extends RecyclerView.ViewHolder {
    TextView name, email;
    public UserViewHolder(View itemView) {
        super(itemView);
        name = itemView.findViewById(R.id.userName);
        email = itemView.findViewById(R.id.userEmail);
    }
}

// 2. Adapter
public class UserAdapter extends RecyclerView.Adapter<UserViewHolder> {
    private List<User> users;
    private final OnItemClickListener listener;

    @Override
    public UserViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
            .inflate(R.layout.item_user, parent, false);
        return new UserViewHolder(view);
    }

    @Override
    public void onBindViewHolder(UserViewHolder holder, int position) {
        User user = users.get(position);
        holder.name.setText(user.getName());
        holder.email.setText(user.getEmail());
        holder.itemView.setOnClickListener(v -> listener.onItemClick(user, position));
    }

    @Override public int getItemCount() { return users.size(); }
}

// 3. Activity setup
RecyclerView rv = findViewById(R.id.recyclerView);
rv.setLayoutManager(new LinearLayoutManager(this));
rv.setAdapter(new UserAdapter(users, (user, pos) -> { /* click */ }));
```

### LayoutManager {#layoutmanagers}
```java
new LinearLayoutManager(context)                              // vertical list
new LinearLayoutManager(context, HORIZONTAL, false)           // horizontal
new GridLayoutManager(context, 2)                             // 2-column grid
new StaggeredGridLayoutManager(2, VERTICAL)                   // Pinterest grid
```

### DiffUtil für effiziente Aktualisierungen {#diffutil-for-efficient-updates}
```java
DiffUtil.DiffResult result = DiffUtil.calculateDiff(new DiffUtil.Callback() {
    @Override public int getOldListSize() { return oldList.size(); }
    @Override public int getNewListSize() { return newList.size(); }
    @Override
    public boolean areItemsTheSame(int old, int new_) {
        return oldList.get(old).getId() == newList.get(new_).getId();
    }
    @Override
    public boolean areContentsTheSame(int old, int new_) {
        return oldList.get(old).equals(newList.get(new_));
    }
});
adapter.setItems(newList);
result.dispatchUpdatesTo(adapter);
```

### Wischen zum Löschen {#swipe-to-delete}
```java
new ItemTouchHelper(new ItemTouchHelper.SimpleCallback(0,
        ItemTouchHelper.LEFT | ItemTouchHelper.RIGHT) {
    @Override public boolean onMove(...) { return false; }
    @Override public void onSwiped(RecyclerView.ViewHolder vh, int dir) {
        adapter.removeItem(vh.getAdapterPosition());
    }
}).attachToRecyclerView(recyclerView);
```

### Benutzerdefinierte View {#custom-view}
```java
public class CircleView extends View {
    private Paint paint;
    public CircleView(Context ctx, AttributeSet attrs) {
        super(ctx, attrs);
        paint = new Paint(Paint.ANTI_ALIAS_FLAG);
        paint.setColor(Color.BLUE);
    }
    @Override
    protected void onDraw(Canvas canvas) {
        canvas.drawCircle(getWidth()/2f, getHeight()/2f, 100f, paint);
    }
}
```

## Fallstricke {#gotchas}

- `notifyDataSetChanged()` aktualisiert ALLE Elemente - für bessere Performance DiffUtil oder gezielt `notifyItemChanged(pos)` verwenden
- `getAdapterPosition()` kann während des Layouts `RecyclerView.NO_POSITION` (-1) zurückgeben - immer prüfen
- RecyclerView hat keine eingebauten Trennlinien - `DividerItemDecoration` manuell hinzufügen
- ViewHolder-Views werden wiederverwendet - alle Felder in `onBindViewHolder` immer zurücksetzen, um veraltete Daten zu vermeiden

## Siehe auch {#see-also}

- [[android-fundamentals-ui]] - XML-Layouts und Views
- [[android-jetpack-compose]] - LazyColumn als Compose-Entsprechung
- [[android-architecture-mvvm]] - ViewModel, das Daten an den Adapter liefert
