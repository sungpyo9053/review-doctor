import type { AnchorHTMLAttributes, ReactNode } from "react";
import { Link, type LinkProps } from "react-router-dom";
import { cx } from "../../utils/cx";
import { A } from "./html";
import styles from "./AppLink.module.css";

type LinkTone = "primary" | "secondary" | "ghost" | "inline" | "nav" | "dark";
type LinkSize = "sm" | "md" | "lg";

interface SharedAppLinkProps {
  tone?: LinkTone;
  size?: LinkSize;
  stretch?: boolean;
  className?: string;
  children: ReactNode;
}

type RouterAppLinkProps = SharedAppLinkProps &
  Omit<LinkProps, "className"> & {
    href?: never;
  };

type AnchorAppLinkProps = SharedAppLinkProps &
  Omit<AnchorHTMLAttributes<HTMLAnchorElement>, "className"> & {
    to?: never;
    href: string;
  };

export function AppLink(props: RouterAppLinkProps | AnchorAppLinkProps) {
  const { tone = "primary", size = "md", stretch = false, className, children } = props;
  const classes = cx(
    styles.link,
    styles[tone],
    styles[size],
    stretch && styles.stretch,
    className,
  );

  if ("to" in props) {
    const {
      tone: _tone,
      size: _size,
      stretch: _stretch,
      className: _className,
      children: _children,
      ...linkProps
    } = props as RouterAppLinkProps;

    return (
      <Link className={classes} {...linkProps}>
        {children}
      </Link>
    );
  }

  const {
    href,
    target,
    rel,
    tone: _tone,
    size: _size,
    stretch: _stretch,
    className: _className,
    children: _children,
    ...anchorProps
  } = props as AnchorAppLinkProps;

  return (
    <A
      className={classes}
      href={href}
      target={target}
      rel={rel}
      {...anchorProps}
    >
      {children}
    </A>
  );
}
