import { lazy, type ComponentType, type LazyExoticComponent } from "react";

export type RouteAccess = "public" | "guest" | "private" | "admin";

interface PageModule {
  default: ComponentType;
}

export interface FileRoute {
  path: string;
  Component: LazyExoticComponent<ComponentType>;
  access: RouteAccess;
}

const pageModules = import.meta.glob<PageModule>("../pages/**/page.tsx");

function segmentToPath(segment: string): string {
  if (segment.startsWith("[") && segment.endsWith("]")) {
    return `:${segment.slice(1, -1)}`;
  }

  if (segment.startsWith("$")) {
    return `:${segment.slice(1)}`;
  }

  return segment;
}

function filePathToRoutePath(filePath: string): string {
  const routePath = filePath
    .replace("../pages/", "")
    .replace(/\/page\.tsx$/, "");

  if (routePath === "index") {
    return "/";
  }

  const segments = routePath
    .split("/")
    .filter((segment) => segment !== "index")
    .map(segmentToPath);

  return `/${segments.join("/")}`;
}

function accessFromRoutePath(path: string): RouteAccess {
  if (path === "/admin" || path.startsWith("/admin/")) {
    return "admin";
  }

  if (path === "/dashboard" || path.startsWith("/dashboard/")) {
    return "private";
  }

  if (path === "/login" || path === "/join" || path.startsWith("/join/")) {
    return "guest";
  }

  return "public";
}

export const fileRoutes: FileRoute[] = Object.entries(pageModules)
  .map(([filePath, loadPageModule]) => {
    const path = filePathToRoutePath(filePath);

    return {
      path,
      access: accessFromRoutePath(path),
      Component: lazy(async () => {
        const pageModule = await loadPageModule();
        return { default: pageModule.default };
      }),
    };
  })
  .sort((left, right) => {
    if (left.path === "/") {
      return -1;
    }

    if (right.path === "/") {
      return 1;
    }

    return left.path.localeCompare(right.path);
  });
