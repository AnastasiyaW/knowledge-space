---
title: "RecyclerView Android et vues personnalisées"
category: concepts
tags: [java-spring, android, recyclerview, adapter, viewholder, diffutil, custom-view]
level: 3
source_sha256: eb25f0d2052eaaee8d4fbc47df3e3e2f36da586111d44e1c0e711a0209feb0f4
translation: machine
translated_at: '2026-10-24'
---
# RecyclerView Android et vues personnalisées {#android-recyclerview-and-custom-views}

RecyclerView pour des listes défilantes efficaces, le modèle Adapter/ViewHolder, les LayoutManagers, DiffUtil pour des mises à jour efficaces, le balayage pour supprimer, et le dessin de vues personnalisées.

## Points clés {#key-facts}

- RecyclerView recycle les ViewHolders pour un défilement efficace - remplace l'ancien ListView, désormais déprécié
- Trois composants : Adapter (crée/lie les ViewHolders), ViewHolder (contient les références aux vues), LayoutManager (positionnement)
- `LinearLayoutManager` = liste, `GridLayoutManager` = grille, `StaggeredGridLayoutManager` = disposition de type Pinterest
- DiffUtil calcule les changements minimaux - bien plus efficace que `notifyDataSetChanged()`
- Les vues personnalisées étendent `View` et redéfinissent `onDraw(Canvas)` pour le rendu personnalisé

## Patrons {#patterns}

### Configuration de RecyclerView {#recyclerview-setup}
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

### LayoutManagers {#layoutmanagers}
```java
new LinearLayoutManager(context)                              // vertical list
new LinearLayoutManager(context, HORIZONTAL, false)           // horizontal
new GridLayoutManager(context, 2)                             // 2-column grid
new StaggeredGridLayoutManager(2, VERTICAL)                   // Pinterest grid
```

### DiffUtil pour des mises à jour efficaces {#diffutil-for-efficient-updates}
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

### Balayer pour supprimer {#swipe-to-delete}
```java
new ItemTouchHelper(new ItemTouchHelper.SimpleCallback(0,
        ItemTouchHelper.LEFT | ItemTouchHelper.RIGHT) {
    @Override public boolean onMove(...) { return false; }
    @Override public void onSwiped(RecyclerView.ViewHolder vh, int dir) {
        adapter.removeItem(vh.getAdapterPosition());
    }
}).attachToRecyclerView(recyclerView);
```

### Vue personnalisée {#custom-view}
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

## Pièges {#gotchas}

- `notifyDataSetChanged()` rafraîchit TOUS les éléments - utilisez DiffUtil ou `notifyItemChanged(pos)` ciblé pour les performances
- `getAdapterPosition()` peut renvoyer `RecyclerView.NO_POSITION` (-1) pendant la mise en page - vérifiez toujours cette valeur
- RecyclerView ne dispose pas de séparateurs intégrés - ajoutez `DividerItemDecoration` manuellement
- Les vues d'un ViewHolder sont réutilisées - réinitialisez toujours tous les champs dans `onBindViewHolder` pour éviter les données obsolètes

## Voir aussi {#see-also}

- [[android-fundamentals-ui]] - mises en page XML et vues
- [[android-jetpack-compose]] - LazyColumn, équivalent dans Compose
- [[android-architecture-mvvm]] - ViewModel alimentant l'adaptateur
