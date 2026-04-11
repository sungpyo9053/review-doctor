import { createElement, type ComponentPropsWithoutRef } from "react";

type AtomTag =
  | "div"
  | "span"
  | "section"
  | "header"
  | "footer"
  | "main"
  | "nav"
  | "aside"
  | "article"
  | "form"
  | "h1"
  | "h2"
  | "h3"
  | "h4"
  | "p"
  | "strong"
  | "small"
  | "button"
  | "input"
  | "label"
  | "a"
  | "ul"
  | "li"
  | "table"
  | "thead"
  | "tbody"
  | "tr"
  | "th"
  | "td";

function createAtom<T extends AtomTag>(tag: T) {
  const Atom = (props: ComponentPropsWithoutRef<T>) => createElement(tag, props);

  Atom.displayName = `Atom.${String(tag)}`;

  return Atom;
}

export const Div = createAtom("div");
export const Span = createAtom("span");
export const Section = createAtom("section");
export const Header = createAtom("header");
export const Footer = createAtom("footer");
export const Main = createAtom("main");
export const Nav = createAtom("nav");
export const Aside = createAtom("aside");
export const Article = createAtom("article");
export const Form = createAtom("form");
export const H1 = createAtom("h1");
export const H2 = createAtom("h2");
export const H3 = createAtom("h3");
export const H4 = createAtom("h4");
export const P = createAtom("p");
export const Strong = createAtom("strong");
export const Small = createAtom("small");
export const ButtonBase = createAtom("button");
export const InputBase = createAtom("input");
export const Label = createAtom("label");
export const A = createAtom("a");
export const Ul = createAtom("ul");
export const Li = createAtom("li");
export const Table = createAtom("table");
export const Thead = createAtom("thead");
export const Tbody = createAtom("tbody");
export const Tr = createAtom("tr");
export const Th = createAtom("th");
export const Td = createAtom("td");
