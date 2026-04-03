---
title: React Router and Navigation
category: react
tags: [react, react-router, routing, navigation, spa, dynamic-routes, nested-routes]
---

# React Router and Navigation

## Key Facts

- **React Router** (v6+) is the standard client-side routing library for React SPAs
- `<BrowserRouter>` wraps the app; uses HTML5 History API for clean URLs
- `<Routes>` contains `<Route>` elements; routes match by path, render `element` prop
- **Nested routes**: child routes render inside parent's `<Outlet />` component
- `useParams()` - access dynamic URL parameters (`:id`); `useSearchParams()` - access query string
- `useNavigate()` - programmatic navigation; `navigate("/path")` or `navigate(-1)` for back
- `<Link to="/path">` for declarative navigation (renders `<a>` without page reload)
- `<NavLink>` adds `active` class/style when route matches; used for navigation menus
- **Lazy loading routes**: `React.lazy()` + `<Suspense>` for code splitting per route
- **Loader/Action pattern** (v6.4+): data fetching and mutations co-located with route definitions
- Related: [[react-components-and-jsx]], [[react-hooks]], [[react-state-management]]

## Patterns

### Basic Route Setup

```tsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="about" element={<About />} />
          <Route path="users" element={<Users />} />
          <Route path="users/:userId" element={<UserProfile />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

### Layout with Outlet

```tsx
import { Outlet, NavLink } from "react-router-dom";

function Layout() {
  return (
    <>
      <nav>
        <NavLink to="/" className={({ isActive }) => isActive ? "active" : ""}>
          Home
        </NavLink>
        <NavLink to="/about">About</NavLink>
      </nav>
      <main>
        <Outlet /> {/* child route renders here */}
      </main>
    </>
  );
}
```

### Dynamic Routes and Params

```tsx
import { useParams, useSearchParams } from "react-router-dom";

function UserProfile() {
  const { userId } = useParams<{ userId: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  const tab = searchParams.get("tab") ?? "profile";

  return (
    <div>
      <h1>User {userId}</h1>
      <button onClick={() => setSearchParams({ tab: "posts" })}>
        Posts
      </button>
    </div>
  );
}
```

### Protected Route

```tsx
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

// Usage in routes
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>
```

### Lazy Loading Routes

```tsx
import { lazy, Suspense } from "react";

const Dashboard = lazy(() => import("./pages/Dashboard"));
const Settings = lazy(() => import("./pages/Settings"));

<Routes>
  <Route
    path="/dashboard"
    element={
      <Suspense fallback={<Spinner />}>
        <Dashboard />
      </Suspense>
    }
  />
</Routes>
```

## Gotchas

- `<Route path="*">` catch-all must be last; React Router uses specificity-based matching, but explicit `*` avoids confusion
- `useNavigate` inside `useEffect` needs the navigation target in deps or use `replace: true` to avoid history stack pollution
- `<Navigate>` renders and redirects; don't wrap in conditional without `return` - it executes on every render
- Query parameters (`?tab=posts`) are NOT part of route matching; use `useSearchParams` to read/write them
- React Router v5 vs v6: `Switch` -> `Routes`, `component` prop -> `element` prop (JSX), `useHistory` -> `useNavigate`

## See Also

- [React Router: Getting Started](https://reactrouter.com/en/main/start/tutorial)
- [React Router: API Reference](https://reactrouter.com/en/main/hooks/use-navigate)
