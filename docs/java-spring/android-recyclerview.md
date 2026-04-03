---
title: Android RecyclerView and Custom Views
category: concepts
tags: [java-spring, android, recyclerview, adapter, viewholder, diffutil, custom-view]
---

# Android RecyclerView and Custom Views

RecyclerView for efficient scrollable lists, Adapter/ViewHolder pattern, LayoutManagers, DiffUtil for efficient updates, swipe-to-delete, and custom View drawing.

## Key Facts

- RecyclerView recycles ViewHolders for efficient scrolling - replaces deprecated ListView
- Three components: Adapter (creates/binds ViewHolders), ViewHolder (holds view refs), LayoutManager (positioning)
- `LinearLayoutManager` = list, `GridLayoutManager` = grid, `StaggeredGridLayoutManager` = Pinterest-style
- DiffUtil calculates minimal changes - far more efficient than `notifyDataSetChanged()`
- Custom views extend `View` and override `onDraw(Canvas)` for custom rendering

## Patterns

### RecyclerView Setup
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

### LayoutManagers
```java
new LinearLayoutManager(context)                              // vertical list
new LinearLayoutManager(context, HORIZONTAL, false)           // horizontal
new GridLayoutManager(context, 2)                             // 2-column grid
new StaggeredGridLayoutManager(2, VERTICAL)                   // Pinterest grid
```

### DiffUtil for Efficient Updates
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

### Swipe to Delete
```java
new ItemTouchHelper(new ItemTouchHelper.SimpleCallback(0,
        ItemTouchHelper.LEFT | ItemTouchHelper.RIGHT) {
    @Override public boolean onMove(...) { return false; }
    @Override public void onSwiped(RecyclerView.ViewHolder vh, int dir) {
        adapter.removeItem(vh.getAdapterPosition());
    }
}).attachToRecyclerView(recyclerView);
```

### Custom View
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

## Gotchas

- `notifyDataSetChanged()` refreshes ALL items - use DiffUtil or specific `notifyItemChanged(pos)` for performance
- `getAdapterPosition()` can return `RecyclerView.NO_POSITION` (-1) during layout - always check
- RecyclerView doesn't have built-in dividers - add `DividerItemDecoration` manually
- ViewHolder views are reused - always reset all fields in `onBindViewHolder` to avoid stale data

## See Also

- [[android-fundamentals-ui]] - XML layouts and views
- [[android-jetpack-compose]] - LazyColumn as Compose equivalent
- [[android-architecture-mvvm]] - ViewModel feeding data to adapter
