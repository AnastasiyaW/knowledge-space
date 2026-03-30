---
title: React Components and JSX
category: react
tags: [react, jsx, components, props, children, composition, conditional-rendering]
---

# React Components and JSX

## Key Facts

- **JSX** is syntactic sugar for `React.createElement(type, props, children)`; compiles to JavaScript
- **Function components** are the standard; class components are legacy (still work but not recommended)
- **Props** are read-only inputs passed from parent to child; destructure in function signature
- `children` is a special prop for content between opening and closing tags
- **Conditional rendering**: ternary `{cond ? <A/> : <B/>}`, short-circuit `{cond && <A/>}`, early return
- **Lists**: `{items.map(item => <Item key={item.id} />)}` - `key` must be stable, unique identifier
- **Fragment**: `<></>` or `<React.Fragment>` groups elements without adding a DOM node
- Component names must be **PascalCase** (`MyComponent`); lowercase = HTML element
- `className` instead of `class`; `htmlFor` instead of `for`; all event handlers are camelCase
- Related: [[react-hooks]], [[react-state-management]], [[typescript-type-system]]

## Patterns

### Function Component with TypeScript

```tsx
interface ButtonProps {
  variant?: "primary" | "secondary";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  onClick: () => void;
  children: React.ReactNode;
}

function Button({
  variant = "primary",
  size = "md",
  disabled = false,
  onClick,
  children,
}: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

### Conditional Rendering

```tsx
function UserProfile({ user }: { user: User | null }) {
  // Early return
  if (!user) return <p>Please log in</p>;

  return (
    <div>
      <h2>{user.name}</h2>
      {/* Short-circuit */}
      {user.isAdmin && <Badge text="Admin" />}
      {/* Ternary */}
      {user.avatar ? (
        <img src={user.avatar} alt={user.name} />
      ) : (
        <DefaultAvatar />
      )}
    </div>
  );
}
```

### List Rendering

```tsx
function TodoList({ todos }: { todos: Todo[] }) {
  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id} className={todo.done ? "completed" : ""}>
          {todo.text}
        </li>
      ))}
    </ul>
  );
}
```

### Composition Patterns

```tsx
// Slot pattern via props
function Card({ header, children, footer }: {
  header: React.ReactNode;
  children: React.ReactNode;
  footer?: React.ReactNode;
}) {
  return (
    <div className="card">
      <div className="card-header">{header}</div>
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}

// Usage
<Card header={<h3>Title</h3>} footer={<Button onClick={save}>Save</Button>}>
  <p>Card content here</p>
</Card>
```

## Gotchas

- `{0 && <Component />}` renders `0` in the DOM; use `{items.length > 0 && ...}` or `{!!count && ...}`
- `key` must be on the outermost element returned by `map`; using array index as key causes bugs with reordering/deletion
- JSX expressions must return a single root element; wrap in `<>...</>` fragment
- `style` prop takes an object, not a string: `style={{ color: "red", fontSize: "16px" }}`
- React event handlers receive `SyntheticEvent`, not native DOM event; access native via `e.nativeEvent`

## See Also

- [React: Components and Props](https://react.dev/learn/passing-props-to-a-component)
- [React: Conditional Rendering](https://react.dev/learn/conditional-rendering)
